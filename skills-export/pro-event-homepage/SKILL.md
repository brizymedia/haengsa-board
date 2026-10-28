---
name: pro-event-homepage
description: 브리지미디어(큰길브리지)가 만든 프로이벤트(PRO EVENT, www.pro-event.kr 리뉴얼) 원페이지 홈페이지(레포 brizymedia/pro-event)를 고치거나 처음부터 다시 만들 때 쓴다. 「프로이벤트」「pro-event」「히어로 영상」「사업분야 무대」「포트폴리오 WORKS」「자동 견적서·전자계약서·거래명세서·행사 일정·사진 올리기·업무 문서함」「행사 이야기·지역 페이지·행사 준비 블로그」「make_pages·build-blog·port_docs」 같은 말이 나오면 이 스킬을 먼저 읽는다.
---

# 프로이벤트 홈페이지 (brizymedia/pro-event)

어두운 잉크 바탕에 코발트→시안 빛을 쓰는 **한 장짜리 정적 사이트** + 대표 전용 **업무 화면 6개** + **생성 페이지(행사 이야기·지역·블로그)**.
서버 없이 GitHub Pages 로 돌고, 서버 일은 Google Apps Script 웹앱이 한다.

이 문서는 2026-10-28 커밋 `af0912d`(레포 커밋은 이것 하나뿐)를 코드로 확인해 쓴 것이다. 확인하지 못한 것은 「확인 필요」로 표시했다.
세부는 `references/` 에 있다 — 작업 종류에 맞는 파일을 열 것.

| 하려는 일 | 읽을 파일 |
|---|---|
| 어느 파일이 무엇인지 | `references/file-map.md` |
| 색·글꼴·반응형·컴포넌트 | `references/design-tokens.md` |
| 섹션 순서·인터랙션·포트폴리오 데이터 | `references/sections.md` |
| 히어로 영상 다시 만들기 | `references/hero-video.md` |
| 견적·계약·명세서·일정·사진·문서함 | `references/workflows.md` |
| Apps Script 서버·배포 | `references/backend.md` |
| 행사 이야기·지역·블로그·sitemap·llms.txt | `references/content-generators.md` |

---

## 1. 회사 정보 (사이트에 공개된 것만)

| 항목 | 값 |
|---|---|
| 상호 | 프로이벤트 (PRO EVENT) — 「특별한 시간을 위한 탁월한 선택」, NO.1 Event Company · Since 2006 |
| 대표 | 배광길 (전문 MC로 소개) |
| 설립 | 2006년 7월 14일 |
| 사업자등록번호 | 206-27-92478 |
| 서울본사 | 서울시 강남구 역삼동 778-3 |
| 화성지사 | 경기도 화성시 효행구 정남면 문학리 85-5 |
| 대표전화 | 02-457-8262 (서울본사, 평일 09:00 ~ 18:00) |
| 메일 | pro-event@daum.net |
| 채널 | 네이버 블로그 `blog.naver.com/pro_event`, 유튜브 `youtube.com/@user-mu8in5ru7u`, 페이스북(index.html 364행) |

- 대표 직통 휴대폰도 사이트(푸터·문의 폼 대체 경로 `SMS_TO`)에 공개돼 있으나 이 스킬에는 옮겨 적지 않는다 — 필요하면 `index.html` 푸터에서 읽는다.
- 확인 필요: 푸터 인스타그램 링크가 `instagram.com/ssukssukedu` 다. 프로이벤트 계정이 맞는지 대표 확인 전.
- 대문 숫자(729회, 최대 20,000명, 섭외 라인업 60+, 전문 MC 8인)는 원본 사이트 기준 문구다. **블로그에서는 이 숫자를 쓰지 않는다**(`_blog/GUIDE.md`).
- 관리: 큰길브리지(1533-7295, www.ai-make.co.kr) — office.html·admin_gate.py 의 안내 문구.

## 2. 레포 · 도메인 · 배포

- 레포 `brizymedia/pro-event`, 브랜치 `main`(사이트) + `photos`(대표가 올린 현장 사진, 갤러리 서버가 커밋 — 클론에 없어 존재 확인 필요).
- 지금 주소 `https://brizymedia.github.io/pro-event/` (하위 폴더). 목표 도메인 www.pro-event.kr 은 **아직 연결 전**(robots.txt 주석).
- 배포: GitHub Pages. `.github/workflows/` 없음 → 푸시하면 Pages 가 그대로 반영(GUIDE: 1분 안). Pages 설정값은 확인 필요.
- **시안 상태**: `index.html` 8행 `<meta name="robots" content="noindex,nofollow">`. 생성 페이지가 이걸 물려받는다. 납품 때 지우고 생성기 두 개를 다시 돌린다.
- 로컬 보기(README): `npx -y http-server <레포경로> -p 8177 -c-1` → `http://localhost:8177` (file:// 로 열면 영상·폰트·fetch 가 안 됨).
- `_raw/`(원본 영상·사진·AI 컷·마스터)는 gitignore — 배포하지 않고 레포에도 없다.

## 3. 파일 지도 (요약 — 전체는 references/file-map.md)

```
index.html            대문 한 장 (생성 페이지 머리글·바닥글의 원본)
assets/style.css      전체 스타일 (460행~ 생성 페이지용)
assets/app.js         공통 스크립트 (커튼·커서·카운터·사업분야 무대·포트폴리오·유튜브·문의 폼·관리자 링크)
assets/img/{works,biz,sys,stories}/   사진 (전부 프로이벤트 원본)
assets/video/hero{,_md,_sm}.mp4       히어로 영상 3크기
quote.html quote-catalog.js contract.html statement.html schedule.html upload.html office.html admin-lock.js   업무 화면 (port_docs 결과물)
apps-script/contract/  apps-script/gallery/    서버 코드 + 설치 README
stories/ areas/        python tools/make_pages.py 결과
_blog/ → blog/ rss.xml  node scripts/build-blog.mjs 결과
llms.txt sitemap.xml robots.txt
tools/make_pages.py tools/port_docs.py tools/admin_gate.py   scripts/build-blog.mjs blog-check.mjs blog-plan.mjs
```

**손으로 고치지 말 것**: `stories/` `areas/` `blog/` `rss.xml` `office.html`, 업무 화면 HTML(→ `tools/port_docs.py` 규칙으로), `quote-catalog.js` 의 `CATALOG`(→ port_docs `CATALOG`).

## 4. 디자인 체계 (요약 — 전체는 references/design-tokens.md)

- 색: 바탕 `--ink #06070B`, 교차 섹션 `--ink-2 #0C0E15`, 카드 `--surface #11141D`, 글자 `--txt #F2F4F8`, 보조 `--muted #8E96AB`, 약함 `--dim #5B627A`, 코발트 `--cobalt #2F6BFF`, 시안 `--cyan #19D3FF`, 그라데이션 `--grad: 92deg #5C8BFF → #19D3FF → #9AF0FF`. 라이브 점 `#FF4D6D`. 살구 `--peach #FFB347` 은 정의만 있고 대문에서 안 씀.
- 글꼴: 한글 Pretendard Variable(jsDelivr v1.3.9 dynamic subset), 영문 라벨·숫자 Unbounded 400/500/600(Google Fonts). `body{word-break:keep-all}` 필수.
- 여백·폭: `--gutter clamp(20px,5vw,72px)`, `--max 1440px`, 섹션 `clamp(88px,11vw,150px)`. 이징 `--ease cubic-bezier(.22,1,.36,1)`.
- 반응형: **1100 / 900 / 640**(대문), 960 / 600(생성 페이지), `(hover:hover) and (pointer:fine)` 일 때만 커서·자석·기울임, `prefers-reduced-motion` 대응.
- 핵심 컴포넌트: 알약 단추(`.btn-pri` 흰 바탕→hover 그라데이션, `.btn-ghost`), eyebrow(시안 영문 라벨+빛 선), `.sec-head.line-draw`, `.reveal`, 포트폴리오 12열 dense 그리드(`.work.big/.wide`), 사업분야 sticky 무대(모서리 괄호+스캔 빛), 시스템 3:4 카드, `.phead` / `.callband` / `.scard`(생성 페이지).

## 5. 섹션 구성 (index.html)

커튼 → 상단 메뉴(+폰 시트) → **히어로**(영상·h1·숫자 4·티커) → 고객 띠(TRUSTED BY) → 회사소개 `#about` → 사업분야 8 `#business` → 포트폴리오 `#works` → 프로세스 5단계 `#process` → 행사시스템 `#system` → 유튜브 `#video` → 섭외 `#casting` → 견적문의 `#contact` → 푸터 → 맨위로 · 라이트박스.
행 번호·문구·데이터 속성은 `references/sections.md`.

## 6. 인터랙션과 구현 위치 (assets/app.js)

| 기능 | 행 | 요점 |
|---|---|---|
| 커튼 | 18~21 | load+700ms, 최대 1900ms 에 열림 |
| 커서 빛 | 24~30 | fine 포인터만, .12 비율 추적 |
| 스크롤 진행·메뉴 활성·맨위로 | 33~46 | 40px 넘으면 메뉴 블러, 화면 40% 기준 현재 섹션 |
| 폰 메뉴 | 49~54 | `.sheet.on` + body 스크롤 잠금 |
| 히어로 영상 선택·자동재생 보장 | 57~73 | 폭×DPR <900 sm, <1300 md, 그 외 1080p. 재시도 최대 8회 |
| 히어로 시차 | 74~88 | 영상 y·.25, 글 투명, h1 포인터 반대로 |
| 티커·고객 띠 | 91 | 내용 2배 복제 + CSS marq |
| 등장 · 카운터 | 94~108 | IntersectionObserver, 카운터 1.8초 |
| 자석 단추 · 카드 기울임 | 111~114, 227~230 | `[data-mag]`, `[data-tilt]` |
| 사업분야 무대 | 117~149 | PC hover 교차, **900 이하 탭하면 항목 아래 인라인 사진** |
| 포트폴리오 | 152~220 | `WORKS` 배열(정본) + photos 브랜치 사진을 앞에 합침, 필터, 라이트박스(키보드) |
| 프로세스 선 | 223~224 | `#steps.in` |
| 유튜브 | 233~241 | 클릭 시 nocookie iframe, maxres 실패 시 hq |
| 문의 폼 | 244~267 | 서버 ok 일 때만 완료, 아니면 폰 `sms:` / PC 복사 |
| 관리자 모드 링크 | 271~282 | 모든 페이지 바닥글 끝 → office.html |

포트폴리오 글·순서·사진 번호를 바꾸려면 `app.js` 의 `WORKS` 만 고친다(`{i,t,o,n,c,s,y}`).
사업분야 문구·사진은 index.html `#bizList` li 의 `data-img data-en data-desc` 와 무대 초기값(188·192행)을 같이 고친다.

## 7. 히어로 영상 제작법 (핵심 — 전체는 references/hero-video.md)

**문제**: AI 영상 생성기는 한글 현수막·간판·LED 글자를 뭉갠다.
**해법**: 글자가 보이는 장면은 **원본 사진을 ffmpeg zoompan 으로 천천히 줌하는 실사 컷**, AI 는 **글자 없는 드론 장면만**, 나머지는 원본 사이트 영상 구간.

4차(2026-09-13) 결과: 1920×1080 · 25fps · 26.92초 · 10컷 · 0.5초 크로스페이드 · 오디오 없음 · faststart.

| # | 출처 | 내용 |
|---|---|---|
| 1 | 원본 slide02 0~2s | 드론 오프닝(포스터와 같은 장면) |
| 2 | AI 텍스트→영상 Wan 2.6 1080p | 강변 축제 드론·불꽃 (글자 없음) |
| 3 | 사진 w14 줌 | 워터밤 야간 |
| 4 | 원본 slide02 32.5s | 드론 수영장 |
| 5 | AI 사진→영상 Wan 2.6 flash(w11) 2.6~5s | 국회 에어바운스 와이드 |
| 6 | 원본 slide01 85.5s | 레드카펫 통로 |
| 7 | AI 텍스트→영상 Wan 2.6 | 야간 콘서트 드론 (글자 없음) |
| 8 | 사진 w18 줌 | 「2025 제5회 순천시 읍면동 체육대회」 현수막 — 글자 정확 |
| 9 | 사진 w17 줌 | 「2025 이용자간담회」 홀 — 글자 정확 |
| 10 | 원본 slide01 79s | 테이프 커팅 |

사진 줌 컷 명령(README 원문, 88프레임 = 3.52초):

```bash
ffmpeg -loop 1 -i 사진.jpg -frames:v 88 -vf "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='min(zoom+0.0018,1.18)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=88:s=1920x1080:fps=25" -r 25 …
```

- 반복문 안 ffmpeg 는 **꼭 `-nostdin`**.
- 글자 뭉개진 AI 컷(`_raw/ai/b2 b3 b4 d1 d3`)은 쓰지 않는다. 생성 결과는 프레임 단위로 검수.
- 워터마크 「CREATIVE PLAN PROEVENT」 는 프로이벤트 것 → 그대로 둔다.
- 마스터 `_raw/master_1080.mp4` → `hero.mp4`(1080p ≈3.3Mbps 11MB) · `hero_md.mp4`(720p ≈1.8Mbps 6MB) · `hero_sm.mp4`(480p ≈0.85Mbps 2.9MB). H.264 High, yuv420p, `-an`, `-movflags +faststart`.
- 크로스페이드·구간 자르기·내보내기 명령은 README 에 없어서 hero-video.md 에 **재현용 예시**로 적었다(원래 CRF 값 확인 필요).
- 확인 필요: 8번 현수막(순천시 읍면동 체육대회)과 WORKS 의 w18 제목(총동문회 체육대회)이 다르다.

## 8. 업무 화면 흐름 (요약 — references/workflows.md)

```
quote.html(손님) ── 문의 서버 → 대표 메일 + 큰길브리지
office.html(대표 암호) → quote.html?admin=1 → 저장함(#q= 코드)
     → contract.html?admin=1#c=…  → 손님 서명 링크 ?c=ID&s=배포ID → PDF·메일·대장
     → statement.html?admin=1#t=…  → 인쇄/PDF
     → schedule.html#new=…         → 직원과 같이 보는 일정·체크리스트
upload.html → photos 브랜치 → 대문 포트폴리오 앞에 합쳐짐 + 블로그·인스타 글 초안
```

- 견적은 서버에 저장하지 않는다 — **견적 하나 = 주소 `#q=` 코드**. 품목표 `quote-catalog.js`, 전부 `price:null`(금액 협의).
- 손님 화면(admin=1 없음)은 직인·품목명·규격·단가·할인·인쇄를 막는다.
- 상태 키(localStorage): `pro-quote-box-v1`, `pro-quote-box-pw`, `pro-sched-pw`, `pro-sched-who`, `pro_pw`/`pro_srv`/`pro_cat`/`pro_ev`, `kg_contract_co`, `kg_stmt_bank`. sessionStorage `pro-office`.
- 잠금: `?admin=1` 화면은 `admin-lock.js`(data-server·data-key·data-name 속성), office.html 은 `tools/admin_gate.py` 가 주입. 둘 다 계약 서버 `boxList` 로 대표 암호(`BOX_PW`)를 확인한다. 암호는 페이지에 없다.
- 업무 화면은 큰길이벤트 원본에서 `python tools/port_docs.py <원본 레포 경로>` 로 옮긴 결과물 → **회사별 수정은 port_docs 「회사 설정」·`*_extra()` 에**. 원본 레포 없이는 재생성 불가.

## 9. Apps Script 백엔드 (주소만 — references/backend.md)

| 서버 | 주소 끝부분 | 코드 |
|---|---|---|
| 공용 문의 | `…AKfycbwvQ4UJ…FA/exec` | 레포에 없음(큰길브리지 공용, `page` 주소의 레포 이름으로 회사 구분) |
| 계약(+보관함·일정) | `…AKfycbxRVcKW…RQ/exec` | `apps-script/contract/Code.gs` |
| 갤러리(사진) | `…AKfycbzPv-Zo…r/exec` | `apps-script/gallery/Code.gs` |

전체 주소는 backend.md, 정본 값은 `tools/port_docs.py` `CONTRACT_URL`·`GALLERY_URL`.
배포 규칙: 웹 앱 · **실행: 나** · **액세스: 모든 사용자**. 고친 뒤 **「배포 관리 → 연필 → 새 버전」**(새 배포를 만들면 주소가 바뀜). 비밀은 스크립트 속성에만: `BOX_PW` `CREW_PW`(계약), `UPLOAD_PW` `GITHUB_TOKEN` `GITHUB_REPO`(갤러리). 요청은 `Content-Type: text/plain` JSON, 응답 `ok:true` 만 성공.

## 10. 생성 페이지와 실행 명령 (references/content-generators.md)

```bash
python tools/make_pages.py          # stories/ 5편 + areas/ 9곳 + sitemap.xml (내용 = 파일 안 STORIES · AREAS 표)
node scripts/blog-plan.mjs          # 다음 블로그 주제 추천
node scripts/blog-check.mjs --new _blog/posts/<파일>.json   # 새 글 검사 (실패 시 exit 1)
node scripts/build-blog.mjs         # blog/ · rss.xml · sitemap(blog) · llms.txt(블로그 절)
```

- 셋 다 index.html 의 머리·머리글·바닥글을 빌린다 → **대문 메뉴·바닥글·robots 를 고치면 make_pages 와 build-blog 를 둘 다 다시 돌린다.**
- 사이트가 하위 폴더라 생성기가 상대 주소에 `../` 를 붙인다. 글 JSON 안 주소는 `/quote.html` 처럼 루트 기준으로 쓴다.
- 블로그 글은 `_blog/GUIDE.md` 규칙(가격·순위·연혁·후기·인원 숫자 금지, regions.json·sources.json 근거만, photos.json 사진만)을 따른다.

## 11. 사장님 수정 모드

- **이 사이트에는 없다.** `assets/edit.js` 가 없어서 office.html 의 「홈페이지 글 · 사진 고치기(`?edit=열쇠`)」 상자가 `hidden` 으로 나간다(port_docs `EDIT_ATTR`).
- 대표가 직접 바꿀 수 있는 것은 지금 두 가지뿐: upload.html 로 사진 올리기(대문 포트폴리오 앞에 붙음), 업무 화면 데이터.
- 글·사진 수정 모드를 붙이려면 다른 고객사 레포의 `assets/edit.js` 를 가져와야 한다(이 레포에 원본 없음 — 확인 필요). 붙이면 port_docs 를 다시 돌려 문서함 안내가 보이게 한다.

## 12. 사진 출처 규칙

1. **프로이벤트 원본만** — 원본 사이트(pro-event.kr) 게시물, 원본 영상 프레임, 네이버 블로그 pro_event 원문 사진(stories/), 대표가 upload.html 로 올린 것.
2. **AI 이미지 금지**(사업분야 사진·포트폴리오·블로그). AI 는 히어로 영상의 글자 없는 드론 컷에만 썼다.
3. 워터마크 「CREATIVE PLAN PROEVENT」 는 프로이벤트 것 — 지우지 않는다. upload.html 은 「프로이벤트」 워터마크를 넣는다.
4. 블로그: `_blog/photos.json` 에 있고 `제외` 없는 사진만, 얼굴이 크게 나온 사진 금지(slider2·slider5·h3_1 등 제외), 같은 묶음 두 장 금지, 장소 모르는 사진에 지역 캡션 금지.
5. `_raw/` 원본은 쓰지 않는다(배포 대상 아님).
6. 사업분야 b1~b8 의 원래 출처는 README 「납품 전에 바꿀 것 4」 — 바꿀 때 거기도 고친다.

## 13. 검증 절차 (고친 뒤 매번)

```bash
node --check assets/app.js && node --check admin-lock.js && node --check quote-catalog.js
python -m py_compile tools/make_pages.py tools/port_docs.py tools/admin_gate.py
node scripts/blog-check.mjs                     # 블로그를 건드렸으면
npx -y http-server . -p 8177 -c-1               # 서버 띄우고
```

브라우저(Playwright 등)로 **375px · 1280px** 두 폭에서 `index.html`, `quote.html`, `quote.html?admin=1`, `contract.html?admin=1`, `statement.html?admin=1`, `schedule.html`, `upload.html`, `office.html`, `stories/index.html`, `areas/index.html`, `blog/` 를 열어:
- 콘솔 오류·pageerror 0 (단, `assets/img/stamp-pro.png` 404 는 직인 파일이 없어서 나는 **알려진 것**)
- `document.documentElement.scrollWidth - innerWidth === 0` (가로 넘침 없음)
- 대문: 커튼이 열리는지, 히어로 영상 재생, 900 이하 사업분야 탭 → 인라인 사진, 포트폴리오 필터·라이트박스, 폼 필수값 경고
- 관리자 화면은 `html.admin-locked` 잠금 화면이 떠야 정상

2026-10-28 사본으로 위 점검을 돌렸을 때: 문법 검사 통과, blog-check 「통과」, 11개 화면 × 2폭 가로 넘침 0, 콘솔 오류는 stamp-pro.png 404 뿐.

## 14. 함정과 같이 고칠 곳

| 고치는 것 | 같이 고칠 곳 |
|---|---|
| 대문 메뉴·바닥글·`<head>` | `python tools/make_pages.py` + `node scripts/build-blog.mjs` 재실행 |
| `style.css` / `app.js` | index.html 의 `?v=` 숫자 올리고 생성기 재실행(생성 페이지가 index 머리를 복사함) |
| 포트폴리오 분류 이름 | index.html `#filters`, app.js `UP_CAT`, port_docs `UPLOAD_CATS` |
| 견적 품목 | port_docs `CATALOG` → 포팅. `make_pages.py` STORIES 의 `quote` id, blog-check 가 품목 이름을 읽음 |
| 서버 주소 | port_docs `CONTRACT_URL`/`GALLERY_URL` → 포팅. 문의 서버는 app.js `FORM_ENDPOINT` · quote.html `문의서버` · contract.html 각각 |
| 회사 전화·주소 | index.html(헤더·시트·연락·푸터), app.js `SMS_TO`, make_pages `TEL/TEL_M`, build-blog `TEL/TEL_M`, port_docs 회사 설정, llms.txt, `_blog/GUIDE.md` 4장 |
| 지역 | make_pages `AREAS`, `_blog/regions.json`, port_docs `UPLOAD_REGIONS`, llms.txt |
| 도메인 연결 | index.html noindex 삭제·og:image 절대주소, make_pages `BASE`, build-blog `SITE`, port_docs `HOME`, upload.html `홈주소`, robots.txt Sitemap, llms.txt 주소 → 생성기·포팅 재실행 |

알려진 문제(코드로 확인):
1. **llms.txt 블로그 절이 빌드마다 늘어난다.** build-blog.mjs 정규식 `(?=^## |\s*$)` 의 `\s*$` 가 m 플래그로 제목 줄 끝에서 걸림. 지금도 목록이 4벌. 고치는 법은 content-generators.md.
2. **README 가 코드보다 낡은 곳**: 「CONTRACT_URL · GALLERY_URL 은 아직 빈 값」「대표 메일 없음」이라고 적혀 있지만 port_docs 에는 주소와 `pro-event@daum.net` 이 들어 있다. `apps-script/contract/README.md` 의 「COMPANY_EMAIL 미정」도 같다. README 파일 표의 「hero.mp4 1280×720 26.5초 8MB 11컷」은 이전 판(실제 1080p 26.92초 11MB 10컷).
3. `apps-script/gallery/README.md` 에 바로기획 흔적: 5단계 주소가 `brizymedia.github.io/baro-event/upload.html`, `gallery.html`·`scripts/prepare-gallery-photos.mjs`·Actions 「갤러리 페이지 · 사이트맵 자동 갱신」 언급 — **이 레포에는 셋 다 없다.**
4. `quote.html` 의 FormSubmit 대체 경로와 계약 서버 `MANAGER_EMAIL` 은 큰길브리지 관리 메일로 간다(회사 메일 아님). 의도인지 대표 확인 필요.
5. `stamp-pro.png` 없음 → 계약서·명세서에 「(인)」만, 콘솔 404 한 건.
6. 대문은 noindex 인데 `quote.html` 은 `index,follow`.
7. 생성 HTML·업무 화면 HTML 을 손으로 고치면 다음 실행 때 사라진다.
8. 사이트가 하위 폴더 → 절대경로 `/assets/…` 를 HTML 에 쓰면 Pages 에서 깨진다(블로그 JSON 안에서만 루트 기준으로 쓰고 빌드가 바꿈).
9. `_blog/` 처럼 밑줄 폴더는 Pages(Jekyll)가 공개하지 않는다 — 공개해야 할 파일을 밑줄 폴더에 두지 말 것.

## 15. 처음부터 다시 만드는 순서

1. **자료 모으기**: 원본 사이트(pro-event.kr) 게시물 사진·영상, 네이버 블로그 원문 사진, 회사 사실(1장). `_raw/` 에 두고 커밋하지 않는다. AI 이미지는 만들지 않는다.
2. **사진 손질**: webp, works·biz 는 긴 변 1400~1600, sys 1200×900, stories 900×675. 얼굴이 크게 나온 사진은 블로그 목록에서 제외 표시.
3. **index.html 뼈대**: 5장 순서대로 섹션 id 를 그대로(`about business works process system video casting contact`) — 생성기·메뉴·app.js 가 이 id 와 `#bizList #bizStage #worksGrid #filters #steps #quoteForm #formDone #heroVideo #sound #media #lb` 를 찾는다. `<main id="top">` 와 `</main>` 은 생성기가 자르는 기준이니 꼭 둔다.
4. **style.css**: design-tokens.md 의 `:root` 부터, 반응형 1100/900/640, reduced-motion.
5. **app.js**: sections.md 인터랙션 표 순서대로. 요소가 없으면 건너뛰게(생성 페이지도 같은 파일을 씀). WORKS 배열 채우기.
6. **히어로 영상**: hero-video.md 7절 순서. 포스터 = 첫 컷.
7. **로컬 확인**(13장) 후 GitHub `brizymedia/pro-event` 에 푸시, Pages 켜기.
8. **서버**: Apps Script 계약·갤러리 배포(backend.md), 스크립트 속성 넣기, 주소를 port_docs 에 넣기.
9. **업무 화면**: 큰길이벤트 원본 레포를 받아 `python tools/port_docs.py <경로>` → 「남은 큰길 흔적: 없음」 확인 → office.html 「서버 연결 상태」 초록 확인.
10. **생성 페이지**: make_pages.py 표 채워 실행 → `_blog/` 데이터와 글 → blog-check → build-blog.
11. **SEO 파일**: llms.txt 위쪽 손으로, robots.txt, sitemap 은 생성기.
12. **납품**: noindex 삭제, og:image 절대주소, 도메인 연결 시 14장 「도메인 연결」 줄 전부, 직인 PNG 받기, 검증 다시.

## 16. 작업 말투

사용자(대표·큰길브리지)는 개발 전문가가 아니다. 한국어로 답하고, 명령은 복사해서 바로 쓸 수 있게 주며 무엇을 왜 하는지 한 줄 덧붙인다. 비밀번호·토큰·개인 연락처는 답변·커밋·문서에 쓰지 않는다.
