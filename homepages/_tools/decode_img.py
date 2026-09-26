"""Firecrawl 결과 파일(weserv encoding=base64)에서 사진을 꺼내 저장한다.

사용: python decode_img.py <firecrawl 결과 .txt 또는 JSON 문자열 파일> <저장할 경로.webp>
네이버 사진 서버(pstatic)는 이 환경에서 직접 못 받는다. 그래서
  https://images.weserv.nl/?url=postfiles.pstatic.net/<경로>?type=w966&w=1600&output=webp&q=82&encoding=base64
를 Firecrawl(formats=["rawHtml"])로 긁고, 그 결과 파일을 이 스크립트로 푼다.
"""
import base64, json, re, sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
raw = open(src, encoding='utf-8').read()
try:
    raw = json.loads(raw).get('rawHtml', raw)
except Exception:
    pass
m = re.search(r'data:image/\w+;base64,([A-Za-z0-9+/=]+)', raw)
if not m:
    sys.exit('사진 데이터가 없습니다: ' + src)
open(dst, 'wb').write(base64.b64decode(m.group(1)))
im = Image.open(dst)
print(dst, im.size)
