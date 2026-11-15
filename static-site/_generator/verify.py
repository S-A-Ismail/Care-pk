#!/usr/bin/env python3
# ============================================================
#  CARE — pre-review checks (stdlib only). Run after process_media.py,
#  documents_meta.py and build.py:
#      python3 static-site/_generator/verify.py [--baseline FILE.sha256]
#  * every internal href/src (and every media path in the embedded events
#    data) resolves; #fragments exist on the target page
#  * every PDF starts with %PDF and its size matches documents.json
#  * no file under static-site/ derives from a consent:"required" image
#  * no visible "TODO" on the Board of Directors page; noindex/sitemap/search
#    match board.json "confirmed"
#  * optional: source originals byte-identical to a sha256 baseline
# ============================================================
import hashlib
import json
import os
import re
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAREPK = os.path.dirname(os.path.dirname(ROOT))
fails = []


def fail(msg):
    fails.append(msg)
    print("FAIL  " + msg)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


pages = sorted(fn for fn in os.listdir(ROOT) if fn.endswith(".html"))
ids_cache = {}


def ids_of(page):
    if page not in ids_cache:
        t = read(os.path.join(ROOT, page))
        ids_cache[page] = set(re.findall(r'\bid="([^"]+)"', t)) | set(re.findall(r'\bdata-tab="([^"]+)"', t))
    return ids_cache[page]


# ---- links ---------------------------------------------------
n_links = 0
for page in pages:
    text = read(os.path.join(ROOT, page))
    for attr, url in re.findall(r'\b(href|src|poster)="([^"]*)"', text):
        if not url or re.match(r"^(https?:|mailto:|tel:|data:|javascript:)", url):
            continue
        n_links += 1
        path, _, frag = url.partition("#")
        path = unquote(path.split("?")[0])
        target = page if not path else path
        if path and not os.path.exists(os.path.join(ROOT, path)):
            fail("%s: %s=%s does not resolve" % (page, attr, url))
            continue
        if frag and target.endswith(".html") and frag not in ids_of(target):
            fail("%s: %s -> #%s not found in %s" % (page, url, frag, target))
    m = re.search(r'<script type="application/json" id="care-events-data">(.*?)</script>', text, re.S)
    if m:
        for ev in json.loads(m.group(1).replace("<\\/", "</")):
            for g in ev["gallery"]:
                for k in ("src", "poster"):
                    v = g.get(k)
                    if isinstance(v, str):
                        n_links += 1
                        if not os.path.exists(os.path.join(ROOT, v)):
                            fail("%s: events data %s -> %s missing" % (page, ev["id"], v))
print("links checked: %d" % n_links)

# ---- documents ----------------------------------------------
docs_path = os.path.join(ROOT, "assets", "data", "documents.json")
if os.path.exists(docs_path):
    docs = json.load(open(docs_path, encoding="utf-8"))
    for d in docs:
        p = os.path.join(ROOT, "assets", "documents", d["file"])
        with open(p, "rb") as f:
            head = f.read(4)
        if head != b"%PDF":
            fail("%s does not start with %%PDF" % d["file"])
        if os.path.getsize(p) != d["bytes"]:
            fail("%s size %d != documents.json %d" % (d["file"], os.path.getsize(p), d["bytes"]))
    print("documents checked: %d" % len(docs))
else:
    fail("documents.json missing")

# ---- consent gate --------------------------------------------
media = json.load(open(os.path.join(ROOT, "assets", "data", "media.json"), encoding="utf-8"))
held = [m["id"] for m in media if m["consent"] == "required"]
for dp, _dn, fns in os.walk(ROOT):
    for fn in fns:
        if any(fn.startswith(h + "-") or fn.startswith(h + ".") for h in held):
            fail("consent-held derivative inside static-site/: " + os.path.join(dp, fn))
for page in pages:
    t = read(os.path.join(ROOT, page))
    for h in held:
        if re.search(r'(src|poster)="[^"]*' + re.escape(h), t) or ('"' + "assets/images/events/" + h) in t:
            fail("%s references held media %s" % (page, h))
print("consent gate: no derivatives of %s under static-site/" % ", ".join(held))

# ---- Board of Directors page ---------------------------------
board = json.load(open(os.path.join(ROOT, "assets", "data", "board.json"), encoding="utf-8"))
bp = read(os.path.join(ROOT, "board-of-directors.html"))
main = re.search(r"<main>(.*)</main>", bp, re.S).group(1)
visible = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", main, flags=re.S))
if re.search(r"\bTODO\b|coming soon", visible, re.I):
    fail("board page shows visible TODO / coming soon text")
names = re.findall(r'class="name">([^<]+)<', main)
want = [m["name"] for m in board["members"]]
if names != want:
    fail("board names %s != board.json %s" % (names, want))
has_noindex = '<meta name="robots" content="noindex">' in bp
in_sitemap = "board-of-directors.html" in read(os.path.join(ROOT, "sitemap.xml"))
in_search = "board-of-directors.html" in read(os.path.join(ROOT, "assets", "js", "search-index.js"))
expected = (False, True, True) if board["confirmed"] else (True, False, False)
if (has_noindex, in_sitemap, in_search) != expected:
    fail("board noindex/sitemap/search state does not match confirmed=%s" % board["confirmed"])
print("board page: %d names, confirmed=%s, noindex=%s, sitemap=%s, search=%s"
      % (len(names), board["confirmed"], has_noindex, in_sitemap, in_search))

# ---- source originals ----------------------------------------
if "--baseline" in sys.argv:
    base = sys.argv[sys.argv.index("--baseline") + 1]
    n = 0
    for line in open(base, encoding="utf-8"):
        digest, rel = line.rstrip("\n").split("  ", 1)
        p = os.path.join(CAREPK, rel)
        with open(p, "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != digest:
                fail("source changed: " + rel)
        n += 1
    print("source originals byte-identical to baseline: %d files" % n)

print("\n%s" % ("ALL CHECKS PASSED" if not fails else "%d FAILURE(S)" % len(fails)))
sys.exit(1 if fails else 0)
