# 업무 화면 — 흐름과 상태 저장

이 화면들은 **큰길이벤트기획 원본 레포에서 `python tools/port_docs.py` 로 옮겨 온 결과물**이다(README 「업무 도구」).
손으로 고치면 다음 포팅 때 사라진다 → 회사별 차이는 `tools/port_docs.py` 「회사 설정」 칸이나 `*_extra()` 규칙으로 넣는다.
(바로기획이 기준본, 큰길이벤트 레포가 실제 복사 원본 — README·port_docs 주석 표현 그대로)

## 한눈에

```
손님: 대문 문의 폼 ─┐
손님: quote.html ───┴→ 공용 문의 서버 → 대표 메일 + 큰길브리지 (실패 시 FormSubmit / 문자·복사)

대표: office.html (관리자 모드, 대표 암호)
  ├ quote.html?admin=1   견적 작성 → 저장함(#q= 코드) ─┬→ contract.html?admin=1#c=…  → 서명 링크 → 손님 서명 → PDF·메일·대장
  │                                                     ├→ statement.html?admin=1#t=…  → 인쇄/PDF
  │                                                     └→ schedule.html#new=…         → 일정·체크리스트(직원과 공유)
  └ upload.html  현장 사진 → photos 브랜치 → 대문 포트폴리오 앞에 합쳐 보임 + 블로그·인스타 글 초안
```

## 화면별

| 화면 | 주소 | 잠금 | 상태가 사는 곳 | 서버 |
|---|---|---|---|---|
| 자동 견적서(손님) | `quote.html` | 없음 | 주소 `#q=<코드>` (`?q=` 로 와도 `#q=` 로 바꿈), `?sent=1` 보낸 뒤 화면 | 공용 문의 서버, 실패 시 `formsubmit.co/ajax/<메일>` |
| 견적서 발행·저장함 | `quote.html?admin=1` | `admin-lock.js` (대표 암호) | 저장함 localStorage `pro-quote-box-v1`(최대 50), 암호 `pro-quote-box-pw`. 암호가 있으면 계약 서버 `boxList/boxPut/boxDel` 로 폰·PC 목록 합침 | 계약 서버 |
| 전자계약서 | `contract.html?admin=1` (작성) · `contract.html?c=<ID>&s=<배포ID>` (손님 서명) · `?preview=1#c=` (예시, 서명 안 받음) | 작성 화면만 잠금 | 작성 중 `#c=<packState>` 자동 저장, 회사 기본값 localStorage `kg_contract_co`. 서명 후 원문은 서버 드라이브 `_data/ID.json` | 계약 서버 `store` / `GET ?id=` / `sign`. 서버 실패 시 긴 링크(`#c=`)+문의 서버로 서명 정보 |
| 거래명세서 | `statement.html?admin=1` | 잠금 | `#t=<b64>` (견적 `#q=` 링크·코드 붙여넣기도 됨), 입금 계좌 localStorage `kg_stmt_bank` | 없음 |
| 행사 일정·체크리스트 | `schedule.html` (`#new=` 견적에서 넘어옴, `#e=<id>` 행사 열기) | 화면 안 암호(보관함 암호 = 전부, 직원 암호 `CREW_PW` = 일정만) | 암호 `pro-sched-pw`, 이름 `pro-sched-who`. 데이터는 서버 `_data/행사일정.json`(최대 300) | 계약 서버 `schedList/schedSave/schedCheck/schedDel` |
| 사진 올리기 | `upload.html` | 업로드 암호(`UPLOAD_PW`, 서버가 확인) | localStorage `pro_pw` `pro_srv` `pro_cat` `pro_ev` | 갤러리 서버 `photo/cover/finish/edit/delete` |
| 업무 문서함 | `office.html` (공개 링크는 바닥글 「관리자 모드」뿐) | `tools/admin_gate.py` 잠금(대표 암호를 계약 서버 `boxList` 로 확인). 열면 sessionStorage `pro-office`=1 | 서버 연결 상태 표시(계약 서버 `box`/`sched` ready, 갤러리 `설정완료`) | — |

공통 규칙
- 서버로 보내는 모든 요청은 `fetch(URL, {method:'POST', headers:{'Content-Type':'text/plain;charset=utf-8'}, body: JSON.stringify(…)})` — Apps Script CORS preflight 를 피하려고 text/plain.
- 응답 `{ok:true}` 일 때만 성공으로 친다. 아니면 반드시 대체 경로(문자 앱·복사·긴 링크)로 간다.
- 암호는 코드에 없다. 서버 스크립트 속성(`BOX_PW` `CREW_PW` `UPLOAD_PW`)에만. 기기에는 localStorage 로 기억.
- 관리자 암호를 한 번 맞히면 `pro-quote-box-pw` 에 저장되고, `pro-sched-pw` 가 비어 있으면 같이 채운다(admin-lock.js·admin_gate.py).

## 견적서 (quote.html)

- 품목표는 `quote-catalog.js` 의 `CATALOG`(그룹: 행사 기획 · 진행 / 음향 / 조명 · 무대 · LED / 천막 · 테이블 / MC · 공연 · 강사 섭외 / 체험 · 놀이 / 기타). **모든 `price:null`** — 금액은 협의라 손님 화면에 금액이 안 나온다. 품목을 고칠 곳은 `tools/port_docs.py` 의 `CATALOG` 문자열(포팅 때 덮어쓰기).
- 견적 코드: 견적 하나 = `#q=` 뒤 짧은 코드. 줄은 id 문자열(카탈로그 그대로) 또는 배열 `[id, 수량, 일수, 단가]`, 완전형 `[id, name, spec, qty, unit, days, price]`. 푸는 함수는 quote-catalog.js 에 있고 schedule 도 같은 것으로 읽는다.
- 손님 화면(`admin=1` 없음): 직인·품목명·규격·단위·단가·할인·인쇄를 막는다(비교견적 악용 방지 — quote.html 926행 주석).
- 관리자 단추: 「이 견적으로 계약서 작성」(`contract.html?admin=1#c=` 완전형, 번호 `PR-YYYYMMDD-XXX`), 「거래명세서 작성」(`#t=`, 할인은 음수 줄), 「행사 체크리스트로」(`schedule.html#new=`), 메일 보내기(폰은 메일 앱, PC 는 Gmail 쓰기 창).
- 문의 전송 순서: 공용 문의 서버 → 실패 시 FormSubmit → 그래도 실패면 confirm 으로 다른 방법 안내.
- 이 페이지만 `<meta name="robots" content="index,follow">` (대문은 noindex 시안인데 손님용 견적서는 색인 허용 — port_docs `quote_extra` 주석).

## 전자계약서 (contract.html)

- 계약 종류: 행사 대행(우리가 을, 고객이 갑) / 출연 섭외(우리가 갑, 출연자가 을). 출연자 개인은 3.3% 원천징수, 사업자는 부가세 10%. 미성년 출연자는 법정대리인 종이 서명란.
- 우리는 늘 날인(`assets/img/stamp-pro.png`, 없으면 「(인)」 — 가짜 도장을 그리지 않음), 상대는 늘 링크 전자서명.
- 서명 시: 서명 이미지 잘라 600px, 문서 SHA-256, 서버가 PDF 생성 → 드라이브 `프로이벤트 계약서/연도/` 저장 → 회사·고객·관리자 메일 → 스프레드시트 「계약 대장」.
- 손님 링크의 `&s=<배포ID>` 로 서버 주소를 복원하므로 손님 기기는 설정이 필요 없다.

## 행사 일정 (schedule.html)

- 월간 일정표 + 행사 카드 + 품목 체크리스트. 여러 날 행사는 끝날 없으면 하루짜리.
- 체크는 `schedCheck` 로 그 항목만 바꿔 직원끼리 덮어쓰지 않게, 글자는 칸을 벗어나면 저장. 품목을 안 건드렸으면 저장 때 빼고 보낸다.
- 「저장해 둔 견적서에서 가져오기」(741행~) 와 견적서에서 넘어온 새 행사(811행~).

## 사진 올리기 (upload.html)

- 갤러리 항목 6(`big corp gov sport cer etc` — 대문 포트폴리오 필터와 같은 이름, port_docs `UPLOAD_CATS`). 지역 찾기 표 `UPLOAD_REGIONS`.
- 사진은 브라우저에서 긴 변 1600px, JPEG 품질 0.82 로 줄이고, 체크 시 오른쪽 위 「프로이벤트」 워터마크. 원본은 휴대폰에만 남는다(드라이브 안 씀).
- 대표 썸네일 2장(정사각 1080×1080, 가로 1200×630, 품질 0.88)은 원본에서 잘라 워터마크를 한 번만 찍는다.
- 순서: `photo`(장마다) → `cover` → `finish`(photos.json 갱신, 실패분은 다음에 먼저 재전송). `edit` 은 항목 옮겨도 파일은 안 옮기고 cat 값만 바꿈.
- 올린 뒤 블로그 제목 후보·본문·인스타 글을 만들어 준다(1047행~).
- 대문 반영: `app.js` 가 photos 브랜치 `photos/photos.json` 을 읽어 WORKS 앞에 붙임(raw.githubusercontent 캐시 때문에 1~5분).

## 회사 설정을 바꿀 때 (tools/port_docs.py)

`ID='pro'`(기기 저장 키 앞글자·`data-site`), `NAME`, `CEO`, `BIZNO`, `ADDR`, `TEL`, `EMAIL`, `REPO`, `HOME`, `CODE_PRE='PR-'`, `BLOG`, `CONTRACT_URL`, `GALLERY_URL`, `LOGO_FILE`, `MAIL_LOGO`, `STAMP`, `COLORS`, `OFFICE`(문서함 색), `EXAMPLES`(입력칸 예시 문구), `CATALOG`, `UPLOAD_CATS`, `UPLOAD_REGIONS`.
실행: `python tools/port_docs.py <큰길이벤트 레포 경로>` — 끝에 파일마다 「남은 큰길 흔적」(`TRACES`)을 출력하니 「없음」인지 볼 것. 원본 레포가 없으면 돌릴 수 없다(이 레포만으로는 업무 화면 재생성 불가).
