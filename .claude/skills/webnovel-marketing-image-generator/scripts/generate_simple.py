#!/usr/bin/env python3
"""
간소화된 웹소설 마케팅 이미지 생성기 - Hugging Face만 사용

Anthropic API 없이 사전 정의된 프롬프트로 이미지 생성
"""

import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from huggingface_hub import InferenceClient


# 장르별 색상 팔레트
GENRE_COLORS = {
    "romance": ["#FFE5E5", "#FFB6C1", "#FF69B4", "#FF1493"],
    "fantasy": ["#4B0082", "#8A2BE2", "#9370DB", "#BA55D3"],
    "thriller": ["#2C2C2C", "#4A4A4A", "#8B0000", "#DC143C"],
    "comedy": ["#FFD700", "#FFA500", "#FF8C00", "#FF6347"],
    "drama": ["#483D8B", "#6A5ACD", "#7B68EE", "#9370DB"],
}

# 이미지 타입별 크기
IMAGE_SIZES = {
    "sns": (1080, 1080),
    "youtube": (1280, 720),
    "teaser": (1080, 1920),
    "profile": (800, 1200),
}


def generate_image(
    visual_prompt: str,
    scene_text: str,
    genre: str,
    image_type: str,
    title: str,
    output_path: str
):
    """이미지 생성 및 텍스트 오버레이"""

    # 환경변수에서 토큰 로드
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        raise ValueError("HUGGINGFACE_TOKEN 환경변수를 설정해주세요")

    # 설정
    width, height = IMAGE_SIZES[image_type]
    colors = GENRE_COLORS.get(genre.lower(), GENRE_COLORS["drama"])

    # Hugging Face 클라이언트
    hf_client = InferenceClient(token=hf_token)

    print("🖼️  AI 이미지 생성 중... (10-20초 소요)")

    try:
        # 이미지 생성
        image = hf_client.text_to_image(
            prompt=visual_prompt,
            model="black-forest-labs/FLUX.1-dev",
            width=width,
            height=height
        )
        print("✅ AI 이미지 생성 완료!")
    except Exception as e:
        print(f"⚠️  이미지 생성 실패: {e}")
        print(f"   대신 {genre} 장르 색상으로 단색 이미지를 생성합니다.")
        # 폴백: 단색 이미지
        image = Image.new("RGB", (width, height), colors[0])

    # 텍스트 오버레이
    print("✍️  텍스트 추가 중...")
    draw = ImageDraw.Draw(image)

    try:
        font_title = ImageFont.truetype("NotoSansKR-Bold.ttf", 60)
        font_text = ImageFont.truetype("NotoSansKR-Regular.ttf", 40)
    except IOError:
        print("⚠️  폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # 제목 추가 (상단 중앙)
    if title:
        draw.text(
            (width // 2, 100),
            title,
            fill="white",
            font=font_title,
            anchor="mm",
            stroke_width=3,
            stroke_fill="black"
        )

    # 장면 텍스트 추가 (하단 중앙)
    if scene_text:
        draw.text(
            (width // 2, height - 150),
            f'"{scene_text}"',
            fill="white",
            font=font_text,
            anchor="mm",
            stroke_width=2,
            stroke_fill="black"
        )

    # 저장
    image.save(output_path)
    print(f"✅ 이미지 저장 완료: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="간소화된 웹소설 마케팅 이미지 생성기")
    parser.add_argument("--prompt", required=True, help="이미지 생성 프롬프트 (영어)")
    parser.add_argument("--text", required=True, help="이미지에 표시할 장면 텍스트 (한글)")
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

    generate_image(
        visual_prompt=args.prompt,
        scene_text=args.text,
        genre=args.genre,
        image_type=args.type,
        title=args.title,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
