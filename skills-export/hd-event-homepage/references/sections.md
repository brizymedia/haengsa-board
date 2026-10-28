# 페이지별 섹션 구성

## index.html (대문, 한 장)

`<title>` 「HD기획 | 기업행사 · 체육대회 · 지자체 행사 기획 대행 — 서울 · 광명 · 남양주」, `robots index,follow,max-image-preview:large`,
canonical/og = `https://www.hdplan.co.kr/`, og:image = `hero_poster.webp`, JSON-LD `@graph`: `Organization+LocalBusiness`(`#business`, 주소 · areaServed 3 · founder · knowsAbout · OfferCatalog 8) + `WebSite`.

| # | 구획 | 선택자 | 내용 |
|---|---|---|---|
| 0 | 상단 흰 띠 | `header.top` | 로고 · 슬로건 · 전화 · 견적 문의 · 햄버거 `#burger` |
| 0 | 검은 메뉴 띠 | `#bar` | 회사소개 `#about` · 사업분야 `#business` · 포트폴리오 `#gallery` · 행사영상 `#video` · 고객후기 `#review` · 공지사항 `#notice` · 블로그 `blog/` · 자동 견적 `quote.html` · 견적문의 `#contact` (9개) |
| 0 | 폰 메뉴 | `#sheet` | 위 + 포트폴리오는 `portfolio.html`, 행사 이야기 · 운영 지역 추가(11개), 아래 대표 · 주소 · 전화 단추 |
| 1 | 히어로 | `section.hero#hero` | 슬라이드 5: ① hero_poster 「행사의 처음부터 끝까지, 한 팀이 책임집니다.」(유일한 h1) ② sys/h2_4 무대·음향·조명 직접 운영 ③ sys/h3_2 기념식·창립·시상식 ④ slider2 체육대회·워크숍 ⑤ sys/h1_8 서울·광명·남양주 현장 답사. 각 장 eyebrow(영문) · 제목(em 강조) · lead · 단추 2개. `#dots` `#prev` `#next` `#cnt` 스크롤 힌트 |
| 2 | 핵심 가치 4탭 | `section.values` `#vtabs` `#vpanes` | PLAN 기획 / DIRECT 연출 / OPERATE 운영 / PARTNER 신뢰 — 사진(sys/h1_4 · h2_1 · h1_6 · h3_3) + 제목 + 글 + 알약 3개 |
| 3 | 바로가기 3장 | `section.trio` | ABOUT HD(slider5) · BUSINESS(sys/h2_2) · CONTACT(sys/h1_3) |
| 4 | 회사소개 | `#about` | 사진 2장(sys/h1_7 큰 것 + slider1 작은 것) + 「SEOUL · GEUMCHEON-GU」 꼬리표, 대표 인사말 2문단, 서명(머리글자 원 「엄」), 숫자 4개 `.stats [data-count]`: 8 분야 · 20000 명(**예시, 대표 확인 전**) · 3 지역 · 1 영업일 |
| 5 | 사업분야 8 | `#business` | 01 기업행사 · 02 체육대회·워크숍 · 03 지자체행사 · 04 관공서·기관행사 · 05 학교행사 · 06 기공식·준공식·개관식 · 07 음향·조명·무대·LED · 08 축제·놀이존·물놀이 (각 영문 꼬리표 · 설명 · 태그 3) |
| 6 | 프로세스 5 | `#process` | 01 CONSULT 상담·견적 → 02 SURVEY 현장 답사 → 03 PLAN 기획·큐시트 → 04 ON SITE 세팅·운영 → 05 WRAP UP 철수·정산 |
| 7 | 갤러리 | `#gallery` `#gal` | app.js `WORKS` 앞 9장, 「+ 전체 포트폴리오 보기」, 아래 「포트폴리오 19건 전체 보기」 · 「행사 이야기 읽기」 |
| 8 | 영상 + 안내 | `#video` `#player` | 왼쪽 영상(포스터 hero_poster), 오른쪽 `.info` 「견적 문의 전에 준비하면 좋은 것」 4가지(목적 · 날짜 · 장소인원 · 예산) + 칩 7 + 단추 |
| 9 | 콘텐츠 3타일 | `#contents` | CASTING MC·공연·강사 섭외 / SYSTEM 음향·조명·무대·LED(장비 단독 대여) / RENTAL 행사 물품·부스·놀이존 |
| 10 | 고객후기 4 | `#review` | 체육대회 · 송년회 · 기념식 · 학교행사 — **구조를 보여 주는 예시 문구**(README: 실제 후기로 바꾸기 전엔 공개하지 말 것) |
| 11 | 공지 · 안내 | `#notice` | 공지 상자 `#noticeList`(app.js `NOTICES`) · 「견적 받는 법, 세 단계」 · 「오시는 길」(주소 · 네이버 지도 링크 · 지역별 이동 시간 링크) |
| 12 | 견적 문의 | `#contact` `#quoteForm` | 왼쪽 소개 + 대표 직통 · 이메일 · 사무실, 오른쪽 폼: 이름* · 연락처* · 기관 · 행사 유형(9) · 예정일 · 인원 · 내용 · 숨은 website · 개인정보 동의 · 완료 덮개 `#formDone` |
| — | 푸터 | `footer.footer` | 로고 · 소개, OFFICE(주소 · TEL · E-MAIL), COMPANY(상호 · 대표 · 운영 지역), `.ftl` 링크 줄, 저작권 · 맨 위로. app.js 가 끝에 「관리자 모드」 링크 추가 |
| — | 고정 요소 | `.quick` `#totop` `#lb` | 폰 하단 3단추, 맨 위로, 라이트박스 |

스크립트: `<script src="assets/app.js?v=20261004">` (body 끝, defer 없음).

## portfolio.html

- `.pagehead`(sys/h2_2) 「현장 사진 전체 보기」 → `#portfolio` 필터 `#filters`: 전체 `all` · 대형행사 `big` · 기업행사 `corp` · 지자체·관공서 `gov` · 체육대회 `sport` · 축제·놀이존 `fest` · 기공식·의전 `cer` → `#pfGrid` → 「이런 행사, 견적 문의하기」.
- 메뉴에서 「포트폴리오」에 `class="act"`, 앵커는 `index.html#…` 꼴.
- og:image `works/w13.webp`.
- 필터 값 = `WORKS[].c` 의 낱말 = `upload.html` 사진 칸 slug(`corp sport gov fest cer`) = `UP_CAT` 키. 하나를 바꾸면 셋을 같이.

## stories/ (행사 이야기, make_pages.py)

- 목록 `stories/index.html`: 머리띠(sys/h2_2) → `.scards.big` 2열 카드 5 → 「더 많은 현장 사진은 포트폴리오에」 → 콜밴드.
- 한 편: 머리띠(첫 사진) → `.story`[왼쪽 aside: Event File dl(행사 · 분야 · 장소 · 연도) · 「비슷한 행사 견적 받기」 · 지역 링크 / 오른쪽: 본문 2문단 · 사진 격자 `.sgrid.n<장수>` · 포트폴리오 단추] → 「다른 현장 이야기」 3장 → 콜밴드.
- 5편과 사진: 국회 개방행사 놀이존 운영(2024, 영등포, works/w13 · biz/b8) · 대기업 임직원 페스티벌(2026, w9 · b1) · 소방학교 신입생 체육대회(2026, w10 · b2) · 어린이날 기념 행사 총괄(2024, w12 · b3) · 해외 장관 초청 기공식(2023, w2). → **전부 워터마크 사진**.

## areas/ (운영 지역, make_pages.py)

- 목록 `areas/index.html`: 머리띠(sys/h1_8) → `.arows` 9행(이름 · 「본사」 또는 「차로 약 N분 · Nkm」 · 실적 또는 「직접 답사 · 진행」) → 이동 시간 기준 안내 → 콜밴드.
- 한 곳: 머리띠 「○○ 행사, HD기획이 갑니다」 → `.area3`[How Far 이동 시간 문단 · 「○○에서 한 행사」(실적 없으면 「아직 이 페이지에 적을 만큼 정리된 기록이 없습니다」) · 관련 이야기 카드 / 사진 3장] → 회색 「○○에서도 이런 행사를 맡습니다」 서비스 8칸 + 다른 지역 링크 → 콜밴드 「○○ 행사 날짜가 잡히셨나요?」.
- 이동(분 · km): 금천 본사 / 구로 10 · 8.7 / 광명 10 · 7.4 / 관악 10 · 8.9 / 영등포 15 · 10.8 / 마포 15 · 16.9 / 강남 20 · 20.4 / 송파 25 · 23.7 / 남양주 45 · 43.6.

## blog/ (build-blog.mjs)

- 독립 템플릿(공통 style.css 를 쓰지 않고 `<style>` 안에 CSS 를 직접 넣음). 상단 검은 띠 56px(로고 · 사업분야 · 블로그 · 행사 이야기 · 운영 지역 · 자동 견적 · 주황 전화), 간단한 푸터.
- 목록: eyebrow 「Blog · Event Guide」 · h1 「행사 준비 블로그」 · 지역 칩(글 수) · 카드 격자(24개씩) · 쪽 이동 · 상담 상자.
- 지역 모음: 같은 구조, 글이 없으면 `noindex,follow` + 「곧 올라옵니다」 + 최근 6편.
- 글: 빵부스러기 → eyebrow(지역 · 날짜) → h1 → meta(지역 글 모음 · 지역 행사 안내 · 읽는 시간 = 본문 500자당 1분) → lead → 표지(16:9) → 「이 글의 요점」 → 목차 → 본문(h2 `id=s1…`) → 자주 묻는 질문(details) → 확인한 자료 → 상담 상자 → 같이 보면 좋은 글 3(같은 지역 먼저, 다음 같은 주제).
- JSON-LD: 글 = BreadcrumbList + BlogPosting(+ spatialCoverage) + FAQPage, 목록 = Blog, 지역 = CollectionPage. publisher 는 대문의 `#business` 를 가리킨다.

## 업무 화면 공통 겉모양

어두운 바탕 `#0B0E15`, Pretendard static. quote.html 은 노이즈 덮개 · 유리 카드(`.glass`), quote · contract 는 iconify 아이콘. 머리 로고는 `favicon.svg`. 화면별 흐름은 `workflows.md`.
