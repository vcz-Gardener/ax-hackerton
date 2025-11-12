#!/usr/bin/env python3
"""
환경 검증 및 빠른 테스트 스크립트

사용법:
    python quick_test.py
"""

import os
import sys


def check_environment():
    """환경변수 및 패키지 검증"""
    print("🔍 환경 검증 시작...\n")

    # 1. 환경변수 체크
    print("1️⃣  환경변수 확인")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    hf_token = os.getenv("HUGGINGFACE_TOKEN")

    if not api_key:
        print("   ❌ ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다")
        print("   👉 설정 방법: export ANTHROPIC_API_KEY='sk-ant-...'")
        return False
    else:
        print(f"   ✅ ANTHROPIC_API_KEY: {api_key[:15]}...")

    if not hf_token:
        print("   ❌ HUGGINGFACE_TOKEN 환경변수가 설정되지 않았습니다")
        print("   👉 설정 방법: export HUGGINGFACE_TOKEN='hf_...'")
        return False
    else:
        print(f"   ✅ HUGGINGFACE_TOKEN: {hf_token[:10]}...")

    # 2. 패키지 체크
    print("\n2️⃣  필수 패키지 확인")
    required_packages = {
        "anthropic": "Anthropic API 클라이언트",
        "huggingface_hub": "Hugging Face API 클라이언트",
        "PIL": "이미지 처리 라이브러리"
    }

    all_installed = True
    for package, description in required_packages.items():
        try:
            if package == "PIL":
                __import__("PIL")
            else:
                __import__(package)
            print(f"   ✅ {package}: {description}")
        except ImportError:
            print(f"   ❌ {package}: 설치되지 않음")
            print(f"      pip install {package.replace('_', '-')}")
            all_installed = False

    if not all_installed:
        return False

    print("\n✅ 모든 환경 검증 통과!\n")
    return True


def test_api_connection():
    """API 연결 테스트"""
    print("🔌 API 연결 테스트...\n")

    try:
        import anthropic
        from huggingface_hub import InferenceClient

        # Claude API 테스트
        print("1️⃣  Claude API 연결 테스트")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": "안녕하세요! 한 단어로 답해주세요."}]
        )
        print(f"   ✅ Claude 응답: {response.content[0].text[:50]}")

        # Hugging Face API 테스트
        print("\n2️⃣  Hugging Face API 연결 테스트")
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        hf_client = InferenceClient(token=hf_token)
        print("   ✅ Hugging Face 클라이언트 초기화 성공")
        print("   ℹ️  이미지 생성은 실제 사용 시 테스트됩니다 (시간 소요)")

        print("\n✅ 모든 API 연결 성공!\n")
        return True

    except Exception as e:
        print(f"   ❌ API 연결 실패: {e}")
        return False


def create_sample_text():
    """샘플 웹소설 텍스트 생성"""
    sample_text = """그날, 나는 처음으로 그를 봤다.
카페 창가에 앉아 책을 읽고 있는 그의 옆모습은 마치 영화 속 한 장면 같았다.
햇살이 그의 검은 머리카락을 비추고 있었고, 그의 손가락은 책장을 천천히 넘기고 있었다.

'저 사람이 내 운명일까?'

나도 모르게 그렇게 생각했다.
그리고 그 생각은 틀리지 않았다."""

    with open("sample_novel.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)

    print("📝 샘플 웹소설 텍스트 생성 완료: sample_novel.txt\n")
    return "sample_novel.txt"


def run_quick_test():
    """빠른 이미지 생성 테스트"""
    print("🎨 빠른 이미지 생성 테스트...\n")

    try:
        from generate_marketing_image import WebnovelMarketingGenerator

        # 샘플 텍스트 생성
        sample_file = create_sample_text()

        # 텍스트 읽기
        with open(sample_file, "r", encoding="utf-8") as f:
            novel_text = f.read()

        # 생성기 초기화
        api_key = os.getenv("ANTHROPIC_API_KEY")
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        generator = WebnovelMarketingGenerator(api_key, hf_token)

        # 이미지 생성
        print("이미지 생성 중... (약 10-20초 소요)")
        output_path = generator.generate(
            novel_text=novel_text,
            image_type="sns",
            genre="romance",
            title="첫 만남",
            output_path="test_output.png"
        )

        print(f"\n✅ 테스트 이미지 생성 완료: {output_path}")
        print("   이미지를 열어서 결과를 확인해보세요!\n")
        return True

    except Exception as e:
        print(f"❌ 테스트 실패: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print(" 웹소설 마케팅 이미지 생성기 - 빠른 테스트")
    print("=" * 60)
    print()

    # 1. 환경 검증
    if not check_environment():
        print("⚠️  환경 설정을 완료한 후 다시 실행해주세요.")
        sys.exit(1)

    # 2. API 연결 테스트
    if not test_api_connection():
        print("⚠️  API 연결 문제를 해결한 후 다시 실행해주세요.")
        sys.exit(1)

    # 3. 빠른 이미지 생성 테스트
    print("=" * 60)
    user_input = input("빠른 이미지 생성 테스트를 실행하시겠습니까? (y/n): ")
    if user_input.lower() in ['y', 'yes', '예']:
        run_quick_test()
    else:
        print("\n테스트를 건너뛰었습니다.")

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)
    print("\n이제 다음 명령어로 실제 이미지를 생성해보세요:")
    print("python generate_marketing_image.py --input novel.txt --type sns --genre romance")
    print()


if __name__ == "__main__":
    main()
