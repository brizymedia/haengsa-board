# 행사 고시 알림판

전국 지자체가 공개한 **행사 관련 입찰공고·축제 일정·고시**를 하루 한 번 모아
보여주는 독립 사이트입니다. 기존 홈페이지와 분리해 단독으로 운영합니다.

```
나라장터 API ─┐
TourAPI     ─┼→ 분류·지역판정·중복제거 → SQLite → events.json → 정적 사이트
지자체 RSS   ─┘
```

백엔드 서버가 필요 없습니다. 배치가 JSON 파일 하나를 갱신하고,
사이트는 그 파일만 읽습니다.

---

# GitHub에 올려 실제로 띄우기

서버를 따로 두지 않아도 됩니다. GitHub Actions가 매일 새벽 5시에 공고를 수집하고
GitHub Pages로 배포합니다. **무료입니다.**

## 1단계 — 저장소 만들기

GitHub에서 새 저장소를 만듭니다. 이름은 예를 들어 `haengsa-board`.
README·gitignore·라이선스는 **추가하지 마세요**(이미 들어 있습니다).

## 2단계 — 올리기

이 폴더에서 아래를 실행합니다. `내계정`과 저장소 이름만 바꾸세요.

```bash
git remote add origin https://github.com/내계정/haengsa-board.git
git push -u origin main
```

> 이미 `git init` 과 첫 커밋까지 되어 있습니다. 위 두 줄이면 끝입니다.
> 비밀번호를 물으면 GitHub 계정 비밀번호가 아니라
> **개인 액세스 토큰(Settings → Developer settings → Personal access tokens)** 을
> 넣어야 합니다.

## 3단계 — Pages 켜기

저장소 **Settings → Pages → Build and deployment → Source** 를
**GitHub Actions** 로 바꿉니다. (기본값인 "Deploy from a branch" 아니면 동작하지 않습니다.)

## 4단계 — API 키 등록

저장소 **Settings → Secrets and variables → Actions → New repository secret**

| 항목 | 값 |
|---|---|
| Name | `DATA_GO_KR_KEY` |
| Secret | 공공데이터포털에서 발급받은 **Decoding 키** |

키가 아직 없다면 data.go.kr 에서 아래 둘을 **활용신청**하세요. 무료이고 즉시 승인됩니다.

| 서비스명 | 용도 |
|---|---|
| 조달청_나라장터 입찰공고정보서비스 | 행사 대행 용역 발주 공고 |
| 한국관광공사_국문 관광정보 서비스 | 전국 축제·행사 일정 |

마이페이지에서 **Decoding 키**를 복사합니다. Encoding 키를 넣으면 동작하지 않습니다.

키를 등록하지 않아도 배포는 됩니다. 다만 **예시 데이터**로 표시되고
Actions 로그에 경고가 남습니다. 키를 넣은 뒤 다시 실행하면 실제 공고로 바뀝니다.

## 5단계 — 확인

**Actions** 탭에서 "수집 및 배포"가 초록색으로 끝나면
`https://내계정.github.io/haengsa-board/` 에서 열립니다. 첫 배포는 1~2분 걸립니다.

이후에는 **매일 새벽 5시(한국시간)에 자동으로** 최신 공고를 수집해 갱신합니다.
바로 돌려보고 싶으면 Actions 탭 → "수집 및 배포" → **Run workflow**.

### 잘 안 될 때

| 증상 | 확인할 것 |
|---|---|
| Actions가 아예 안 돎 | Pages Source가 **GitHub Actions** 인지 |
| "예시 데이터" 배지가 계속 뜸 | 시크릿 이름이 정확히 `DATA_GO_KR_KEY` 인지 |
| 배포는 됐는데 404 | 주소 끝에 저장소 이름과 `/` 가 붙었는지 |
| 수집 0건으로 실패 | Decoding 키인지(Encoding 키 아님), 두 API 모두 활용신청했는지 |

---

## 그냥 화면부터 보고 싶다면 (웹서버 없이)

```bash
cd collector && python mockgen.py    # 예시 데이터 121건 생성
cd .. && python build_single.py      # 미리보기.html 한 파일로 합치기
```

만들어진 **`미리보기.html`을 더블클릭**하면 바로 열립니다. CSS·자바스크립트·데이터가
모두 그 안에 들어 있어서 파일 하나만 있으면 되고, 남에게 보여줄 때도 이것만 보내면
됩니다.

> `index.html` 하나만 열면 글자만 나옵니다. 스타일·기능·데이터가 별도 파일이라
> 따라오지 않고, 브라우저는 `file://` 에서 보안 정책상 `events.json` 을 읽지
> 못하기 때문입니다. 폴더째 쓰려면 아래 `serve.py` 로 여세요.
>
> 미리보기 파일은 데이터가 박제되어 있어 배치가 갱신해도 바뀌지 않습니다.
> **실제 운영은 `site/` 폴더를 올리는 방식**입니다.

## 서버로 띄워 보기

```bash
python serve.py             # http://localhost:8000
```

예시 데이터로 도는 동안에는 화면 상단에 붉은 **"예시 데이터로 표시 중"** 표시가
뜹니다. 실제 API를 연결하면 자동으로 사라집니다.

## 내 PC에서 실제 데이터로 돌려보기

GitHub Actions가 알아서 하므로 꼭 필요하진 않습니다. 키워드를 다듬을 때 유용합니다.

```bash
pip install -r requirements.txt
export DATA_GO_KR_KEY="발급받은_Decoding_키"

cd collector
python tests.py       # 분류 로직 점검 (30개 항목)
python run.py         # 실제 수집 → ../site/data/events.json 갱신
```

## GitHub 말고 다른 곳에 올리려면

`site/` 폴더가 곧 사이트입니다. 정적 파일뿐이라 Netlify, Vercel, 카페24,
기존 웹호스팅 어디든 그대로 올라갑니다.

이 경우 수집은 별도 서버의 cron 으로 돌리고, 결과 `events.json` 만
`site/data/` 로 전송하면 됩니다.

```
0 5 * * * cd /srv/board/collector && /usr/bin/python3 run.py >> ../logs/run.log 2>&1
```

---

## 폴더 구조

```
collector/              배치 수집기
  config.py             API 키, 지역코드, 키워드 사전   ← 주로 여기를 손봅니다
  collectors/nara.py    나라장터 입찰공고
  collectors/tour.py    TourAPI 축제·행사
  collectors/rss.py     지자체 RSS (robots.txt 확인 포함)
  classify.py           행사 판정 · 지역 추출 · 중복 제거 · 정렬
  store.py              SQLite 저장 · JSON 내보내기
  run.py                실행 진입점
  mockgen.py            예시 데이터 생성 (운영 후 삭제 가능)
  tests.py              단위 테스트

site/                   정적 사이트 (이 폴더만 배포)
  index.html            알림판 — 검색·필터·정렬·페이지 이동
  calendar.html         축제 달력 — 월별
  about.html            이용안내 · 출처 · 저작권
  assets/style.css
  assets/app.js
  data/events.json      배치가 갱신

serve.py                로컬 미리보기 서버
build_single.py         미리보기.html 한 파일로 합치기
verify.py               브라우저 자동 검증 (24개 항목)
.github/workflows/      매일 수집 + Pages 자동 배포
```

## 검증

```bash
cd collector && python tests.py     # 수집기 로직
python serve.py &                   # 서버를 띄운 뒤
python verify.py                    # 브라우저 동작 (playwright 필요)
```

`verify.py`는 실제 크롬을 띄워 데이터 로드, 구분·지역 필터, 검색과
하이라이트, 세 가지 정렬, 페이지 이동, 빈 상태, 달력 이동, 모바일 레이아웃,
자바스크립트 오류까지 확인합니다.

---

## 손볼 곳

| 파일 | 항목 | 언제 고치나 |
|---|---|---|
| `config.py` | `EVENT_KEYWORDS` | 잡혀야 할 공고가 안 잡힐 때 |
| `config.py` | `EXCLUDE_KEYWORDS` | 엉뚱한 공고가 섞일 때 |
| `config.py` | `RSS_FEEDS` | 지자체를 늘리거나, 개편으로 주소가 바뀌었을 때 |
| `config.py` | `LOOKBACK_DAYS` | 소급 조회 기간 조정 |
| `classify.py` | `score()` | 노출 우선순위 조정 |
| `about.html` | 문의처 | 배포 전 반드시 |

운영 첫 2주는 `run.py` 출력의 상위 항목을 눈으로 보면서 키워드를 다듬으세요.
**이 튜닝이 서비스 품질의 대부분을 결정합니다.**

RSS 피드는 지자체가 홈페이지를 개편하면 조용히 죽습니다. 주기적으로 확인하세요:
```bash
cd collector && python -m collectors.rss --check
```

## 지켜야 할 선

- **본문 전재 금지.** 제목·기관·기간·링크까지만. RSS 요약은 200자에서 자릅니다.
- **공공누리 유형 확인.** 제1유형만 상업적 이용이 자유롭습니다. 제2유형(상업적
  이용 금지) 자료를 광고가 있는 페이지에 실으면 문제가 됩니다. RSS 수집분은
  `license`가 `확인 필요`로 들어가니 지자체별로 확인 후 채우세요.
- **robots.txt 준수.** `collectors/rss.py`가 확인하고 거부 시 건너뜁니다.
- **요청 간격 유지.** `REQUEST_DELAY`를 1초 미만으로 낮추지 마세요.
- **출처 표기.** 각 페이지 하단 고지와 `about.html`을 지우지 마세요.

## 알려진 한계

- 나라장터를 거치지 않는 소액 수의계약 공고는 잡히지 않습니다.
- 한국관광공사에 등록하지 않은 소규모 행사는 달력에 없습니다.
- 제목만으로 행사 여부를 판정하므로 드물게 오탐·누락이 있습니다.
- TourAPI 엔드포인트는 버전이 오르면 `KorService1 → KorService2`처럼 바뀝니다.
  호출이 갑자기 실패하면 `config.TOUR_BASE`부터 확인하세요.
