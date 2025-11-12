---
name: webnovel-marketing-image-generator
description: 웹소설의 핵심 장면을 SNS 홍보용 이미지로 자동 변환. 캐릭터 프로필, 명대사, 하이라이트 장면을 티저/썸네일/프로모션 이미지로 생성하여 마케팅 효율 극대화.
---

# 웹소설 마케팅 이미지 생성기

## 목적

웹소설 플랫폼(글링)의 작가와 마케터가 작품을 효과적으로 홍보할 수 있도록, 텍스트 기반 콘텐츠를 시각적 마케팅 자료로 자동 변환합니다.

## 사전 준비

### 필수 API 키
1. **Anthropic API 키**: [발급 방법](SETUP.md#1-anthropic-api-키-발급)
2. **Hugging Face 토큰**: [발급 방법](SETUP.md#2-hugging-face-토큰-발급-무료)

### 환경변수 설정
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export HUGGINGFACE_TOKEN="hf_..."
```

### 패키지 설치
```bash
pip install -r requirements.txt
```

**상세 가이드**: [SETUP.md](SETUP.md) 참조

## 핵심 기능

### 1. 4가지 비주얼 스타일 (신규) 🎨
사용자가 마케팅 목적에 맞게 이미지 스타일을 선택할 수 있습니다:

- **Photorealistic (실사화)**: 영화 포스터 같은 드라마틱한 사진 스타일
  - 용도: 시리즈 메인 포스터, 프리미엄 광고
  - 특징: 영화급 조명, 카메라 앵글, 심도 표현

- **Sticker (스티커)**: 귀엽고 캐주얼한 아이콘 스타일
  - 용도: SNS 프로필, 이모티콘, 굿즈 디자인
  - 특징: 투명 배경, 깔끔한 라인, 치비 캐릭터

- **Figure (피규어)**: 나노 바나나 스타일의 미니어처 느낌
  - 용도: 수집 이벤트, 한정판 굿즈 홍보
  - 특징: 3D 피규어 렌더링, 수집 욕구 자극

- **Anime (애니메이션)**: 일본 애니메이션 스타일
  - 용도: 웹툰 홍보, 영상 썸네일, 팬아트
  - 특징: 풍부한 감정 표현, 동적 구도, 셀 셰이딩

**상세 가이드**: [references/image_style_guide.md](references/image_style_guide.md)

### 2. 장면 추출 및 분석
- 웹소설 텍스트에서 시각적으로 임팩트 있는 장면 자동 추출
- 감정선이 높은 대화, 클라이맥스, 캐릭터 등장 장면 식별

### 3. 이미지 타입별 생성
- **SNS 카드뉴스**: 인스타그램/트위터용 정사각형 (1:1)
- **유튜브 썸네일**: 16:9 비율, 클릭 유도 텍스트 포함
- **티저 포스터**: 세로형 (9:16), 스토리 하이라이트
- **캐릭터 프로필**: 캐릭터 중심 비주얼 + 소개 텍스트

### 4. 지능형 프롬프트 확장 (신규) 🤖
사용자의 간단한 장면 설명을 AI가 자동으로 상세 프롬프트로 확장:

- **스타일별 기술 디테일 추가**: 조명, 카메라 앵글, 재질 표현
- **장르 분위기 반영**: 로맨스는 따뜻하게, 스릴러는 어둡게
- **추가 디테일 선택**: 시간대(golden hour), 날씨(rainy), 감정(tense)
- **고품질 키워드 자동 삽입**: 8K, professional, cinematic 등

**예시**:
```
사용자 입력: "warrior with sword"
AI 확장: "High-quality modern anime style, detailed digital painting,
         warrior character holding glowing sword, dynamic battle pose,
         cinematic lighting with rim light effects, epic fantasy atmosphere,
         Korean manhwa aesthetic, 8K resolution, professional anime production quality"
```

### 5. 자동 디자인 요소
- 장르에 맞는 색상 팔레트 적용 (로맨스: 파스텔, 판타지: 진한 색, 스릴러: 어두운 톤)
- 폰트 자동 선택 및 타이포그래피 최적화
- 작품 로고/제목 자동 배치
- 명대사 강조 레이아웃

### 6. 프로세스 로깅 및 디버깅 (신규) 📋
모든 생성 과정을 터미널과 로그 파일에 기록:

- 확장된 프롬프트 전문 출력
- 각 단계별 성공/실패 상태
- API 호출 결과 및 오류 메시지
- 생성 시간 및 파일 크기 정보

**로그 저장 위치**: `.claude/skills/webnovel-marketing-image-generator/logs/`

## 워크플로우

### Phase 1: 콘텐츠 분석
```
사용자 입력 → 텍스트 분석 → 핵심 장면/대사 추출 → 감정/장르 태깅
```

### Phase 2: 마케팅 문구 생성 (SLAP)
```
장면 분석 → SLAP 프레임워크 적용 → 5단계 창의성 레벨 제안 → 사용자 선택
```
- **Stop**: 시선을 확 끄는 첫 문장
- **Look**: 핵심 포인트를 직관적으로 제시
- **Act**: 명확한 행동 유도
- **Purchase**: 구매/구독 전환 유도

**창의성 레벨**:
- 레벨 1 (보수적) → 레벨 5 (파격적)까지 5가지 옵션 제공
- 사용자가 마케팅 전략에 맞게 선택 가능

### Phase 3: 비주얼 기획
```
장면 해석 → 이미지 구도 결정 → 색상/폰트 선택 → 레이아웃 설계
```

### Phase 4: 이미지 생성
```
AI 이미지 생성 → SLAP 텍스트 오버레이 → 브랜딩 요소 추가 → 최종 출력
```

## 사용 시나리오

### 시나리오 A: 신작 홍보
**입력**: 웹소설 1화 전체 텍스트
**출력**:
- 주인공 첫 등장 장면 티저 이미지
- 핵심 갈등 소개 카드뉴스 (3장)
- 유튜브 예고편용 썸네일

### 시나리오 B: 화제 장면 바이럴
**입력**: 특정 회차의 명장면 텍스트
**출력**:
- 대사 중심 SNS 이미지 (인스타그램 스토리용)
- 반전 장면 스포일러 방지 블러 처리 이미지
- 댓글 유도 질문 포함 이미지

### 시나리오 C: 캐릭터 소개
**입력**: 캐릭터 설정 텍스트 (외모, 성격, 배경)
**출력**:
- 캐릭터 프로필 카드
- 대표 대사 포함 캐릭터 이미지
- 캐릭터 관계도 다이어그램

### 시나리오 D: SLAP 마케팅 문구 생성 (신규)
**입력**: 웹소설 핵심 장면 텍스트
**프로세스**:
1. Claude가 작품을 분석하여 5가지 SLAP 문구 제안 (보수적→파격적)
2. 사용자가 마케팅 전략에 맞는 레벨 선택 (예: "레벨 5로 작업해줘")
3. 선택된 문구를 이미지에 자동 오버레이

**출력 예시 (레벨 5 - 파격적)**:
- Stop: 손오공: "이번 생은 검으로 먹고 살아볼까?"
- Look: 신무림 서유기 | 웹소설 역사를 다시 쓴다
- Act: 읽지 않으면 당신만 모름
- Purchase: 지금 읽는 1000명에게 작가 사인 이벤트

**상세 가이드**: [references/marketing_best_practices.md](references/marketing_best_practices.md#slap-마케팅-문구-프레임워크)

### 시나리오 E: 스타일 선택 생성 (신규) 🎨
**입력**: "손오공이 검을 든 장면을 anime 스타일로 만들어줘"

**프로세스**:
1. 스타일 선택: anime
2. 프롬프트 자동 확장: "warrior with sword" → 상세 anime 프롬프트
3. 장르 분위기 적용: fantasy → 웅장하고 신비로운 톤
4. 이미지 생성 + 로그 기록

**출력**:
- 애니메이션 스타일의 판타지 전사 이미지 (1080x1080)
- 로그 파일: 확장된 프롬프트 전문, 생성 시간, 결과 상태

**명령어 예시**:
```bash
python scripts/generate_with_style.py \
  --prompt "warrior with glowing sword in fantasy world" \
  --style anime \
  --text "검으로 세상을 구한다" \
  --genre fantasy \
  --title "신화의 검" \
  --time "golden hour" \
  --emotion "determined" \
  --output my_anime_image.png
```

## 기술 스택

### 이미지 생성
- **Anthropic Claude API**: 장면 해석 및 프롬프트 생성
- **Hugging Face Inference API (FLUX.1-dev)**: 실제 이미지 생성 (무료, 시간당 300회)
- **Pillow (PIL)**: 텍스트 오버레이 및 후처리

### 디자인 자동화
- 장르별 색상 팔레트 데이터베이스
- 폰트 라이브러리 (한글 지원 필수)
- 템플릿 기반 레이아웃 시스템

### 비용
- **Anthropic Claude**: 이미지당 약 $0.01 (신규 가입 시 $5 무료 크레딧)
- **Hugging Face**: 완전 무료 (카드 등록 불필요)

## 실행 방법

### 1. 기본 사용
```python
python scripts/generate_marketing_image.py \
  --input "웹소설_텍스트.txt" \
  --type sns \
  --genre romance
```

### 2. 배치 생성
```python
python scripts/batch_generate.py \
  --input-dir ./novels \
  --output-dir ./marketing_images \
  --types sns,youtube,teaser
```

### 3. 대화형 모드
```python
python scripts/interactive_generator.py
# 프롬프트에서 단계별 입력 및 미리보기
```

## 주의사항

- **저작권**: 생성된 이미지는 원작의 2차 창작물로 간주, 상업적 사용 전 권리 확인 필요
- **스포일러 관리**: 핵심 반전이 포함된 장면은 블러 처리 또는 텍스트만 사용 권장
- **브랜드 가이드라인**: 글링 플랫폼의 CI/BI 적용 시 `assets/templates/brand_guide.json` 참조

## 확장 계획

- [ ] 실시간 AB 테스트 (여러 버전 동시 생성 및 성과 추적)
- [ ] 동영상 티저 자동 생성 (이미지 → 짧은 영상 변환)
- [ ] 타닥(AI 채팅 게임) 시각화 연동
- [ ] 다국어 지원 (영문 웹소설 → 글로벌 마케팅 이미지)

## 참조 문서

- [웹소설 마케팅 베스트 프랙티스](references/marketing_best_practices.md)
- [장르별 비주얼 가이드](references/genre_visual_guide.md)
- [이미지 생성 프롬프트 템플릿](references/prompt_templates.md)
