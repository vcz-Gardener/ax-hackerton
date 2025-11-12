#!/usr/bin/env python3
"""
여러 웹소설/회차를 한 번에 처리하는 배치 생성 스크립트

사용법:
    python batch_generate.py --input-dir ./novels --output-dir ./output --types sns,youtube
"""

import argparse
import os
from pathlib import Path
from typing import List
from generate_marketing_image import WebnovelMarketingGenerator


def process_batch(
    input_dir: str,
    output_dir: str,
    image_types: List[str],
    genre: str = "drama"
) -> None:
    """
    디렉토리 내 모든 텍스트 파일을 처리

    Args:
        input_dir: 입력 디렉토리
        output_dir: 출력 디렉토리
        image_types: 생성할 이미지 타입 리스트
        genre: 장르
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # API 키 로드
    api_key = os.getenv("ANTHROPIC_API_KEY")
    hf_token = os.getenv("HUGGINGFACE_TOKEN")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY 환경변수를 설정해주세요")
    if not hf_token:
        raise ValueError("HUGGINGFACE_TOKEN 환경변수를 설정해주세요")

    generator = WebnovelMarketingGenerator(api_key, hf_token)

    # 모든 .txt 파일 처리
    txt_files = list(input_path.glob("*.txt"))
    print(f"📚 총 {len(txt_files)}개 파일 발견")

    for idx, txt_file in enumerate(txt_files, 1):
        print(f"\n[{idx}/{len(txt_files)}] {txt_file.name} 처리 중...")

        with open(txt_file, "r", encoding="utf-8") as f:
            novel_text = f.read()

        # 각 이미지 타입별로 생성
        for img_type in image_types:
            output_filename = f"{txt_file.stem}_{img_type}.png"
            output_filepath = output_path / output_filename

            try:
                generator.generate(
                    novel_text=novel_text,
                    image_type=img_type,
                    genre=genre,
                    title=txt_file.stem,
                    output_path=str(output_filepath)
                )
            except Exception as e:
                print(f"❌ {output_filename} 생성 실패: {e}")
                continue

    print(f"\n✅ 배치 작업 완료! 결과: {output_dir}")


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(description="웹소설 마케팅 이미지 배치 생성기")
    parser.add_argument("--input-dir", required=True, help="입력 디렉토리 (웹소설 .txt 파일들)")
    parser.add_argument("--output-dir", default="./output", help="출력 디렉토리")
    parser.add_argument(
        "--types",
        default="sns,youtube",
        help="생성할 이미지 타입 (쉼표로 구분, 예: sns,youtube,teaser)"
    )
    parser.add_argument("--genre", default="drama", help="웹소설 장르")

    args = parser.parse_args()

    # 이미지 타입 파싱
    image_types = [t.strip() for t in args.types.split(",")]

    process_batch(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        image_types=image_types,
        genre=args.genre
    )


if __name__ == "__main__":
    main()
