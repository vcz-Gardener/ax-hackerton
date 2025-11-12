#!/usr/bin/env python3
"""
웹소설 마케팅 이미지 생성기 - 메인 스크립트

사용법:
    python generate_marketing_image.py --input novel.txt --type sns --genre romance
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Literal
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import anthropic
from huggingface_hub import InferenceClient
import io


@dataclass
class SceneExtraction:
    """추출된 장면 정보"""
    text: str
    emotion: str  # "긴장", "설렘", "슬픔", "분노" 등
    characters: List[str]
    setting: str
    visual_description: str


@dataclass
class ImageConfig:
    """이미지 생성 설정"""
    width: int
    height: int
    color_palette: List[str]
    font_primary: str
    font_secondary: str
    layout_type: str


class WebnovelMarketingGenerator:
    """웹소설 마케팅 이미지 생성 클래스"""

    # 이미지 타입별 크기 설정
    IMAGE_SIZES = {
        "sns": (1080, 1080),  # 인스타그램 정사각형
        "youtube": (1280, 720),  # 유튜브 썸네일
        "teaser": (1080, 1920),  # 세로형 티저
        "profile": (800, 1200),  # 캐릭터 프로필
    }

    # 장르별 색상 팔레트
    GENRE_COLORS = {
        "romance": ["#FFE5E5", "#FFB6C1", "#FF69B4", "#FF1493"],
        "fantasy": ["#4B0082", "#8A2BE2", "#9370DB", "#BA55D3"],
        "thriller": ["#2C2C2C", "#4A4A4A", "#8B0000", "#DC143C"],
        "comedy": ["#FFD700", "#FFA500", "#FF8C00", "#FF6347"],
        "drama": ["#483D8B", "#6A5ACD", "#7B68EE", "#9370DB"],
    }

    def __init__(self, anthropic_api_key: str, hf_token: str):
        """
        Args:
            anthropic_api_key: Anthropic API 키
            hf_token: Hugging Face API 토큰
        """
        self.claude_client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.hf_client = InferenceClient(token=hf_token)

    def extract_key_scenes(self, novel_text: str, num_scenes: int = 3) -> List[SceneExtraction]:
        """
        웹소설 텍스트에서 마케팅에 적합한 핵심 장면 추출

        Args:
            novel_text: 웹소설 전문 텍스트
            num_scenes: 추출할 장면 개수

        Returns:
            추출된 장면 리스트
        """
        prompt = f"""다음 웹소설 텍스트에서 SNS 마케팅에 가장 효과적인 장면 {num_scenes}개를 추출해주세요.

웹소설 텍스트:
{novel_text}

각 장면에 대해 다음 정보를 JSON 형식으로 제공해주세요:
- text: 해당 장면의 원문 (100자 이내로 요약)
- emotion: 주요 감정 (긴장, 설렘, 슬픔, 분노, 희망 중 선택)
- characters: 등장 캐릭터 이름 리스트
- setting: 장면의 배경 (예: "왕궁 연회장", "어두운 골목")
- visual_description: 이미지 생성을 위한 시각적 묘사 (영어, 200자 이내)

JSON 배열 형식으로만 응답해주세요."""

        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # JSON 파싱
        response_text = message.content[0].text
        scenes_data = json.loads(response_text)

        return [SceneExtraction(**scene) for scene in scenes_data]

    def get_image_config(
        self,
        image_type: Literal["sns", "youtube", "teaser", "profile"],
        genre: str
    ) -> ImageConfig:
        """
        이미지 타입과 장르에 맞는 설정 반환

        Args:
            image_type: 이미지 타입
            genre: 웹소설 장르

        Returns:
            이미지 생성 설정
        """
        width, height = self.IMAGE_SIZES[image_type]
        colors = self.GENRE_COLORS.get(genre.lower(), self.GENRE_COLORS["drama"])

        return ImageConfig(
            width=width,
            height=height,
            color_palette=colors,
            font_primary="NotoSansKR-Bold.ttf",
            font_secondary="NotoSansKR-Regular.ttf",
            layout_type=image_type
        )

    def generate_image_with_huggingface(
        self,
        scene: SceneExtraction,
        config: ImageConfig
    ) -> Image.Image:
        """
        Hugging Face Inference API로 이미지 생성

        Args:
            scene: 장면 정보
            config: 이미지 설정

        Returns:
            생성된 PIL Image
        """
        # Stable Diffusion 프롬프트 구성
        prompt = f"{scene.visual_description}, high quality, detailed, {scene.setting}, manhwa style, webtoon art"

        try:
            # Hugging Face Inference API 호출
            image = self.hf_client.text_to_image(
                prompt=prompt,
                model="black-forest-labs/FLUX.1-dev",
                width=config.width,
                height=config.height
            )
            return image
        except Exception as e:
            print(f"⚠️  이미지 생성 실패: {e}")
            print("   대신 색상 팔레트 기반 이미지를 생성합니다.")
            # 폴백: 그라데이션 이미지 생성
            image = Image.new("RGB", (config.width, config.height), config.color_palette[0])
            return image

    def add_text_overlay(
        self,
        image: Image.Image,
        scene: SceneExtraction,
        config: ImageConfig,
        title: str = ""
    ) -> Image.Image:
        """
        이미지에 텍스트 오버레이 추가

        Args:
            image: 베이스 이미지
            scene: 장면 정보
            config: 이미지 설정
            title: 작품 제목

        Returns:
            텍스트가 추가된 이미지
        """
        draw = ImageDraw.Draw(image)

        # 폰트 로드 (실제 구현 시 경로 수정 필요)
        try:
            font_title = ImageFont.truetype(config.font_primary, 60)
            font_text = ImageFont.truetype(config.font_secondary, 40)
        except IOError:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()

        # 제목 추가
        if title:
            draw.text(
                (config.width // 2, 100),
                title,
                fill="white",
                font=font_title,
                anchor="mm",
                stroke_width=3,
                stroke_fill="black"
            )

        # 장면 텍스트 추가 (중앙 하단)
        draw.text(
            (config.width // 2, config.height - 150),
            f'"{scene.text}"',
            fill="white",
            font=font_text,
            anchor="mm",
            stroke_width=2,
            stroke_fill="black"
        )

        return image

    def generate(
        self,
        novel_text: str,
        image_type: Literal["sns", "youtube", "teaser", "profile"],
        genre: str,
        title: str = "",
        output_path: str = "output.png"
    ) -> str:
        """
        전체 워크플로우 실행

        Args:
            novel_text: 웹소설 텍스트
            image_type: 이미지 타입
            genre: 장르
            title: 작품 제목
            output_path: 출력 파일 경로

        Returns:
            생성된 이미지 파일 경로
        """
        # 1. 장면 추출
        print("📖 핵심 장면 추출 중...")
        scenes = self.extract_key_scenes(novel_text, num_scenes=1)
        scene = scenes[0]

        # 2. 설정 로드
        print("🎨 이미지 설정 구성 중...")
        config = self.get_image_config(image_type, genre)

        # 3. 이미지 생성
        print("🖼️  AI 이미지 생성 중...")
        base_image = self.generate_image_with_huggingface(scene, config)

        # 4. 텍스트 오버레이
        print("✍️  텍스트 추가 중...")
        final_image = self.add_text_overlay(base_image, scene, config, title)

        # 5. 저장
        final_image.save(output_path)
        print(f"✅ 이미지 생성 완료: {output_path}")

        return output_path


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(description="웹소설 마케팅 이미지 생성기")
    parser.add_argument("--input", required=True, help="웹소설 텍스트 파일 경로")
    parser.add_argument(
        "--type",
        choices=["sns", "youtube", "teaser", "profile"],
        default="sns",
        help="이미지 타입"
    )
    parser.add_argument("--genre", default="drama", help="웹소설 장르")
    parser.add_argument("--title", default="", help="작품 제목")
    parser.add_argument("--output", default="marketing_image.png", help="출력 파일명")

    args = parser.parse_args()

    # 환경변수에서 API 키 로드
    api_key = os.getenv("ANTHROPIC_API_KEY")
    hf_token = os.getenv("HUGGINGFACE_TOKEN")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY 환경변수를 설정해주세요")
    if not hf_token:
        raise ValueError("HUGGINGFACE_TOKEN 환경변수를 설정해주세요")

    # 입력 파일 읽기
    with open(args.input, "r", encoding="utf-8") as f:
        novel_text = f.read()

    # 생성기 실행
    generator = WebnovelMarketingGenerator(api_key, hf_token)
    generator.generate(
        novel_text=novel_text,
        image_type=args.type,
        genre=args.genre,
        title=args.title,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
