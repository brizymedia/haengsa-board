# -*- coding: utf-8 -*-
"""로컬 미리보기 서버 — site/ 폴더를 그대로 띄운다.

  python serve.py          # http://localhost:8000
  python serve.py 8899     # 포트 지정
"""
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        # events.json 이 배치로 갱신되므로 캐시를 끈다
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass    # 조용히


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), Handler) as srv:
        print(f"http://localhost:{PORT}  (중단: Ctrl+C)")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
