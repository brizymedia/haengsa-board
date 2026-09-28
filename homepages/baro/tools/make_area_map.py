# -*- coding: utf-8 -*-
"""
대문 「운영 지역」 경기도 지도 SVG 만들기 — 결과를 index.html 의 <!--MAP--> … <!--/MAP--> 사이에 넣는다.

  python tools/make_area_map.py        (pip install shapely requests 필요)

지도 데이터: southkorea/southkorea-maps (통계청 2013 시군구 경계, 간략본)
  https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_municipalities_geo_simple.json
위치: 사무실 · 각 시청 좌표는 OpenStreetMap(Nominatim) 2026-09-28 조회값.
이동 시간은 OSRM(막히지 않을 때 기준) 조회값을 5분 단위로 반올림해 index.html 목록에 손으로 적었다.
"""
import json, os, re, io, urllib.request
from shapely.geometry import shape, box, Point
from shapely.ops import unary_union

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_municipalities_geo_simple.json'

LON0, LON1, LAT0, LAT1 = 126.56, 127.27, 36.93, 37.56
K = 1000 / (LAT1 - LAT0) * 0.62          # 세로 약 620
COS = 0.7955                              # cos(37.3°)
def xy(lon, lat): return ((lon - LON0) * COS * K, (LAT1 - lat) * K)
VW, VH = xy(LON1, LAT0)

# 사무실 · 도시 표시점 (OSM 좌표)
OFFICE = (126.8540, 37.2829)
PTS = {  # key: (lon, lat, 이름)
    'hwaseong': (126.8206, 37.1897, '화성'), 'suwon': (127.0319, 37.2616, '수원'), 'anyang': (126.9569, 37.3943, '안양'),
    'siheung': (126.8057, 37.3821, '시흥'), 'gwangmyeong': (126.8646, 37.4786, '광명'), 'dongtan': (127.0956, 37.2004, '동탄'),
    'yongin': (127.1776, 37.2411, '용인'), 'pyeongtaek': (127.1130, 36.9914, '평택'),
}
GROUP = {'3101': 'suwon', '3102': 'seongnam', '3104': 'anyang', '3105': 'bucheon', '3109': 'ansan', '3110': 'goyang', '3119': 'yongin'}
BYCODE = {'31240': 'hwaseong', '31150': 'siheung', '31060': 'gwangmyeong', '31070': 'pyeongtaek', '31140': 'osan', '31160': 'gunpo',
          '31170': 'uiwang', '31110': 'gwacheon', '31250': 'gwangju', '31220': 'anseong', '31180': 'hanam', '31230': 'gimpo'}
ACTIVE = {'hwaseong', 'suwon', 'anyang', 'siheung', 'gwangmyeong', 'yongin', 'pyeongtaek'}
FADED_LABEL = {'seoul': ('서울', 126.93, 37.515), 'incheon': ('인천', 126.70, 37.47), 'bucheon': ('부천', 126.78, 37.50), 'gunpo': ('군포', 126.925, 37.345),
               'uiwang': ('의왕', 126.985, 37.35), 'gwacheon': ('과천', 127.0, 37.43), 'seongnam': ('성남', 127.12, 37.41), 'osan': ('오산', 127.055, 37.155),
               'anseong': ('안성', 127.23, 37.02), 'gwangju': ('광주', 127.24, 37.39)}

def key(code):
    if code[:2] == '11': return 'seoul'
    if code[:2] == '23': return 'incheon'
    if code[:2] in ('33', '34'): return 'other'
    return BYCODE.get(code) or GROUP.get(code[:4]) or 'gg'

def path(geom):
    polys = [geom] if geom.geom_type == 'Polygon' else list(geom.geoms)
    out = []
    for p in polys:
        if p.area < 2e-6: continue
        for ring in [p.exterior] + list(p.interiors):
            pts = [xy(x, y) for x, y in ring.coords]
            out.append('M' + 'L'.join('%.1f,%.1f' % q for q in pts) + 'Z')
    return ''.join(out)

def main():
    d = json.load(io.TextIOWrapper(urllib.request.urlopen(URL), encoding='utf-8'))
    win = box(LON0, LAT0, LON1, LAT1)
    groups = {}
    for f in d['features']:
        g = shape(f['geometry'])
        if not g.intersects(win): continue
        groups.setdefault(key(f['properties']['code']), []).append(g.intersection(win))
    ox, oy = xy(*OFFICE)
    svg = ['<svg class="gmap" viewBox="0 0 %d %d" role="img" aria-label="바로기획 운영 지역 지도 — 안산 본사에서 화성 · 수원 · 안양 · 시흥 · 광명 · 동탄 · 용인 · 평택까지">' % (VW, VH)]
    svg.append('<defs><radialGradient id="gmGlow"><stop offset="0" stop-color="#E3C57E" stop-opacity=".55"/><stop offset="1" stop-color="#E3C57E" stop-opacity="0"/></radialGradient></defs>')
    svg.append('<g class="land">')
    order = sorted(groups, key=lambda k: (k == 'ansan', k in ACTIVE))
    for k in order:
        geom = unary_union(groups[k]).simplify(0.0008, preserve_topology=True)
        cls = 'hq' if k == 'ansan' else ('on' if k in ACTIVE else ('far' if k in ('other',) else 'off'))
        svg.append('<path class="%s" data-c="%s" d="%s"/>' % (cls, k, path(geom)))
    svg.append('</g>')
    for k, (nm, lon, lat) in FADED_LABEL.items():
        x, y = xy(lon, lat); svg.append('<text class="lf" x="%.0f" y="%.0f">%s</text>' % (x, y, nm))
    svg.append('<text class="sea" x="%.0f" y="%.0f">서 해</text>' % xy(126.60, 37.12))
    svg.append('<g class="routes">')
    for k, (lon, lat, nm) in PTS.items():
        x, y = xy(lon, lat)
        mx, my = (ox + x) / 2, (oy + y) / 2
        dx, dy = x - ox, y - oy
        cx, cy = mx - dy * .18, my + dx * .18          # 살짝 휜 선
        svg.append('<path class="rt" data-c="%s" d="M%.1f,%.1fQ%.1f,%.1f %.1f,%.1f" pathLength="1"/>' % (k, ox, oy, cx, cy, x, y))
    svg.append('</g><g class="pins">')
    for k, (lon, lat, nm) in PTS.items():
        x, y = xy(lon, lat)
        svg.append('<g class="pin" data-c="%s" transform="translate(%.1f %.1f)"><circle r="11" class="halo"/><circle r="5.5"/><text y="-17">%s</text></g>' % (k, x, y, nm))
    svg.append('<g class="hqpin" transform="translate(%.1f %.1f)"><circle r="46" fill="url(#gmGlow)" class="pulse"/><circle r="21" class="ring"/><image href="assets/img/logo-mark.svg" x="-17" y="-17" width="34" height="34"/><text y="44">안산 본사</text></g>' % (ox, oy))
    svg.append('</g></svg>')
    out = ''.join(svg)
    p = os.path.join(SITE, 'index.html'); s = open(p, encoding='utf-8').read()
    s2 = re.sub(r'<!--MAP-->.*?<!--/MAP-->', lambda m: '<!--MAP-->' + out + '<!--/MAP-->', s, flags=re.S)
    if s2 == s: raise SystemExit('index.html 에 <!--MAP--> 표시가 없습니다.')
    open(p, 'w', encoding='utf-8', newline='\n').write(s2)
    print('지도 넣음: %d 글자, %dx%d' % (len(out), VW, VH))

if __name__ == '__main__':
    main()
