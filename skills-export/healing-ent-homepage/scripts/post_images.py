"""네이버 블로그 글(m.blog.naver.com/<id>/<글번호>)을 Firecrawl 로 긁은 결과 파일에서 사진 주소를 뽑는다.

사용: python post_images.py <firecrawl 결과 파일>
출력: 한 줄에 하나씩, decode 용 weserv 주소 (그대로 Firecrawl rawHtml 로 긁으면 된다)
"""
import json, re, sys
raw = open(sys.argv[1], encoding='utf-8').read()
try:
    d = json.loads(raw); raw = d.get('html') or d.get('rawHtml') or raw
except Exception:
    pass
seen, out = set(), []
for u in re.findall(r'https://(?:postfiles|blogfiles|mblogthumb-phinf|blogthumb)\.pstatic\.net/([^"\'?\s]+)', raw):
    if u in seen or not re.search(r'\.(jpe?g|png|webp)$', u, re.I):
        continue
    seen.add(u)
    out.append('https://images.weserv.nl/?url=postfiles.pstatic.net/' + u + '?type=w966&w=1600&output=webp&q=82&encoding=base64')
print('\n'.join(out))
print(f'# {len(out)}장', file=sys.stderr)
