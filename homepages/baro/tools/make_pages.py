# -*- coding: utf-8 -*-
"""
행사 이야기(stories/) · 지역 페이지(areas/) 만들기 — 사이트 틀(머리글 · 푸터)은 notice.html 에서 빌려 온다.

  python tools/make_pages.py

내용은 아래 STORIES · AREAS 표만 고치면 된다. 사실만 적을 것(회사소개서 · 블로그 · 대표님 확인분).
만든 뒤 sitemap.xml 도 같이 다시 쓴다.
"""
import os, re, html, json, datetime

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://brizymedia.github.io/baro-event/'
BLOG = 'https://blog.naver.com/mot2256789/'
E = html.escape

# ── 행사 이야기 ──────────────────────────────────────────────
STORIES = [
    dict(slug='suwon-church-sports', title='6개 교회 600여 명, 교회 연합 체육대회', cat='체육대회', date='2026.06', place='수원 합동신학대학원 대운동장', area='suwon',
         lead='그동안 집사님들이 직접 진행하던 연합 체육대회를, 올해는 음향 · 게임도구 · 전문 MC · 진행 스텝까지 바로기획에 통째로 맡기셨습니다.',
         facts=[('행사', '교회 연합 체육대회'), ('규모', '6개 교회 · 600여 명'), ('장소', '수원 합동신학대학원 대운동장'), ('맡은 일', '음향 · 게임도구 · 전문 MC · 진행 스텝 · 입장 아치')],
         body=['6개 교회가 한자리에 모이는 날이라 종목은 누구나 함께할 수 있는 단체 게임 위주로 짰습니다. 대형 공 굴리기, 단체 이어달리기처럼 교회별로 힘을 모으는 종목이 운동장을 채웠습니다.',
               '운동장이 넓어 음향은 본부석과 응원석 양쪽에 소리가 고르게 가도록 세팅하고, 믹서는 현장에서 계속 조절했습니다. 입장 아치와 축포로 시작을 열고, 전문 MC가 처음부터 끝까지 진행을 맡았습니다.'],
         photos=['s03', 's06', 's02', 's09', 's05', 's12'], blog='224360419895', quote=['p1', 'a3', 'f1', 'h3', 'd10']),
    dict(slug='sunoeul-water-festival', title='제5회 수노을 물놀이축제 — 갑자기 쏟아진 비에도 끝까지', cat='물놀이 축제', date='2026.08.22', place='화성 새솔동 수노을중앙공원', area='hwaseong',
         lead='오후에 예보에 없던 비가 내렸지만 물대포 · 워터건 · 영유아존을 그대로 운영했고, 전기 배선 방수와 미끄럼 방지 매트로 안전사고 없이 마쳤습니다.',
         facts=[('행사', '제5회 수노을 물놀이축제'), ('날짜', '2026년 8월 22일'), ('장소', '화성 새솔동 수노을중앙공원'), ('맡은 일', '대형 풀장 · 에어 물놀이 기구 · 물대포 · 영유아존 · 안전 관리')],
         body=['공원 한가운데 대형 풀장과 에어 물놀이 기구를 이어 놓고, 어린아이들이 따로 놀 수 있는 영유아존을 나눠 두었습니다.',
               '비가 오자 가장 먼저 전기 배선의 방수를 다시 확인하고, 미끄러지기 쉬운 동선에는 매트를 깔았습니다. 비 때문에 멈추지 않고 끝까지 운영할 수 있었던 건 이런 준비 덕분입니다.',
               '수노을 물놀이축제는 바로기획이 2023년부터 해마다 맡아 온 행사입니다.'],
         photos=['m01', 'm21', 'm09'], blog='224392145062', quote=['p5', 'h2', 'a2', 'd3']),
    dict(slug='yongin-school-water', title='학교 운동장에 차린 여름 물놀이', cat='물놀이 행사', date='2026.08', place='용인다움학교 운동장', area='yongin',
         lead='설치 면적과 수도 위치를 먼저 확인하고, 워터슬라이드 입구 · 출구에 안전요원을 세워 순서를 정리했습니다.',
         facts=[('행사', '학교 여름 물놀이행사'), ('장소', '용인다움학교 운동장'), ('맡은 일', '물놀이 풀 · 워터슬라이드 · 물고기 잡기 체험 풀 · 안전요원')],
         body=['학교 운동장은 행사장마다 수도 위치와 바닥 상태가 다릅니다. 그래서 설치 전에 면적과 급수 위치부터 확인하고 풀과 슬라이드 자리를 정했습니다.',
               '아이들이 한꺼번에 몰리는 워터슬라이드는 입구와 출구에 안전요원을 세워 순서대로 타게 했고, 물고기 잡기 체험 풀도 함께 운영했습니다.'],
         photos=['y01', 'y07', 'y03'], blog='224395601984', quote=['p5', 'h2', 'f5']),
    dict(slug='ansan-cutting', title='동물병원 이전개업 커팅식', cat='커팅식', date='2026.08', place='안산', area='ansan',
         lead='레드카펫 · 오색띠 · 금장가위 · 흰장갑 · 꽃장식 · 풍선장식 · 포토존까지 빠짐없이 준비했습니다.',
         facts=[('행사', '동물병원 이전개업 커팅식'), ('장소', '안산'), ('맡은 일', '레드카펫 · 오색띠 · 금장가위 · 흰장갑 · 꽃장식 · 풍선장식 · 포토존')],
         body=['커팅식은 짧은 순서라 준비물 하나만 빠져도 티가 납니다. 레드카펫 동선부터 오색띠 길이, 금장가위와 흰장갑 수까지 참석 인원에 맞춰 챙겼습니다.',
               '입구에는 풍선 아치로 개업 분위기를 내고, 손님들이 사진을 남길 수 있게 포토존을 따로 꾸몄습니다.'],
         photos=['c16', 'c03', 'c11'], blog='224393003161', quote=['p3', 'h6', 'h5', 'b5']),
    dict(slug='gyeonggi-tree-lighting', title='경기도 성탄트리 점등식 — 9년째 함께한 겨울 밤', cat='점등식', date='2017~2025', place='수원', area='suwon',
         lead='경기도기독교총연합회가 여는 수원 성탄트리 점등식을 2017년부터 2025년까지 해마다 맡았습니다.',
         facts=[('행사', '경기도 성탄트리 점등식 · 크리스마스 페스티벌'), ('주최', '경기도기독교총연합회'), ('장소', '수원'), ('기간', '2017~2025 (9년)')],
         body=['대형 트리에 불이 들어오는 순간을 위해 점등 순서와 식순, 무대 진행을 준비했습니다.',
               '점등식과 함께 어린이 합창 같은 크리스마스 거리 공연도 이어졌습니다.'],
         photos=['n05', 'n06'], blog='', quote=['p6', 'a2', 'b1', 'f1']),
]

# ── 지역 ────────────────────────────────────────────────────
# 분 · km: 본사에서 각 시청까지 OSRM(막히지 않을 때) 2026-09-28 조회, 5분 단위 반올림
AREAS = [
    dict(slug='ansan', name='안산', min=0, km=0, hq=True,
         done=['2010 와스타디움 국가대표 대 할렐루야 축구경기 하프타임 진행', '안산 다문화가정 어린이 기성용 축구 클리닉 진행', '안산 도민체전 화성시 입장식 행사 기획', '2026 동물병원 이전개업 커팅식'],
         photos=['n03', 'c16', 'n00']),
    dict(slug='hwaseong', name='화성', min=20, km=15.6,
         done=['화성시 새솔동 수노을 워터밤 물놀이축제 (2023~)', '화성시 봉선축제 기획 · 연출', '화성시 남양동 광복절 기념 체육대회', '화성시 우리꽃 식물원 들국화 축제', '화성시 삼괴중 · 고등학교 총동문회', '남양성지 가을음악회', '경기도 생활대축전 화성시 입장식 퍼레이드'],
         photos=['m01', 'm21', 'n16']),
    dict(slug='suwon', name='수원', min=20, km=19.4,
         done=['경기도기독교총연합회 수원 성탄트리 점등식 (2017~2025)', '2026 수원 6개 교회 연합 체육대회 (600여 명)'],
         photos=['n05', 's03', 's06']),
    dict(slug='siheung', name='시흥', min=20, km=17.3, done=[], photos=['n12', 'n17', 'n14']),
    dict(slug='anyang', name='안양', min=20, km=18.5, done=[], photos=['n00', 'n11', 'n12']),
    dict(slug='gwangmyeong', name='광명', min=30, km=26.9, done=[], photos=['n09', 'n10', 'n02']),
    dict(slug='dongtan', name='동탄', min=30, km=33.1, done=[], photos=['n17', 'n16', 'n13']),
    dict(slug='yongin', name='용인', min=35, km=35.8, done=['2026 용인다움학교 여름 물놀이행사'], photos=['y01', 'y07', 'n16']),
    dict(slug='pyeongtaek', name='평택', min=50, km=54.3, done=[], photos=['n17', 'n18', 'n14']),
]

SERVICES = [('체육대회 · 명랑운동회', '종목 구성 · 게임도구 · 전문 MC'), ('지역축제 · 주민행사', '무대 · 음향 · 체험 부스 · 공연'), ('커팅식 · 오픈 이벤트', '레드카펫 · 오색띠 · 풍선장식'),
            ('송년회 · 레크리에이션', 'MC · 레크 강사 · 경품 진행'), ('물놀이 축제', '풀장 · 워터슬라이드 · 안전요원'), ('음향 · 천막 · 장비', '필요한 것만 빌려 쓰셔도 됩니다')]


def shell():
    s = open(os.path.join(SITE, 'notice.html'), encoding='utf-8').read()
    head_end = s.index('<main id="top">')
    main_end = s.index('</main>') + len('</main>')
    return s[:head_end], s[main_end:]


def page(path, title, desc, main, img='assets/img/og.jpg', depth=1):
    top, bottom = shell()
    url = BASE + path
    top = re.sub(r'<title>.*?</title>', '<title>' + E(title) + '</title>', top, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        top = re.sub(r'(<meta ' + prop + r' content=")[^"]*', r'\g<1>' + E(desc).replace('\\', '\\\\'), top, count=1)
    top = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + E(title), top, count=1)
    top = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\g<1>' + url, top, count=1)
    top = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>' + url, top, count=1)
    top = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>' + BASE + img, top, count=1)
    top = re.sub(r'<meta name="baro-edit"[^>]*>\n?', '', top)            # 대표님 수정 모드는 기본 6쪽에만
    top = top.replace(' class="act"', '').replace('class="act" ', '')
    bottom = re.sub(r'<script src="assets/edit\.js[^"]*"></script>\n?', '', bottom)
    out = top + '<main id="top">\n' + main + '\n</main>' + bottom
    pre = '../' * depth
    out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|sms:|#|/|\.\./)([^"]+)"', lambda m: m.group(1) + '="' + pre + m.group(2) + '"', out)
    out = re.sub(r"url\((?!https?:)(assets/[^)]+)\)", lambda m: 'url(' + pre + m.group(1) + ')', out)
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(out)
    return url


def pic(f, big=False):
    return 'assets/img/' + ('p/' if big else 't/') + f + '.webp'


def cta(title='행사 날짜가 잡히셨나요?', sub='규모가 작아도 괜찮습니다. 날짜 · 장소 · 대략의 인원만 알려 주세요. (상담 오전 8시 ~ 저녁 8시)', bg='n19'):
    return ('<section class="callband" style="background-image:url(assets/img/p/' + bg + '.webp)"><div class="wrap"><div class="rv"><h2>' + title +
            '<br><em>바로기획</em>이 바로 준비합니다.</h2><p>' + sub + '</p></div><div class="rv d1"><a class="num" href="tel:010-2758-0655">010-2758-0655</a>'
            '<div class="btns"><a class="btn btn-gold" href="tel:010-2758-0655">전화 상담</a><a class="btn btn-ghost" href="quote.html">자동 견적서</a><a class="btn btn-ghost" href="contact.html">견적 문의 폼</a></div></div></div></section>')


def story_pages():
    urls = []
    for i, st in enumerate(STORIES):
        facts = ''.join('<dt>' + E(a) + '</dt><dd>' + E(b) + '</dd>' for a, b in st['facts'])
        body = ''.join('<p>' + E(p) + '</p>' for p in st['body'])
        photos = ''.join('<a href="' + pic(f, True) + '" target="_blank" rel="noopener"><img src="' + pic(f) + '" alt="' + E(st['title']) + ' 현장" loading="lazy" width="800" height="600"></a>' for f in st['photos'])
        area = next(a for a in AREAS if a['slug'] == st['area'])
        others = [o for o in STORIES if o['slug'] != st['slug']][:3]
        more = ''.join('<a class="scard" href="' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(o['cat'] + ' · ' + o['date']) + '</small>' + E(o['title']) + '</span></a>' for o in others)
        blog = ('<a class="btn btn-line" href="' + BLOG + st['blog'] + '" target="_blank" rel="noopener">블로그 원문 보기 ↗</a>') if st['blog'] else ''
        main = ('<section class="phead" style="background-image:url(' + pic(st['photos'][0], True) + ')"><div class="wrap"><p class="crumb"><a href="index.html">홈</a> · <a href="stories/index.html">행사 이야기</a> · <b>' + E(st['cat']) + '</b></p>'
                '<h1>' + E(st['title']) + '</h1><p>' + E(st['lead']) + '</p></div></section>'
                '<section class="sec"><div class="wrap story">'
                '<aside class="rv"><span class="en">Event File</span><dl>' + facts + '<dt>날짜</dt><dd>' + E(st['date']) + '</dd></dl>'
                '<a class="btn btn-gold" href="quote.html">비슷한 행사 견적 받기</a><a class="alink" href="areas/' + area['slug'] + '.html">' + E(area['name']) + ' 행사 안내 →</a></aside>'
                '<div class="rv d1 sbody">' + body + '<div class="sgrid">' + photos + '</div><div class="sbtns">' + blog + '<a class="btn btn-line" href="portfolio.html">현장 사진 더 보기</a></div></div>'
                '</div></section>'
                '<section class="sec gray"><div class="wrap"><div class="head rv"><div><span class="en">More Stories</span><h2>다른 <em>현장 이야기</em></h2></div><a class="more" href="stories/index.html">전체 보기 →</a></div><div class="scards">' + more + '</div></div></section>'
                + cta())
        main = main.replace('href="stories/index.html"', 'href="index.html"').replace('href="areas/', 'href="../areas/')
        # 같은 폴더 안 링크는 page() 가 ../ 를 붙이지 않게 따로 표시
        main = main.replace('href="' + '../areas/', 'href="@@areas/')
        for o in STORIES: main = main.replace('href="' + o['slug'] + '.html"', 'href="@@stories/' + o['slug'] + '.html"')
        main = main.replace('href="index.html">전체 보기', 'href="@@stories/index.html">전체 보기').replace('<a href="index.html">행사 이야기</a>', '<a href="@@stories/index.html">행사 이야기</a>')
        url = page('stories/' + st['slug'] + '.html', st['title'] + ' | 바로기획 행사 이야기', st['lead'][:120], main, img=pic(st['photos'][0], True))
        urls.append(url)
    cards = ''.join('<a class="scard rv" href="@@stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(o['cat'] + ' · ' + o['date'] + ' · ' + o['place']) + '</small>' + E(o['title']) + '<em>' + E(o['lead'][:60]) + '…</em></span></a>' for o in STORIES)
    main = ('<section class="phead" style="background-image:url(' + pic('n05', True) + ')"><div class="wrap"><p class="crumb"><a href="index.html">홈</a> · <b>행사 이야기</b></p><h1>행사 이야기</h1><p>바로기획이 준비한 행사를 한 편씩 기록했습니다. 어떤 준비를 했는지, 현장에서 무엇이 있었는지 사진과 함께 보실 수 있습니다.</p></div></section>'
            '<section class="sec"><div class="wrap"><div class="scards big">' + cards + '</div><p class="snote">더 많은 현장 기록은 <a href="' + BLOG + '" target="_blank" rel="noopener">바로기획 네이버 블로그</a>에 있습니다.</p></div></section>' + cta())
    urls.insert(0, page('stories/index.html', '행사 이야기 | 바로기획 — 체육대회 · 물놀이축제 · 커팅식 · 점등식 현장 기록', '바로기획이 준비한 행사를 한 편씩 기록했습니다. 교회 연합 체육대회, 수노을 물놀이축제, 커팅식, 성탄트리 점등식 현장.', main, img=pic('n05', True)))
    return urls


def area_pages():
    urls = []
    for a in AREAS:
        n = a['name']
        if a.get('hq'):
            how = '<b>바로기획 본사</b>가 있는 곳입니다. 경기도 안산시 상록구 장화1길 56, 103호(사동) — 안산 안에서는 대부분 30분 안에 현장에 닿습니다.'
        else:
            how = '안산 본사에서 ' + n + (' 시청' if n != '동탄' else '역') + '까지 차로 약 <b>' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km</b>(막히지 않을 때 기준)입니다. 행사 전날 · 당일 아침 일찍 도착해 설치를 마칩니다.'
        if a['done']:
            done = '<ul class="alist">' + ''.join('<li>' + E(x) + '</li>' for x in a['done']) + '</ul>'
        else:
            done = '<p class="muted">아직 이 페이지에 적을 만큼 정리된 기록이 없습니다. ' + n + ' 행사도 안산 본사에서 출발해 똑같이 준비합니다.</p>'
        stories = [s for s in STORIES if s['area'] == a['slug']]
        sl = ''.join('<a class="scard" href="@@stories/' + s['slug'] + '.html"><img src="' + pic(s['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(s['cat'] + ' · ' + s['date']) + '</small>' + E(s['title']) + '</span></a>' for s in stories)
        svc = ''.join('<li><b>' + E(x) + '</b><span>' + E(y) + '</span></li>' for x, y in SERVICES)
        photos = ''.join('<img src="' + pic(f) + '" alt="바로기획 행사 현장" loading="lazy" width="800" height="600">' for f in a['photos'])
        others = ' · '.join('<a href="@@areas/' + o['slug'] + '.html">' + o['name'] + '</a>' for o in AREAS if o['slug'] != a['slug'])
        title = n + ' 행사대행 · 체육대회 · 축제 · 커팅식 | 바로기획'
        desc = n + ' 체육대회 · 지역축제 · 커팅식 · 송년회 · 물놀이 축제, 음향 · 천막 · MC 섭외까지. ' + ('안산 본사 — 2005년부터.' if a.get('hq') else '안산 본사에서 차로 약 ' + str(a['min']) + '분. 2005년부터 경기 행사를 준비해 온 바로기획.')
        main = ('<section class="phead" style="background-image:url(' + pic(a['photos'][0], True) + ')"><div class="wrap"><p class="crumb"><a href="index.html">홈</a> · <a href="@@areas/index.html">운영 지역</a> · <b>' + n + '</b></p>'
                '<h1>' + n + ' 행사, 바로기획이 갑니다</h1><p>체육대회 · 지역축제 · 커팅식 · 송년회 · 물놀이 축제. 2005년부터 경기 행사를 준비해 온 바로기획이 ' + n + ' 현장도 처음부터 끝까지 챙깁니다.</p></div></section>'
                '<section class="sec"><div class="wrap area3"><div class="rv"><span class="en">How Far</span><h2 class="h2s">' + n + (' — 본사' if a.get('hq') else '까지') + '</h2><p>' + how + '</p>'
                '<h3 class="h3s">' + n + '에서 한 행사</h3>' + done + ('<div class="scards sm">' + sl + '</div>' if sl else '') + '</div>'
                '<div class="rv d1"><div class="apics">' + photos + '</div></div></div></section>'
                '<section class="sec gray"><div class="wrap"><div class="head rv"><div><span class="en">What We Do</span><h2>' + n + '에서도 <em>이런 행사</em>를 맡습니다</h2></div></div><ul class="asvc">' + svc + '</ul>'
                '<p class="snote">다른 지역: ' + others + ' · <a href="@@areas/index.html">운영 지역 전체</a></p></div></section>' + cta(n + ' 행사 날짜가 잡히셨나요?'))
        urls.append(page('areas/' + a['slug'] + '.html', title, desc, main, img=pic(a['photos'][0], True)))
    # 운영 지역 목록 — 대문 지도 SVG 를 그대로 쓴다
    idx = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
    m = re.search(r'<!--MAP-->(.*?)<!--/MAP-->', idx, re.S)
    svg = m.group(1).replace('href="assets/', 'href="../assets/') if m else ''
    rows = ''.join('<a class="arow" href="@@areas/' + a['slug'] + '.html"><b>' + a['name'] + '</b><span>' + ('본사' if a.get('hq') else '차로 약 ' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km') + '</span><em>' + (E(a['done'][0]) if a['done'] else '출장 진행') + '</em></a>' for a in AREAS)
    main = ('<section class="phead" style="background-image:url(' + pic('m01', True) + ')"><div class="wrap"><p class="crumb"><a href="index.html">홈</a> · <b>운영 지역</b></p><h1>운영 지역</h1><p>안산 본사에서 출발해 경기 어디든 달려갑니다. 지역을 누르면 그 지역에서 한 행사와 이동 시간을 보실 수 있습니다.</p></div></section>'
            '<section class="sec"><div class="wrap area2"><div class="mapbox go rv" id="gmap">' + svg + '<p class="src">지도: 통계청 행정구역 경계 · 선은 실제 도로가 아닌 방향 표시입니다.</p></div><div class="rv d1"><div class="arows">' + rows + '</div><p class="note">이동 시간은 본사에서 각 시청까지 차로 걸리는 시간(막히지 않을 때 기준)입니다. 표에 없는 지역도 전화 주시면 상담해 드립니다.</p></div></div></section>' + cta())
    urls.insert(0, page('areas/index.html', '운영 지역 | 바로기획 — 안산 · 화성 · 수원 · 시흥 · 용인 · 안양 · 광명 · 평택 행사대행', '안산 본사에서 경기 어디든. 지역별 이동 시간과 그 지역에서 한 행사를 보실 수 있습니다.', main, img=pic('m01', True)))
    return urls


def fix_same_folder(path_prefix):
    """@@stories/x.html 같은 표시를 실제 상대 경로로(두 폴더 모두 한 단계 아래라 ../ 로 통일)."""
    for d in ('stories', 'areas'):
        for f in os.listdir(os.path.join(SITE, d)):
            p = os.path.join(SITE, d, f)
            s = open(p, encoding='utf-8').read()
            s = s.replace('../@@', '../').replace('@@', '../')
            open(p, 'w', encoding='utf-8', newline='\n').write(s)


def sitemap(extra):
    today = datetime.date.today().isoformat()
    pages = ['', 'about.html', 'service.html', 'portfolio.html', 'notice.html', 'contact.html', 'quote.html']
    urls = [BASE + p for p in pages] + extra
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + u + '</loc><lastmod>' + today + '</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)


if __name__ == '__main__':
    a = story_pages(); b = area_pages(); fix_same_folder(None); sitemap(a + b)
    print('행사 이야기', len(a), '· 지역', len(b), '· sitemap.xml 갱신')
