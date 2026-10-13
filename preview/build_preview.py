# Local preview of my-theme.html without uploading to Tumblr.
#
# live-snapshot.html is the test blog's real page, saved while it was wearing
# snapshot-theme.html. This swaps that page's <style> and <script> blocks for
# the ones in the current my-theme.html, so styling and script changes can be
# seen locally. Changes to the page structure (HTML tags, {block:...} tags)
# do NOT show up here: paste the theme into Tumblr and take a new snapshot.
import re
import sys
from pathlib import Path

here = Path(__file__).parent
BLOCK = re.compile(r"<(style|script)\b[^>]*>(.*?)</\1>", re.S)


def blocks(path):
    return [m.group(2) for m in BLOCK.finditer(path.read_text(encoding="utf-8"))]


page = (here / "live-snapshot.html").read_text(encoding="utf-8")
old, new = blocks(here / "snapshot-theme.html"), blocks(here.parent / "my-theme.html")
if len(old) != len(new):
    sys.exit("The theme gained or lost a <style>/<script> block. Paste it into Tumblr and take a new snapshot.")

for before, after in zip(old, new):
    if before not in page:
        sys.exit("Snapshot and snapshot-theme.html don't match. Take a new snapshot.")
    page = page.replace(before, after, 1)

(here / "index.html").write_text(page, encoding="utf-8", newline="")
print("preview/index.html rebuilt")
