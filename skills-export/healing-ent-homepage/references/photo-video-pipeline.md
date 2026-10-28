# 사진 · 히어로 영상 만드는 법

도구 3개는 이 스킬 `scripts/` 에 복사해 두었다(원본 `/home/user/haengsa-board/homepages/_tools/`). 공통 지침 BRIEF.md 4~5장의 방식 그대로다.

## 1. 원칙
- 고객 본인 네이버 블로그(**leehh2153**) · 고객이 준 자료(대표 MC 프로필 PDF · 카톡 사진)만. AI 그림 · 인포그래픽 · 글자판 · 캡처 · 남의 뉴스 사진 · 다른 회사 워터마크 금지.
  블로그에 섞인 AI 썸네일(ChatGPT 이미지)도 뺐다.
- 학생 · 아이 사진은 원경 · 뒷모습 위주, 얼굴이 크게 나온 근접 사진 금지(블로그 photos.json 도 「얼굴 큰 사진 제외」).
- 받은 사진은 `Read` 로 직접 보고 고른다. 출처는 `assets/img/SOURCES.md` 에 「파일명 — 글 제목 — 글 주소 (원본 이름)」.
- 크기: `works/` 긴 변 1600px webp, `works/th/` 800px 썸네일. 대표 실적 `sig/` 는 프로필 PDF 쪽에서 잘라냄.
- 새 사진을 넣으면 같이 고칠 곳: `assets/img/SOURCES.md` · `assets/app.js WORKS`(f · t 제목 · o 장소 · c 분류) · 필요하면 `_blog/photos.json`(블로그용, 장소를 아는 사진만 `지역`) · `make_pages.py` 의 photos.

## 2. 네이버 블로그 사진 받기 (이 환경은 blog.naver.com · pstatic 직접 접속이 막혀 있다)
Firecrawl MCP 도구로 우회한다: `mcp__Firecrawl-cd3a0493__firecrawl_scrape`, 안 되면 `mcp__Firecrawl__firecrawl_scrape`. 여러 개를 병렬로 불러도 된다.

1. 글 목록: `https://rss.blog.naver.com/leehh2153.xml` 을 formats `["rawHtml"]` 로 긁는다 → 최근 50편 제목 · 링크 · 대표 사진 · 요약.
2. 행사 · 현장 글을 골라 `https://m.blog.naver.com/leehh2153/<글번호>` 를 formats `["html"]` 로 긁는다. 결과가 크면 도구가 파일로 저장하고 경로를 알려 준다.
3. 사진 주소 뽑기:
   ```bash
   python3 scripts/post_images.py <긁은 결과 파일>
   ```
   → 한 줄에 하나씩 `https://images.weserv.nl/?url=postfiles.pstatic.net/<경로>?type=w966&w=1600&output=webp&q=82&encoding=base64` (postfiles · blogfiles · mblogthumb-phinf · blogthumb 주소 중 jpg/png/webp 만, 중복 제거, 장수는 stderr).
4. 사진 한 장 = 그 weserv 주소를 formats `["rawHtml"]` 로 긁기 → 저장된 파일을 풀기:
   ```bash
   python3 scripts/decode_img.py <긁은 결과 파일> assets/img/works/w29.webp
   ```
   (`data:image/…;base64,` 을 찾아 저장하고 크기를 출력. PIL 필요.)
5. 800px 썸네일 예(PIL):
   ```bash
   python3 -c "from PIL import Image;im=Image.open('assets/img/works/w29.webp');im.thumbnail((800,800));im.save('assets/img/works/th/w29.webp','WEBP',quality=80)"
   ```
   (썸네일을 원래 어떤 품질로 만들었는지는 기록이 없다 — 확인 필요.)

이 사이트 사진 28장은 블로그 글 4편에서 왔다: 초등학교 운동회(224408721656) · 학교체육대회 영상 캡처(224410240152) · 전농동 상권 활성화 축제(223702427949) · 16개동 연합 워크숍(223913412790).
b1~b4 는 보육인대회 글(223704847391, 긴 변 966px)에서 — 행사 이야기에만 쓴다.

## 3. 히어로 영상 (`scripts/make_hero.py`)
- AI 영상은 한글 · 간판을 뭉갠다 → **실제 현장 사진만** 쓴다. 가로 사진 6~8장, 글자가 큰 사진(현수막 정면)은 피한다.
- 준비: ffmpeg 를 `imageio_ffmpeg` 로 찾는다 → `pip install imageio-ffmpeg` (이 환경엔 없을 수 있음).
- 실행:
  ```bash
  python3 scripts/make_hero.py assets/video assets/img/works/w2.webp assets/img/works/w4.webp assets/img/works/w3.webp \
      assets/img/works/w5.webp assets/img/works/w7.webp assets/img/works/w12.webp assets/img/works/w1.webp
  ```
  (지금 영상의 사진 순서 = SOURCES.md 기록 w2 · w4 · w3 · w5 · w7 · w12 · w1.)
- 하는 일: 장마다 4초 · 30fps, 2배 크기로 키워 자른 뒤 zoompan 으로 천천히 확대/축소 + 이동(움직임 6가지를 돌려 씀) → 0.8초 `xfade` 교차 전환으로 잇기
  → `hero.mp4`(1920×1080, H.264 CRF 25, 무음, faststart) → `hero_sm.mp4`(960×540, CRF 27) → `hero_poster.webp`(0.5초 장면). 7장이면 7×4 − 6×0.8 = **23.2초**.
- `hero_sm.webm` 은 make_hero.py 가 만들지 않는다. 지금 파일은 VP9 960×540 23.2초 약 527kbps. 만드는 예(원래 쓴 옵션은 기록 없음 — 확인 필요):
  ```bash
  ffmpeg -y -i assets/video/hero.mp4 -vf scale=960:540 -an -c:v libvpx-vp9 -b:v 0 -crf 40 -row-mt 1 assets/video/hero_sm.webm
  ```
- 페이지 쪽: `<video id="heroVideo" autoplay muted loop playsinline preload="auto" poster=… data-src=hero.mp4 data-src-sm=hero_sm.mp4 data-src-webm=hero_sm.webm>`.
  `<source media>` 를 쓰지 않고 app.js `pickSrc()` 가 고른다: H.264 못 틀면 webm, (창 폭 × DPR(최대 2)) < 900 이면 sm, 아니면 큰 것. reduced-motion 이면 src 를 안 넣고 포스터만.
  `.poster` div 가 영상 뒤에 같은 그림으로 깔려 있어 로딩 중에도 빈 화면이 아니다. 영상을 바꾸면 `SOURCES.md` 히어로 항목도 고친다.
- og.jpg(1200×630)는 로고 + 문구 + works/w4 로 만든 것(만든 스크립트는 레포에 없음 — 확인 필요).
