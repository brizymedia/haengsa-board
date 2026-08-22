# 순천승주청년회의소 인트로 영상

`Landscapes Volume 4K (UHD).mp4` 에서 장면을 자동으로 골라
**2분짜리 1920×1080 인트로 영상**을 만듭니다.

- 구성과 멘트 전문 → [`구성표.md`](구성표.md)
- 문구·타이밍 설정 → [`config.json`](config.json)

---

## 1. 준비 (처음 한 번만)

파워셸을 열고 아래를 붙여넣으세요. ffmpeg 이 없으면 설치합니다.

```powershell
winget install Gyan.FFmpeg
```

설치 후 **파워셸 창을 닫았다 새로 여세요.** (PATH 를 다시 읽어야 합니다.)

## 2. 만들기

저장소를 받은 폴더에서:

```powershell
cd promo\suncheon-jc-intro
powershell -ExecutionPolicy Bypass -File .\만들기.ps1
```

원본 경로는 스크립트에 이미 넣어 뒀습니다. 다른 영상을 쓰려면:

```powershell
powershell -ExecutionPolicy Bypass -File .\만들기.ps1 -Source "D:\영상\다른원본.mp4"
```

끝나면 원본과 같은 폴더에 **`순천승주청년회의소_인트로.mp4`** 가 생기고
탐색기가 그 파일을 띄웁니다.

소요 시간은 4K 원본 기준 **10~25분** 정도입니다. 대부분 장면 분석에 쓰입니다.
두 번째부터는 분석 결과를 재사용해 훨씬 빨라집니다.

---

## 3. 마음에 안 들 때

### 멘트를 고치고 싶다

`config.json` 의 `ments` 에서 `text` 만 바꾸고:

```powershell
powershell -ExecutionPolicy Bypass -File .\만들기.ps1 -SubsOnly
```

`-SubsOnly` 는 이미 만든 컷을 그대로 쓰고 자막과 소리만 다시 입힙니다. **1~2분**이면 끝납니다.

### 어느 장면을 골랐는지 먼저 보고 싶다

```powershell
powershell -ExecutionPolicy Bypass -File .\만들기.ps1 -PlanOnly
```

컷별로 원본의 몇 초 지점을 쓰는지 목록만 뽑고 끝냅니다.
마음에 안 드는 컷이 있으면 `_intro_build\cuts.json` 의 `start` 값을 직접 고친 뒤
그 컷 파일(`_intro_build\cut03.mp4` 등)을 지우고 다시 돌리세요.

### 음악이 마음에 안 든다

원본의 다른 지점 음악을 쓰려면 시작 초를 지정합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\만들기.ps1 -SubsOnly -AudioStart 420
```

### 장면 선택이 엉성하다

기본은 키프레임만 훑는 **빠른 스캔**입니다. 정확도를 올리려면:

```powershell
$env:PYTHONIOENCODING="utf-8"
python .\build_intro.py --source "C:\Users\gilau\Videos\4K Video Downloader+\Landscapes Volume 4K (UHD).mp4" --full-scan
```

느리지만(원본 길이의 1/4 정도) 장면 전환을 훨씬 촘촘히 잡습니다.

---

## 4. 구조

```
build_intro.py    빌더 본체 (윈도우·리눅스 공용, ffmpeg 만 있으면 됨)
config.json       멘트·컷 길이·색보정·사운드 설정   ← 대부분의 수정은 여기
만들기.ps1        윈도우용 실행 스크립트
구성표.md         2분 구성과 멘트 전문
_intro_build/     중간 파일 (원본 폴더에 생김, 지워도 됨)
```

빌더가 하는 일:

1. **장면 분석** — 원본에서 장면이 바뀌는 지점을 찾습니다
2. **컷 배치** — 21개 컷을 영상 전체에 고르게 퍼뜨리되 장면 전환 직후로 붙입니다
3. **컷 렌더링** — 1920×1080 으로 맞추고 천천히 줌, 색보정, 비네트
4. **사운드** — 음악이 가장 꽉 찬 2분 구간을 통으로 잘라 페이드·정규화
5. **자막 + 인코딩** — 멘트를 얹고 H.264 로 최종 인코딩

## 5. 알아둘 것

- **배경 영상은 순천 풍경이 아닙니다.** 원본은 세계 각지의 풍경 모음이라
  "순천만의 물길이…" 같은 멘트는 비유로 읽힙니다. 실제 순천 풍경을 쓰려면
  순천만·국가정원·조계산 등을 직접 촬영하거나 확보한 뒤 `--source` 를 바꾸세요.
- **원본 영상의 저작권을 확인하세요.** 다운로드한 스톡 영상이라면 상업적·공개
  이용 조건을 먼저 확인해야 합니다. 대외 홍보용으로 배포할 계획이면 특히 그렇습니다.
- 폰트는 설치된 것 중에서 Pretendard → 맑은 고딕 순으로 자동으로 고릅니다.
