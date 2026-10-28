# 히어로 영상 제작법

근거: `README.md` 「히어로 영상 (2026-09-13 4차)」 절 + 결과 파일 ffprobe + 1초 간격 프레임 확인.
README 에 적힌 명령은 **사진 줌 컷 하나뿐**이다. 나머지 명령은 결과 파일 규격에 맞춘 **재현용 예시**이며 원래 쓴 값(CRF 등)은 확인 필요.

## 1. 원칙 (이 사이트에서 배운 것)

1. **AI 영상은 한글·간판을 뭉갠다.** 글자가 보이는 장면(현수막·무대 LED·간판)은 AI 로 만들지 않는다.
   → 글자가 있는 장면은 **원본 사진을 ffmpeg zoompan 으로 천천히 줌**하는 실사 컷으로 만든다(글자 정확).
   → AI 드론 컷은 **간판·무대 화면 글자가 없는 장면**으로만 생성한다(강변 축제·야간 콘서트 등).
2. 글자가 뭉개진 AI 컷(`_raw/ai/b2 b3 b4 d1 d3`)은 버렸다. 생성 후 반드시 프레임을 넘겨 보며 글자·로고·사람 손가락을 확인한다.
3. 실사(원본 사이트 영상) 컷을 섞어 「NOW SHOWING · REAL FOOTAGE」 문구가 거짓이 되지 않게 한다 — 10컷 중 AI 는 3컷(2·5·7)뿐.
4. 영상에 박힌 워터마크 「CREATIVE PLAN PROEVENT」 는 프로이벤트 것이므로 지우지 않고 그대로 둔다.
5. 사진 출처 규칙과 같다: 프로이벤트 원본만, 다른 회사 사진·스톡·AI 사진을 실사처럼 넣지 않는다.

## 2. 컷 표 (4차, 1920×1080, 10컷, 0.5초 크로스페이드, 총 26.92초)

| 순서 | 대략 위치(초) | 출처 | 내용 | 글자 |
|---|---|---|---|---|
| 1 | 0~2 | 원본 영상 slide02 0~2s | 드론 오프닝 — 숲 속 광장 천막·이동식 수영장·에어바운스 (포스터와 같은 장면) | 없음 |
| 2 | 2~5 | AI 텍스트→영상 (Wan 2.6 1080p) | 강변 축제 드론 · 대관람차 · 불꽃 · 천막 | 없음(의도) |
| 3 | 5~8 | 사진 w14 줌 | 워터밤 야간 무대(분수·조명·관객) | 워터마크 |
| 4 | 8~11 | 원본 slide02 32.5s~ | 드론 — 수영장·천막 내려다보기 | 없음 |
| 5 | 11~13 | AI 사진→영상 (Wan 2.6 flash, 입력 w11) 중 2.6~5s 구간 | 국회 앞 에어바운스 와이드 | 워터마크 |
| 6 | 13~15 | 원본 slide01 85.5s~ | 레드카펫 통로(유리문) | 작음 |
| 7 | 15~18 | AI 텍스트→영상 (Wan 2.6) | 야간 콘서트 드론 · 불꽃 · LED 무대(글자 없음) | 없음(의도) |
| 8 | 18~21 | 사진 w18 줌 | 「2025 제5회 순천시 읍면동 체육대회」 현수막 | **정확해야 함** |
| 9 | 21~24 | 사진 w17 줌 | 「2025 이용자간담회」 홀 | **정확해야 함** |
| 10 | 24~27 | 원본 slide01 79s~ | 테이프 커팅 | 작음 |

- 「대략 위치」는 1초 간격 프레임으로 본 것(크로스페이드 때문에 ±0.5초).
- 원본 slide01·slide02 = 프로이벤트 원본 사이트(pro-event.kr)의 영상. 원본·AI 결과·마스터(`_raw/master_1080.mp4`)는 `_raw/`(gitignore)에만 있고 **레포에 없다**.
- 확인 필요: 8번 현수막은 「순천시 읍면동 체육대회」인데 `app.js` WORKS 에서 w18 제목은 「총동문회 체육대회 · 초대가수 섭외」다. 어느 쪽이 맞는지 대표 확인 전에는 둘 다 고치지 말 것.

## 3. 컷 만들기

### 사진 줌 컷 (README 원문 명령)

```bash
ffmpeg -loop 1 -i 사진.jpg -frames:v 88 -vf "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='min(zoom+0.0018,1.18)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=88:s=1920x1080:fps=25" -r 25 …
```

- 88프레임 = 25fps 에서 3.52초. 확대는 프레임당 0.0018, 최대 1.18배, 가운데 고정.
- 4K 로 먼저 키운 뒤 zoompan 하는 이유: 1080p 에서 바로 줌하면 계단·떨림이 생긴다.
- 출력 부분(`…`)은 README 에 생략돼 있다. 예: `-an -c:v libx264 -pix_fmt yuv420p -crf 18 cut08.mp4` (예시).
- **반복문 안에서 ffmpeg 를 돌릴 땐 꼭 `-nostdin`** (README). 없으면 ffmpeg 가 표준입력을 먹어 반복이 깨진다.

### 원본 영상 구간 컷 (예시)

```bash
ffmpeg -nostdin -ss 32.5 -i _raw/slide02.mp4 -t 3.5 -an \
  -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=25,format=yuv420p" \
  -c:v libx264 -crf 18 cut04.mp4
```

### AI 컷 (Wan 2.6)

- 텍스트→영상: 글자 없는 드론 장면만. 프롬프트에 간판·현수막·LED 글자를 넣지 않는다.
- 사진→영상(flash): 원본 사진(w11)을 넣어 카메라만 움직이게. 결과 중 깨지지 않은 구간만 잘라 쓴다(5번은 2.6~5초).
- 생성 도구·프롬프트 원문은 레포에 기록이 없다(확인 필요).

## 4. 잇기 (0.5초 크로스페이드, 예시)

xfade 의 offset = (앞 컷들 길이 합) − (앞에서 한 페이드 수 × 0.5).

```bash
# 컷 길이가 d1..d10 이면 k번째 xfade offset = (d1+…+dk) - k*0.5
ffmpeg -nostdin -i cut01.mp4 -i cut02.mp4 … -i cut10.mp4 -filter_complex \
 "[0][1]xfade=transition=fade:duration=0.5:offset=O1[v1];[v1][2]xfade=transition=fade:duration=0.5:offset=O2[v2]; … [v8][9]xfade=transition=fade:duration=0.5:offset=O9,format=yuv420p[v]" \
 -map "[v]" -an -c:v libx264 -crf 18 _raw/master_1080.mp4
```

모든 컷은 같은 해상도·fps(25)·픽셀형식이어야 xfade 가 된다.

## 5. 세 가지 크기로 내보내기 (결과 규격에 맞춘 예시)

| 파일 | 규격 | 예시 명령 핵심 |
|---|---|---|
| `assets/video/hero.mp4` | 1920×1080, ≈3.3Mbps, 11MB | `-vf scale=1920:1080` |
| `assets/video/hero_md.mp4` | 1280×720, ≈1.8Mbps, 6MB | `-vf scale=1280:720` |
| `assets/video/hero_sm.mp4` | 854×480, ≈0.85Mbps, 2.9MB | `-vf scale=854:480` |

공통: `ffmpeg -nostdin -i _raw/master_1080.mp4 -an -c:v libx264 -profile:v high -pix_fmt yuv420p -r 25 -movflags +faststart …`
- **오디오 없음**(muted 자동재생이라 소리 트랙이 필요 없고 용량만 늘림).
- **faststart 필수**(현재 세 파일 모두 moov 가 앞에 있음) — 없으면 폰에서 다 받을 때까지 안 나온다.
- CRF·preset 원값은 확인 필요. 용량 목표: 폰용 3MB 안팎, 1080p 11MB 안팎.

포스터 `assets/img/hero_poster.webp`(1600×900)는 1번 컷과 같은 드론 장면이다(프레임 비교로 확인, 정확한 추출 시점은 확인 필요). 영상을 바꾸면 첫 컷과 포스터를 맞춰야 로딩 중→재생 전환이 튀지 않는다. 예: `ffmpeg -nostdin -ss 0.5 -i hero.mp4 -frames:v 1 -vf scale=1600:900 -quality 80 hero_poster.webp`

## 6. 페이지에 넣는 방식 (index.html 66~69행, app.js 57~73행)

```html
<video id="heroVideo" muted loop playsinline preload="auto" poster="assets/img/hero_poster.webp"
  data-src="assets/video/hero.mp4" data-src-md="assets/video/hero_md.mp4" data-src-sm="assets/video/hero_sm.mp4"></video>
```

- `src` 를 HTML 에 직접 쓰지 않는다 → JS 가 `innerWidth × min(DPR,2)` 로 고른다: <900 sm, <1300 md, 그 외 1080p.
- 뒤에 `.poster` div(배경 이미지)를 깔아 영상이 늦어도 화면이 비지 않게.
- 자동재생 실패 대비: canplay, 첫 터치, 다시 화면에 들어올 때, 이유 없는 pause 시 최대 8회 재시도. 사용자가 `#sound` 로 멈춘 건 존중.
- 위에 어둠막(`.scrim`: 위·아래·왼쪽 어둡게) — 밝은 컷에서도 흰 h1 이 읽혀야 한다. 컷을 바꾸면 375px 폭에서 글자 대비를 다시 볼 것.
- README 파일 표 맨 위의 「1280×720, 26.5초, 8MB, 11컷」은 이전 판 설명이다. 실제 파일은 위 표(4차)가 맞다.

## 7. 다시 만들 때 순서

1. 원본 영상·사진 확보(프로이벤트 원본만). `_raw/` 에 둔다(커밋 금지).
2. 글자 있는 장면 목록 → 사진 줌 컷. 글자 없는 장관 → 원본 드론 컷, 부족하면 AI(글자 없는 장면만).
3. AI 결과는 프레임 단위로 검수, 깨진 구간 버림.
4. 컷 3~3.5초, 0.5초 크로스페이드, 25~30초 전체, 첫 컷 = 포스터 장면.
5. 마스터 → 3가지 크기, 오디오 제거, faststart.
6. 375 / 1280 에서 재생·포스터·글자 대비 확인. 폰 실제 기기에서 자동재생 확인(저전력 모드 포함).
