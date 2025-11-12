#!/usr/bin/env python3
"""
스타일 선택 가능한 웹소설 마케팅 이미지 생성기

4가지 비주얼 스타일:
1. photorealistic - 실사화
2. sticker - 스티커/아이콘
3. figure - 피규어/미니어처
4. anime - 일본 애니메이션
"""

import argparse
import os
import json
from pathlib import Path
from datetime import datetime
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

# 스타일별 프롬프트 확장 템플릿
STYLE_TEMPLATES = {
    "photorealistic": {
        "base": "Photorealistic cinematic photography, professional quality, high detail, 8K resolution",
        "lighting": "dramatic cinematic lighting with soft shadows and rim light",
        "camera": "shot with 85mm portrait lens, shallow depth of field (f/1.8), bokeh background",
        "mood": "cinematic color grading, film-like atmosphere",
        "quality": "ultra-detailed textures, natural skin tones, professional photography",
        "negative": "cartoon, anime, illustration, painting, low quality, blurry"
    },
    "sticker": {
        "base": "Cute sticker illustration, kawaii style, simple clean design",
        "style": "transparent background, bold black outline, flat color with minimal shading",
        "character": "chibi proportions with big head and small body, expressive face with large eyes",
        "colors": "vibrant saturated colors, playful cheerful palette",
        "quality": "vector-style clean lines, high resolution PNG, emoji-inspired design",
        "negative": "realistic, photograph, complex details, shadows, 3d render"
    },
    "figure": {
        "base": "Miniature collectible figure, super deformed chibi proportions (2.5 heads tall)",
        "material": "smooth plastic finish with hand-painted details, matte coating, resin material",
        "lighting": "studio lighting setup with soft shadows, professional product photography",
        "background": "clean white background, display stand included, collectible presentation",
        "quality": "toy-like charm, high-quality figure render, 8K product photography",
        "negative": "flat 2d, cartoon, realistic human, painting, sketch"
    },
    "anime": {
        "base": "High-quality modern anime style, detailed digital painting, Japanese animation",
        "art": "anime cel-shading with vibrant saturated colors, sharp clean lineart",
        "character": "expressive large eyes with detailed highlights, flowing hair with individual strands",
        "effects": "dynamic composition, soft gradient shadows, atmospheric lighting",
        "quality": "professional anime production quality, key visual artwork, cinematic anime",
        "negative": "realistic photo, 3d render, western cartoon, low quality, sketch"
    }
}


def expand_prompt_with_style(
    base_prompt: str,
    style: str,
    genre: str,
    additional_details: dict = None
) -> str:
    """
    사용자 프롬프트를 스타일과 장르에 맞게 자동으로 확장

    Args:
        base_prompt: 사용자가 입력한 기본 장면 설명
        style: 선택한 비주얼 스타일
        genre: 웹소설 장르
        additional_details: 추가 디테일 (시간대, 날씨, 감정 등)

    Returns:
        확장된 상세 프롬프트
    """
    if style not in STYLE_TEMPLATES:
        raise ValueError(f"지원하지 않는 스타일: {style}. 사용 가능: {list(STYLE_TEMPLATES.keys())}")

    template = STYLE_TEMPLATES[style]

    # 기본 구조
    expanded_parts = [
        template["base"],
        base_prompt,  # 사용자 입력
    ]

    # 스타일별 기술적 디테일 추가
    for key in ["lighting", "camera", "style", "character", "material",
                "background", "art", "effects", "mood", "colors"]:
        if key in template:
            expanded_parts.append(template[key])

    # 추가 디테일 반영
    if additional_details:
        if "time_of_day" in additional_details:
            expanded_parts.append(f"{additional_details['time_of_day']} lighting")
        if "weather" in additional_details:
            expanded_parts.append(f"{additional_details['weather']} atmosphere")
        if "emotion" in additional_details:
            expanded_parts.append(f"{additional_details['emotion']} mood and expression")

    # 장르별 분위기 추가
    genre_moods = {
        "romance": "romantic tender atmosphere, soft dreamy feel, warm emotional tones",
        "fantasy": "epic majestic atmosphere, magical mystical elements, grand scale composition",
        "thriller": "tense mysterious atmosphere, dark moody tones, suspenseful composition",
        "comedy": "lighthearted fun atmosphere, bright cheerful colors, playful energy",
        "drama": "emotional storytelling atmosphere, realistic human moments, dramatic tension"
    }
    if genre in genre_moods:
        expanded_parts.append(genre_moods[genre])

    # 품질 키워드
    expanded_parts.append(template["quality"])

    # 한국 웹소설 특화
    expanded_parts.append("Korean webtoon aesthetic, manhwa style")

    # 최종 조합
    full_prompt = ", ".join(expanded_parts)

    return full_prompt


def get_negative_prompt(style: str) -> str:
    """스타일별 네거티브 프롬프트 반환"""
    base_negative = "low quality, blurry, pixelated, distorted anatomy, bad proportions, extra limbs, deformed hands, ugly face, watermark, signature, text overlay, amateur, poorly drawn"

    style_negative = STYLE_TEMPLATES.get(style, {}).get("negative", "")

    return f"{base_negative}, {style_negative}" if style_negative else base_negative


def log_process(log_file: Path, message: str, data: dict = None):
    """터미널 출력 및 로그 파일 기록"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 터미널 출력
    print(f"[{timestamp}] {message}")
    if data:
        print(json.dumps(data, indent=2, ensure_ascii=False))

    # 로그 파일 기록
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"[{timestamp}] {message}\n")
        if data:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
            f.write("\n")


def generate_image(
    base_prompt: str,
    style: str,
    scene_text: str,
    genre: str,
    image_type: str,
    title: str,
    output_path: str,
    additional_details: dict = None,
    log_dir: Path = None
):
    """스타일 선택 가능한 이미지 생성 및 텍스트 오버레이"""

    # 로그 디렉토리 설정
    if log_dir is None:
        log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # 프로세스 시작 로그
    log_process(log_file, "🚀 이미지 생성 프로세스 시작", {
        "style": style,
        "genre": genre,
        "image_type": image_type,
        "title": title
    })

    # 환경변수에서 토큰 로드
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        error_msg = "HUGGINGFACE_TOKEN 환경변수를 설정해주세요"
        log_process(log_file, f"❌ 오류: {error_msg}")
        raise ValueError(error_msg)

    log_process(log_file, "✅ Hugging Face 토큰 로드 성공")

    # 프롬프트 확장
    log_process(log_file, "🔧 프롬프트 자동 확장 시작", {
        "원본 프롬프트": base_prompt,
        "스타일": style,
        "장르": genre,
        "추가 디테일": additional_details
    })

    expanded_prompt = expand_prompt_with_style(base_prompt, style, genre, additional_details)
    negative_prompt = get_negative_prompt(style)

    log_process(log_file, "✅ 프롬프트 확장 완료", {
        "확장된 프롬프트": expanded_prompt,
        "네거티브 프롬프트": negative_prompt
    })

    # 설정
    width, height = IMAGE_SIZES[image_type]
    colors = GENRE_COLORS.get(genre.lower(), GENRE_COLORS["drama"])

    log_process(log_file, "⚙️  이미지 설정", {
        "크기": f"{width}x{height}",
        "색상 팔레트": colors
    })

    # Hugging Face 클라이언트
    hf_client = InferenceClient(token=hf_token)

    log_process(log_file, "🖼️  Hugging Face API 호출 시작 (10-20초 소요)")

    try:
        # 이미지 생성
        image = hf_client.text_to_image(
            prompt=expanded_prompt,
            model="black-forest-labs/FLUX.1-dev",
            width=width,
            height=height
        )
        log_process(log_file, "✅ AI 이미지 생성 성공!")

    except Exception as e:
        error_details = {
            "오류 메시지": str(e),
            "폴백": "단색 이미지 생성"
        }
        log_process(log_file, f"⚠️  이미지 생성 실패", error_details)
        print(f"   대신 {genre} 장르 색상으로 단색 이미지를 생성합니다.")
        # 폴백: 단색 이미지
        image = Image.new("RGB", (width, height), colors[0])

    # 텍스트 오버레이
    log_process(log_file, "✍️  텍스트 오버레이 시작")
    draw = ImageDraw.Draw(image)

    try:
        font_title = ImageFont.truetype("NotoSansKR-Bold.ttf", 60)
        font_text = ImageFont.truetype("NotoSansKR-Regular.ttf", 40)
        log_process(log_file, "✅ 폰트 로드 성공: NotoSansKR")
    except IOError:
        log_process(log_file, "⚠️  폰트 파일 없음, 기본 폰트 사용")
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # 제목 추가
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
        log_process(log_file, f"✅ 제목 추가: {title}")

    # 장면 텍스트 추가
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
        log_process(log_file, f"✅ 장면 텍스트 추가: {scene_text}")

    # 저장
    image.save(output_path)
    log_process(log_file, f"💾 이미지 저장 완료", {
        "파일 경로": output_path,
        "파일 크기": f"{os.path.getsize(output_path) / 1024:.2f} KB"
    })

    print(f"\n{'='*80}")
    print(f"✅ 전체 프로세스 완료!")
    print(f"📁 이미지: {output_path}")
    print(f"📋 로그: {log_file}")
    print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description="스타일 선택 가능한 웹소설 마케팅 이미지 생성기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
스타일 옵션:
  photorealistic - 실사 사진 스타일 (드라마틱한 포스터)
  sticker        - 귀여운 스티커/아이콘 (SNS 프로필, 굿즈)
  figure         - 피규어/미니어처 (수집 이벤트, 3D 느낌)
  anime          - 일본 애니메이션 (웹툰 홍보, 감정 표현)

사용 예시:
  python generate_with_style.py \\
    --prompt "a warrior with sword in fantasy world" \\
    --style anime \\
    --text "검으로 세상을 구한다" \\
    --genre fantasy \\
    --title "신화의 검" \\
    --output result.png
        """
    )

    parser.add_argument("--prompt", required=True, help="기본 장면 설명 (영어 권장)")
    parser.add_argument(
        "--style",
        choices=["photorealistic", "sticker", "figure", "anime"],
        required=True,
        help="비주얼 스타일 선택"
    )
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

    # 추가 디테일 (선택사항)
    parser.add_argument("--time", help="시간대 (예: golden hour, night, dawn)")
    parser.add_argument("--weather", help="날씨 (예: sunny, rainy, foggy)")
    parser.add_argument("--emotion", help="감정 (예: happy, sad, tense, excited)")

    args = parser.parse_args()

    # 추가 디테일 딕셔너리 구성
    additional_details = {}
    if args.time:
        additional_details["time_of_day"] = args.time
    if args.weather:
        additional_details["weather"] = args.weather
    if args.emotion:
        additional_details["emotion"] = args.emotion

    generate_image(
        base_prompt=args.prompt,
        style=args.style,
        scene_text=args.text,
        genre=args.genre,
        image_type=args.type,
        title=args.title,
        output_path=args.output,
        additional_details=additional_details if additional_details else None
    )


if __name__ == "__main__":
    main()
