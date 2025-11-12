# 환경 설정 가이드

웹소설 마케팅 이미지 생성기를 사용하기 위한 환경 설정 방법입니다.

---

## 📋 필요 사항

### 1. Python 3.9 이상
```bash
# 버전 확인
python --version
# 또는
python3 --version
```

### 2. API 계정

#### A. Anthropic Claude API (필수)
- **용도**: 웹소설 텍스트 분석 및 장면 추출
- **비용**: 신규 가입 시 $5 무료 크레딧 제공

#### B. Hugging Face (필수)
- **용도**: AI 이미지 생성
- **비용**: **완전 무료** (시간당 300회 제한)

---

## 🔑 API 키 발급 방법

### 1. Anthropic API 키 발급

#### Step 1: 계정 생성
1. [Anthropic Console](https://console.anthropic.com/) 접속
2. Sign Up (Google/GitHub 계정으로 가능)
3. 이메일 인증 완료

#### Step 2: API 키 생성
1. [API Keys 페이지](https://console.anthropic.com/settings/keys) 접속
2. "Create Key" 클릭
3. 키 이름 입력 (예: "webnovel-generator")
4. 생성된 키 복사 (**한 번만 표시됨!**)

**형식**: `sk-ant-api03-...` (약 100자)

#### Step 3: 크레딧 확인
- 신규 계정: $5 무료 크레딧 자동 지급
- [Usage 페이지](https://console.anthropic.com/settings/usage)에서 잔액 확인
- 예상 사용량: 이미지 1개당 약 $0.01-0.02

---

### 2. Hugging Face 토큰 발급 (무료)

#### Step 1: 계정 생성
1. [Hugging Face](https://huggingface.co/) 접속
2. Sign Up (이메일 또는 GitHub)
3. ⭐ **카드 등록 불필요!**

#### Step 2: 토큰 생성
1. 로그인 후 프로필 클릭 → Settings
2. 왼쪽 메뉴에서 [Access Tokens](https://huggingface.co/settings/tokens) 선택
3. "New token" 클릭
4. 토큰 설정:
   - Name: `webnovel-image-gen`
   - Type: **Read** 선택 (Write 불필요)
5. "Generate token" 클릭
6. 생성된 토큰 복사

**형식**: `hf_...` (약 40자)

#### Step 3: 사용 제한 확인
- **무료 Tier**: 시간당 300회
- **등록 없이**: 시간당 1회
- 충분한 테스트 및 데모 가능!

---

## 💻 환경변수 설정

### macOS / Linux

#### 임시 설정 (현재 터미널 세션만)
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export HUGGINGFACE_TOKEN="hf_..."
```

#### 영구 설정 (권장)

**Bash 사용 시 (~/.bashrc 또는 ~/.bash_profile)**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.bashrc
echo 'export HUGGINGFACE_TOKEN="hf_..."' >> ~/.bashrc
source ~/.bashrc
```

**Zsh 사용 시 (~/.zshrc) - macOS 기본**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.zshrc
echo 'export HUGGINGFACE_TOKEN="hf_..."' >> ~/.zshrc
source ~/.zshrc
```

### Windows

#### PowerShell
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-api03-..."
$env:HUGGINGFACE_TOKEN="hf_..."
```

#### 영구 설정 (시스템 환경변수)
1. "시스템 환경 변수 편집" 검색
2. "환경 변수" 클릭
3. "새로 만들기"로 각 변수 추가

---

## 📦 패키지 설치

### Step 1: 프로젝트 디렉토리로 이동
```bash
cd .claude/skills/webnovel-marketing-image-generator
```

### Step 2: 의존성 설치
```bash
pip install -r requirements.txt
```

**설치되는 패키지:**
- `anthropic>=0.18.0` - Claude API 클라이언트
- `huggingface-hub>=0.20.0` - Hugging Face API 클라이언트
- `pillow>=10.0.0` - 이미지 처리 라이브러리

### Step 3: 설치 확인
```bash
python -c "import anthropic, huggingface_hub, PIL; print('✅ 모든 패키지 설치 완료')"
```

---

## ✅ 환경 검증

### 자동 검증 스크립트 실행
```bash
python scripts/quick_test.py
```

**검증 항목:**
- ✅ 환경변수 설정 확인
- ✅ 패키지 설치 확인
- ✅ Claude API 연결 테스트
- ✅ Hugging Face API 연결 테스트
- ✅ 샘플 이미지 생성 테스트

**예상 출력:**
```
🔍 환경 검증 시작...

1️⃣  환경변수 확인
   ✅ ANTHROPIC_API_KEY: sk-ant-api03-...
   ✅ HUGGINGFACE_TOKEN: hf_...

2️⃣  필수 패키지 확인
   ✅ anthropic: Anthropic API 클라이언트
   ✅ huggingface_hub: Hugging Face API 클라이언트
   ✅ PIL: 이미지 처리 라이브러리

✅ 모든 환경 검증 통과!
```

---

## 🎨 첫 이미지 생성하기

### Step 1: 샘플 텍스트 파일 생성
```bash
cat > test_novel.txt << 'EOF'
그날, 나는 처음으로 그를 봤다.
카페 창가에 앉아 책을 읽고 있는 그의 옆모습은
마치 영화 속 한 장면 같았다.
'저 사람이 내 운명일까?'
나도 모르게 그렇게 생각했다.
EOF
```

### Step 2: 이미지 생성 실행
```bash
python scripts/generate_marketing_image.py \
  --input test_novel.txt \
  --type sns \
  --genre romance \
  --title "첫 만남" \
  --output my_first_image.png
```

### Step 3: 결과 확인
- **출력 파일**: `my_first_image.png` (1080x1080px)
- **소요 시간**: 약 10-20초
- **비용**: Anthropic $0.01 + Hugging Face 무료

---

## 🔧 문제 해결

### Q1: "ANTHROPIC_API_KEY 환경변수를 설정해주세요" 오류

**원인**: 환경변수가 설정되지 않음

**해결:**
```bash
# 1. 환경변수 확인
echo $ANTHROPIC_API_KEY

# 2. 비어있다면 설정
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# 3. 다시 확인
echo $ANTHROPIC_API_KEY
```

---

### Q2: "HUGGINGFACE_TOKEN 환경변수를 설정해주세요" 오류

**원인**: Hugging Face 토큰 미설정

**해결:**
```bash
export HUGGINGFACE_TOKEN="hf_..."
```

---

### Q3: "No module named 'anthropic'" 오류

**원인**: 패키지 미설치

**해결:**
```bash
pip install anthropic huggingface-hub pillow
```

---

### Q4: "Rate limit exceeded" 오류 (Hugging Face)

**원인**: 시간당 300회 제한 초과

**해결 방법:**
1. **대기**: 1시간 후 자동 리셋
2. **Pro 계정**: $9/월로 무제한 사용 (선택사항)
3. **다른 모델**: SKILL.md 참조하여 모델 변경

---

### Q5: 한글 폰트가 깨짐

**원인**: NotoSansKR 폰트 미설치

**해결:**

**macOS:**
```bash
brew install font-noto-sans-cjk
```

**Ubuntu/Debian:**
```bash
sudo apt-get install fonts-noto-cjk
```

**Windows:**
1. [Noto Sans KR 다운로드](https://fonts.google.com/noto/specimen/Noto+Sans+KR)
2. C:\Windows\Fonts에 복사

**대안**: 스크립트가 자동으로 기본 폰트로 폴백됨 (품질 저하 가능)

---

### Q6: 이미지 생성이 너무 느림 (30초 이상)

**원인**: Hugging Face 무료 서버 혼잡

**해결:**
- 정상 범위: 10-30초
- 60초 이상: 다른 시간대 재시도
- 대안: 로컬 Stable Diffusion 설치 (고급)

---

## 📊 비용 계산

### 예상 비용 (이미지 1개당)

| 항목 | 비용 | 설명 |
|------|------|------|
| **Claude API** | ~$0.01 | 장면 분석 (input 500토큰 + output 200토큰) |
| **Hugging Face** | **무료** | 시간당 300회 제한 |
| **총계** | ~$0.01 | Anthropic $5 크레딧으로 약 500개 생성 가능 |

### 배치 작업 (100개 이미지)
- Claude API: $1.00
- Hugging Face: 무료 (단, 시간당 300개 제한)
- 예상 시간: 약 30-50분

---

## 🚀 다음 단계

환경 설정이 완료되었습니다! 이제:

1. [QUICK-START.md](../../QUICK-START.md) - 빠른 사용 가이드
2. [SKILL.md](SKILL.md) - 전체 기능 문서
3. [AX-HACKATHON-DEV-LOG.md](../../AX-HACKATHON-DEV-LOG.md) - 상세 개발 문서

---

## 📞 지원

문제가 지속되면:
- GitHub Issues 등록
- 팀 슬랙 채널: #ax-hackathon
- 이메일: [팀 이메일]

---

*마지막 업데이트: 2025년 11월 7일*
