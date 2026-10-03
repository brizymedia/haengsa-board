# -*- coding: utf-8 -*-
"""
행사 이야기(stories/) · 지역 페이지(areas/) 만들기 — 사이트 틀(머리글 · 푸터)은 notice.html 에서 빌려 온다.
(바로기획 tools/make_pages.py 를 예그리나 틀 · 색 · 내용으로 옮긴 것)

  python tools/make_pages.py

내용은 아래 STORIES · AREAS 표만 고치면 된다. 사실만 적을 것(블로그 원문 · 회사 제출 자료 · 대표님 확인분).
만든 뒤 sitemap.xml 도 같이 다시 쓴다.
"""
import os, re, html, datetime

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://brizymedia.github.io/yegrina/'
BLOG = 'https://blog.naver.com/yegrinai/'
NAME = '한국체대 예그리나'
TEL = '02-482-1934'
E = html.escape

# ── 행사 이야기 ──────────────────────────────────────────────
# 근거: 네이버 블로그 원문(blog 칸의 글 번호). date 는 블로그에 올린 달. 블로그에 장소 · 기관명이 없어 area 는 비움(None).
STORIES = [
    dict(slug='church-sports-day', title='전교인 체육대회 — 영아부부터 어르신까지 온 세대가 함께', cat='교회 체육대회', date='2026.06', place='교회 전교인 · 실내 체육관', area=None,
         lead='자체적으로 준비하시다 막힌 부분이 있어 연락 주신 교회였습니다. 준비는 예그리나가 모두 맡고, 성도님들은 오셔서 즐기시기만 하면 되도록 진행했습니다.',
         facts=[('행사', '교회 전교인 체육대회'), ('참가', '영아부 · 유치부 · 초등아동부 · 중고등부 · 청년부 · 어르신'), ('맡은 일', '프로그램 구성 · 사회 · 게임 진행 · 준비 일체')],
         body=['교회 체육대회는 유치원이나 학교 운동회와 달리 모든 연령이 한자리에 모입니다. 그래서 어느 한쪽으로 치우치지 않도록 연령 · 인원 · 공간에 맞춰 프로그램을 짰습니다.',
               '영아부 · 유치부 · 초등아동부 · 중고등부 · 청년부 부서별 게임과 교구별 게임, 그리고 전교인이 다 함께하는 단체 경기로 이어졌습니다.',
               '처음엔 어색하던 분들이 어느새 서로 배려하며 함께 웃고 응원하는 모습으로 하루를 마쳤습니다.'],
         photos=['w11', 'w13', 'w14', 'w15', 'w12', 'w16'], blog='224330870862', quote=['p3', 'f1', 'f2', 'h8', 'h9']),
    dict(slug='elementary-sports-day', title='초등학교 운동회 — 학교마다 다른 운동장, 맞춤 프로그램', cat='초등학교 운동회', date='2026.03', place='초등학교 운동장 · 체육관', area=None,
         lead='여러 초등학교에서 해마다 다시 불러 주시는 운동회입니다. 승패보다 학생 · 학부모 · 교직원이 함께 웃는 운동회를 목표로 준비합니다.',
         facts=[('행사', '초등학교 운동회'), ('프로그램', '준비운동 · 학년별 프로그램 · 단체게임 · 부모님 경기'), ('맞춘 것', '운동장 환경 · 참여 인원 · 실내/실외/우천 · 예산')],
         body=['운동회는 준비운동부터 학년별 프로그램, 단체게임과 부모님 경기까지 모든 순서가 시간에 맞춰 자연스럽게 이어져야 합니다. 아이들이 자연스럽게 참여하도록 이끌고, 무엇보다 안전하게 진행합니다.',
               '소규모 학교부터 전교생이 많은 학교까지, 운동장 환경과 참여 인원, 실내 · 실외 · 우천 상황과 예산을 함께 보고 학교마다 프로그램을 맞춥니다.'],
         photos=['w01', 'w02', 'w03', 'w04'], blog='224207058180', quote=['p2', 'h8', 'h9', 'f1', 'd1']),
    dict(slug='yearly-kindergarten-sports', title='5년 · 10년째 찾는 원의 체육대회 — 해마다 다른 게임으로', cat='어린이집 · 유치원 체육대회', date='2025.07', place='어린이집 · 유치원', area=None,
         lead='5년 이상, 10년 이상 계속 불러 주시는 원들이 있습니다. 3년째가 되면 「그 프로그램이 그 프로그램」이 되기 쉬워, 해마다 게임을 바꿔 준비합니다.',
         facts=[('행사', '어린이집 · 유치원 체육대회 · 운동회'), ('함께한 기간', '5년 이상 · 10년 이상 이어진 원'), ('준비 방식', '호응 좋았던 기본 틀은 유지 · 게임만 해마다 수정')],
         body=['아무 프로그램이나 새로 넣으면 흐름이 깨지거나 다치는 일이 생길 수 있습니다. 그래서 가장 호응이 좋았던 기본 틀은 그대로 두고, 해마다 게임만 바꿔 겹치지 않게 진행합니다.',
               '원에서 원하시는 방법과 프로그램, 원하시는 방향에 맞춰 준비해 찾아갑니다.'],
         photos=['w07', 'w08'], blog='223928519118', quote=['p1', 'h8', 'f2']),
    dict(slug='bible-school-water-play', title='여름성경학교 물놀이 — 4 · 5세를 위한 낮은 수영장', cat='물놀이 행사', date='2024.07', place='교회 여름성경학교', area=None,
         lead='장마철이라 비 예보가 있었지만 맑은 날씨 속에 진행했습니다. 4 · 5세 어린 친구들을 위해 낮은 수영장을 여러 개 준비했습니다.',
         facts=[('행사', '교회 여름성경학교 물놀이'), ('대상', '4 · 5세 어린 친구들'), ('준비한 것', '유아용 낮은 수영장 여러 개 · 슬라이드 · 환영 아치 · 포토존 · 에어아바타')],
         body=['물놀이는 점심 식사 뒤 오후에 시작하는 순서라, 새벽에 일찍 도착해 수영장과 슬라이드 자리를 먼저 잡고 물을 받기 시작했습니다.',
               '물이 차는 동안 여름성경학교 입구에 환영 아치와 포토존 아치를 꾸몄고, 새로 들인 에어아바타 꿀벌도 이날 처음 선보였습니다.',
               '어린 친구들 물놀이라 낮은 슬라이드와 수영장을 부모님들이 특히 마음에 들어 하셨습니다.'],
         photos=['w19', 'w20', 'w21'], blog='223514941397', quote=['p5', 'h3', 'h4', 'h5', 'h7']),
    dict(slug='rain-indoor-playground', title='비 예보에 하루 전 실내놀이터로 — 유치부 여름성경학교', cat='놀이기구 렌탈', date='2024.07', place='교회 실내 + 야외 한쪽', area=None,
         lead='행사 하루 전, 당일 새벽부터 낙뢰를 동반한 집중호우가 온다는 예보가 나와 야외 수영장 물놀이를 실내놀이터로 바꿨습니다.',
         facts=[('행사', '교회 유치부 여름성경학교'), ('바꾼 것', '야외 수영장 물놀이 → 실내놀이터 (하루 전)'), ('준비한 것', '놀이바운스 · 바이킹 · 자이언트 빅블럭 · 너프건 사격장 · 작은 슬라이드')],
         body=['유치부 어린 친구들은 비를 조금만 맞아도 감기에 걸릴 수 있어, 하루 전 연락을 받고 실내놀이터로 바꿨습니다. 하루 전에만 말씀해 주시면 이렇게 바꿔 드립니다.',
               '그런데 당일에는 비가 조금도 오지 않았습니다. 그래서 가져간 작은 슬라이드를 야외 한쪽에 깔아, 물놀이를 기다리던 친구들도 놀 수 있게 했습니다.',
               '실내 한쪽에는 신나게 뛰어놀 놀이바운스와 바이킹을, 다른 한쪽에는 쉬어 가며 놀 수 있는 자이언트 빅블럭과 너프건 사격장을 꾸몄습니다.'],
         photos=['w22', 'w23'], blog='223526106582', quote=['h2', 'h1', 'h3']),
]

# ── 지역 ────────────────────────────────────────────────────
# 분 · km: 사무실(남양주 별내면 청학리)에서 각 시청 · 구청까지 OSRM(막히지 않을 때) 2026-10-03 조회, 5분 단위 반올림
# done(그 지역에서 한 행사)은 기록이 있을 때만 — 지금은 블로그에 지역이 적힌 글이 없어 모두 비어 있음
AREAS = [
    dict(slug='namyangju', name='남양주', to='', min=0, km=0, hq=True, done=[], photos=['w05', 'w24', 'w09']),
    dict(slug='uijeongbu', name='의정부', to='의정부시청', min=10, km=8.3, done=[], photos=['w01', 'w03', 'w06']),
    dict(slug='nowon', name='노원구', to='노원구청', min=15, km=9.9, done=[], photos=['w09', 'w10', 'w26']),
    dict(slug='yangju', name='양주', to='양주시청', min=15, km=11.9, done=[], photos=['w07', 'w08', 'w02']),
    dict(slug='guri', name='구리', to='구리시청', min=20, km=16.2, done=[], photos=['w22', 'w23', 'w24']),
    dict(slug='jungnang', name='중랑구', to='중랑구청', min=20, km=14.5, done=[], photos=['w17', 'w18', 'w12']),
    dict(slug='hanam', name='하남', to='하남시청', min=25, km=24.5, done=[], photos=['w19', 'w20', 'w21']),
    dict(slug='pocheon', name='포천', to='포천시청', min=25, km=26.9, done=[], photos=['w04', 'w02', 'w03']),
    dict(slug='gangdong', name='강동구', to='강동구청', min=25, km=25.3, done=[], photos=['w11', 'w14', 'w27']),
]

SERVICES = [('어린이집 · 유치원 운동회', '가족한마음 체육대회 · 실내 체육관 운동회'), ('초등학교 운동회', '학년별 프로그램 · 단체게임 · 부모님 경기'),
            ('교회 전교인 체육대회', '부서별 · 교구별 게임 · 전교인 단체 경기'), ('발표회 · 재롱잔치 사회', '분위기 게임 · 돌발 상황까지 챙기는 진행'),
            ('여름 물놀이 행사', '에어 워터슬라이드 · 유아용 수영장 · 환영 아치'), ('유아체육 수업 · 놀이기구 렌탈', '동화체육 · 파라슈트 · 에어바운스 · 실내놀이터')]

SVG_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
SVG_QUOTE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 16h5"/></svg>'
SVG_MSG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/></svg>'


def shell():
    s = open(os.path.join(SITE, 'notice.html'), encoding='utf-8').read()
    head_end = s.index('<main>')
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
    top = re.sub(r'<meta property="og:image:(width|height)"[^>]*>\n?', '', top)        # 그림 크기가 og.jpg 와 다르다
    top = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>\n?', '', top, flags=re.S)
    top = re.sub(r'<meta name="yg-edit"[^>]*>\n?', '', top)              # 대표님 수정 모드는 기본 8쪽에만
    top = top.replace(' class="act"', '').replace('class="act" ', '')
    bottom = re.sub(r'<script src="assets/edit\.js[^"]*"></script>\n?', '', bottom)
    out = top + '<main>\n' + main + '\n</main>' + bottom
    pre = '../' * depth
    out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|sms:|#|/|\.\./|data:)([^"]+)"', lambda m: m.group(1) + '="' + pre + m.group(2) + '"', out)
    out = re.sub(r"url\((?!https?:)(assets/[^)]+)\)", lambda m: 'url(' + pre + m.group(1) + ')', out)
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(out)
    return url


def pic(f, big=False):
    return 'assets/img/works/' + ('' if big else 's/') + f + '.webp'


def phead(bg, crumbs, h1, p):
    c = '<a href="index.html">HOME</a>' + ''.join('<span>›</span>' + (('<a href="' + h + '">' + E(t) + '</a>') if h else '<span>' + E(t) + '</span>') for t, h in crumbs)
    return ('<section class="ph-head"><div class="bg" style="background-image:url(' + pic(bg, True) + ')"></div><div class="wrap">'
            '<div class="crumb">' + c + '</div><h1>' + E(h1) + '</h1><p>' + E(p) + '</p></div></section>')


def cta(title='행사 날짜가 정해졌다면', sub='날짜 · 장소(실내/야외) · 인원만 알려 주셔도 프로그램과 참고 비용을 안내해 드립니다.'):
    return ('<section class="sec" style="padding-top:0"><div class="wrap"><div class="cta rv"><div class="confetti" aria-hidden="true"></div>'
            '<div style="position:relative;z-index:1"><h2>' + E(title) + '<br>예그리나가 준비합니다.</h2><p>' + E(sub) + '</p></div>'
            '<div class="ways">'
            '<a href="tel:' + TEL + '"><span class="ic">' + SVG_TEL + '</span><span><small>대표전화 · 평일 11~19시</small>' + TEL + '</span></a>'
            '<a href="quote.html"><span class="ic">' + SVG_QUOTE + '</span><span><small>항목만 골라 문의</small>자동 견적서</span></a>'
            '<a href="contact.html"><span class="ic">' + SVG_MSG + '</span><span><small>홈페이지 문의 폼</small>예약 · 문의 남기기</span></a>'
            '</div></div></div></section>')


def scard(o, cls='scard', long=False):
    meta = o['cat'] + ' · ' + o['date'] + (' · ' + o['place'] if long else '')
    return ('<a class="' + cls + '" href="@@stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(meta) + '</small>' + E(o['title']) +
            ('<em>' + E(o['lead'][:60]) + '…</em>' if long else '') + '</span></a>')


def story_pages():
    urls = []
    for st in STORIES:
        facts = ''.join('<dt>' + E(a) + '</dt><dd>' + E(b) + '</dd>' for a, b in st['facts'])
        body = ''.join('<p>' + E(p) + '</p>' for p in st['body'])
        photos = ''.join('<a href="' + pic(f, True) + '" target="_blank" rel="noopener"><img src="' + pic(f) + '" alt="' + E(st['title']) + ' 현장" loading="lazy" width="800" height="600"></a>' for f in st['photos'])
        area = next((a for a in AREAS if a['slug'] == st['area']), None) if st['area'] else None
        alink = ('<a class="alink" href="@@areas/' + area['slug'] + '.html">' + E(area['name']) + ' 행사 안내 →</a>') if area else '<a class="alink" href="@@areas/index.html">운영 지역 · 이동 시간 →</a>'
        others = [o for o in STORIES if o['slug'] != st['slug']][:3]
        more = ''.join(scard(o) for o in others)
        blog = ('<a class="btn btn-line" href="' + BLOG + st['blog'] + '" target="_blank" rel="noopener">블로그 원문 보기 ↗</a>') if st['blog'] else ''
        main = (phead(st['photos'][0], [('행사 이야기', '@@stories/index.html'), (st['cat'], '')], st['title'], st['lead']) +
                '<section class="sec"><div class="wrap story">'
                '<aside class="rv"><span class="kicker">Event File</span><dl>' + facts + '<dt>기록</dt><dd>' + E(st['date']) + ' 블로그</dd></dl>'
                '<a class="btn btn-sun" href="quote.html">비슷한 행사 견적 받기</a>' + alink + '</aside>'
                '<div class="rv sbody" style="--d:.1s">' + body + '<div class="sgrid">' + photos + '</div><div class="sbtns">' + blog + '<a class="btn btn-line" href="portfolio.html">현장사진 더 보기</a></div></div>'
                '</div></section>'
                '<section class="sec mint"><div class="wrap"><div class="sec-h rv"><span class="kicker">More Stories</span><h2>다른 <em>현장 이야기</em></h2></div><div class="scards">' + more + '</div>'
                '<p class="snote"><a href="@@stories/index.html">행사 이야기 전체 보기 →</a></p></div></section>'
                + cta())
        urls.append(page('stories/' + st['slug'] + '.html', st['title'] + ' | ' + NAME + ' 행사 이야기', st['lead'][:120], main, img=pic(st['photos'][0], True)))
    cards = ''.join(scard(o, 'scard rv', True) for o in STORIES)
    main = (phead('w05', [('행사 이야기', '')], '행사 이야기', '예그리나가 준비한 행사를 한 편씩 기록했습니다. 어떤 준비를 했는지, 현장에서 무엇이 있었는지 사진과 함께 보실 수 있습니다.') +
            '<section class="sec"><div class="wrap"><div class="scards big">' + cards + '</div><p class="snote">더 많은 현장 기록은 <a href="' + BLOG + '" target="_blank" rel="noopener">예그리나 네이버 블로그</a>에 있습니다.</p></div></section>' + cta())
    urls.insert(0, page('stories/index.html', '행사 이야기 | ' + NAME + ' — 운동회 · 전교인 체육대회 · 물놀이 · 실내놀이터 현장 기록',
                        '예그리나가 준비한 행사를 한 편씩 기록했습니다. 교회 전교인 체육대회, 초등학교 운동회, 유치원 체육대회, 여름성경학교 물놀이, 실내놀이터 렌탈 현장.', main, img=pic('w05', True)))
    return urls


def area_pages():
    urls = []
    for a in AREAS:
        n = a['name']
        if a.get('hq'):
            how = '<b>' + NAME + ' 사무실</b>이 있는 곳입니다. 경기도 남양주시 별내면 청학리 346-1, 301호 — 방문 상담은 미리 전화로 약속해 주세요.'
        else:
            how = '남양주 별내 사무실에서 ' + a['to'] + '까지 차로 약 <b>' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km</b>(막히지 않을 때 기준)입니다. 행사 당일 일찍 도착해 장비 자리를 잡고 세팅합니다.'
        if a['done']:
            done = '<ul class="alist">' + ''.join('<li>' + E(x) + '</li>' for x in a['done']) + '</ul>'
        else:
            done = '<p class="muted">아직 이 페이지에 적을 만큼 정리된 기록이 없습니다. ' + n + ' 행사도 남양주 사무실에서 출발해 똑같이 준비합니다.</p>'
        stories = [s for s in STORIES if s['area'] == a['slug']]
        sl = ''.join(scard(s) for s in stories)
        svc = ''.join('<li><b>' + E(x) + '</b><span>' + E(y) + '</span></li>' for x, y in SERVICES)
        photos = ''.join('<img src="' + pic(f) + '" alt="' + NAME + ' 행사 현장" loading="lazy" width="800" height="600">' for f in a['photos'])
        others = ' · '.join('<a href="@@areas/' + o['slug'] + '.html">' + o['name'] + '</a>' for o in AREAS if o['slug'] != a['slug'])
        title = n + ' 운동회 · 체육대회 · 물놀이 · 놀이기구 렌탈 | ' + NAME
        desc = n + ' 어린이집 · 유치원 · 초등학교 운동회, 교회 전교인 체육대회, 발표회 사회, 여름 물놀이, 에어바운스 렌탈, 유아체육 수업. ' + ('남양주 별내 사무실 — 2014년부터.' if a.get('hq') else '남양주 별내에서 차로 약 ' + str(a['min']) + '분. 2014년부터 어린이 행사를 준비해 온 ' + NAME + '.')
        main = (phead(a['photos'][0], [('운영 지역', '@@areas/index.html'), (n, '')], n + ' 행사, 예그리나가 갑니다',
                      '운동회 · 전교인 체육대회 · 발표회 사회 · 물놀이 · 놀이기구 렌탈 · 유아체육 수업. 2014년부터 어린이 행사를 준비해 온 예그리나가 ' + n + ' 현장도 처음부터 끝까지 챙깁니다.') +
                '<section class="sec"><div class="wrap area3"><div class="rv"><span class="kicker">How Far</span><h2 class="h2s">' + n + (' — 사무실' if a.get('hq') else '까지') + '</h2><p>' + how + '</p>'
                '<h3 class="h3s">' + n + '에서 한 행사</h3>' + done + ('<div class="scards sm">' + sl + '</div>' if sl else '') + '</div>'
                '<div class="rv" style="--d:.1s"><div class="apics">' + photos + '</div></div></div></section>'
                '<section class="sec mint"><div class="wrap"><div class="sec-h rv"><span class="kicker">What We Do</span><h2>' + n + '에서도 <em>이런 일</em>을 맡습니다</h2></div><ul class="asvc">' + svc + '</ul>'
                '<p class="snote">다른 지역: ' + others + ' · <a href="@@areas/index.html">운영 지역 전체</a></p></div></section>' + cta(n + ' 행사 날짜가 정해졌다면'))
        urls.append(page('areas/' + a['slug'] + '.html', title, desc, main, img=pic(a['photos'][0], True)))
    rows = ''.join('<a class="arow" href="@@areas/' + a['slug'] + '.html"><b>' + a['name'] + '</b><span>' + ('사무실' if a.get('hq') else '차로 약 ' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km') + '</span><em>' + (E(a['done'][0]) if a['done'] else ('남양주 별내면 청학리' if a.get('hq') else a['to'] + '까지')) + '</em></a>' for a in AREAS)
    main = (phead('w01', [('운영 지역', '')], '운영 지역', '남양주 별내 사무실에서 출발해 서울 · 경기 어디든 찾아갑니다. 지역을 누르면 이동 시간과 그 지역 안내를 보실 수 있습니다.') +
            '<section class="sec"><div class="wrap"><div class="sec-h rv"><span class="kicker">Areas</span><h2>사무실에서 <em>가까운 곳</em>부터</h2><p>이동 시간은 남양주 별내 사무실에서 각 시청 · 구청까지 차로 걸리는 시간(막히지 않을 때 기준)입니다. 출퇴근 시간에는 더 걸릴 수 있습니다.</p></div>'
            '<div class="arows rv">' + rows + '</div><p class="snote">표에 없는 지역도 전화 주시면 상담해 드립니다 · <a href="tel:' + TEL + '">' + TEL + '</a></p></div></section>' + cta())
    urls.insert(0, page('areas/index.html', '운영 지역 | ' + NAME + ' — 남양주 · 의정부 · 노원 · 양주 · 구리 · 중랑 · 하남 · 포천 · 강동',
                        '남양주 별내 사무실에서 서울 · 경기 어디든. 지역별 이동 시간과 하는 일을 보실 수 있습니다.', main, img=pic('w01', True)))
    return urls


def fix_same_folder():
    """@@stories/x.html 같은 표시를 실제 상대 경로로(두 폴더 모두 한 단계 아래라 ../ 로 통일)."""
    for d in ('stories', 'areas'):
        for f in os.listdir(os.path.join(SITE, d)):
            p = os.path.join(SITE, d, f)
            s = open(p, encoding='utf-8').read()
            s = s.replace('../@@', '../').replace('@@', '../')
            open(p, 'w', encoding='utf-8', newline='\n').write(s)


def sitemap(extra):
    today = datetime.date.today().isoformat()
    pages = ['', 'about.html', 'service.html', 'portfolio.html', 'video.html', 'notice.html', 'recruit.html', 'contact.html', 'quote.html']
    urls = [BASE + p for p in pages] + extra
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + u + '</loc><lastmod>' + today + '</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)


if __name__ == '__main__':
    a = story_pages(); b = area_pages(); fix_same_folder(); sitemap(a + b)
    print('행사 이야기', len(a), '· 지역', len(b), '· sitemap.xml 갱신')
