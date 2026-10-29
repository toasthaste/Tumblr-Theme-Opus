# Tumblr Theme — project notes

Remi's own Tumblr theme, started 2026-10-07 from a friend's theme (with her permission). Her source is the repo PrecociouslyDigital/skyedelaciel, which is her whole Astro website; the theme is generated from it. We work from the built theme file, not her source.

## Files
- `my-theme.html`: **the theme**, the only file that matters. Paste it into Tumblr's Edit HTML.
- `friend-original.html`: her untouched built theme, kept for reference.
- `assets/`: local copies of the fonts and images. The live copies are hosted in the public GitHub repo **toasthaste/Tumblr-Theme-Opus** and served via `https://cdn.jsdelivr.net/gh/toasthaste/Tumblr-Theme-Opus@main/<file>`. jsDelivr can take up to about 12 hours to show a replaced file. GitHub's web upload accepts at most 100 files at a time.
- `upload batch 1/`, `upload batch 2/`, `upload missing/`: leftover copies from the first asset upload. Safe to delete.
- `preview/`: local preview tooling (see below).

## Workflow
1. Claude edits `my-theme.html`, and tests in the local preview.
2. Claude puts the file on the clipboard. Remi pastes it into **themes-test-blog** (Customize, then Edit HTML, then Ctrl+A, Ctrl+V, Save). Claude's simulated Ctrl+V does *not* paste into Tumblr's editor, so Remi does this step.
3. The live blog can take a few minutes to update. To verify, Claude fetches https://themes-test-blog.tumblr.com/ and checks that each `<style>`/`<script>` block of `my-theme.html` appears in it verbatim.
   **Since 2026-10-24, plain `curl` gets Tumblr's "Checking your browser..." bot page.** Don't try to get around it. Verify in the built-in browser instead:
   - Inside the tab, `fetch(location.href)` returns the raw HTML.
   - Tumblr now serves the CSS minified, so compare by content or behaviour, not verbatim.
   - The page's CSP blocks posting it to localhost, and it's too big (about 330KB) to pass through chat.
   - For CSS tweaks on new structure, inject a `<style>` into the live page in the browser pane and measure.
4. After any change to the page *structure* (HTML or `{block:...}` tags), take a fresh snapshot: copy the live page to `preview/live-snapshot.html` and `my-theme.html` to `preview/snapshot-theme.html`.

Tumblr refuses to save a theme containing a literal `http://` anywhere, even inside an inline SVG's `xmlns`. Write it as `http%3A//` in data URIs. Check before handing over: `grep -c "http://" my-theme.html` should print 0.

Tumblr strips the whitespace between tags such as `</li><li>` when it renders the page, but the preview snapshot still has it. So inline-flowing items get no break points live: the tag bubbles add an invisible `\200B` after each tag for this. When testing inline layout in the preview, remove the whitespace text nodes first.

The test blog is a sideblog, so saving there is always safe. The poastbot account (an admin of it) is signed in to Claude's built-in browser pane; use it only for themes-test-blog. Remi has OK'd Claude making test posts there. The new-post editor defaults to posting as poastbot, so **check the blog picker before every post**.

## Local preview
- `uv run --no-project python preview/build_preview.py` writes `preview/index.html`. It's the saved live page with `my-theme.html`'s style and script blocks swapped in, so it only reflects CSS and JS changes.
- To serve it, the server named "theme-preview" (in the parent folder's `.claude/launch.json`) runs on port 8765. Test at 1440×900; notes only appear at ≥80rem (1280px) wide.
- Quirks of the built-in browser pane when it's hidden:
  - The viewport can collapse to 0×0 (re-apply the size and dispatch `resize`).
  - Animations freeze (inject `*{transition:none!important;animation:none!important}`).
  - `scrollTo()` fires no events (use real scroll actions).
  - Screenshots lag or time out (trust measurements).

## Current design (as of 2026-10-13)
- **Layout:** posts in the middle. One sidebar holds the menu (logo, three links, dark-mode toggle) with the list of dates/titles under it; the dates on screen are highlighted. Tags go on the **opposite side** from the menu.
- **Customize option:** "Menu on right" (`<html data-menu="right">`). Default: menu left, tags right.
- **Tags = margin notes:** each post has `<aside class="margin-note"><ol class="note-tags">` in the template. The note box runs the post's full height just outside it. The speech bubble inside is centred on the post, and `position: sticky` (top and bottom 2rem) so it nudges to stay on screen, but it can never leave its own post's height. Its tail is centred on the bubble, clamped to the visible part of the post.
- **Too many tags to fit beside a short post:** *all* of its tags go into a bubble under the post (created by the script, `.note-spill` / `.spill-tags`). It's shifted toward the notes' side by half the note reach (`--spill-shift`), with a hooked SVG tail that curls up to point at the post's notes-side edge.
- **Narrow screens (<80rem):** no notes; tags show in each post's footer.
- **Knobs:** `SHOW_IF_POST_VISIBLE` (.5) and `SHOW_IF_SCREEN_FILLED` (.33) at the top of the script control date highlighting. `--note-gap`, `--note-width` and `--spill-shift` are set on `main.feed` in the CSS.
- Removed during the overhaul: vine decorations, green corner brackets, her name, links and favicon. Her flower logo is still in place, waiting for Remi's own.

## Tried and rejected (don't redo)
- Bubbles inside the sidebar list with "current post" handover timing (many variants). Tails ended up pointing at the wrong post.
- "Bubble follows post" (the sidebar list drifting with scroll): too much motion.
- Separate left/right checkboxes for tags and menu: replaced by one, with tags always opposite the menu.
- Splitting tags into a side bubble plus a linked continuation under the post (comic neck): it reads leftward when tags are on the right.
- Height caps or click-to-expand for long tag lists: **Remi strongly dislikes these.** Remi writes very long, rambly tags, so those must be handled gracefully.

## Shelved: hexagon background (git tag `hexagon-background`)
Built 2026-10-12/13, then shelved by Remi with a possible return later. Restore it with `git show hexagon-background:my-theme.html`.
- **What it was:** small tiled hexagons (subdued yellow-orange, off-white lines) on a `<canvas>` behind the page, made by the script. Near the mouse, each hexagon gets one flat, blended colour by distance: redder bodies, darker lines.
- **Knobs:** `BLUSH_RADIUS` (Remi set 30) and `BLUSH_STEPS` sit at the top of the script; colours and `--hex-size` are in the CSS.
- **Performance:** it redraws only the patch around the mouse, and costs nothing while the mouse is still.
- **Text backings it needed:** solid panels behind posts, the menu and date list (separately!), the blog header, pagination and the date strips.
- **Lessons:**
  - A smooth CSS radial glow looked "airbrushed". Per-hexagon flat colour fixed that.
  - One panel around the whole sidebar fused the menu and dates, which Remi disliked.
- **Ideas not done:** fisheye enlargement under the cursor, and Customize-menu colour options.

## Ideas / to-do (not started)
- Replace her flower logo; possibly swap fonts and images (Remi plans a broader visual overhaul).
- Long reblog chains (more than about 25) fall back to Tumblr's old nested style on most themes. Low priority; worth poking at sometime.
- Remi might eventually want date/title labels and tags arranged differently. Undecided.
- Optional: back the git history up to GitHub (the existing repo is public, so a private repo might suit better).

## Version history (git)
This folder is a local git repo (set up 2026-10-12, branch `main`, nothing pushed anywhere). Remi doesn't use git; Claude does.
- **Commit after each version Remi pastes and is happy with**, with a plain-English message saying what changed. Commit `NOTES.md` updates alongside.
- Repo-local settings: `user.name Remi`, `user.email remi@local` (a placeholder, so no real email lands in history if it's ever pushed publicly), `core.autocrlf false` (keeps line endings exactly as written, which the verbatim live-page check relies on).
- **GitHub backup** (since 2026-10-28): `git push origin main:theme-history --tags`, run when Remi asks.
  - It goes to the **`theme-history` branch** of the public toasthaste/Tumblr-Theme-Opus repo. Remi chose to back up the full history.
  - **Never push to that repo's `main`.** It holds the assets jsDelivr serves, and its layout differs: files at the root, not in `assets/`.
- `.gitignore` skips the `upload batch`/`upload missing` folders and the generated `preview/index.html`.
