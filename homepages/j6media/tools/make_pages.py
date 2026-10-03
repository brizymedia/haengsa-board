# -*- coding: utf-8 -*-
"""
행사 이야기(stories/) · 지역 페이지(areas/) 만들기 — 사이트 틀(머리글 · 푸터)은 notice.html 에서 빌려 온다.
(바로기획 tools/make_pages.py 를 이 사이트 틀 · 클래스에 맞춰 옮긴 것)

  python tools/make_pages.py

내용은 아래 STORIES · AREAS 표만 고치면 된다. 사실만 적을 것(대표 블로그 martin301 원문 · 사이트 글 · 대표님 확인분).
만든 뒤 sitemap.xml 도 같이 다시 쓴다.
"""
import os, re, html, json, datetime

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://brizymedia.github.io/j6media/'
BLOG = 'https://blog.naver.com/martin301/'
TEL = '010-4450-4212'
NAME = '제이식스미디어'
E = html.escape

# ── 행사 이야기 (블로그 원문 기준 · 2026-10-03 읽음) ──────────────────
# area: AREAS 의 slug. 운영 지역 9곳 밖의 현장(원주 등)은 None → 「운영 지역」 목록으로 잇는다.
STORIES = [
    dict(slug='wonju-oakvalley-retreat', title='원주 오크밸리리조트 그랜드볼룸, 교회 전가족수련회 음향', cat='교회행사', date='2026.08', place='원주 오크밸리리조트 그랜드볼룸', area=None,
         lead='리조트에 설치된 장비로는 풀밴드 찬양과 모니터링을 감당하기 어려워, 수련회에 맞춘 음향 시스템을 따로 준비해 그랜드볼룸에 설치했습니다.',
         facts=[('행사', '나들목동행교회 전가족수련회'), ('장소', '원주 오크밸리리조트 그랜드볼룸'), ('공간', '앞뒤 약 30m · 좌우 약 17m'), ('맡은 일', '음향 장비 렌탈 · 설치')],
         body=['그랜드볼룸은 앞뒤로 약 30m, 좌우로 약 17m 되는 큰 공간입니다. 리조트에 설치된 장비로는 풀밴드 찬양과 모니터링 시스템을 해결하기 어려워, 수련회에 맞춘 음향 시스템을 따로 준비했습니다.',
               '뒷벽과 좌우 벽에서 생기는 플러터 에코를 최대한 피하려고 스피커 각도와 위치를 여러 번 조정했습니다. 그래도 공간 자체의 울림이 많은 편이었습니다.',
               '내년에도 같은 장소가 예정되어 있어, 공간을 보완할 방법과 새로 적용해 볼 장비를 미리 준비하고 있습니다.'],
         photos=[10, 11, 12, 13], blog='224396313056', quote=['p1', 'a2', 'a5', 'f1']),
    dict(slug='bucheon-fantastic-portal', title='부천국제판타스틱영화제 30주년 「판타스틱 포털」 제막식 음향', cat='지자체 행사', date='2026.06.09', place='부천시청 앞 잔디광장', area='bucheon',
         lead='영화제의 시작을 알리는 제막식이 부천시청 앞 잔디광장에서 열렸습니다. 영화제 30주년을 기념하는 구조물 「판타스틱 포털」을 처음 공개하는 자리의 음향을 맡았습니다.',
         facts=[('행사', '부천국제판타스틱영화제 제막식'), ('장소', '부천시청 앞 잔디광장'), ('맡은 일', '제막식 음향'), ('함께한 일', '2024~2026 영화제 AI 컨퍼런스 · 마켓 음향')],
         body=['6월 9일, 부천시청 앞 잔디광장에서 영화제의 시작을 예고하는 제막식이 열렸습니다. 이날 공개된 구조물이 영화제 30주년을 기념하는 「판타스틱 포털」로, 영화제 기간에는 찾아오는 관객들이 이곳에서 XR을 경험할 수 있다고 합니다.',
               '시장과 조직위원장 등 많은 분이 참석한 야외 공식 행사였습니다. 제이식스미디어는 2024년부터 이 영화제의 AI 컨퍼런스와 마켓 음향도 함께 맡아 오고 있습니다.'],
         photos=[16, 17], blog='224311909715', quote=['p3', 'a2', 'a4', 'f1']),
    dict(slug='hanabok-seminar', title='하나복 본강좌 — 10년 넘게 함께한 세미나 음향', cat='교회행사', date='2026.06', place='곤지암 소망수양관', area='gwangju',
         lead='「하나님 나라 복음으로 교회 세우기」 세미나 본강좌. 해마다 6월 본강좌와 11월 심화강좌에 음향 스태프로 함께하고 있습니다.',
         facts=[('행사', '하나복네트워크 「하나님 나라 복음으로 교회 세우기」 세미나 본강좌'), ('일정', '2026년 6월 1~3일'), ('장소', '곤지암 소망수양관'), ('맡은 일', '세미나 음향')],
         body=['하나복네트워크의 「하나님 나라 복음으로 교회 세우기」 세미나 본강좌가 2026년 6월 1일부터 3일까지 곤지암 소망수양관에서 열렸습니다.',
               '김호진 대표는 매년 6월 본강좌와 11월 심화강좌에 음향 스태프로 참여하고 있습니다. 나들목교회에서 일하던 때부터 이어 온 일이라 벌써 10년이 넘었고, 해마다 참여하는 분들이 늘고 있습니다.'],
         photos=[18, 57, 32], blog='224304136814', quote=['p1', 'a1', 'a4', 'f1']),
    dict(slug='dream-interpretation-exhibition', title='강신욱 작가 음악 전시 「꿈의 해석」 — 스피커 27대의 이머시브 사운드', cat='전시 · 공연', date='2023.09', place='서울 삼성역 C스퀘어', area='seoul',
         lead='자동 연주 피아노와 이머시브 사운드, 영상이 어우러지는 작품. 공연장 조명바턴에 스피커를 매달고, 프로젝터 3대로 피아노의 움직임에 맞춘 영상을 띄웠습니다.',
         facts=[('전시', '강신욱(SHINUK KANG) 음악 전시 「꿈의 해석」'), ('장소', '컬처랜드 타워 C스퀘어 (서울 삼성역 근처)'), ('구성', 'Genelec 8010 27대 · Neumann KH120 · 18인치 서브우퍼 2대 · 프로젝터 3대'), ('맡은 일', '음향 · 영상 셋팅')],
         body=['야마하 자동 연주 피아노 2대와 작가의 아날로그 신디사이저에, 공연장 조명바턴을 이용해 Genelec 8010 스피커 27대와 Neumann KH120 스피커를 설치했습니다. 바닥에는 18인치 서브우퍼 2대를 놓았습니다.',
               '프로젝터 3대로 정면에는 스팟의 움직임을, 좌우 화면에는 각 피아노의 움직임에 맞춘 영상을 보여 줍니다. 모두 9곡, 40분 동안 이어지는 전시입니다.',
               '같은 해 부천 아트벙커 B39, 부천아트센터 개관 전시 「프리즘」에 이어 작가와 세 번째로 함께 준비한 작품입니다. 설치 기간이 짧아 전시 전날 늦게까지 테스트하고 조정했습니다.'],
         photos=[3, 4, 5], blog='223209619397', quote=['p5', 'i4']),
    dict(slug='imundong-church-remodeling', title='이문동교회 리모델링 — 본당과 주일학교 부서 6곳 음향 · 영상', cat='설치', date='2024~2025', place='서울 이문동교회', area='seoul',
         lead='20년 가까이 쓴 스피커와 앰프를 바꾸고, 본당과 주일학교 부서 6곳의 음향 · 영상을 리모델링했습니다. 전체 비용의 30% 정도가 아이들 부서 장비에 쓰였습니다.',
         facts=[('현장', '이문동교회 본당 + 주일학교 부서 6곳'), ('기간', '2024년 하반기 ~ 2025년 초'), ('본당 장비', 'LSS SP530 + PSUB1 · 딜레이 LSS MIL130 5대 · MIDAS M32 + DL16 · SHURE SLXD 8대'), ('맡은 일', '음향 · 영상 시스템 리모델링')],
         body=['외대앞 이문동교회의 본당과 주일학교 부서 6곳을 2024년 하반기부터 2025년 초까지 리모델링했습니다. 20년 가까이 쓰던 스피커와 앰프를 새것으로 바꿨습니다.',
               '본당 메인 스피커는 LSS SP530과 PSUB1, 뒤쪽 딜레이 스피커는 LSS MIL130 5대입니다. 목사님 모니터 LSS SP220 2대, 찬양팀 모니터 QUEST QM10 4대, 파워앰프 POWERSOFT Quattrocanali, 믹서 MIDAS M32와 DL16, 무선마이크 SHURE SLXD BETA58 8대를 갖췄습니다. 전광판과 영상장비, 모듈레이터 등은 기존 장비를 다시 쓴 것이 많습니다.',
               '현장 설명회 때부터 교회가 본당만큼 아이들 부서도 신경 써 달라고 부탁하셨습니다. 그래서 전체 비용의 30% 정도가 아이들 부서의 음향 · TV · 악기 장비에 쓰였고, 마지막으로 찬양팀 밴드 연습과 레슨을 하는 합주실 장비까지 마무리했습니다.'],
         photos=[23, 24, 25], blog='223821012265', quote=['i1', 'i5', 'i6']),
]

# ── 지역 ────────────────────────────────────────────────────
# 분 · km: 별내 사무실(37.6524324, 127.1293090)에서 각 시청 · 군청까지 OSRM(막히지 않을 때) 2026-10-03 조회, 5분 단위 반올림
# done: 그 지역에서 한 일 — 블로그 · 사이트 기록이 있는 것만
AREAS = [
    dict(slug='namyangju', name='남양주', hall='', min=0, km=0, hq=True, done=[], photos=[41, 36, 57]),
    dict(slug='guri', name='구리', hall='구리시청', min=10, km=8.8, done=[], photos=[44, 39, 47]),
    dict(slug='seoul', name='서울', hall='서울시청', min=25, km=19.9,
         done=['2023 강신욱 작가 음악 전시 「꿈의 해석」 음향 · 영상 셋팅 (삼성역 C스퀘어)', '2024~2025 이문동교회 본당 · 주일학교 음향 · 영상 리모델링',
               '2025 서울라이트 빛섬축제 음향 (웨이오디오와 함께)', '2026 S/S FASHION KODE 패션쇼 음향 (2025)',
               '서울대병원 융합의학기술원 입체음향 스튜디오 설치', '정림건축종합건축사사무소 김정철홀 영상 · 음향 설치', '성공회 정오음악회 야외 음향'],
         photos=[3, 23, 48]),
    dict(slug='yangju', name='양주', hall='양주시청', min=20, km=20.6, done=['양주 백석고 축제 무대 음향 · 조명'], photos=[50, 51, 41]),
    dict(slug='pocheon', name='포천', hall='포천시청', min=30, km=35.8, done=['2025 포천 태광성서교회 음향 점검 · 교체 (교회음향 지원사업 — 비용 전액 제이식스미디어 부담)'], photos=[57, 39, 44]),
    dict(slug='gapyeong', name='가평', hall='가평군청', min=50, km=51.2,
         done=['2024 더스테이힐링파크 야외 공연 음향 · 영상', '더스테이힐링파크 고객초청음악회 · 송년 콘서트', '2025 더스테이힐링파크 어린이날 축제 · 힐링키즈 페스티벌 음향',
               '2024 더스테이힐링파크 별빛정원 정원 스피커 설치', '2025 더스테이힐링파크 카페 외부 방수 스피커 설치'],
         photos=[41, 40, 1]),
    dict(slug='gwangju', name='경기 광주', hall='광주시청', min=30, km=32.2, done=['하나복네트워크 본강좌 세미나 음향 — 곤지암 소망수양관 (2026.6)'], photos=[18, 57, 32]),
    dict(slug='goyang', name='고양', hall='고양시청', min=30, km=35.6, done=['2022 고양호수예술축제 숲속 공연 음향'], photos=[31, 38, 49]),
    dict(slug='bucheon', name='부천', hall='부천시청', min=45, km=53.9,
         done=['2026 부천국제판타스틱영화제 제막식 음향 (부천시청 앞 잔디광장)', '2024~2026 부천국제판타스틱영화제 AI 컨퍼런스 · 마켓 음향',
               '2023 강신욱 작가 전시 음향 — 부천 아트벙커 B39 · 부천아트센터 개관 전시 「프리즘」'],
         photos=[16, 45, 46]),
]

SERVICES = [('교회행사', '예배 · 세미나 · 수련회'), ('기업행사', '포럼 · 고객초청 · 어린이날 · 송년 콘서트'), ('지자체 행사', '영화제 · 제막식 · 컨퍼런스'),
            ('학교행사', '체육대회 · 축제'), ('전시 · 공연', '입체음향 · 콘서트'), ('음향 · 영상 · 방송장비 설치', '교회 · 카페 · 강당 · 스튜디오')]

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'


def shell():
    s = open(os.path.join(SITE, 'notice.html'), encoding='utf-8').read()
    head_end = s.index('<section class="phead">')
    main_end = s.index('</main>') + len('</main>')
    return s[:head_end], s[main_end:]


def area_of(slug):
    return next((a for a in AREAS if a['slug'] == slug), None)


def page(path, title, desc, phead, main, img='assets/img/og.jpg', crumbs=()):
    """path: 사이트 기준 경로. 본문 안 링크도 전부 사이트 기준(예: stories/x.html)으로 쓰면 깊이에 맞춰 ../ 를 붙인다."""
    top, bottom = shell()
    url = BASE + path
    top = re.sub(r'<title>.*?</title>', '<title>' + E(title) + '</title>', top, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        top = re.sub(r'(<meta ' + prop + r' content=")[^"]*', lambda m: m.group(1) + E(desc), top, count=1)
    top = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + E(title), top, count=1)
    top = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, top, count=1)
    top = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, top, count=1)
    top = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + BASE + img, top, count=1)
    # 이동 경로(BreadcrumbList)를 이 페이지 것으로
    items = [('홈', BASE)] + [(n, BASE + p) for n, p in crumbs]
    bc = {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
          'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}
    top = re.sub(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"BreadcrumbList".*?</script>',
                 lambda m: '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False, separators=(',', ':')) + '</script>', top, count=1, flags=re.S)
    top = re.sub(r'<meta name="es-edit"[^>]*>\n?', '', top)            # 대표님 수정 모드는 기본 페이지에만
    bottom = re.sub(r'<script src="assets/edit\.js[^"]*"></script>\n?', '', bottom)
    out = top + phead + '\n\n<main>\n' + main + '\n</main>' + bottom
    depth = path.count('/')
    pre = '../' * depth
    out = re.sub(r'(href|src|poster)="(?!https?:|mailto:|tel:|sms:|#|/|\.\./|data:)([^"]+)"', lambda m: m.group(1) + '="' + pre + m.group(2) + '"', out)
    out = re.sub(r"url\((?!https?:)(assets/[^)]+)\)", lambda m: 'url(' + pre + m.group(1) + ')', out)
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(out)
    return url


def pic(i, big=False):
    return 'assets/img/works/' + ('w' if big else 't') + str(i) + '.webp'


def phead(bg, eyebrow, h1, sub, crumbs):
    c = '<a href="index.html">홈</a>' + ''.join('<span>›</span>' + ('<a href="' + h + '">' + E(n) + '</a>' if h else '<span>' + E(n) + '</span>') for n, h in crumbs)
    return ('<section class="phead">\n  <div class="bg" style="background-image:url(' + pic(bg, True) + ')"></div>\n  <div class="wrap">\n'
            '    <p class="eyebrow">' + eyebrow + '</p>\n    <h1>' + E(h1) + '</h1>\n    <p>' + E(sub) + '</p>\n'
            '    <div class="crumb">' + c + '</div>\n  </div>\n</section>')


def cta(title='예배 · 공연 · 행사, 소리와 빛이 필요하신가요?', sub='날짜와 장소, 대략의 규모만 알려 주세요. 현장에 맞는 구성을 함께 찾아 드립니다.'):
    return ('<section class="sec" style="padding-top:clamp(48px,6vw,72px)">\n  <div class="wrap">\n    <div class="ctaband reveal">\n'
            '      <div class="eq" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>\n'
            '      <div><h2>' + E(title) + '</h2><p>' + E(sub) + '</p></div>\n'
            '      <div class="btns"><a class="btn btn-w" href="tel:' + TEL + '">' + PHONE + TEL + '</a><a class="btn btn-ink" href="quote.html">자동 견적서' + ARROW + '</a></div>\n'
            '    </div>\n  </div>\n</section>')


def stcard(o, extra=''):
    return ('<a class="stcard reveal" href="stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600">'
            '<span><small>' + E(o['cat'] + ' · ' + o['date'] + extra) + '</small>' + E(o['title']) + '</span></a>')


def story_pages():
    urls = []
    for st in STORIES:
        facts = ''.join('<dt>' + E(a) + '</dt><dd>' + E(b) + '</dd>' for a, b in st['facts'])
        body = ''.join('<p>' + E(p) + '</p>' for p in st['body'])
        photos = ''.join('<a href="' + pic(f, True) + '" target="_blank" rel="noopener"><img src="' + pic(f) + '" alt="' + E(st['title']) + ' 현장" loading="lazy" width="800" height="600"></a>' for f in st['photos'])
        area = area_of(st['area']) if st['area'] else None
        alink = ('<a class="alink" href="areas/' + area['slug'] + '.html">' + E(area['name']) + ' 음향 · 설치 안내 →</a>') if area else '<a class="alink" href="areas/index.html">운영 지역 보기 →</a>'
        others = [o for o in STORIES if o['slug'] != st['slug']][:3]
        more = ''.join(stcard(o) for o in others)
        blog = ('<a class="btn btn-line" href="' + BLOG + st['blog'] + '" target="_blank" rel="noopener">블로그 원문 보기 ↗</a>') if st['blog'] else ''
        ph = phead(st['photos'][0], 'Event Story · ' + E(st['cat']), st['title'], st['lead'], [('행사 이야기', 'stories/index.html'), (st['cat'], '')])
        main = ('<section class="sec"><div class="wrap story">'
                '<aside class="reveal"><span class="en">Event File</span><dl>' + facts + '<dt>날짜</dt><dd>' + E(st['date']) + '</dd></dl>'
                '<a class="btn btn-amb" href="quote.html">비슷한 행사 견적 받기</a>' + alink + '</aside>'
                '<div class="reveal d1 sbody">' + body + '<div class="sgrid">' + photos + '</div><div class="sbtns">' + blog + '<a class="btn btn-line" href="portfolio.html">현장 사진 더 보기</a></div></div>'
                '</div></section>\n'
                '<section class="sec sand"><div class="wrap"><div class="sec-head reveal"><div class="t"><p class="eyebrow">More Stories</p><h2 class="h2">다른 <em>현장 이야기</em>.</h2></div>'
                '<a class="btn btn-line" href="stories/index.html">전체 보기' + ARROW + '</a></div><div class="stcards">' + more + '</div></div></section>\n' + cta())
        urls.append(page('stories/' + st['slug'] + '.html', st['title'] + ' | ' + NAME + ' 행사 이야기', st['lead'][:120], ph, main,
                         img=pic(st['photos'][0], True), crumbs=[('행사 이야기', 'stories/index.html'), (st['title'], 'stories/' + st['slug'] + '.html')]))
    cards = ''.join('<a class="stcard reveal" href="stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(o['cat'] + ' · ' + o['date'] + ' · ' + o['place']) + '</small>' + E(o['title']) + '<em>' + E(o['lead'][:64]) + '…</em></span></a>' for o in STORIES)
    ph = phead(41, 'Event Stories', '행사 이야기', '제이식스미디어가 맡았던 현장을 한 편씩 기록했습니다. 어떤 장비로 어떻게 준비했는지, 현장에서 무엇이 있었는지 사진과 함께 보실 수 있습니다.', [('행사 이야기', '')])
    main = ('<section class="sec"><div class="wrap"><div class="stcards big">' + cards + '</div><p class="snote">더 많은 현장 기록은 <a href="' + BLOG + '" target="_blank" rel="noopener">대표 네이버 블로그(martin301)</a>와 <a href="notice.html#board">게시판 · 현장 소식</a>에 있습니다.</p></div></section>\n' + cta())
    urls.insert(0, page('stories/index.html', '행사 이야기 | ' + NAME + ' — 수련회 · 영화제 · 세미나 · 입체음향 전시 · 교회 리모델링 현장 기록',
                        '제이식스미디어가 맡았던 현장을 한 편씩 기록했습니다. 원주 오크밸리 수련회, 부천국제판타스틱영화제 제막식, 하나복 본강좌, 강신욱 작가 전시 「꿈의 해석」, 이문동교회 리모델링.',
                        ph, main, img=pic(41, True), crumbs=[('행사 이야기', 'stories/index.html')]))
    return urls


def how_far(a):
    n = a['name']
    if a.get('hq'):
        return '<b>제이식스미디어 사무실</b>이 있는 곳입니다. 경기도 남양주시 순화궁로 282 에이스하이엔드타워별내 319호 — 방문 상담은 미리 연락 주시고 오시면 됩니다.'
    return '남양주 별내 사무실에서 ' + a['hall'] + '까지 차로 약 <b>' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km</b>(막히지 않을 때 기준)입니다.'


def area_pages():
    urls = []
    for a in AREAS:
        n = a['name']
        if a['done']:
            done = '<ul class="alist">' + ''.join('<li>' + E(x) + '</li>' for x in a['done']) + '</ul>'
        else:
            done = '<p class="muted">아직 이 페이지에 적을 만큼 정리된 기록이 없습니다. ' + n + ' 현장도 별내 사무실에서 출발해 똑같이 준비합니다.</p>'
        stories = [s for s in STORIES if s['area'] == a['slug']]
        sl = ''.join(stcard(s) for s in stories)
        svc = ''.join('<li><b>' + E(x) + '</b><span>' + E(y) + '</span></li>' for x, y in SERVICES)
        photos = ''.join('<img src="' + pic(f) + '" alt="제이식스미디어 현장" loading="lazy" width="800" height="600">' for f in a['photos'])
        others = ' · '.join('<a href="areas/' + o['slug'] + '.html">' + o['name'] + '</a>' for o in AREAS if o['slug'] != a['slug'])
        title = n + ' 음향 렌탈 · 행사 음향 · 음향 설치 | ' + NAME
        desc = (n + ' 예배 · 세미나 · 공연 · 행사 음향 · 조명 렌탈과 운영, 교회 · 카페 · 강당 음향 · 영상 · 방송장비 설치. ' +
                ('제이식스미디어 사무실이 있는 곳.' if a.get('hq') else '남양주 별내 사무실에서 차로 약 ' + str(a['min']) + '분.'))
        ph = phead(a['photos'][0], 'Area · ' + E(n), n + ' 행사 음향 · 설치, 제이식스미디어', '예배 · 공연 · 행사의 음향과 조명, 음향 · 영상 · 방송장비 설치까지. 2005년부터 음향의 길을 걸어온 제이식스미디어가 ' + n + ' 현장도 함께합니다.',
                   [('운영 지역', 'areas/index.html'), (n, '')])
        main = ('<section class="sec"><div class="wrap area3"><div class="reveal"><span class="en">How Far</span><h2 class="h2s">' + n + (' — 사무실' if a.get('hq') else '까지') + '</h2><p>' + how_far(a) + '</p>'
                '<h3 class="h3s">' + n + '에서 한 일</h3>' + done + ('<div class="stcards sm">' + sl + '</div>' if sl else '') + '</div>'
                '<div class="reveal d1"><div class="apics">' + photos + '</div></div></div></section>\n'
                '<section class="sec sand"><div class="wrap"><div class="sec-head reveal"><div class="t"><p class="eyebrow">What We Do</p><h2 class="h2">' + n + '에서도 <em>이런 일</em>을 맡습니다.</h2></div></div><ul class="asvc reveal">' + svc + '</ul>'
                '<p class="snote">다른 지역: ' + others + ' · <a href="areas/index.html">운영 지역 전체</a></p></div></section>\n' + cta(n + ' 행사, 소리와 빛이 필요하신가요?'))
        urls.append(page('areas/' + a['slug'] + '.html', title, desc, ph, main, img=pic(a['photos'][0], True), crumbs=[('운영 지역', 'areas/index.html'), (n, 'areas/' + a['slug'] + '.html')]))
    rows = ''.join('<a class="arow" href="areas/' + a['slug'] + '.html"><b>' + a['name'] + '</b><span>' + ('사무실' if a.get('hq') else '차로 약 ' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km') + '</span><em>' + (E(a['done'][0]) if a['done'] else '출장 진행') + '</em></a>' for a in AREAS)
    ph = phead(45, 'Service Area', '운영 지역', '남양주 별내 사무실에서 출발해 서울 · 경기 어디든 갑니다. 지역을 누르면 그 지역에서 한 일과 이동 시간을 보실 수 있습니다.', [('운영 지역', '')])
    main = ('<section class="sec"><div class="wrap area3"><div class="reveal"><span class="en">From Byeollae</span><h2 class="h2s">별내에서 <em>어디든</em></h2>'
            '<p>' + how_far(AREAS[0]) + '</p><div class="apics">' + ''.join('<img src="' + pic(f) + '" alt="제이식스미디어 현장" loading="lazy" width="800" height="600">' for f in (41, 45, 3)) + '</div></div>'
            '<div class="reveal d1"><div class="arows">' + rows + '</div><p class="snote">이동 시간은 사무실에서 각 시청 · 군청까지 차로 걸리는 시간(막히지 않을 때 기준)입니다. 출퇴근 시간에는 더 걸릴 수 있습니다. 표에 없는 지역(원주 · 제주 등)도 다녀왔습니다 — 지역과 일정을 알려 주시면 가능 여부를 안내해 드립니다.</p></div></div></section>\n' + cta())
    urls.insert(0, page('areas/index.html', '운영 지역 | ' + NAME + ' — 남양주 · 구리 · 서울 · 양주 · 포천 · 가평 · 경기 광주 · 고양 · 부천 음향 렌탈 · 설치',
                        '남양주 별내 사무실에서 서울 · 경기 어디든. 지역별 이동 시간과 그 지역에서 한 일을 보실 수 있습니다.', ph, main, img=pic(45, True), crumbs=[('운영 지역', 'areas/index.html')]))
    return urls


def sitemap(extra):
    today = datetime.date.today().isoformat()
    pages = ['', 'about.html', 'service.html', 'equipment.html', 'portfolio.html', 'notice.html', 'contact.html', 'quote.html']
    urls = [BASE + p for p in pages] + extra
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + u + '</loc><lastmod>' + today + '</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)


if __name__ == '__main__':
    a = story_pages(); b = area_pages(); sitemap(a + b)
    print('행사 이야기', len(a), '· 지역', len(b), '· sitemap.xml 갱신')
