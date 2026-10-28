# 디자인 토큰 · 컴포넌트 — `assets/style.css`

외부 CSS 라이브러리 없음(구글 폰트만). 업무 화면 5종 · office.html 은 각자 `<style>` 을 갖고 이 파일을 쓰지 않는다(맨 아래 참고).

## :root 변수 전부

```css
--bg: #FBF6EE;   --bg2: #F5ECDF;   --paper: #FFFFFF;
--ink: #2B211B;  --ink2: #5A4A3E;  --mute: #86766A;  --line: #EADFCF;
--amb: #E58A2B;  --amb-d: #B45F12; --glow: #FFC870;  --cream: #FFF4E2;
--night: #221913; --night2: #33271E; --night-line: rgba(255, 220, 170, .14);
--r: 20px; --r-s: 12px;
--kr:   'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', system-ui, sans-serif;
--kr-h: 'Gowun Batang', 'Noto Serif KR', serif;
--en:   'Fraunces', Georgia, serif;
--shadow: 0 18px 40px -22px rgba(74, 44, 16, .35);
--wrap: 1200px;
```

변수 밖에서 자주 쓰는 고정값: 앰버 그라데이션 끝색 `#F0A24A`(`.ctaband`), 점등 전 단어 `#CDBDAE`, 목록 번호 `#D5C3B0`,
칩 테두리 `#F3D9B5`, 지도 카드 바탕 `#EFE4D3`, 앰버 반투명 `rgba(229,138,43,.12~.25)`, 밤 반투명 `rgba(34,25,19,…)`,
`meta theme-color` `#221913`, 수정 모드 노랑 `#FFE85C`/`#E0A100`(edit.js 안).

## 글꼴

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,800;1,9..144,600;1,9..144,700&family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
```

- 본문 `body { font: 400 16px/1.75 var(--kr) }` (860 이하 15.5px). `word-break: keep-all; overflow-wrap: break-word`.
- 한글 제목(h1 · .h2 · 카드 제목 · 시트 메뉴) = 고운바탕 700.
- 영문 장식(eyebrow 아님 — 숫자 `01`, 연도, `since 2005`, 메뉴 `<small>HOME</small>`, 마퀴, 바닥글 h4) = Fraunces 이탤릭.
- `.eyebrow` 는 Noto Sans KR 700 15.5px + 앞에 28×2px 선(앰버 진한색, 어두운 바탕에선 `--glow`).

## 크기 · 간격

| 요소 | 값 |
|---|---|
| `.wrap` | `width: min(1200px, 100% - 40px)`; 640 이하 `calc(100% - 32px)` |
| `.sec` | `padding: clamp(72px, 10vw, 120px) 0` — 변형 `.sand`(bg2) `.white`(paper) `.night` |
| CTA 띠 섹션 | 인라인 `padding-top: clamp(48px,6vw,72px)` |
| `.sec-head` | flex 양끝, 아래 `clamp(36px, 5vw, 56px)`, 제목 칸 최대 720px, 설명 최대 440px |
| `.h2` | `700 clamp(28px, 4.2vw, 44px)/1.3 var(--kr-h)`; `em` = 앰버 진한 + 아래 38% 형광(`rgba(255,200,112,.45)`) |
| `.hero h1` | `clamp(36px, 6.2vw, 72px)/1.22` (640 이하 `clamp(29px, 8.4vw, 36px)`), `em` 은 `--glow` |
| `.phead h1` | `clamp(32px, 5vw, 54px)`; phead 위아래 150/70 (640 이하 116/50) |
| `.btn` | 높이 50, 좌우 24, 999px, 700 15.5px, hover 위로 2px |
| 머리 `.hd .wrap` | 높이 76 (640 이하 64), 로고 높이 40 (34) |
| `.lead` | `clamp(16px, 1.6vw, 18px)` `--ink2` |

## 반응형 기준

| 기준 | 바뀌는 것 |
|---|---|
| ≤1080 | 메뉴 · 전화 · CTA 숨김 → 햄버거. 장비 격자 2열. 연혁 세로선. trio3 2열(첫 칸 가로 전체) |
| ≤960 | (이야기 · 지역) `.story` `.area3` 1열, 이야기 aside 고정 해제, 카드 2열 |
| ≤860 | 2단 레이아웃 전부 1열(intro · works6 · greet · cgrid · map · svc · rpane). works6 사진판 숨고 각 줄에 76px 썸네일. 갤러리 2열 160px, 캡션 항상 보임. 바닥 1열 |
| ≤640 | 폰: 히어로 글을 아래로, CTA 단추 반씩. 폰 하단 고정 `.quick`(전화 · 문자 · 견적 문의 1:1:1.6). totop 위로 90px. 폼 1열. 게시판 줄 2열. 라이트박스 화살표 아래로 |
| ≤600 | (이야기 · 지역) 카드 1열, 사진 격자 2열 |
| ≥1000 | 브랜드 로고 7열 |
| reduced-motion | 모든 animation/transition 끔, `.reveal` 즉시 보임, 영상 자동재생 안 함 |

## 컴포넌트 클래스 사전

| 클래스 | 설명 |
|---|---|
| `.progress` | 맨 위 3px 스크롤 진행 막대(glow→amb) |
| `.hd` `.on-dark` `.solid` | 고정 머리. 대문만 `on-dark`(흰 로고 `.w` 보임), 40px 스크롤 뒤 `.solid`(반투명 아이보리 + blur) |
| `.burger` `.sheet` | 햄버거 · 오른쪽에서 밀려오는 전체 메뉴(고운바탕 21px, 영문 small) + 하단 연락처 |
| `.hero` | 100svh(최소 640, 최대 980). 포스터 img + video + 왼쪽→오른쪽 어둡게 + 오른쪽 위 호흡하는 빛(`breathe` 7s). `.foot` 에 `.years`(2005 —● 2026) + `.vctl`(이퀄라이저 `.eq` + 정지 단추) |
| `.phead` | 서브 페이지 머리: `.bg` 사진(불투명 .5) + 그라데이션 + eyebrow · h1 · p · `.crumb` |
| `.marquee` | 앰버 띠, 브랜드 이름 Fraunces 이탤릭 22px + `✦`, 38s 무한, hover 멈춤 |
| `.intro .quote .w .lit .hl` | 단어 점등 문장(스크롤에 따라 회색→먹색, em 단어는 앰버) |
| `.collage .a .b .tag` | 사진 두 장 겹친 콜라주 + `since 2005` 꼬리표 |
| `.twin` | 음향 · 조명 2칸 카드 |
| `.sig` | 대표 서명줄(동그라미 「김」 + 이름 + 단추) |
| `.works6 .stage .wlist` | 하는 일: 왼쪽 sticky 사진판(4:4.4), 오른쪽 목록. 고른 줄 `li.on` |
| `.night .beam .b1 .b2` `.strong2 .scard` | 밤 무대 섹션(빛기둥 두 개 흔들림) · 강점 카드(큰 번호 · 태그 · 사진) |
| `.rtabs` `.rpane` `.rlist` | 실적 탭(검정 알약이 켜짐) · 탭 판(사진+목록) · 앰버 점 목록 |
| `.tl` `li.now` | 연혁 5칸 가로선(≤1080 세로), 현재 칸 빛나는 점 |
| `.gal` `.gal.home` `.pf .gal` | 사진 격자 4열 210px. 대문은 1번 2×2, 6번 가로 2칸. 포트폴리오는 7n+1 세로 2칸 + dense |
| `.filters button.act` | 포트폴리오 분야 필터(앰버가 켜짐, 개수 `<small>`) |
| `.lb` | 라이트박스(검정 .94, 화살표 · 닫기 · 캡션) |
| `.trio3 .box .box.dark .nlist .hours` | 공지 · 오시는 길 · 바로 상담 3칸 |
| `.ctaband` | 앰버 그라데이션 CTA 띠(흰 단추 `.btn-w` + 검정 `.btn-ink`) |
| `.greet .facts .info-t .map .mapcard .pin` | 회사소개 인사말 · 숫자 · 정보 표 · SVG 그림 지도 + 핑 |
| `.svc .places` | 하는 일 지그재그(짝수 줄 사진 오른쪽) · 설치 사례 카드 |
| `.eqgrid .eqc .brands .brand .eqphotos .note-s` | 장비 카드 4열 · 브랜드 로고 칸(img 클래스 `.m` 34px, `.t` 46px 높이) · 사진 3장 |
| `.btabs .bpane .board .row .files .blog-l .bnote` | 게시판 탭 · 펼치는 줄 · 자료실 · 블로그 목록 |
| `.cgrid .ways .form .kinds .agree .done .faq` | 문의 페이지 |
| `.ft .ftl .sns .bot` | 바닥글(3열 → 1열), 바닥 링크 줄, 저작권 · 제작 큰길브리지 |
| `.quick` `.totop` | 폰 하단 고정 단추 · 맨 위로 |
| `.story .sbody .sgrid .stcards .stcard .snote` | 행사 이야기(왼쪽 어두운 사실표 aside + 본문 + 사진 격자) · 카드 |
| `.area3 .h2s .h3s .alist .apics .asvc .arows .arow .muted` | 지역 페이지 |
| `.chip` `.reveal .d1 .d2 .d3` `.sr` `.en` | 칩 · 등장 지연 · 화면낭독 전용 · 영문 이탤릭 |

## 업무 화면의 별도 디자인 (이식 결과)

- 바탕 `#221913`, 카드 `#33271E`, 선 `rgba(255,220,170,.16)`, 강조 `#E58A2B` / `#FFC870`, 버튼 글자색 `#221913`.
- 글꼴 Pretendard(`cdn.jsdelivr.net/gh/orioncactus/pretendard`), 아이콘 `iconify-icon 2.3.0`.
- quote.html: `.glass` 카드, `.accent-grad`(#FFC870→#E58A2B→#B45F12 글자 그라데이션), `.btn-primary`(앰버 그라데이션), 노이즈 오버레이.
- 큰길이벤트 주황(#F59E0B 계열) → 이 회사 색으로 바꾸는 표가 `tools/port_docs.py` 의 `COLORS`, office 색은 `OFFICE`.
  업무 화면 색을 바꾸려면 HTML 이 아니라 이 두 표를 고치고 이식기를 다시 돌린다.
