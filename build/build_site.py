#!/usr/bin/env python3
"""Build the site pages from build/index.src.html. Run from anywhere: python build/build_site.py

One HTML file per page, clean URLs, relative asset paths (works at a project URL and at the domain root),
no prototype notes, no router script. British spelling, captions as built.
"""
import re, os, shutil, html

BUILD = os.path.dirname(os.path.abspath(__file__))   # the build/ folder
ROOT = os.path.dirname(BUILD)                         # the site root (repo)
SRC = os.path.join(BUILD, 'index.src.html')
SVG = open(os.path.join(BUILD, 'schematic.svg.part'), encoding='utf-8').read()
DIST = ROOT

SITE = 'Rufino Q. Jimenez'
DOMAIN = 'https://rufinoqjimenez.com'

PAGES = {
    # id: (slug, nav label / title, description)
    'home':       ('',                 '',                 'Artist, researcher and art consultant. Conceptual works in systems aesthetics, and the practice-research PhD The Ethics of Entropy at Goldsmiths, University of London.'),
    'drawings':   ('drawings',         'drawings',         'Large-format drawings in charcoal and pastel by Rufino Q. Jimenez: the Rorschach principle at the scale of a wall.'),
    'conceptual': ('conceptual',       'conceptual',       'Conceptual works by Rufino Q. Jimenez: The Ethics of Entropy, Artist Statement, A drawing of all art that has ever been or will be, where does the sadness lie.'),
    'research':   ('research',         'phd research',     'The Ethics of Entropy: a practice-research PhD in systems aesthetics and systems theory at Goldsmiths, University of London. The ECT Entanglement Map, filmed tour and statement.'),
    'writing':    ('writing',          'writing',          'Papers and talks from the doctorate. Coming soon.'),
    'statement':  ('artist-statement', 'artist statement', 'Artist statement: systems aesthetics, the convection of validation, and five stations from encounter to entanglement.'),
    'cv':         ('cv',               'cv',               'Curriculum vitae of Rufino Q. Jimenez: exhibitions, presentations, teaching, consulting, awards.'),
    'contact':    ('contact',          'contact',          'Contact Rufino Q. Jimenez: studio, research and consulting enquiries by email.'),
    'rights':     ('rights',           'rights',           'Rights and permissions for the works, images, texts and films on this site, including The Ethics of Entropy.'),
}

src = open(SRC, encoding='utf-8').read()

style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
fonts = '\n'.join(re.findall(r'<link [^>]*>', src.split('<style>')[0]))
header = re.search(r'<header class="top">.*?</header>', src, re.S).group(0)
footer = re.search(r'<footer class="foot">.*?</footer>', src, re.S).group(0)

templates = {}
for m in re.finditer(r'<template id="t-([a-z]+)">(.*?)</template>', src, re.S):
    templates[m.group(1)] = m.group(2)
assert set(templates) == set(PAGES), (set(templates) ^ set(PAGES))

# strip the CSS for the prototype notes and the router-only bits stay harmless; remove note blocks from content
def strip_notes(h):
    return re.sub(r'\s*<details class="note">.*?</details>', '', h, flags=re.S)

def strip_flags(h):
    h = re.sub(r' <span class="flag">\([^<]*\)</span>', '', h)
    return h

FAVICON = "data:image/svg+xml," + (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><circle cx='16' cy='16' r='12.5' fill='none' stroke='%231a1a1a' stroke-width='1.6'/><circle cx='16' cy='16' r='2.6' fill='%239c2b1e'/></svg>"
).replace('<', '%3C').replace('>', '%3E')

def rel(depth):
    return '' if depth == 0 else '../' * depth

def page_href(pid, depth):
    slug = PAGES[pid][0]
    return rel(depth) + (slug + '/' if slug else '')

def rewrite(h, depth, current):
    # hash links -> paths
    def sub_link(m):
        pid = m.group(1)
        if pid in PAGES:
            return 'href="' + page_href(pid, depth) + '"'
        return m.group(0)
    h = re.sub(r'href="#([a-z]+)"', sub_link, h)
    # asset paths
    h = re.sub(r'(src|poster|href)="(img|media)/', lambda m: f'{m.group(1)}="{rel(depth)}{m.group(2)}/', h)
    h = re.sub(r'srcset="([^"]*)"', lambda m: 'srcset="' + m.group(1).replace('img/', rel(depth) + 'img/') + '"', h)
    h = h.replace('href="schematic.html"', f'href="{rel(depth)}schematic.html"')
    return h

def nav_with_current(hdr, pid, depth):
    hdr = rewrite(hdr, depth, pid)
    if pid != 'home':
        href = page_href(pid, depth)
        hdr = hdr.replace(f'<a href="{href}">', f'<a href="{href}" aria-current="page">', 1)
    return hdr

def build_page(pid):
    slug, label, desc = PAGES[pid]
    depth = 0 if not slug else 1
    body = templates[pid]
    body = strip_notes(body)
    body = strip_flags(body)
    body = body.replace('<!--SCHEMATIC-->', SVG)
    body = rewrite(body, depth, pid)
    title = SITE if pid == 'home' else f'{label} · {SITE}'
    canonical = DOMAIN + '/' + (slug + '/' if slug else '')
    og_image = DOMAIN + '/img/home-poster.jpg'
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
{fonts}
<style>
html{{background:#e8e6e1}}
@media (prefers-color-scheme: dark){{html{{background:#0b0c10}}}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
{style}
</style>
</head>
<body>
<div class="site">
  {nav_with_current(header, pid, depth)}

  <main id="page">
{body}
  </main>

  {rewrite(footer, depth, pid)}
</div>
</body>
</html>
'''
    return head, slug

# write pages in place (img/ and media/ are kept as they are; only html, robots, sitemap are regenerated)
for pid in PAGES:
    out, slug = build_page(pid)
    d = os.path.join(DIST, slug) if slug else DIST
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)

# assets: img/ and media/ live in the repo; schematic.html is copied from build/
shutil.copy(os.path.join(BUILD, 'schematic.html'), os.path.join(DIST, 'schematic.html'))
open(os.path.join(DIST, '.nojekyll'), 'w').close()
open(os.path.join(DIST, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: ' + DOMAIN + '/sitemap.xml\n')
urls = ''.join(f'  <url><loc>{DOMAIN}/{(s + "/") if s else ""}</loc></url>\n' for s, _, _ in PAGES.values())
open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
# 404: same look, one line
templates['notfound'] = '<div class="page-head"><h1 class="page-title">Not found</h1><p class="standfirst">That page is not here. <a href="#home">Home</a>.</p></div>'
PAGES['notfound'] = ('404', 'not found', 'Page not found.')
nf, _ = build_page('notfound')
open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8').write(nf.replace('href="../', 'href="/').replace('src="../', 'src="/').replace('poster="../', 'poster="/'))
del PAGES['notfound']
print('built', sorted(os.listdir(DIST)))
