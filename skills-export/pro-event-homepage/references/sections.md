# 섹션 구성과 인터랙션 — index.html · assets/app.js

## 섹션 순서 (index.html)

| # | 요소 / id | 행 | 내용 | 메뉴 노출 |
|---|---|---|---|---|
| 0 | `#curtain` `.grain` `#cursor` `.progress` | 23~29 | 커튼 인트로(로고 + SINCE 2006 + 그라데이션 막대), 질감, 커서 빛, 스크롤 진행 막대 | — |
| 1 | `header.nav#nav` + `.sheet#sheet` | 32~61 | 로고, 메뉴 7(회사소개·사업분야·포트폴리오·행사시스템·섭외·블로그·견적문의), 전화 알약, 견적 단추, 햄버거. 폰 시트는 10항목(+자동 견적서·행사 이야기·운영 지역·블로그) | — |
| 2 | `section.hero` (`main#top` 첫 칸) | 65~121 | 배경 영상(`#heroVideo`) + 포스터, 어둠막, 격자, 빛줄기, eyebrow, h1 「특별한 시간을 위한 / 탁월한 선택.」(낱말마다 `.w>span --i`), 리드, CTA 2, 숫자 4(2006 · 729회 · 20,000명 · 60+), 실적 티커(11개), 오른쪽 세로 문구 `NOW SHOWING · REAL FOOTAGE`, SCROLL, 재생/정지 단추 `#sound` | — |
| 3 | `section.clients` | 124~131 | TRUSTED BY + 고객 이름 18개 마퀴(`#clientTrack`) | — |
| 4 | `#about` | 134~159 | 「다르게 생각하고, 다르게 접근하고, 다르게 만든다.」(`.hl` 밑줄이 그려짐), 대표 서명, 카운터 카드(20년 · 729회 · 20,000명 + w13 사진), 회전 궤도 `.orbit` | 회사소개 |
| 5 | `#business` | 162~196 | 사업분야 8: 목록 `#bizList`(li 의 `data-img` `data-en` `data-desc`) + 무대 `#bizStage` | 사업분야 |
| 6 | `#works` | 199~216 | 필터 6(전체·대형행사·기업행사·지자체 · 관공서·체육대회·기공식 · 의전) + `#worksGrid`(JS 가 그림) + 행사 이야기/운영 지역 단추 | 포트폴리오 |
| 7 | `#process` | 219~234 | 5단계(CONSULT→PLAN→PRODUCE→ON SITE→WRAP UP), 들어오면 선이 채워지고 점이 차례로 켜짐 | (없음) |
| 8 | `#system` | 237~265 | 음향·조명·무대 LED 카드 3(`data-tilt`, 배경 sys/h1_7·h2_4·h3_1) + 물품 대여 메모 | 행사시스템 |
| 9 | `#video` | 268~287 | 유튜브 4개(`data-yt`: NGP2fyARgCg 메인, NFvKmA4WinY, D-LITMRHWYw, G1nbTLEQdUE). 썸네일 클릭 시 iframe | (없음) |
| 10 | `#casting` | 290~310 | MC 문구 + 칩 6 + 카드 5(라인업 60+, 전문 MC 8인 이름, 개그맨·가수·강사) | 섭외 |
| 11 | `#contact` | 313~350 | 연락 방법 4(서울본사 전화, 대표 직통, 자동 견적서, 네이버 블로그) + 문의 폼 `#quoteForm`(이름·연락처 필수, 기관, 유형 9, 날짜, 인원, 내용, 개인정보 동의) + 완료 덮개 `#formDone` | 견적문의 |
| 12 | `footer.footer` | 354~380 | 로고·소개·SNS 4(네이버 블로그·유튜브·인스타·페이스북), OFFICE, COMPANY(사업자번호·설립일), `.ftl` 링크 줄, 저작권 | — |
| — | `#totop`, `#lb` 라이트박스 | 382~390 | | — |
| — | `<script src="assets/app.js?v=20261004">` | 392 | | — |

캐시 무효화: `style.css?v=9`, `app.js?v=20261004` — 고치면 숫자를 올린다(생성 페이지는 index.html 머리를 그대로 빌리므로 생성기 재실행).

## 인터랙션 목록 (assets/app.js)

| 기능 | 행 | 동작 | 조건 |
|---|---|---|---|
| 문의 전송처 상수 | 13~15 | `FORM_ENDPOINT`(공용 문의 서버), `SMS_TO`(대표 직통), `COMPANY` | — |
| 커튼 | 18~21 | `load` 뒤 700ms 에 `.done`(위로 올라감), 늦어도 1900ms 에 강제 | — |
| 커서 빛 | 24~30 | 포인터를 .12 비율로 따라감(rAF), 520px 원 중심 맞추기(-260) | fine && !reduce |
| 스크롤 상태 | 33~46 | 진행 막대 scaleX, 40px 넘으면 `.nav.on`(블러 바탕), 900px 넘으면 맨위로 단추, 화면 40% 지점 기준 현재 섹션 메뉴 `.act` | — |
| 모바일 메뉴 | 49~54 | 햄버거 → `.sheet.on` + body 스크롤 잠금, 링크 누르면 닫힘 | — |
| 히어로 영상 | 57~73 | 화면폭×DPR(최대 2) 로 파일 선택: <900 `hero_sm`, <1300 `hero_md`, 그 외 `hero`. muted 강제, `play()` 재시도: canplay·첫 pointerdown·IntersectionObserver 재진입·이유 없는 pause 시 최대 8번(사용자가 멈춘 건 `data-userPaused` 로 존중) | — |
| 히어로 시차 | 74~88 | 스크롤 시 영상 translateY(y·.25), 글 묶음 투명해짐. h1 이 포인터 반대로 최대 14/10px | !reduce, h1 은 fine |
| 마퀴 복제 | 91 | `#tickerTrack` `#clientTrack` innerHTML 두 번 | — |
| 등장 | 94~97 | `.reveal, .line-draw, [data-hl]` → `.in` (rootMargin 아래 -10%) | — |
| 숫자 카운터 | 100~108 | `[data-count]` 60% 보이면 1.8초, ko-KR 쉼표(`data-plain` 은 생략) | reduce 면 즉시 |
| 자석 단추 | 111~114 | `[data-mag]` | fine && !reduce |
| 사업분야 무대 | 117~149 | 사진 미리 읽기. PC: hover 로 무대 이미지 2장 교차 + 캡션 교체. 터치 PC: 첫 탭은 선택만. **900px 이하: 탭하면 그 항목 아래 `.biz-inline`(사진+설명+「이 행사 견적 문의 →」), 다시 탭하면 접힘.** `matchMedia` change 대응 | — |
| 포트폴리오 데이터 | 152~171 | `WORKS` 18개: `{i: 사진번호, t: 제목, o: 기관, n: 인원(0이면 배지 없음), c: 분류(공백 구분 big/corp/gov/sport/cer), s: 크기 big/wide/'', y: 연도}` | — |
| 업로드 사진 합치기 | 173~204 | `photos` 브랜치의 `photos/photos.json`(raw.githubusercontent, 5분 단위 캐시 키) 을 읽어 **앞에** 붙임. 사진은 jsDelivr `gh/brizymedia/pro-event@photos/`. 분류 `UP_CAT`(big·corp·gov·sport·cer·etc) | 실패해도 조용히 무시 |
| 필터 | 179~182, 205~209 | `data-c` 에 필터값이 없으면 `.hide` | — |
| 라이트박스 | 211~219 | 카드 클릭 → `#lb.on`, 보이는 카드만 이전/다음, Esc·←·→, 바깥 클릭 닫기 | — |
| shine | 191~193 | `--mx --my` CSS 변수 | fine && !reduce |
| 프로세스 선 | 223~224 | 40% 보이면 `#steps.in` | — |
| 카드 기울임 | 227~230 | `[data-tilt]` rotateX ±3°, rotateY ±4° | fine && !reduce |
| 유튜브 | 233~241 | 클릭 시 `youtube-nocookie.com/embed/<id>?autoplay=1&rel=0&modestbranding=1` iframe. maxres 썸네일 404 면 hqdefault 로 | — |
| 문의 폼 | 244~267 | 이름·연락처·동의 검사 → JSON 을 `text/plain` 으로 POST(서버는 `page` 주소의 레포 이름으로 회사 구분). 응답 `ok` 일 때만 완료. 아니면 `local()`: 폰은 `sms:` 앱(본문 채움, iOS `&body` / 안드로이드 `?body`), PC 는 클립보드 복사 + 대표 직통 안내 | — |
| 관리자 모드 링크 | 271~282 | 모든 페이지 `footer` 끝에 자물쇠 + 「관리자 모드」 → `office.html`(스크립트 주소에서 상대 경로 계산) | — |

## 포트폴리오 사진 번호 ↔ 내용 (WORKS, 대문 표시 순)

w13 국회 개방행사(big) · w9 삼성 모바일디스플레이 페스티벌 · w8 SK하이닉스 대축제 · w11 국회 에어바운스 놀이존 · w12 광주 어린이날 · w14 WATER BOM · w2 말레이시아 장관 기공식(wide) · w19 공기업 오징어게임 체육대회(wide) · w16 KAID 송년회(big) · w6 현대산업개발 체육대회 · w7 삼성전자 중국사원 체육대회 · w10 경기도 소방학교 체육대회 · w3 제22회 춘천시 양성평등대회 · w15 춘천시 양성평등 송년회 · w4 교육부 비대면 20차수(wide) · w1 SK하이닉스 어린이날(wide) · w17 강서가족지원센터 송년회(wide) · w18 총동문회 체육대회(wide).
w5 는 WORKS 에 없다(파일은 있음).

## 사업분야 사진 출처 (README 그대로)

b1 삼성 페스티벌(w9) · b2 소방학교(w10) · b3 광주 어린이날(w12) · b4 강서 간담회(w17) · b5 학교행사 게시판 s3(운동장 단체) · b6 slide01 80.5s 프레임 · b7 워터밤 야간 무대(w14) · b8 국회 에어바운스 와이드(assembly/n06). **전부 프로이벤트 원본, AI 이미지 금지.**
