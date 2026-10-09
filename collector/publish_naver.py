# -*- coding: utf-8 -*-
"""네이버 블로그(ty-health) 발행 — 어대리(Aside CLI)에게 시킨다.

큰길이벤트 저장소 `_column/naver/<파일>.json` 원고가 https://큰길이벤트.com/naver/ 에 올라온 뒤 쓴다.
그 페이지의 「제목 · 본문(링크·전화·태그 포함) · 사진」을 그대로 뽑아 어대리 작업 폴더에 놓고,
`aside exec` 로 네이버 글쓰기 화면에 넣어 발행하게 한다. 비밀번호 · 보안문자는 어대리가 입력하지 않는다
(이미 로그인된 ty-health 주인 계정만 쓰고, 아니면 멈춘다).

  python collector/publish_naver.py 2026-10-09-grant-application-event-prep.json
  python collector/publish_naver.py <파일> --prepare-only   # 발행하지 않고 준비만(제목·본문·사진·프롬프트)

같은 원고를 두 번 발행하지 않도록 collector/naver_published.json 에 기록한다(시작할 때 started, 끝나면 주소).
기록이 있는 원고는 거절한다 — 정말 다시 발행해야 하면 기록을 사람이 확인한 뒤 --force.
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "naver_published.json")
PAGE = "https://xn--wk0bn7yi8h24iszc.com/naver/"          # 큰길이벤트.com/naver/
DRAFTS = os.path.join(os.path.expanduser("~"), "Documents", "클로드코드", "_column", "naver")
ASIDE = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Aside", "CLI", "current", "aside.exe")
WORK = os.path.join(os.path.expanduser("~"), ".aside", "u", "0", "workspace", "naver-post")
BLOG = "https://blog.naver.com/ty-health"

PROMPT = """Task: publish ONE blog post on the Naver blog "ty-health" ({blog}). The owner of this blog (the user) has explicitly asked for this post to be published. The post content is already written and must be used exactly as given.

Files (UTF-8, in folder {work}\\):
- title.txt  : the post title (one line)
- body.txt   : the post body. Paragraphs are separated by blank lines. The markers "[사진 N]" (Korean for "[photo N]") show where to insert photo N. The LAST line of the file is a hashtag line (starts with #) - those are the tags.
{photos}
Steps:
1. Open the Naver blog write page: {blog}?Redirect=Write . If you are NOT already signed in to Naver as the owner of the ty-health blog, STOP immediately and report that. Never type or enter any password, ID, OTP or CAPTCHA answer; never create an account.
2. Title: type the exact text of title.txt into the title field.
3. Body: enter body.txt paragraph by paragraph, exactly as written, without changing, adding or removing any word. Do not include the final hashtag line in the body. At each "[사진 N]" marker, do not leave the marker text; instead upload the matching photo file (photoN.jpg) at that position using the editor's photo button (a local file upload). If the browser cannot upload straight from the folder above, copy the photo files to a folder it can read first and verify the copies are byte-identical. The URL line and the phone line must stay in the body as plain text.
4. Tags: put the hashtags of the last line of body.txt (without the # sign, one per tag) in the tag field of the publish settings panel.
5. Publish settings: public to everyone (전체공개), allow comments as the default, leave the category as the default. Then press the publish (발행) button.
6. After publishing, open the published post and verify: the title is exactly title.txt, every photo is visible, the first and last paragraphs match body.txt, the tags are present. Report the final post URL (https://blog.naver.com/ty-health/<number>) and anything that did not match.

If anything unexpected happens (login screen, security check/CAPTCHA, editor error, upload failure that you cannot fix, a draft-restore dialog), stop and report exactly what you see instead of improvising. Do not publish anything other than this one post. Do not edit or delete any existing posts.
"""


def load_state():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"_note": "네이버(ty-health)에 발행한(발행을 시작한) 원고 → 글 주소. publish_naver.py 가 쓴다.", "published": {}}


def save_state(st):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")


def fetch(url, tries=1):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (publish_naver; gilcaro@naver.com)"})
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(20)
    raise RuntimeError(f"{url} 를 못 읽었다: {last}")


def get_card(draft_title, wait_minutes=6):
    """/naver/ 페이지에서 그 제목의 카드를 찾는다(갤러리 워크플로가 페이지를 다시 만들 때까지 기다린다)."""
    end = time.time() + wait_minutes * 60
    while True:
        page = fetch(PAGE + "?t=%d" % int(time.time()), tries=2).decode("utf-8", "replace")
        for c in page.split('<article class="card">')[1:]:
            m = re.search(r'<h2 id="t(\d+)">(.*?)</h2>', c, re.S)
            if m and html.unescape(m.group(2)).strip() == draft_title:
                k = m.group(1)
                body = html.unescape(re.search(r'<pre class="body" id="b%s">(.*?)</pre>' % k, c, re.S).group(1))
                figs = [html.unescape(u) for u, _ in re.findall(r'<img src="([^"]+)" alt="([^"]*)"', c)]
                return draft_title, body, figs
        if time.time() > end:
            raise RuntimeError(f"{PAGE} 에 제목 「{draft_title}」 카드가 없다 — 푸시 후 갤러리 워크플로가 끝났는지 확인")
        time.sleep(30)


def prepare(name):
    path = os.path.join(DRAFTS, name)
    with open(path, encoding="utf-8") as f:
        draft = json.load(f)
    title, body, figs = get_card(draft["제목"])
    os.makedirs(WORK, exist_ok=True)
    for old in os.listdir(WORK):
        if re.fullmatch(r"(title\.txt|body\.txt|photo\d+\.\w+|prompt\.txt)", old):
            os.remove(os.path.join(WORK, old))
    with open(os.path.join(WORK, "title.txt"), "w", encoding="utf-8") as f:
        f.write(title)
    with open(os.path.join(WORK, "body.txt"), "w", encoding="utf-8") as f:
        f.write(body)
    plist = []
    for i, u in enumerate(figs, 1):
        fn = f"photo{i}.jpg"
        with open(os.path.join(WORK, fn), "wb") as f:
            f.write(fetch(u, tries=2))
        plist.append(f"- {fn} : photo to insert at the marker \"[사진 {i}]\"")
    n_markers = len(re.findall(r"\[사진 \d+\]", body))
    if n_markers != len(figs):
        raise RuntimeError(f"본문의 [사진 N] 표시({n_markers})와 사진 수({len(figs)})가 다르다")
    prompt = PROMPT.format(blog=BLOG, work=WORK, photos="\n".join(plist))
    with open(os.path.join(WORK, "prompt.txt"), "w", encoding="utf-8") as f:
        f.write(prompt)
    return title, prompt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft", help="_column/naver 안의 원고 파일 이름")
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(os.path.join(DRAFTS, a.draft)):
        print(f"원고가 없다: {os.path.join(DRAFTS, a.draft)}", file=sys.stderr)
        return 2
    st = load_state()
    if not a.prepare_only and a.draft in st["published"] and not a.force:
        print(f"이미 발행했거나 발행을 시작한 원고다: {a.draft} → {st['published'][a.draft]}", file=sys.stderr)
        return 3
    if not a.prepare_only and not os.path.exists(ASIDE):
        print(f"어대리(Aside CLI)를 못 찾았다: {ASIDE}", file=sys.stderr)
        return 4

    title, prompt = prepare(a.draft)
    print(f"준비 완료: 「{title}」 → {WORK}")
    if a.prepare_only:
        return 0

    st["published"][a.draft] = "started " + time.strftime("%Y-%m-%d %H:%M")
    save_state(st)
    try:
        r = subprocess.run([ASIDE, "exec", prompt], capture_output=True, timeout=25 * 60)
    except subprocess.TimeoutExpired:
        print("어대리가 25분 안에 끝나지 않았다 — 네이버 블로그를 직접 확인할 것(발행됐을 수 있다)", file=sys.stderr)
        return 5
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    log = os.path.join(WORK, "aside-run.log")
    with open(log, "w", encoding="utf-8") as f:
        f.write(out)
    urls = re.findall(r"https://blog\.naver\.com/ty-health/(\d{8,})", out)
    if urls:
        url = f"https://blog.naver.com/ty-health/{urls[-1]}"
        st["published"][a.draft] = url
        save_state(st)
        print("발행됨:", url)
    else:
        print("글 주소를 못 찾았다 — 어대리 보고를 읽고 발행됐는지 확인할 것(기록은 started 로 남겨 두었다)", file=sys.stderr)
    print("----- 어대리 보고(끝부분) -----")
    print(out[-2500:])
    return 0 if urls else 1


if __name__ == "__main__":
    sys.exit(main())
