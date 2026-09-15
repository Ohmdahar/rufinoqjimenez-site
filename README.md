# rufinoqjimenez.com

Static site, served by GitHub Pages from the main branch.

- `build/index.src.html` is the single source: the styles, the header, one `<template id="t-...">` per page.
- `python build/build_site.py` regenerates every `index.html`, `404.html`, `robots.txt` and `sitemap.xml` in place.
- `img/` holds the work photographs (about 1800 px on the long edge); `media/ect-map-tour.mp4` is the filmed tour (720p); `schematic.html` is the animated Artist Statement, unchanged from the original file.
- `CNAME` carries the custom domain once DNS points here.

To change a caption or a paragraph: edit `build/index.src.html`, run the build, commit, push. Pages redeploys in about a minute.

All works, images, texts and films: (c) Rufino Q. Jimenez. All rights reserved. See /rights/.
