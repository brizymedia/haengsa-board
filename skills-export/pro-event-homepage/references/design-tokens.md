# 디자인 체계 — 프로이벤트

출처: `assets/style.css` 1~28행 `:root` 와 각 컴포넌트 규칙. 숫자는 코드 그대로.
분위기: **어두운 잉크 바탕 + 코발트→시안 빛**. 영화관·무대 조명 느낌(빛줄기, 격자, 필름 그레인, 커서 빛).

## 색 토큰 (`:root`)

| 토큰 | 값 | 쓰임 |
|---|---|---|
| `--ink` | `#06070B` | 바탕(body, 커튼, theme-color) |
| `--ink-2` | `#0C0E15` | 번갈아 나오는 섹션 바탕(사업분야·프로세스·섭외·푸터, `.sec.gray`) |
| `--surface` | `#11141D` | 카드·사진 자리 바탕 |
| `--line` | `rgba(255,255,255,.08)` | 얇은 선 |
| `--line-2` | `rgba(255,255,255,.14)` | 테두리 |
| `--txt` | `#F2F4F8` | 본문 글자, 주 단추 바탕 |
| `--muted` | `#8E96AB` | 보조 글자 |
| `--dim` | `#5B627A` | 더 약한 글자(번호·라벨) |
| `--cobalt` | `#2F6BFF` | 주 강조(선택 영역, 체크박스) |
| `--cyan` | `#19D3FF` | 포인트(eyebrow, 라벨, 테두리 강조, 점) |
| `--glow` | `rgba(47,107,255,.55)` | 단추 그림자 |
| `--peach` | `#FFB347` | 주석상 "아주 드물게" — 대문에서는 쓰는 곳 없음 |
| `--grad` | `linear-gradient(92deg,#5C8BFF 0%,#19D3FF 55%,#9AF0FF 100%)` | 제목 강조 글자(`.grad`), 진행 막대, 커튼 막대, 주 단추 hover |

토큰 밖에서 직접 쓰는 색: 본문 밝은 회색 `#C9CFDD`·`#C9CFDC`·`#D5DAE5`, 라이브 점 빨강 `#FF4D6D`.
업무 화면(port_docs 치환 결과) 색: 시안 `#19D3FF`, 밝은 시안 `#5FE0FF`·`#9AF0FF`, 짙은 시안 `#14A9CC`, 짙은 파랑 `#1F4FD1`, 카드 `#11141D`, 바탕 `#06070B`.
(큰길이벤트 주황 `#F59E0B` 등을 이 색으로 바꾸는 표가 `tools/port_docs.py` 의 `COLORS`.)

## 글꼴

| 토큰 | 값 | 불러오기 |
|---|---|---|
| `--ff-body` | `"Pretendard Variable",Pretendard,"Noto Sans KR",-apple-system,system-ui,sans-serif` | jsDelivr `orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css` |
| `--ff-disp` | `"Unbounded","Pretendard Variable",Pretendard,sans-serif` | Google Fonts `Unbounded:wght@400;500;600` |

- 한글 제목·본문 = Pretendard(굵기 800 제목, 600~700 단추). 영문 라벨·숫자 = Unbounded(500~600, 자간 넓게 `.2em~.4em`, 대문자).
- `body{word-break:keep-all}` — 한글 낱말이 안 쪼개지게. 빼지 말 것.
- 업무 화면은 별도: Pretendard(정적) + `iconify-icon@2.3.0`(code.iconify.design).

## 기타 토큰

| 토큰 | 값 |
|---|---|
| `--ease` | `cubic-bezier(.22,1,.36,1)` (대부분의 전환) |
| `--ease-io` | `cubic-bezier(.65,0,.35,1)` (커튼·메뉴 시트·스캔) |
| `--gutter` | `clamp(20px,5vw,72px)` |
| `--max` | `1440px` (`.wrap{width:min(100% - gutter*2, max)}`) |

모서리: 단추·칩 `99px`(알약), 카드 14~28px(작은 것 14, 카드 20~24, 무대 26, 폼 28). 섹션 여백 `.sec{padding:clamp(88px,11vw,150px) 0}`.

## 글자 크기 (clamp)

| 요소 | 크기 |
|---|---|
| 히어로 h1 | `clamp(40px,7.6vw,118px)`, 줄간 1.02, 자간 -.035em, 최대 14ch. 640 이하 `clamp(38px,11.5vw,60px)` |
| 섹션 h2 (`.sec-head h2`) | `clamp(32px,5vw,68px)`, 최대 18ch |
| 견적문의 h2 | `clamp(34px,5vw,72px)` |
| 소개 큰 문구 `.about .big` | `clamp(28px,3.8vw,52px)` |
| eyebrow | 11px Unbounded, 자간 .28em, 시안, 앞에 28px 빛나는 선 |
| 생성 페이지 h1 (`.phead h1`) | `clamp(30px,4.6vw,58px)` |

## 반응형 기준 (max-width)

| 기준 | 바뀌는 것 |
|---|---|
| 1100px | 히어로 오른쪽 `.side` 숨김, 포트폴리오 12열에서 6칸, 프로세스 가로 스크롤(scroll-snap), 푸터 2열 |
| 900px | 상단 메뉴·견적 단추 숨기고 햄버거(`.burger`)+전체화면 시트(`.sheet`), 2단 그리드 → 1단, **사업분야 무대(`.biz-stage`) 숨기고 항목 아래 인라인 사진(`.biz-inline`)**, 영상 1단 |
| 640px | 전화 단추 아이콘만, 로고 옆 SINCE 숨김, 포트폴리오 1열, 폼 1열, 고객 띠 라벨 숨김 |
| 960px / 600px | 생성 페이지(`.story` `.area3` `.callband` `.scards` `.asvc` `.arow`) 전용 |
| `(hover:hover) and (pointer:fine)` | 커서 빛 표시. JS 도 같은 조건(`fine`)으로 자석 단추·기울임·shine·사업분야 hover |
| `prefers-reduced-motion:reduce` | 모든 애니메이션 0.01ms, reveal·히어로 글자 바로 보이기. JS 도 `reduce` 로 카운터 즉시값, 시차 끔 |

검증 폭: **375 / 1280** (가로 넘침 0 이어야 함).

## 핵심 컴포넌트 (클래스 → 위치)

| 컴포넌트 | 클래스 | 특징 |
|---|---|---|
| 주 단추 | `.btn.btn-pri` | 흰 바탕 잉크 글자, hover 시 `::after` 그라데이션이 깔림 + glow. 화살표 svg `.arr` 4px 이동 |
| 유령 단추 | `.btn.btn-ghost` | 반투명 + blur, 테두리 `--line-2` |
| 자석 단추 | `[data-mag]` | JS: 포인터 위치 따라 x·.25, y·.35 이동 |
| eyebrow | `.eyebrow` | 섹션 머리 라벨(영문) |
| 섹션 머리 | `.sec-head.line-draw` | 2열(제목/설명), 들어오면 위쪽 선이 왼쪽→오른쪽 그려짐 |
| 등장 | `.reveal` → `.in` | 36px 아래에서 올라오며 나타남(IntersectionObserver) |
| 숫자 카운터 | `[data-count]` (+`data-plain` 은 천 단위 쉼표 없음) | 1.8초 easeOutQuart |
| 마퀴 띠 | `.ticker .track`, `.clients .track` | JS 가 내용을 두 번 이어 붙이고 CSS `marq` 로 -50% 이동(60s / 45s) |
| 포트폴리오 카드 | `.work` (+`.big` 8×6, `.wide` 6×3, 기본 4×3, `.tall`) | 12열 dense 그리드, 행 104px. 인원 배지 `.num`, 커서 따라가는 `.shine` |
| 무대 | `.biz-stage` | sticky, 5:4, 이미지 2장 교차(.img.on), 네 모서리 시안 괄호 `.corner`, 위→아래 스캔 빛 `.scan` |
| 시스템 카드 | `.sys[data-tilt]` | 3:4, 배경 사진 + 아래 어둡게, JS 3D 기울임 |
| 마름모 | `.diamond` | 회전 45° 시안 테두리 — 서명·접수 완료 표시 |
| 생성 페이지 머리 | `.phead` | 배경 사진 + 위아래 어둡게, crumb + h1 + 설명 |
| 상담 띠 | `.callband` | 배경 사진(w14) + 전화번호 크게 + 견적 단추 |
| 카드 목록 | `.scards` `.scard` | 16:10 사진 + 제목, hover 시 시안 테두리 |

배경 질감: `.grain`(SVG feTurbulence 노이즈, 7% overlay, z 120), `.cursor`(520px 방사 그라데이션, z 1), 히어로 `.grid-lines`(120px 격자, 방사 마스크), `.beams`(시안 빛줄기 4개, `--x --r --d` 변수, screen 합성).

z-index 순서: 커튼 200 > 라이트박스 150 > 맨위로 140 > 진행 막대 130 > 그레인 120 > 상단 메뉴 100 > 메뉴 시트 99.
