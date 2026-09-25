# venkappavidya.github.io

Personal site for Vidya Venkappa. Static HTML, CSS and a little vanilla
JavaScript. No framework, no npm, no build step for the main page.

## Structure

```
index.html            Home: about, experience, education, projects, research, skills, contact
blog.html             Writing index          (generated, do not edit by hand)
blog/*.html           Individual posts       (generated, do not edit by hand)
content/*.md          Post sources           (edit these)
build.py              Regenerates blog.html and blog/*.html from content/
assets/css/style.css  The whole design system
assets/js/            theme-init.js (pre-paint theme), main.js (nav, theme, reveals)
assets/img/           Portrait
assets/*.pdf          Résumé
```

## Editing

**Home page.** Edit `index.html` directly.

**Blog.** Edit or add a Markdown file in `content/`, then run:

```sh
python3 build.py
```

That regenerates `blog.html` and every page under `blog/`. Requires nothing
beyond Python 3. No packages to install.

### Post front matter

Each file in `content/` starts with a small metadata block:

```markdown
---
title: The title as it appears everywhere
date: March 2025
order: 1
kind: Essay
tags: AI, Web Development, Personal
repo: https://github.com/...     (optional, adds a repository link at the end)
excerpt: One or two sentences used on the index and in search results.
---

Body starts here.
```

`order` controls position in the list: **1 is newest**. When you add a post at
the top, give it `order: 1` and bump the others down.

Supported Markdown: `##` and `###` headings, paragraphs, `-` bullet lists,
numbered lists, `**bold**`, `*italic*`, `` `code` ``, `[links](url)`, `---` rules,
and `> ` for a highlighted callout box. Wrapped lines inside a list item are
joined onto that item, so you can keep the source at a comfortable width.

## Local preview

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploying to GitHub Pages

Commit everything to the `main` branch of `venkappavidya.github.io` and enable
Pages with the source set to `main` / root. `.nojekyll` is present so GitHub
serves the files as-is.

## Design notes

- Colours live as custom properties at the top of `style.css`. The palette is
  deliberately neutral: there is no accent hue, contrast does the work.
- Light and dark are both defined. Dark follows the system setting by default;
  the header toggle overrides it and the choice is remembered in `localStorage`.
- Typefaces are Newsreader (serif, for headings and article body) and Inter
  (sans, for UI), loaded from Google Fonts with system fallbacks.
- Sections fade in on scroll. If JavaScript is unavailable, a `<noscript>` rule
  makes everything visible immediately.
