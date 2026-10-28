# 디자인 체계 — 이벤트와 교육연구소

출처: `assets/style.css` 머리 주석 「로고의 아치 · 산호 · 연두에서 출발한 디자인」. 이 파일은 손으로 고쳐도 된다(페이지 HTML 만 생성물).

## 색 토큰 (`:root`)

| 토큰 | 값 | 쓰임 |
|---|---|---|
| `--ink` | `#3D3938` | 글자, 어두운 섹션 · CTA 상자 · 띠 · 바닥글 · 히어로 뒤 바탕, 기본 단추 |
| `--soft` | `#6B6461` | 보조 글 |
| `--cream` | `#FFF9F1` | 페이지 바탕, theme-color, 900 이하 히어로 바탕 |
| `--sand` | `#F7EEE2` | `.sec.sand` 교차 섹션, `.phead` |
| `--white` | `#fff` | |
| `--line` | `rgba(61,57,56,.12)` | 카드 안쪽 선(`box-shadow:inset 0 0 0 1px`) |
| `--coral` | `#FA8A7A` | 아치 바깥 띠, 점, 따옴표, 포커스 |
| `--coral-ink` | `#C8432F` | 강조 글자 `.hl`, 주 단추 `.btn.coral`, 전화 단추, NEW 딱지 |
| `--coral-bg` | `#FFE9E4` | 꼬리표 `.eb` 바탕 |
| `--lime` | `#CFE5A3` | 아치 안쪽, 현재 메뉴, `.btn.lime`, 체크 동그라미 |
| `--lime-ink` | `#3F7A2A` | `.hl-l`, `.eb.lime` 글자 |
| `--lime-bg` | `#EEF6DC` | `.eb.lime` 바탕, 완료 상자 |
| `--sun` | `#F4A55A` | 포커스 테두리, 띠 점 |
| `--mint` `--sky` `--grape` | `#A8D8C4` `#8CC3EA` `#B79AE0` | 보조(색종이 등) |

토큰 밖에서 쓰는 값:
- 숫자 색: 2번째 `--lime-ink`, 3번째 `#C77A1F`, 4번째 `#2F78B5`. 연두 점 `#7DB55A`.
- 파스텔 카드 `--c`(build_site): `#FFD9D1` `#CFE5A3` `#FBD9A8` `#C9E6F7` `#E3D6F6` `#C7EBDD`. 핵심 가치 · 연표 `#FA8A7A` `#7DB55A` `#F4A55A` `#8CC3EA`.
- 색종이(app.js): `#FA8A7A #CFE5A3 #F4A55A #A8D8C4 #FFFFFF #F6C2C0`.
- 히어로 덮개: 행사 `rgba(250,138,122,.18) → rgba(168,52,32,.35) → rgba(61,28,22,.88)`, 교육 `rgba(207,229,163,.12) → rgba(63,100,40,.38) → rgba(30,48,22,.9)`.
- 카카오 단추 `#FEE500` / 글자 `#3a1d1d`. 그림자 `--shadow: 0 30px 60px -28px rgba(120,70,50,.28), 0 8px 22px -12px rgba(120,70,50,.14)`.

### 업무 화면 색 (port_docs.py)
- `OFFICE`: bg `#221E1D` · card `#2D2827` · line `rgba(250,138,122,.2)` · accent `#FA8A7A` · accent2 `#FFB09F` · ink `#2A1612`.
- `COLORS` 치환표(큰길 주황 → 이 회사): `#F59E0B→#FA8A7A` · `#FBBF24→#FFB09F` · `#D97706→#E8604F` · `#B45309→#C8432F` · `#FCD34D→#CFE5A3` · `#a05c00→#C8432F` · `#09090b`/`#0B0A10→#221E1D` · `#16141C`/`#131317→#2D2827` (+ 같은 rgba 계열).
- admin-lock.js 잠금 화면도 `#221E1D` / `#2D2827` / `#FA8A7A`.
- 수정 모드 막대(edit.js): 검정 `#111` 막대 + 노랑 `#FFE85C` 보내기 단추, 편집 칸 점선 `#E0A100`.

## 글꼴

```css
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css");
@import url("https://fonts.googleapis.com/css2?family=Jua&display=swap");
```
- `--display: "Jua", "Pretendard Variable", Pretendard, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif` — h1~h4(weight 400), 숫자, 띠, 폰 메뉴 큰 글씨, 서명, 전화 큰 글씨.
- `--body: "Pretendard Variable", Pretendard, …` — 본문 17px · line-height 1.75 · `word-break:keep-all; overflow-wrap:break-word`.
- 영문 대문자 꼬리표는 별도 영문 글꼴 없이 본문 글꼴 + `letter-spacing:.16em` 정도.
- 업무 화면 · office: `pretendard/dist/web/static/pretendard.min.css`(버전 없음).

## 크기 · 간격

| 항목 | 값 |
|---|---|
| `.wrap` | `width:min(1200px, 100% - 40px)` |
| `.sec` 위아래 | `clamp(72px,10vw,140px)` |
| `.h2` | `clamp(30px,4.6vw,56px)` · `.phead h1` `clamp(36px,6vw,76px)` · 히어로 h1 `clamp(29px,3.5vw,47px)` |
| 둥글기 | `--r-lg 32px` · `--r-md 22px` · 알약 999px |
| 이징 | `--spring: cubic-bezier(.32,.72,0,1)` |
| `scroll-padding-top` | 96px (떠 있는 머리글 아래로 앵커) |

## 반응형 기준

| 폭 | 바뀌는 것 |
|---|---|
| ≤1060 | 머리글 메뉴 · 전화 숨김 → 햄버거 `.mbtn`. 대상 카드 2열(마지막 카드 전체 폭) |
| ≤980 | 후기 2열, 교육 카드 2열, 포트폴리오 2열, 실적 지역 2열, 영상 2열 |
| ≤900 | 히어로 1열(아치 위, 사진 둘 아래), 문의 1열 |
| ≤860 | 두 파트 · 대표 · `.two` · 행사 블록 1열, 핵심 가치 1열, 바닥글 2열 |
| ≤760 | 숫자 2열, 갤러리 2열, 비전/미션 · 왜 우리 · 이력 · 회차 1열, **`.dock` 하단 고정 단추 + body 아래 84px** |
| ≤640 | 후기 1열, 교육 1열, 수정 모드 막대 줄바꿈 |
| ≤560 | 포트폴리오 · 실적 · 영상 1열, 폼 두 칸 → 한 칸 |
| ≤480 | 대상 카드 1열 |

`prefers-reduced-motion`: 모든 애니메이션 · 전환 끔, 색종이 · 시차 · 숫자 애니 생략(app.js).

## 컴포넌트

| 클래스 | 모양 |
|---|---|
| `.hdr .pill` | 떠 있는 알약 머리글(fixed top 14px, `rgba(255,249,241,.82)` + blur 18px). `.solid` 는 더 하얗게 |
| `.sheet` | 폰 전체 화면 메뉴(Jua 큰 글씨, 순차 등장) |
| `.hero` `.pane.ev/.ed` `.core .arch` | 2분할 히어로 + 세 겹 아치(산호 16px → 흰 14px → 연두) |
| `.confetti` `.scrollcue` | 떨어지는 색종이 · SCROLL 글자 |
| `.ticker` | 어두운 띠, Jua 19px, 항목 뒤 색 점(산호 · 연두 · 해), 42초 무한 |
| `.eb` (`.lime`) | 알약 꼬리표(점 + 대문자 영문) |
| `.sechead` | 꼬리표 + h2 왼쪽, 설명/단추 오른쪽 |
| `.btn` `.ar` | 알약 단추 + 둥근 화살표(hover 시 화살표가 오른쪽 위로) — coral · lime · line · white · sm |
| `.bz > .in` | 더블 베젤 카드(바깥 연한 테두리 8px + 안쪽 흰 카드) |
| `.stats .stat` | 숫자 카드(Jua 큰 숫자 + small 단위) |
| `.parts .part.ev/.ed` | 행사 · 교육 두 카드(흰→산호/연두 그라데이션, 16:9 사진, 칩) |
| `.aud a` | 대상 카드(오른쪽 위 파스텔 원이 hover 시 커짐) |
| `.ceo .pic .arch` | 아치 사진 틀(연두 바탕 + 산호 14px + 흰 28px 테두리) |
| `.gal figure(.w .t .s)` | 12칸 갤러리(w=6칸, t=3줄, s=3칸), hover 캡션 |
| `.rvs figure` | 후기 카드(큰 따옴표, `<mark>` 연두 형광펜) · `.shot` 캡처 |
| `.notes` | 공지 목록(날짜 92px + 제목 + NEW) |
| `.cta .box` | 어두운 CTA 상자 + 오른쪽 아래 산호 · 연두 반원 |
| `.ft` `.dock` `.lb` | 바닥글 · 하단 고정 상담 단추 · 라이트박스 |
| `.phead` `.crumb` | 서브 머리(모래 바탕 + 연두 원 + 산호 반원) |
| `.vm` `.vals .val` `.why` `.cvgrid .cvbox` `.tl` `.letter` | about · ceo 블록 |
| `.cat` `.tabs` `.ex` `.phw .thumbs` | event 블록(짝수 번째는 사진이 오른쪽) · sticky 탭(top 78px) · 구성 예시 상자 |
| `.edugrid .edu` `.steps3` `.vids .vid` | 교육 카드 · 회차 3단 · 영상 |
| `.filters` `.pf` `.later` `.empty` `.regions` | 포트폴리오 필터 · 카드 · 더 보기 숨김 · 빈 상태 · 실적 접이식 |
| `form.f` `.cgrid` `.side .card` `.faq` `.done` | 문의 폼 · 옆 카드 · FAQ · 완료 상자 |
| `.rv` `.in` `.d1~d4` | 스크롤 등장(`html.js` 일 때만 숨김) |

## 로고

이미지 로고다(CSS 로고 아님). 머리글 `logo-h.png` 높이 36px, 바닥글은 같은 PNG 를 흰 둥근 상자(`background:#fff; padding:8px 12px; border-radius:14px`) 위에. 업무 화면은 `favicon.png` 를 네모 마크로.
