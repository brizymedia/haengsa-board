# 디자인 체계 — HD기획

출처: `assets/style.css` 머리 주석 「깔끔한 화이트 톤 행사기획사 홈페이지」.

## 색 토큰 (`:root`)

| 토큰 | 값 | 쓰임 |
|---|---|---|
| `--bg` | `#FFFFFF` | 바탕 |
| `--bg2` | `#F4F5F7` | 회색 섹션(`.sec.gray`), 칩 · 태그 바탕 |
| `--bg3` | `#EDEFF2` | 사진 로딩 바탕 |
| `--ink` | `#111318` | 제목 글자, 검은 메뉴 띠, 가치 탭 띠, `theme-color` |
| `--txt` | `#22252D` | 본문 |
| `--muted` | `#6B7180` | 보조 글 |
| `--dim` | `#9AA0AD` | 더 흐린 글 |
| `--line` | `#E4E6EB` | 선 |
| `--line2` | `#CFD3DB` | 진한 선(단추 테두리) |
| `--acc` | `#F0472B` | 포인트 오렌지레드(단추 · 영문 꼬리표 · 밑줄) |
| `--acc2` | `#FF7A4D` | 밝은 포인트(어두운 바탕 위 강조 `em`) |
| `--navy` | `#101522` | 히어로 · 서브 머리띠 · 콜밴드 바탕 |
| 단추 hover | `#D63A20` | `.bar .cta:hover` |

블로그 페이지(`build-blog.mjs CSS`)는 같은 값에 `--acc-ink:#C9371F`(흰 바탕 위 링크 글자) 추가, 푸터 `#0B0E15`.

업무 화면(어두운 테마, `port_docs.py COLORS · OFFICE`):

| 이름 | 값 |
|---|---|
| 바탕 | `#0B0E15` |
| 카드 | `#161A24` |
| 선 | `rgba(255,122,77,.16)` |
| 포인트 | `#F0472B` / `#FF7A4D` / 진한 `#D63A20` · `#B02E17` / 옅은 `#FF9C78` |
| contract.html | `--amber:#F0472B; --amber-2:#FF7A4D; --amber-ink:#B02E17; --dark:#0B0E15; --ink:#161A24` |

큰길이벤트 원본 주황(`#F59E0B` 등)을 위 색으로 치환하는 표가 `port_docs.py COLORS` 에 있다.

## 글꼴

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
```
- `--ff: "Pretendard Variable", Pretendard, "Noto Sans KR", -apple-system, system-ui, sans-serif`
- `--en: "Montserrat", "Pretendard Variable", Pretendard, sans-serif` — 영문 꼬리표(대문자, `letter-spacing .2~.3em`), 숫자, 전화번호
- 업무 화면 · office.html: `pretendard/dist/web/static/pretendard.min.css`(버전 없음) + 아이콘 `iconify-icon@2.3.0`(quote · contract)
- 본문 16px / line-height 1.65, 제목 `letter-spacing:-.035em`, 굵기 800

## 기타 토큰

| 토큰 | 값 |
|---|---|
| `--ease` | `cubic-bezier(.22,1,.36,1)` |
| `--ease-io` | `cubic-bezier(.65,0,.35,1)` |
| `--gutter` | `clamp(18px,4.5vw,64px)` |
| `--max` | `1280px` (`.wrap{width:min(100% - gutter*2, max)}`) |
| `--r` | `16px` 카드 모서리 |
| `--sh` | `0 20px 50px -24px rgba(17,19,24,.25)` |
| 섹션 위아래 | `.sec{padding:clamp(64px,8vw,112px) 0}` |
| 단추 | `padding:14px 26px; border-radius:8px; font-weight:700; 15px` |

## 반응형 기준

| 폭 | 바뀌는 것 |
|---|---|
| ≤1100 | 사업분야 4→2열, 프로세스 5→3열(화살표 숨김), 후기 4→2열, 공지 구획 2열(공지 상자 한 줄 다 씀), 푸터 2열, 지역 서비스 `.asvc` 4→2열 |
| ≤960 | 이야기 `.story` · 지역 `.area3` · 콜밴드 1열, 이야기 aside sticky 해제, `.scards` 2열 |
| ≤900 | 상단 흰 띠 높이 84→68, 슬로건 · 전화 숨김, 햄버거 표시, 검은 띠 메뉴 숨김(미니 로고 · CTA 항상 보임, 높이 48), 가치 패널 1열, 바로가기 1열(16:8), 회사소개 1열, 숫자 2열, 영상 구획 1열, 타일 1열, 문의 1열, **`.quick` 하단 빠른 단추 표시 + `body{padding-bottom:56px}`**, 맨 위로 bottom 72, 히어로 높이 `min(72vh,640px)`, 스크롤 힌트 숨김 |
| ≤600 | 갤러리 3→2열(캡션 항상 보임), 프로세스 · 후기 · 공지 · 폼 줄 · 푸터 1열, 히어로 카운터 숨김, 가치 탭 4→2×2 |
| ≤640 (블로그) | 상단 메뉴 글자 작게, `.hide-sm` 숨김 |
| reduced-motion | 애니메이션 0.01ms, `.reveal` 바로 보임 |

## 핵심 컴포넌트 (클래스)

| 클래스 | 모양 |
|---|---|
| `.top` | 흰 머리 띠 84px: 로고 · 세로선 · 슬로건 2줄 · 오른쪽 전화(원형 아이콘 + 「행사 상담 · 견적」) · 주황 「견적 문의」 단추 · 햄버거 |
| `.logo .mark` | 40px 검은 둥근 네모 「HD」(Montserrat 800) + `::after` 오른쪽 아래 20px 주황 원 |
| `.bar` | 검은 메뉴 띠 56px, `position:sticky;top:0`, 링크 밑에 3px 주황 줄이 왼쪽부터 자람. `.stuck` 일 때 왼쪽 미니 로고(흰 30px 네모) · 오른쪽 주황 CTA 등장 |
| `.sheet` | 폰 전체 화면 메뉴(오른쪽에서 밀려옴), 링크 오른쪽에 영문 작은 꼬리표 |
| `.hero` | `min(78vh,760px)`, 최소 520, 남색 바탕, 슬라이드 겹침 페이드 1.1s, 왼쪽→오른쪽 어두운 그라데이션, 왼쪽 아래 진행 점, 오른쪽 아래 원형 이전/다음 + `01 / 05` |
| `.values` | 검은 4칸 탭(선택 칸 주황 + 아래 삼각형) + 흰 패널(16:9 사진 + 글 + 알약 목록) |
| `.trio` | 4:3 사진 카드 3장, 가운데 정렬 글, hover 시 주황 그라데이션 · 밑줄 길어짐 |
| `.sec-head` | 왼쪽 `.en-t`(주황 원 테두리 점 + 대문자 영문) + h2, 오른쪽 설명 또는 검은 `.more` 단추 |
| `.biz .card` | 16:10 사진 + 왼쪽 위 번호 칩 + 영문 꼬리표 · 제목 · 설명 · 태그 알약 |
| `.gal figure` | 4:3, hover 확대 + 아래 캡션 올라옴, 오른쪽 위 인원 알약(`.num`) |
| `.player` | 16:9 영상, 가운데 84px 주황 재생 원, 왼쪽 위 「SKETCH MOVING」 빨간 점 라벨 |
| `.rv` | 후기 카드(분류 태그 · 큰 따옴표 · 별 · 글 · 머리글자 원) |
| `.form` | 2칸 줄(`.row`), 숨은 `website` 함정, 동의 체크, 완료 덮개 `.done.on` |
| `.quick` | 폰 하단 고정 3칸(전화 · 문자 · 주황 견적 문의 1.3fr) |
| `.lb` | 라이트박스(검정 94%) |
| `.pagehead` | 서브 페이지 머리띠(남색 + 사진 28% + 빵부스러기 + 영문 + h1 + 설명) |
| `.story` / `.scards` / `.sgrid` | 이야기: 왼쪽 300px 남색 sticky 정보 상자, 오른쪽 본문 17px · 사진 격자(첫 장 2×2) |
| `.area3` / `.asvc` / `.arows` / `.alist` | 지역: 2열 소개 + 사진, 서비스 4칸, 지역 목록 행(이름 · 이동 시간 · 메모), 마름모 점 목록 |
| `.callband` | 사진 위 남색 그라데이션 띠, 큰 전화번호 + 단추 3개(전화 · 자동 견적서 · 문의 폼) |
| `.ftl` | 푸터 링크 줄(블로그 · 자동 견적서 · 행사 이야기 · 운영 지역 · 포트폴리오) |

애니메이션: `kb`(히어로 7초 확대→원래), `up`(글자 순차 0.3/0.45/0.6/0.75s), `fill`(점 진행 6s), `hint`(스크롤 선), `fade`(탭 패널).
