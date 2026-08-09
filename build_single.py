# -*- coding: utf-8 -*-
"""미리보기.html 한 파일로 합치기

site/ 의 세 페이지와 CSS·JS·데이터를 문서 하나에 심는다.
file:// 에서는 브라우저가 fetch 로 events.json 을 읽지 못하므로,
더블클릭만으로 열리는 단일 파일이 필요할 때 쓴다.

  python build_single.py        # → 미리보기.html
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")


def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()


def content_of(page):
    """<!-- content:이름 --> … <!-- /content --> 사이를 뽑는다."""
    html = read(SITE, page)
    m = re.search(r"<!-- content:(\w+) -->\n?(.*?)\n?<!-- /content -->", html, re.S)
    if not m:
        raise SystemExit(f"{page} 에서 content 표식을 찾지 못했습니다.")
    return m.group(1), m.group(2)


def main():
    data_path = os.path.join(SITE, "data", "events.json")
    if not os.path.exists(data_path):
        raise SystemExit("site/data/events.json 이 없습니다. 먼저 실행하세요: "
                         "cd collector && python mockgen.py")
    data = json.load(open(data_path, encoding="utf-8"))

    css = read(SITE, "assets", "style.css")
    js = read(SITE, "assets", "app.js")

    sections = []
    for page in ("index.html", "calendar.html", "about.html"):
        name, body = content_of(page)
        if name != "board":
            # id 는 문서당 하나만 — 달력 쪽 #genAt·#total·#mockflag 를 제거한다
            body = re.sub(r'\s+id="(genAt|total|mockflag)"', "", body)
        hidden = "" if name == "board" else " hidden"
        sections.append(f'<section data-view="{name}"{hidden}>\n{body}\n</section>')

    payload = json.dumps(data, ensure_ascii=False)
    out = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>행사 고시 알림판 — 미리보기</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>
{css}
.nav a{{cursor:pointer}}
section[hidden]{{display:none}}
</style>
</head>
<body data-page="single">

<div class="masthead">
  <div class="wrap">
    <div class="masthead-in">
      <a class="brand" data-go="board">
        <span class="mark">행사 고시 알림판</span>
        <span class="sub">전국 지자체 공고 수집</span>
      </a>
    </div>
    <nav class="nav">
      <a data-go="board">알림판</a>
      <a data-go="calendar">축제 달력</a>
      <a data-go="about">이용안내</a>
    </nav>
  </div>
</div>

{chr(10).join(sections)}

<script>
// 수집 데이터를 문서에 심는다 (file:// 에서는 fetch 가 막히기 때문)
window.__EVENTS__ = {payload};
</script>
<script>
{js}
</script>
</body>
</html>
"""
    dest = os.path.join(HERE, "미리보기.html")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"미리보기.html 생성 ({data.get('count', 0)}건"
          + (", 예시 데이터" if data.get("mock") else "") + ")")


if __name__ == "__main__":
    main()
