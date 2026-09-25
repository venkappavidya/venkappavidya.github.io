#!/usr/bin/env python3
"""
Static builder for the writing section.

Reads the Markdown files in content/, writes blog/<slug>.html for each post and
regenerates blog.html. Run it after adding or editing a post:

    python3 build.py

Each source file starts with a simple key: value front-matter block, closed by a
line of three dashes.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
BLOG_DIR = ROOT / "blog"

SITE_URL = "https://venkappavidya.github.io"
AUTHOR = "Vidya Venkappa"

# --------------------------------------------------------------- front matter

def parse_source(text):
    """Split a source file into a metadata dict and a Markdown body."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = lines.index("---", 1)
        head, body = lines[1:end], lines[end + 1:]
    else:
        head, body = [], lines

    meta = {}
    for line in head:
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()

    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    return meta, "\n".join(body).strip()


# ------------------------------------------------------------------- markdown

INLINE = [
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])"), r"<em>\1</em>"),
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
]


def inline(text):
    out = html.escape(text, quote=False)
    for pattern, repl in INLINE:
        out = pattern.sub(repl, out)
    return out


def render(markdown):
    """Convert the Markdown subset used by these posts into HTML."""
    out = []
    list_tag = None          # 'ul' | 'ol' | None
    paragraph = []
    quote = []

    def flush_paragraph():
        if paragraph:
            out.append("<p>%s</p>" % inline(" ".join(paragraph).strip()))
            paragraph.clear()

    def flush_quote():
        if quote:
            out.append('<p class="callout">%s</p>' % inline(" ".join(quote).strip()))
            quote.clear()

    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append("</%s>" % list_tag)
            list_tag = None

    def flush_all():
        flush_paragraph()
        flush_quote()
        close_list()

    def continue_item(text):
        """Append a wrapped continuation line onto the open list item."""
        out[-1] = out[-1][: -len("</li>")] + " " + inline(text) + "</li>"

    for raw in markdown.splitlines():
        stripped = raw.strip()

        if not stripped:
            flush_all()
            continue

        if stripped == "---":
            flush_all()
            out.append("<hr>")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            close_list()
            quote.append(stripped[2:])
            continue
        flush_quote()

        heading = re.match(r"^(#{2,3})\s+(.*)$", stripped)
        if heading:
            flush_all()
            level = len(heading.group(1))
            out.append("<h%d>%s</h%d>" % (level, inline(heading.group(2)), level))
            continue

        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet:
            flush_paragraph()
            if list_tag != "ul":
                close_list()
                out.append("<ul>")
                list_tag = "ul"
            out.append("<li>%s</li>" % inline(bullet.group(1)))
            continue

        numbered = re.match(r"^\d+\.\s+(.*)$", stripped)
        if numbered:
            flush_paragraph()
            if list_tag != "ol":
                close_list()
                out.append("<ol>")
                list_tag = "ol"
            out.append("<li>%s</li>" % inline(numbered.group(1)))
            continue

        # A non-blank line inside an open list is a wrapped continuation of the
        # item above it, not the start of a new paragraph.
        if list_tag:
            continue_item(stripped)
            continue

        paragraph.append(stripped)

    flush_all()
    return "\n".join(out)


# ------------------------------------------------------------------ templates

ICON_GITHUB = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
               '<path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3z"/></svg>')

ARROW_LEFT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M19 12H5M11 18l-6-6 6-6"/></svg>')

ARROW_RIGHT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def head(title, description, prefix, canonical):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{canonical}">

<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='14' fill='%2316181b'/><text x='50' y='71' font-size='62' font-family='Georgia,serif' fill='%23fdfdfc' text-anchor='middle'>V</text></svg>">

<script src="{prefix}assets/js/theme-init.js"></script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
<noscript><style>.reveal{{opacity:1;transform:none}}</style></noscript>

</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="container site-header__inner">
    <a class="wordmark" href="{prefix}index.html">Vidya Venkappa</a>

    <nav class="nav" aria-label="Primary">
      <ul class="nav__links" id="nav-links">
        <li><a href="{prefix}index.html#about">About</a></li>
        <li><a href="{prefix}index.html#experience">Experience</a></li>
        <li><a href="{prefix}index.html#education">Education</a></li>
        <li><a href="{prefix}index.html#projects">Projects</a></li>
        <li><a href="{prefix}index.html#research">Research</a></li>
        <li><a href="{prefix}blog.html" aria-current="page">Writing</a></li>
        <li><a href="{prefix}index.html#contact">Contact</a></li>
      </ul>

      <div class="nav__actions">
        <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch colour theme">
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.2M12 19.2v2.2M4.2 4.2l1.6 1.6M18.2 18.2l1.6 1.6M2.6 12h2.2M19.2 12h2.2M4.2 19.8l1.6-1.6M18.2 5.8l1.6-1.6"/></svg>
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7z"/></svg>
        </button>
        <button class="icon-btn nav__toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="nav-links" aria-label="Toggle navigation menu">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
      </div>
    </nav>
  </div>
</header>
"""


def foot(prefix):
    return f"""
<footer class="site-footer">
  <div class="container site-footer__inner">
    <p style="margin:0">© <span data-year>2026</span> {AUTHOR}</p>
    <nav aria-label="Footer">
      <a href="{prefix}index.html#about">About</a>
      <a href="{prefix}index.html#projects">Projects</a>
      <a href="{prefix}blog.html">Writing</a>
      <a href="mailto:venkappavidya@gmail.com">Email</a>
      <a href="https://www.linkedin.com/in/vidya-venkappa/" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://github.com/vidyavenkappa" target="_blank" rel="noopener">GitHub</a>
    </nav>
  </div>
</footer>

<script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def reading_time(markdown):
    words = len(re.findall(r"\w+", markdown))
    return max(1, round(words / 220))


def render_post(post, prev_post, next_post):
    prefix = "../"
    body = render(post["body"])
    tags = "".join("<li>%s</li>" % html.escape(t) for t in post["meta"]["tags"])
    canonical = f"{SITE_URL}/blog/{post['slug']}.html"

    repo = post["meta"].get("repo")
    repo_link = ""
    if repo:
        repo_link = (
            '<div class="card__links" style="margin-top:2.5rem">'
            f'<a href="{repo}" target="_blank" rel="noopener">{ICON_GITHUB}View the repository</a>'
            "</div>"
        )

    nav_prev = ""
    if prev_post:
        nav_prev = (f'<a href="{prev_post["slug"]}.html">{ARROW_LEFT}'
                    f'<span><span class="label">Previous</span>{html.escape(prev_post["meta"]["title"])}</span></a>')
    nav_next = ""
    if next_post:
        nav_next = (f'<a href="{next_post["slug"]}.html" style="text-align:right">'
                    f'<span><span class="label">Next</span>{html.escape(next_post["meta"]["title"])}</span>{ARROW_RIGHT}</a>')

    return (
        head(f"{post['meta']['title']} | {AUTHOR}", post["meta"]["excerpt"], prefix, canonical)
        + f"""
<main id="main">
  <article class="article">
    <div class="container">

      <p style="margin-bottom:2rem">
        <a class="backlink" href="{prefix}blog.html">{ARROW_LEFT}All writing</a>
      </p>

      <header class="article__header">
        <p class="eyebrow">{html.escape(post['meta'].get('kind', 'Essay'))}</p>
        <h1 class="article__title">{html.escape(post['meta']['title'])}</h1>
        <div class="article__meta">
          <span>{html.escape(post['meta']['date'])}</span>
          <span class="dot">·</span>
          <span>{post['read']} min read</span>
          <span class="dot">·</span>
          <span>{AUTHOR}</span>
        </div>
        <ul class="tags article__tags">{tags}</ul>
      </header>

      <div class="prose">
{body}
      </div>

      {repo_link}

      <nav class="post-nav" aria-label="More posts">
        {nav_prev}
        {nav_next}
      </nav>

    </div>
  </article>
</main>
"""
        + foot(prefix)
    )


def render_index(posts):
    items = []
    for p in posts:
        tags = "".join("<li>%s</li>" % html.escape(t) for t in p["meta"]["tags"])
        items.append(f"""        <article class="post-item reveal">
          <p class="post-item__date">{html.escape(p['meta']['date'])}<br><span style="color:var(--ink-4)">{p['read']} min read</span></p>
          <div>
            <h2 class="post-item__title"><a href="blog/{p['slug']}.html">{html.escape(p['meta']['title'])}</a></h2>
            <p class="post-item__excerpt">{html.escape(p['meta']['excerpt'])}</p>
            <ul class="tags">{tags}</ul>
            <a class="post-item__more" href="blog/{p['slug']}.html">Read the post {ARROW_RIGHT}</a>
          </div>
        </article>""")

    return (
        head(f"Writing | {AUTHOR}",
             "Essays on applied AI, retrieval-augmented generation, security analytics and working while studying.",
             "", f"{SITE_URL}/blog.html")
        + """
<main id="main">
  <section class="section">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Writing</p>
        <h1 style="font-size:var(--step-3)">Notes on applied AI</h1>
        <p class="lede measure">Longer pieces on the systems I build and the decisions behind them: retrieval
        pipelines, model evaluation, security analytics, and the occasional reflection on the way
        this career has actually gone.</p>
      </div>

      <div class="postlist">
"""
        + "\n".join(items)
        + """
      </div>
    </div>
  </section>
</main>
"""
        + foot("")
    )


# ----------------------------------------------------------------------- main

def main():
    BLOG_DIR.mkdir(exist_ok=True)

    posts = []
    for path in sorted(CONTENT.glob("*.md")):
        meta, body = parse_source(path.read_text(encoding="utf-8"))
        posts.append({
            "slug": path.stem,
            "meta": meta,
            "body": body,
            "read": reading_time(body),
            "order": int(meta.get("order", "0")),
        })

    posts.sort(key=lambda p: p["order"])  # newest first

    for i, post in enumerate(posts):
        prev_post = posts[i - 1] if i > 0 else None
        next_post = posts[i + 1] if i < len(posts) - 1 else None
        target = BLOG_DIR / f"{post['slug']}.html"
        target.write_text(render_post(post, prev_post, next_post), encoding="utf-8")
        print(f"  blog/{post['slug']}.html  ({post['read']} min)")

    (ROOT / "blog.html").write_text(render_index(posts), encoding="utf-8")
    print(f"  blog.html  ({len(posts)} posts)")


if __name__ == "__main__":
    main()
