# 페이지별 섹션 구성과 문구 위치

「문구 위치」: **HTML** = 그 파일 안에 글자가 있음(수정 모드로도 고침) / **app.js** = `assets/app.js` 데이터 칸이 그려 넣음 /
**make_pages** = `tools/make_pages.py` 표 / **이식** = `tools/port_docs.py`.

## 공통 틀 (대문 + 서브 6쪽에 같은 복사본)

1. `<head>`: title · description · robots(`index,follow,max-image-preview:large`) · `theme-color #221913` · canonical · keywords(대문) ·
   OG(1200×630 og.jpg) · twitter card · geo(KR-41 남양주시, 좌표) · JSON-LD `LocalBusiness`(`@id …/#business`, 영업시간 · sameAs · 서비스 6) ·
   서브는 `BreadcrumbList`, contact 는 `FAQPage` 추가, 대문은 `WebSite` · `meta es-edit` · 파비콘 · 구글 폰트 · `style.css?v=6` · `stats.js data-site="j6"`.
2. `.progress` → `header.hd#hd`(로고 d/w 두 장 · 메뉴 6 · 전화 · 「견적 문의」 단추 · 햄버거). 대문만 `class="hd on-dark"`.
   PC 메뉴: 회사소개 · 하는 일 · 장비 · 브랜드 · 현장 사진 · 공지 · 자료 · 자동 견적.
3. `.sheet#sheet` 모바일 메뉴 10개(홈 · 회사소개 · 하는 일 · 장비 · 브랜드 · 현장 사진 · 공지 · 자료 · 자동 견적서 · 행사 이야기 · 운영 지역 · 견적 문의, 각 영문 small) + 대표 · 영업시간 · 주소 · 전화 단추.
4. `<main>` 본문.
5. CTA 띠(서브 · 생성 페이지 끝, 대문은 맨 끝): 「예배 · 공연 · 행사, 소리와 빛이 필요하신가요?」 + 전화 · 견적 문의(생성 페이지는 「자동 견적서」).
6. `footer.ft`: 흰 로고 · 한 줄 소개 · SNS 3(인스타 · 블로그 · 네이버 플레이스) / Contact(전화 · 이메일 · 영업 · 주소) / Company(상호 · 대표 · 사업자번호 · 블로그) →
   `.ftl`(자동 견적서 · 행사 이야기 · 운영 지역 · 현장 사진 · 장비 · 브랜드) → `.bot`(© 2026 … · 제작 큰길브리지 → ai-make.co.kr) → (app.js 가 「관리자 모드」 링크 추가).
7. `.quick`(폰 하단 전화 · 문자 · 견적 문의) · `.totop` · `.lb#lb` 라이트박스 틀 · `app.js?v=20261004` · `edit.js?v=1`.

## 대문 `index.html` (섹션 순서)

| # | 요소 | 바탕 | 내용 · 문구 위치 |
|---|---|---|---|
| 1 | `section.hero` | 영상 | eyebrow 「Sound & Light · Since 2005」, h1 「2005년부터 2026년까지,<br>계속 이어온 <em>음향의 길</em>.」, lead, 단추 「견적 문의하기」「하는 일 보기」, 바닥 `.years` 2005—2026 + 영상 정지 단추. 영상 주소는 `video` 의 `data-src*` (HTML) |
| 2 | `.marquee` | 앰버 | 브랜드 14개 span (HTML, JS 가 두 번 복제) |
| 3 | `section.sec.intro` | bg | eyebrow 「About · J6 MEDIA」, `#litQuote` 점등 문장(수정 모드 제외), lead, `.twin` 음향 · 조명, `.sig` 대표 김호진 + 회사소개 단추 / 콜라주 w41 · w36 |
| 4 | `#service` `.sec.sand` | sand | 「하는 일, <em>여섯 가지</em>.」 `.works6`: `#wstage` 사진 6장(w57 w41 w45 w50 w36 w54) + `#wlist` 6줄(번호 · 이름 · 설명 · 썸네일 t57…, `data-en` 영문이 사진판 글자) → `service.html#…` |
| 5 | `.sec.night` | night | 「좋은 소리는<br><em>좋은 장비</em>에서 시작합니다.」 `.strong2` 카드 2: 「3~4년 내외의 신품 장비 보유」(w29) · 「보급형부터 하이엔드급까지」(w34) + 「장비 · 취급 브랜드 보기」 |
| 6 | `#record` | bg | 「함께한 <em>현장</em>들.」 `.rtabs[data-tabs="#record .rpane"]` 6탭 + `.rpane` 6판(사진 w39 w40 w46 w50 w47 w48, 목록, 「자세히」 → service 앵커) |
| 7 | `#history` | sand | 「대표가 걸어온 <em>음향의 길</em>.」 `ol.tl` 5칸(마지막 `.now`) — about.html 에 같은 목록 |
| 8 | `#gallery` | bg | 「현장 <em>사진</em>.」 「행사 이야기」「현장 사진 전체 보기」 + `#gal.gal.home data-pick="41,36,57,44,45,47,48,50"` (app.js WORKS 에서 그림) |
| 9 | `.sec.sand .trio3` | sand | 공지사항 `#noticeList`(app.js NOTICES 위 4개) / 오시는 길(주소 · 영업 · 네이버 지도 · 자세히 · 운영 지역) / `.box.dark` 바로 상담(큰 전화번호 · 문자) |
| 10 | CTA 띠 | bg | 공통 문구 + 이퀄라이저(폰에선 숨김) |

## 서브 페이지 (모두 `section.phead` → 본문 → CTA 띠)

| 페이지 | phead 사진 · eyebrow · h1 | 본문 섹션 순서 |
|---|---|---|
| `about.html` | w42 · About J6 MEDIA · 「소리와 빛으로<br>자리를 아름답게.」 | ① `.greet` 인사말(사진 w44 sticky, 「가장 기본이면서<br>가장 <em>중요한 것</em>.」 문단 4 + `.facts` 2005 / 2022 / 6 / 14) ② `#history` 연혁(sand) ③ `#info` 회사 정보 표 `.info-t` 8줄 ④ `#map` 오시는 길(sand, SVG 그림 지도 + 핀 「제이식스미디어 · 319호」 + 정보 박스) |
| `service.html` | w40 · What We Do · 「하는 일, 여섯 가지.」 | ① `article.svc` 6개 `#church #corp #gov #school #show #install`(사진 w39 w41 w45 w50 w36 w54 + `<i>01 · Church</i>`, eyebrow, h2, 설명, 칩, `.done` 「함께한 현장 (고객 제공 자료)」, 「○○ 문의하기」 → `contact.html#k=교회/기업/지자/학교/전시/장비`) ② `#places` 설치 사례 15곳 `.places`(sand) + `.eqphotos` w23 w24 w25 |
| `equipment.html` | w34 · Equipment & Brands · 「장비와 브랜드.」 | ① `#sound` 음향 8칸: NEXO 라인어레이 · 풀레인지 스피커 · 컬럼어레이 · 디지털 믹서 · 무선마이크 · 모니터 스피커 · 무선 인이어 · 퍼스널 모니터 + 사진 w29 w44 w35 ② `#light`(night) 조명 5칸: 무빙라이트 · 빔라이트 · 레이저 · 바 조명 · 스트로보 + 「조명 구성 상담」 칸 + 사진 w6 w20 w8 ③ `#brands` 로고 14(`assets/img/brands/*.png`, KANALS 는 `<b>` 글자) + 상표 고지 `.note-s` |
| `portfolio.html` (`<main class="pf">`) | w11 · On Site · 「현장 사진.」 | ① `#filters` 8(전체 · 교회행사 · 기업행사 · 지자체 · 축제 · 학교행사 · 전시 · 공연 · 설치 · 장비) + `#pfGrid`(app.js: photos.json + WORKS) ② `#story`(sand) 「현장 <em>이야기</em>.」 `#blogList data-limit="10"` + `#blogMore` |
| `notice.html` | w57 · Notice · Board · Files · 「공지 · 게시판 · 자료실.」 | `#btabs` 탭(`data-id` notice/board/files ↔ 주소 해시) → `#noticeBoard`(펼치는 줄) / `#blogList data-limit="15"` / `#fileBoard` |
| `contact.html` | w43 · Contact · 「견적 문의.」 | ① `.cgrid`: `#ready` 연락 방법 `.ways` 4(전화 · 문자 · 이메일 · 인스타) + 「문의 전에 정리해 두면 좋은 것」 4줄 + 자동 견적서 링크 / `form#quoteForm`(성함* · 연락처* · 단체 · 분야 체크 8 · 날짜 · 장소 · 규모 · 내용 · 함정칸 website · 동의 `#fAgree` · `#formDone`) ② `#faq` 6문항(sand, JSON-LD 와 같은 문구) |

문의 폼 분야 체크 값 8: 교회행사 (예배 · 세미나 · 수련회) / 기업행사 (포럼 · 콘서트) / 지자체 행사 (영화제 · 컨퍼런스) / 학교행사 (체육대회 · 축제) /
전시 · 공연 (입체음향 · 콘서트) / 장비 설치 (음향 · 영상 · 방송) / 장비만 렌탈 / 기타. `#k=` 해시는 값의 **앞부분 일치**로 체크한다(그래서 `#k=지자` 처럼 짧게 씀).

## 생성 페이지 (`tools/make_pages.py`)

**행사 이야기 한 편** `stories/<slug>.html`:
phead(첫 사진 w, eyebrow 「Event Story · 분야」, h1 = title, p = lead, 이동경로 홈 › 행사 이야기 › 분야)
→ `.story`: 왼쪽 aside(「Event File」 사실표 facts + 날짜, 「비슷한 행사 견적 받기」, 지역 링크 또는 「운영 지역 보기」) /
오른쪽 `.sbody` 본문 문단 + `.sgrid` 사진(첫 장 2×2, 누르면 원본 새 창) + 블로그 원문 · 현장 사진 단추
→ More Stories(sand) 다른 이야기 3장 → CTA.
표 필드: `slug title cat date place area lead facts[(이름,값)] body[문단] photos[번호] blog(글 번호) quote[견적 품목 id]`
(`quote` 는 현재 페이지 출력에 쓰이지 않는다 — 코드상 사용처 없음).

**이야기 목록** `stories/index.html`: phead(w41) → `.stcards.big` 카드(분야 · 날짜 · 장소, 제목, lead 64자…) → 블로그 · 게시판 안내 → CTA.

**지역 한 곳** `areas/<slug>.html`: phead(첫 사진, 「Area · 이름」, h1 「○○ 행사 음향 · 설치, 제이식스미디어」)
→ `.area3`: How Far(사무실에서 시청 · 군청까지 차로 약 N분 · Nkm, 막히지 않을 때) + 「○○에서 한 일」 목록(없으면 안내 문장) + 그 지역 이야기 카드 / 사진 3장
→ What We Do(sand) `SERVICES` 6칸 + 다른 지역 링크 → CTA(「○○ 행사, 소리와 빛이 필요하신가요?」).
표 필드: `slug name hall min km hq done[] photos[]`. 이동 시간은 OSRM 2026-10-03 조회, 5분 단위 반올림(주석).

**지역 목록** `areas/index.html`: phead(w45) → 「별내에서 <em>어디든</em>」 + 사진 3 / `.arows` 9줄(이름 · 이동 시간 · 첫 실적) + 이동 시간 안내 → CTA.

title 규칙: 이야기 `제목 | 제이식스미디어 행사 이야기`, 지역 `○○ 음향 렌탈 · 행사 음향 · 음향 설치 | 제이식스미디어`.
description 은 lead 120자 / 지역 고정 문장. og:image 는 첫 사진 w.

## 업무 화면 (이식) — 화면 이름과 주요 칸

- `quote.html`: 입력칸 `#q-org #q-name #q-tel #q-email #q-title #q-date #q-place #q-people #q-memo`, 품목 체크 `#catalog input[data-id]`,
  할인 `#s-discount`, 단추 `#btn-send`(문의) `#btn-print` `#btn-link` `#btn-to-customer` `#btn-box`(저장함) `#btn-contract` `#btn-stmt` `#btn-sched`.
  품목은 `quote-catalog.js` 의 7묶음(행사 음향 · 조명 운영 p1~p5 / 음향 렌탈 a1~a7 / 조명 렌탈 b1~b3 / 영상 b4 / 운영 인력 f1 f2 f5 / 설치 i1~i6 / 기타 g2 g3), 모든 `price:null`.
- `contract.html`: 왼쪽 관리자 패널(계약 종류 · 우리 회사 정보 · 서버 설정 · 갑/을 · 행사 · 품목 · 지급조건 · 취소규정 · 특약) / 오른쪽 종이 `#paper` / 고객 모드 서명 패널.
- `statement.html`: 공급자(우리) · 공급받는자 · 품목 표(on 체크) · 부가세 별도/포함 · 입금액 · 계좌(이 기기 저장) · 메모.
- `schedule.html`: 잠금(암호 + 이름) → 목록(월간 일정표 + 행사 카드) / `#e=ID` 행사 하나(개요 + 체크리스트, 체크는 한 칸씩 서버 반영).
- `upload.html`: 처음 한 번 서버 주소 · 비밀번호 → 사진 칸 7(교회행사 · 기업행사 · 지자체 · 축제 · 학교행사 · 전시 · 공연 · 설치 · 장비) → 행사명 · 날짜 · 장소 · 설명 → 사진 고르기(워터마크 체크) → 올리기 → 블로그 제목 후보 · 본문 · 인스타 글 / 올린 사진 목록 수정 · 삭제.
- `office.html`: 도구 카드 3묶음(견적 · 계약 / 행사 준비 / 홈페이지 · 검색), 업무 흐름 7단계, 서버 연결 상태(GET 핑), 암호 안내, 수정 모드 안내.
