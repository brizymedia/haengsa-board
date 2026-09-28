# -*- coding: utf-8 -*-
"""
바로기획 로고(C안 · 빨리감기 B) SVG 만들기 — 글자는 도형(아웃라인)으로 바꿔 넣는다.
  python tools/make_logo.py "<Pretendard-Black.otf 경로>" "<Montserrat-BlackItalic.ttf 경로>"
만드는 파일: assets/img/logo-mark.svg · logo-mark-white.svg · favicon.svg · logo-h.svg · logo-h-white.svg · logo-v.svg
"""
import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, 'assets', 'img')
NAVY, GOLD, GOLD2, INK, WHITE = '#0E1F3F', '#C9A24B', '#E3C57E', '#131A2A', '#FFFFFF'
GOLD_T = '#B08A36'   # 흰 바탕 위 금색 글자(조금 진하게)

def text_path(font, s, size, x, y, skew=0.0, track=0.0):
    """글자 s 를 (x, y=기준선) 에 size px 로. skew: 오른쪽으로 기울기(tan)."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
    k = size / upm; d = []; cx = x
    for ch in s:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        # 글꼴 좌표(y 위로) → SVG(y 아래로) + 기울임
        tp = TransformPen(pen, (k, 0, k * skew, -k, cx, y))
        gs[g].draw(tp)
        d.append(pen.getCommands())
        cx += gs[g].width * k + track
    return ' '.join(d), cx

def mark(bg, stem, chev1, chev2, lines):
    return ('<rect width="100" height="100" rx="24" fill="%s"/><g transform="translate(4 0)">'
            '<rect x="28" y="20" width="12" height="60" rx="2" fill="%s"/>'
            '<path d="M44 20h10l20 15-20 15H44l20-15z" fill="%s"/>'
            '<path d="M44 50h12l24 15-24 15H44l24-15z" fill="%s"/>'
            '<g fill="%s" opacity=".75"><rect x="8" y="33" width="14" height="4" rx="2"/><rect x="12" y="48" width="10" height="4" rx="2"/><rect x="6" y="63" width="16" height="4" rx="2"/></g></g>') % (bg, stem, chev1, chev2, lines)

def svg(vb, body): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">%s</svg>\n' % (vb, body)
def w(name, s): open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(s); print(name)

def main(pret, mont):
    kr, en = TTFont(pret), TTFont(mont)
    M = mark(NAVY, GOLD, GOLD, GOLD2, GOLD)
    MW = mark(WHITE, NAVY, NAVY, '#1D3A6B', GOLD)
    w('logo-mark.svg', svg('0 0 100 100', M)); w('favicon.svg', svg('0 0 100 100', M)); w('logo-mark-white.svg', svg('0 0 100 100', MW))
    SK = 0.18
    def lockup(dark):
        # 마크 64 + 글자
        a, x1 = text_path(kr, '바로', 40, 78, 40, SK, -1.6)
        b, x2 = text_path(kr, '기획', 40, x1, 40, SK, -1.6)
        c, x3 = text_path(en, 'BARO PLANNING', 9.2, 80, 56, 0, 1.9)
        body = '<g transform="scale(.64)">%s</g>' % (M if not dark else M.replace('rx="24" fill="%s"' % NAVY, 'rx="24" fill="%s" stroke="%s" stroke-opacity=".5" stroke-width="2"' % (NAVY, GOLD)))
        body += '<path fill="%s" d="%s"/><path fill="%s" d="%s"/><path fill="%s" d="%s"/>' % (GOLD2 if dark else GOLD_T, a, WHITE if dark else INK, b, GOLD2 if dark else '#6B7385', c)
        return svg('0 0 %d 64' % (max(x2, x3) + 4), body), int(max(x2, x3) + 4)
    s, W1 = lockup(False); w('logo-h.svg', s)
    s, W2 = lockup(True); w('logo-h-white.svg', s)
    # 세로형
    a, x1 = text_path(kr, '바로', 44, 0, 150, SK, -1.8); b, x2 = text_path(kr, '기획', 44, x1, 150, SK, -1.8)
    c, x3 = text_path(en, 'BARO PLANNING', 10.5, 0, 172, 0, 2.2)
    VW = 200; ox = (VW - x2) / 2; ox2 = (VW - x3) / 2
    body = '<g transform="translate(50 6)">%s</g><g transform="translate(%.1f 0)"><path fill="%s" d="%s"/><path fill="%s" d="%s"/></g><path transform="translate(%.1f 0)" fill="#6B7385" d="%s"/>' % (M, ox, GOLD_T, a, INK, b, ox2, c)
    w('logo-v.svg', svg('0 0 %d 182' % VW, body))
    print('WIDTH', W1, W2)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
