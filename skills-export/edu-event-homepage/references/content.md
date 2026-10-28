# build_site.py 자료 구조 · 사진 · 영상

`tools/build_site.py`(776줄)가 공개 페이지 10개와 sitemap.xml · robots.txt · llms.txt 를 만든다.
실행: `python tools/build_site.py` (**Python 3.12+**). 쓰기는 `__main__` 에서만 하므로 `import build_site` 는 안전하다(`blog_shell.py` 가 그렇게 쓴다).
모든 파일은 `encoding='utf-8', newline='\n'` 으로 쓴다.

## 1. 회사 정보 상수 (파일 맨 위)

| 상수 | 값 / 뜻 |
|---|---|
| `NAME` · `NAME_EN` | `이벤트와 교육연구소` · `Event & Education institute` |
| `CEO` | 황윤수 |
| `BIZNO` | 578-03-01411 |
| `ADDR` | 인천광역시 남동구 문화서로62번길 17, 3층 302호 |
| `TEL` · `TEL_RAW` | 사이트 대표 번호(이 문서에 안 적음) · 하이픈 뺀 값(`tel:` 링크) |
| `EMAIL` | ihaha2040@gmail.com |
| `KAKAO` | `http://pf.kakao.com/_XVrSs/chat` (https 가 아니라 http 로 적혀 있음) |
| `NBLOG` | `https://blog.naver.com/event_edu` |
| `BASE` | `https://brizymedia.github.io/edu-event` — 도메인 정하면 여기만 |
| `NOINDEX` | `True` — 오픈 때 `False` |
| `VER` | `'1'` — CSS/JS 캐시 꼬리표 (`?v=`) |
| `EDIT_HASH` | 수정 모드 열쇠의 sha256(64자 hex). 열쇠 원문은 없다 |
| `OG` | `BASE + '/assets/img/og.jpg'` |
| `MAP` | 네이버 지도 검색 주소(주소 문자열 퍼센트 인코딩) |
| `NAV` | `[(about.html,회사 소개),(event.html,행사),(education.html,교육),(portfolio.html,포트폴리오),(contact.html,견적 문의)]` |

## 2. 자료

### EVENT_CATS (행사 대상 5개, event.html · index 대상 카드 · llms.txt)
각 항목 `dict(id, name, c, title, img, alt, intro, prog)`.

| id | name | c(파스텔) | title | img |
|---|---|---|---|---|
| kinder | 유치원 · 어린이집 | #FFD9D1 | 처음 만나는 운동회, 가장 즐거운 하루 | g10 |
| school | 초등학교 | #CFE5A3 | 운동회부터 학교 축제까지 | p/school11 |
| corp | 기업체 · 기관 | #FBD9A8 | 순서와 격식이 중요한 행사 | p/corp01 |
| local | 지자체 · 축제 | #C9E6F7 | 무대부터 사람까지 | p/univ03 |
| church | 교회 | #E3D6F6 | 온 교회가 함께 웃는 시간 | p/church01 |

- `prog` = 프로그램 칩 목록(kinder 5 · school 9 · corp 12 · local 5 · church 5).
- `img` 가 빈 문자열이면 「축제 현장 사진을 준비하고 있어요」 빗금 자리표시(`.ph.pending`)가 나온다(현재는 모두 사진 있음).
- `AUD_SHORT[id]` = 대문 대상 카드의 한 줄 설명. 대문 카드 색은 `build_index()` 의 `aud_cols`(EVENT_CATS 의 c 와 같은 값)를 따로 갖고 있다.
- `EVENT_EXTRA[id]` = event.html 큰 사진 밑 썸네일(kinder 2 · 나머지 3). `.thumbs:has(img:nth-child(2):last-child)` 로 2장이면 2열.
- kinder 블록만 「프로그램 구성 예시 (명랑운동회)」 상자(10:00 개회식 → 10:20 준비운동 → 10:40 학년별 경기 · 놀이 → 「실제 시간표는 … 함께 짭니다」)가 `build_event()` 안에 하드코딩.
- 「이 행사 견적 문의」 = `contact.html?type=<name 공백→%20>#form` → app.js 가 문의 종류 선택.

### EDU (교육 6개)
`dict(n, who, c, ic, fx, t)` — 이름 · 대상 · 색 · 아이콘 키 · 기대효과 · 소개.

| n | who | ic | fx |
|---|---|---|---|
| 감정교육 | 유아 · 초등 | heart | 정서지능 향상, 또래 관계 개선 |
| 임원 리더십 | 초등 · 청소년 | flag | 리더십, 자신감, 협동심 |
| 발표회 | 초등 · 청소년 | mic | 발표력, 자기표현력 |
| 과학실험 마술수업 | 유치부 · 초등부 | flask | 과학 흥미, 탐구력 |
| 직업체험 | 초중고 | brief | 직업 이해, 진로 동기 |
| 진로탐색 강의 | 초중고 | compass | 자기이해, 진로 설계 |

아이콘은 `ICONS` 사전의 SVG path(선 아이콘, viewBox 24). 교육 카드 단추는 모두 `contact.html?type=교육#form`.

### 포트폴리오 사진: WORKS_OLD · PHOTO_SETS · WORKS
- 한 장 = 튜플 `(코드, 제목, 부제, 분류, 클래스)`. 코드는 `assets/img/<코드>.webp` 경로 조각(`g01`, `p/school09`). 분류는 공백으로 여러 개(`'kinder magic'`). 필터 slug: `kinder school corp gov local church edu magic`.
- `WORKS_OLD` 10장(g01~g10, 기존 시안): 초등학교 체육대회 2 · 어린이집 크리스마스 매직쇼 · 초등학교 명랑운동회 · 초등학교 운동회 · 성탄 축하 행사 매직쇼(church magic) · 운동회 에어바운스 · 대학 홈커밍데이 매직쇼(2018, corp magic) · 비둘기 마술(corp magic) · 유치원 매직쇼.
- `PHOTO_SETS` = `(접두어, 장수, 제목, 분류)` 7줄 → `WORKS_NEW[접두어]` 에 `p/<접두어>01 …` 를 자동 생성(제목은 묶음 제목 하나, 부제 없음).
- `_mix()` 가 `order = ['school','sci','church','univ','corp','magic','gov']` 순서로 한 장씩 번갈아 섞음 → `WORKS = _mix() + WORKS_OLD` (총 97장).
- `W(code)` = WORKS 에서 코드 찾기(없으면 StopIteration).
- `PF_FILTERS` 9개: all 전체 / school 초등학교 / kinder 유치원 · 어린이집 / corp 기업체 · 기관 / gov 관공서 체육대회 / local 지자체 · 축제 / church 교회 / edu 교육 / magic 마술 · 공연. **실제 사진이 있는 분류만** 단추가 만들어진다(`cats_with`).
- 포트폴리오 캡션의 회색 줄 = 첫 번째 분류 이름 + 부제.

### 그 밖
| 상수 | 쓰는 곳 |
|---|---|
| `REVIEWS` 4개 `(HTML 문장, 누구)` — `<mark>` 로 강조 | 대문 앞 3개, 포트폴리오 4개 + 카톡 캡처 |
| `TIMELINE` 4개 `(연도, 색, 제목, 설명)` — ~2010 · 2011 · 2013~2019 · 현재 | ceo 「운동장에서 보낸 20년」 |
| `TICKER` 14개 | 대문 흐르는 띠 |
| `FAQ` 5개 | contact FAQ + FAQPage JSON-LD |
| `SCHOOLS` ← `assets/data/schools.json` `[{region,count,schools:[[학교,연도들]]}]` 4지역 | 포트폴리오 실적 |
| `NOTICES` ← `assets/data/notices.json` `[{d,t,n?,b?}]` 3개(2026.10.20) | 대문 4개 · notice 전체, `NJ`(escape 된 JSON)를 `data-static` 으로 |

about 의 핵심 가치 3 · 왜 우리인가요 7, ceo 인사말 · 이력 4칸, 대문 숫자 4 · 두 파트 · 대표 요약 문구, education 회차 3단은 **상수가 아니라 각 `build_*()` 안**에 있다.

## 3. 조각 함수

| 함수 | 하는 일 |
|---|---|
| `btn(href, text, cls, ext)` | `.btn` + 둥근 화살표 SVG. ext 면 새 창 |
| `header(cur)` | 건너뛰기 링크 + 알약 머리글(로고 · NAV · 전화) + 폰 메뉴 `#sheet`(NAV + 보조 링크 5 + 전화 단추). `cur` 와 같은 메뉴에 `aria-current="page"` |
| `footer()` | 바닥글 4칸(정보 · 회사 · 서비스 · 문의) + © + 사진 저작 고지 + `.dock` + 라이트박스 `.lb` + 스크립트 3개 |
| `jsonld_biz()` | LocalBusiness JSON-LD(대문만) — founder 소장, areaServed 서울 · 인천 · 경기, knowsAbout 10개, sameAs 네이버 블로그 |
| `page(fn, title, desc, body, cur, extra_head, og_img)` | 문서 전체를 써서 저장. robots(NOINDEX) · theme-color `#FFF9F1` · `edu-edit` 메타(notice-admin · 404 제외) · canonical · og · twitter |
| `phead(crumb, eb, h1, lead)` | 서브 페이지 머리(빵부스러기 · 꼬리표 · h1 · 설명) |
| `cta_band(title, sub)` | 어두운 CTA 상자(전화 큰 글씨 + 견적 문의 · 카카오톡 단추) |
| `gal_fig(w, cls)` | 갤러리 figure(`data-t` = 제목 · 부제) |
| `thumbs(codes)` | event 썸네일 줄(WORKS 에 없어도 동작, alt 「행사 현장」) |

페이지 함수: `build_index` · `build_about` · `build_ceo` · `build_event` · `build_edu` · `build_portfolio` · `build_contact` · `build_notice` · `build_notice_admin`(port_docs.py 를 읽어 GALLERY_URL 추출) · `build_404` · `build_meta`(sitemap 9쪽 · robots · llms.txt).

`cur` 값: about · ceo 는 둘 다 `about.html` 을 현재 메뉴로 표시, notice · 404 · notice-admin 은 없음.

## 4. 사진 넣는 법

1. 원본(카톡 받은 파일 등)을 폴더 · 행사별로 나눈다. 얼굴 · 학교 이름이 크게 보이는 사진은 대표 확인.
2. WebP 로 변환해 `assets/img/p/<접두어><두 자리 번호>.webp` 로 저장. README 기준 긴 변 1400px(원본이 더 작으면 키우지 않는 것으로 보임 — 현재 파일 긴 변 분포: 1280px 55장 · 1400px 24장 · 그 밖 8장). 품질값 · 도구는 레포에 기록 없음(확인 필요).
   - 이 저장소의 다른 도구(`apply_edits.py`)는 PIL 로 `WEBP quality=82, method=6` 을 쓴다 — 같은 값을 쓰면 무난하다(제안).
3. `PHOTO_SETS` 에 `(접두어, 장수, 제목, 분류)` 추가 · 장수 수정. 새 접두어는 `_mix()` 의 `order` 에도 넣어야 「전체」에 섞인다(**안 넣으면 WORKS 에서 빠진다** — `_mix` 는 order 에 있는 키만 돈다).
4. 새 분류 slug 면 `PF_FILTERS` 에 단추, (업로드에서도 쓰려면) `port_docs.py UPLOAD_CATS` 와 `app.js UP_CAT`.
5. 대문 갤러리(`build_index` 의 6개 목록) · 교육 수업 현장(`build_edu` 의 6개) · 행사 대표 사진(`EVENT_CATS.img`) · 썸네일(`EVENT_EXTRA`) · ceo 무대 사진(하드코딩 3장)은 코드를 직접 지정한다.
6. `python tools/build_site.py && node scripts/build-blog.mjs`, 포트폴리오 필터 · 더 보기 · 라이트박스 확인.
7. 블로그에 쓰려면 사진을 직접 열어 본 뒤 `_blog/photos.json` 에 `{path, 제목(=WORKS 제목), 부제, 보이는것, 쓰임}` 으로 추가.

히어로 사진 교체: `assets/img/hero-event.webp` · `hero-edu.webp` 를 같은 이름으로 덮고(현재 1280×721, `<img width height>` 도 그 값), `style.css` 의 `.pane.ev img` · `.pane.ed img` `object-position` 을 맞춘다. `<link rel="preload">` 는 hero-event 만.

## 5. 영상

| 파일 | 크기 | 길이 | 쓰는 곳 |
|---|---|---|---|
| `sci-v1~3.mp4` | 406×720(세로) | 6~10초 | education 수업 현장 |
| `sci-v4~5.mp4` | 768×432 | 약 22초 | education 수업 현장 |
| `magic-v1.mp4` | 768×432 | 약 102초 · 7.8MB | portfolio 현장 영상 |

- 모두 h264 + aac. 포스터는 같은 이름 `.jpg`(ffmpeg Lavc 주석이 있는 첫 화면 캡처).
- `<video controls preload="none" playsinline poster>`. education 은 `.vids` 3열(980 이하 2열, 560 이하 1열), 영상 칸은 `aspect-ratio:4/3; object-fit:contain`(세로 영상도 검은 여백으로). portfolio 는 `.vids.one`(최대 820px, 16:9).
- 새 영상: 같은 규칙으로 이름 붙이고 `build_edu()` 의 `range(5)` 같은 개수를 고친다. 인코딩 값은 기록 없음(확인 필요).

## 6. llms.txt · sitemap · robots (build_meta)

- `sitemap.xml`: `''(대문) about ceo event education portfolio contact notice quote` 9개, lastmod=실행일. 블로그 줄은 build-blog 가 뒤에 붙인다.
- `robots.txt`: NOINDEX 면 `Disallow: /`. 해제하면 `Allow: /` + 업무 화면 6개(contract · statement · office · schedule · upload · notice-admin) Disallow + GPTBot · ClaudeBot · PerplexityBot · Google-Extended Allow. quote.html 은 막지 않는다.
- `llms.txt`: 회사 요약 · 소장 · 주소 · 전화 · 메일 · 블로그 · 활동 지역 → 「## 행사 (대상별)」(EVENT_CATS) → 「## 교육」(EDU) → 「## 페이지」 6줄. 「## 블로그」 절은 build-blog 가 이어 붙인다.
