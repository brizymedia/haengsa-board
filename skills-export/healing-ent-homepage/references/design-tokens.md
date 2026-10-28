# 디자인 토큰 · 컴포넌트 (assets/style.css 782줄, ?v=24)

파일 머리 주석: 「화이트 + 블루 기본, 오렌지 · 옐로 포인트. 어두운 배경 · 네온 없음. 글꼴: Noto Sans KR(본문 · 제목) + Outfit(숫자 · 영문)」

## 1. 색 (`:root`)

| 토큰 | hex | 쓰임 |
|---|---|---|
| `--blue` | `#1B5CF2` | 주 색 · 버튼 `.btn-pri` · 링크 · 강조 글자 · theme-color |
| `--blue2` | `#3D8BFF` | CTA 띠 그라데이션 끝 |
| `--blue-d` | `#1448C8` | 파란 버튼 hover |
| `--navy` | `#132F6B` | 제목 · 진한 글자 · 히어로 무대 바탕(영상 전) · 행사 이야기 옆 상자 |
| `--ink` | `#1A2440` | 본문 글자 |
| `--sub` | `#56627E` | 보조 글자 |
| `--sky` | `#EEF4FF` | 아이콘 바탕 · `.sec.sky` |
| `--sky2` | `#F6F9FF` | `.sec.tint` · 바닥글 바탕 |
| `--line` | `#DCE5F5` | 테두리 |
| `--or` | `#FF8A1E` | 포인트 버튼 `.btn-or`(빠른 견적) · 현재 메뉴 점 · 밑줄 |
| `--or-d` | `#E8730A` | 오렌지 hover · 노랑 바탕 위 아이콘 |
| `--ye` | `#FFC23A` | 히어로 거대 숫자 「20」 · 점 장식 |
| `--ye-l` | `#FFF4D6` | 제목 `<em>` 형광 밑줄 · 전화 아이콘 바탕 |

기타: `--r:18px` `--r-s:12px` `--sh:0 10px 30px rgba(27,92,242,.10)` `--sh2:0 18px 48px rgba(19,47,107,.16)` `--hd:72px`(폰 62px).
`.svc5` 카드 테두리 `#7F9DD6`, 번호 `#94ABD8`. 카톡 단추 `#FEE500`/`#3C1E1E`.

업무 화면(port_docs 변환) 색: 바탕 `#0C1838`, 카드 `#132F6B`, 포인트 `#FF8A1E` · `#FFB066` · `#E8730A` · `#B85A06` · `#FFC98F`
(큰길 원본 `#F59E0B → #FF8A1E` 처럼 `COLORS` 표로 1:1 치환). 관리자 잠금(admin-lock.js · admin_gate.py)도 같은 남색 + 오렌지.

블로그(build-blog.mjs 안 CSS): `--acc #1B5CF2` `--acc-ink #1448C8` `--or #FF8A1E` `--ink #1A2440` `--navy #132F6B` `--txt #2A3450`
`--muted #56627E` `--dim #8A94AB` `--line #DCE5F5` `--bg2 #F3F7FF`, 남색 sticky 상단 바(56px).

## 2. 글꼴

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
```
`--ko:'Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif` (body) · `--en:'Outfit',system-ui,sans-serif` (숫자 · 영문 eyebrow · 전화번호).
body: 16px(폰 15.5px), line-height 1.65, `word-break:keep-all; overflow-wrap:break-word`.
제목: `.sh h2/.h2` `clamp(28px,3.6vw,42px)` 800 navy · 히어로 「20」 `clamp(140px,14.5vw,210px)` Outfit 800 노랑(폰 128px) · `.ph-head h1` `clamp(32px,4.2vw,50px)` 900.
로고 SVG 글자는 Outfit · Noto Sans KR 을 패스로 바꿔 넣었다(폰트 없이도 같게 보임).

## 3. 반응형 기준 (max-width)

| 폭 | 바뀌는 것 |
|---|---|
| 1320 | 머리 간격 · 메뉴 여백 줄임 (메뉴 9개 한 줄 유지) |
| 1180 | 머리 전화번호 글자 숨김(아이콘만), 메뉴 15px |
| 1120 | 메뉴 14.5px · 여백 7px |
| **1024** | 메뉴 · 전화 · 빠른 견적 숨김 → **햄버거 + 시트**, 서비스 5칸 → 3+2, 카드 2열, MC · 신뢰 · 문의 그리드 1열, 진행 2열, 바닥 2열, `.ph-head` 사진 숨김 |
| 960 | 행사 이야기 · 지역 페이지 1열, 옆 상자 static |
| **760** | **폰**: `--hd:62px`, wrap 좌우 16px, `.sec` 72px, 히어로 무대 둥근 22px · 덮개는 아래→위 그라데이션, 숫자 2개만(`.org` 숨김), 서비스 2열(마지막 전체폭), **하단 고정 4단추 `.quick`**(전화 · 카톡 · 문자 · 빠른 견적, body 아래 70px 여백) |
| 600 | 이야기 카드 1열, 지역 행 2열 |
| reduced-motion | 애니메이션 끔 · 영상 대신 포스터 |

## 4. 핵심 컴포넌트 클래스

- 버튼 `.btn`(52px 알약, 굵게) + `.btn-pri`(파랑) `.btn-or`(오렌지) `.btn-line`(흰 바탕 테두리) `.btn-glass`(흰색, 히어로) `.btn-white` `.btn-sm`.
- 머리 `.hd`(sticky, 반투명 흰색 + blur, 스크롤하면 `.stuck` 테두리 · 그림자) · `.logo img` 44px · `.menu a.act::after` 오렌지 점 · `.tel` · `.hbtn` · `.burger(.x)` · `.sheet(.on)`.
- 섹션 `.sec`(110px) `.tint` `.sky` · 머리줄 `.sh`(좌 제목 / 우 설명 · 더보기, `.center`) · `.eyebrow`(영문 대문자 + 오렌지 · 옐로 점 두 개) · `.more`(화살표 링크).
- 등장 `.rv` → `.in` (아래에서 26px), 지연 `.d1~.d4`(0.08s 간격). 히어로는 `.hx` 로 스크롤 없이 바로 등장.
- 히어로 `.hero .stage`(margin 14px, 둥근 30px, min-height `clamp(600px, 100svh - 머리 - 50px, 880px)`) · `.screen video/.poster`(처음 1.14배에서 줄어듦) ·
  `.screen::after` 파란 덮개(왼쪽 짙게 `rgba(15,44,120,.88)` → 오른쪽 투명) · `.live`(「REAL EVENT · 실제 행사 현장」, 깜빡이는 오렌지 점) · `.play`(재생/정지) ·
  `.kick`(유리 알약) · `h1 .yr b`(거대 「20」) · `.ln.nm`(회사 이름 아래 오렌지 밑줄이 그어짐) · `.stats li`(유리 카드, 숫자 Outfit 36px, 단위 노랑) · `.cta`.
- 서비스 5칸 `.svc5`(히어로 아래 -84px 겹침, 2 · 4번째는 오렌지 윗줄 · 노랑 아이콘, 폰에서도 테두리 · 화살표가 늘 보이게).
- 키워드 띠 `.marq .track`(JS 가 내용을 두 번 이어 붙임).
- 카드 `.cards .card(.wide)` · MC `.mc .pic .main.face` + `.name` + `.certs.all` · 대표 실적 맛보기 `.sigt a`(배경 사진 4칸) ·
  강점 `.why article`(번호 · 아이콘) · 진행 `.steps li` · 갤러리 `.gal.home` / `#pfGrid` + 필터 `#filters [data-f]` · 라이트박스 `.lb` ·
  신뢰 `.trust .facts` + `.stories .story` · 영상 `.vids`(`.ypromo` 홍보영상 + `.ytc` 채널 카드) `.vgrid` `#vfilters` · 공지 `.duo .box .nlist` ·
  문의 `.contact .ways` `.form.qform`(`.types` 라디오 알약, `.done` 접수 화면) · FAQ `.faq` · 서브 머리 `.ph-head`(`.crumb` `.subnav` `.pimg` + 노랑 네모 장식) ·
  CTA `.band .in`(파랑 그라데이션 + 노랑 · 오렌지 큰 원) · 바닥 `.ft .top/.sns/.ftl/.bot` · `.quick` · `.totop` · `.skip`(본문 바로가기).
- 행사 이야기 · 지역: `.sstory`(300px 남색 옆 상자 + 본문) `.sgrid` `.scards(.big/.sm) .scard` `.area3` `.alist`(오렌지 마름모) `.apics` `.asvc` `.arows .arow`(지역 · 이동 시간 · 기록).
