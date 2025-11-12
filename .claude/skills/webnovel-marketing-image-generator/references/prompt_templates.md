# 이미지 생성 프롬프트 템플릿

## 기본 구조

모든 프롬프트는 다음 요소를 포함합니다:

```
[장면 설명] + [스타일] + [분위기] + [기술 파라미터]
```

## 장르별 프롬프트

### 로맨스

#### 커플 장면
```
A romantic scene of [character A description] and [character B description]
gazing at each other under [setting],
soft pastel colors, dreamy atmosphere, bokeh background,
manhwa style, high quality digital art, detailed faces
```

**예시**:
```
A romantic scene of a tall man in a business suit and a young woman in a flowing dress
gazing at each other under cherry blossom trees,
soft pastel pink and white colors, dreamy atmosphere, bokeh background,
manhwa style, high quality digital art, detailed faces, warm lighting
```

#### 고백 장면
```
[Character] confessing love with emotional expression,
[setting description], sunset lighting, dramatic composition,
korean webtoon art style, cinematic, 4k quality
```

### 판타지

#### 마법 전투
```
Epic fantasy battle scene, [character] casting [spell type] magic,
glowing [color] magic circles, medieval armor, dramatic lighting,
fantasy landscape background, volumetric lighting,
detailed illustration, trending on artstation
```

**예시**:
```
Epic fantasy battle scene, silver-haired mage casting ice magic,
glowing blue magic circles, ornate robes, dramatic lighting,
ancient castle ruins background, volumetric fog,
detailed illustration, cinematic composition, 8k quality
```

#### 왕궁/궁정
```
Majestic [palace/throne room], [character] in [royal attire],
golden accents, ornate architecture, stained glass windows,
fantasy medieval setting, grand composition,
high detail, professional digital painting
```

### 스릴러/미스터리

#### 긴장감 조성
```
Dark mysterious scene, [character] in shadows,
noir atmosphere, dramatic lighting, high contrast,
urban night setting, rain effects, moody color grading,
thriller movie poster style, photorealistic
```

**예시**:
```
Dark mysterious scene, detective in trench coat standing in alley,
noir atmosphere, dramatic side lighting, high contrast black and blue,
urban night setting, rain puddles reflecting neon signs,
thriller movie poster style, cinematic composition
```

#### 반전 장면
```
Shocking revelation moment, [character] with surprised expression,
dramatic spotlight, blurred background, focus on face,
intense emotion, dark thriller aesthetic,
professional illustration, story climax atmosphere
```

### 현대 드라마

#### 일상 장면
```
Modern realistic scene, [character] in [everyday situation],
contemporary Korean city setting, natural lighting,
slice of life atmosphere, clean composition,
webtoon illustration style, relatable mood
```

**예시**:
```
Modern realistic scene, office worker drinking coffee at cafe window,
contemporary Seoul cityscape background, soft morning light,
slice of life atmosphere, clean minimalist composition,
webtoon illustration style, warm and relatable mood
```

#### 갈등 장면
```
Emotional confrontation, [character A] and [character B] facing each other,
tense atmosphere, modern interior, dramatic shadows,
korean drama cinematography, detailed facial expressions,
high quality digital art, 16:9 composition
```

## 캐릭터 프로필용 프롬프트

### 남성 주인공
```
Character portrait of [age] year old Korean man,
[hair style and color], [eye color], [distinctive features],
[outfit description], [personality trait] expression,
professional character design, clean background,
manhwa/webtoon style, full color, high detail
```

**예시**:
```
Character portrait of 28 year old Korean man,
short black hair slightly messy, deep brown eyes, sharp jawline,
black business suit with loosened tie, confident but tired expression,
professional character design, white gradient background,
manhwa style, full color illustration, 8k quality
```

### 여성 주인공
```
Character portrait of [age] year old Korean woman,
[hair description], [eye description], [features],
wearing [outfit], [emotion/personality] expression,
detailed character sheet style, soft lighting,
webtoon art style, vibrant colors, professional quality
```

### 악역/조연
```
[Role] character design, [age] [gender],
[distinctive villainous/supporting features],
[costume that reflects their role],
[characteristic expression],
detailed character concept art, dynamic pose,
korean webtoon style, dramatic lighting
```

## SNS 마케팅용 특수 프롬프트

### 카드뉴스형
```
Social media card design, [key scene or quote],
minimalist composition, bold typography area,
[genre-appropriate color palette],
instagram post style, 1:1 ratio, clean and modern,
professional graphic design, eye-catching
```

### 유튜브 썸네일
```
YouTube thumbnail style, [dramatic scene],
character in dynamic pose, exaggerated expression,
bold text area for title, high contrast colors,
clickbait but professional, 16:9 ratio,
attention-grabbing composition, trending style
```

### 티저 포스터
```
Movie poster style teaser, [main character(s)],
[genre atmosphere], dramatic composition,
space for title text overlay, 9:16 vertical ratio,
cinematic lighting, professional movie marketing aesthetic,
high quality digital art, compelling visual
```

## 기술 파라미터 가이드

### 품질 향상
- `high quality`, `8k`, `4k`, `detailed`, `professional`
- `masterpiece`, `trending on artstation`
- `highly detailed`, `ultra realistic`

### 스타일 지정
- `manhwa style`, `webtoon art style`, `korean webtoon`
- `digital painting`, `illustration`, `concept art`
- `anime style`, `semi-realistic`

### 조명 효과
- `dramatic lighting`, `cinematic lighting`
- `soft lighting`, `volumetric lighting`
- `golden hour`, `sunset lighting`, `neon lights`

### 구도/카메라
- `cinematic composition`, `rule of thirds`
- `close-up portrait`, `wide shot`, `medium shot`
- `dutch angle`, `from below`, `bird's eye view`

## 네거티브 프롬프트

항상 포함할 것:
```
low quality, blurry, distorted, ugly, bad anatomy,
extra limbs, poorly drawn hands, poorly drawn face,
mutation, deformed, bad proportions, duplicate,
watermark, signature, text errors
```

## 프롬프트 조합 예시

### 완성된 로맨스 장면 프롬프트
```
Positive:
A romantic scene of a handsome man in dark blue suit and beautiful woman in white dress
standing face to face in modern rooftop garden at sunset,
Seoul city skyline background, cherry blossom petals floating,
soft pink and golden lighting, dreamy bokeh effect,
manhwa style, highly detailed faces, emotional atmosphere,
professional digital art, cinematic composition, 8k quality

Negative:
low quality, blurry, distorted, ugly, bad anatomy,
poorly drawn hands, mutation, watermark, duplicate
```

### 완성된 판타지 전투 프롬프트
```
Positive:
Epic fantasy battle, silver-haired female knight wielding flaming sword,
casting fire magic with glowing red magic circles,
ornate silver armor with gold details, flowing cape,
ancient ruins background, dramatic sunset, volumetric fog,
dynamic action pose, detailed illustration,
trending on artstation, cinematic lighting, 4k quality

Negative:
low quality, static pose, boring composition,
modern elements, bad anatomy, poorly drawn weapon,
blurry, watermark, signature
```

## 프롬프트 최적화 팁

1. **우선순위 순서**: 중요한 요소를 앞쪽에 배치
2. **구체성**: "beautiful" 대신 "elegant with soft features"
3. **일관성**: 스타일 키워드 중복 사용 (manhwa, webtoon 등)
4. **균형**: 너무 많은 요소 지양 (20개 이하 ���워드 권장)
5. **테스트**: 동일 장면을 다양한 프롬프트로 실험
