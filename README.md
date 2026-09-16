# rufinoqjimenez.com

Static site, served by GitHub Pages from the main branch.

- `build/index.src.html` is the single source: the styles, the header, one `<template id="t-...">` per page.
- `python build/build_site.py` regenerates every `index.html`, `404.html`, `robots.txt` and `sitemap.xml` in place.
- `img/` holds the work photographs at three sizes: `name-s.jpg` (1200 px), `name.jpg` (2200 px) and `name-full.jpg` (the largest, up to 3840 px); the pages choose by screen and link to the full file. The map stills are 1280 / 1920 / 3840. `media/ect-map-tour.mp4` is the filmed tour (720p, phones) and `media/ect-map-tour-1080.mp4` the same cut at 1080p (wider screens); `schematic.html` is the animated Artist Statement, unchanged from the original file.
- Every image carries authorship and rights metadata (EXIF, IPTC and XMP: creator, copyright, title, description, usage terms, a link to /rights/ and a data-mining prohibition for machine-learning training); both films carry title, artist and copyright tags. For a new image: add its record to `build/works_meta.json`, then `python build/embed_meta.py img/<file>.jpg` (needs exiftool, exiftool.org). `robots.txt` and `.well-known/tdmrep.json` are written by the build and declare the same to crawlers.
- `python build/strip_c2pa.py .` removes the content-credential blocks that a file transfer through Claude adds to JPEGs and to `build/schematic.svg.part`; run it after such files arrive, then build.
- `CNAME` carries the custom domain once DNS points here.

To change a caption or a paragraph: edit `build/index.src.html`, run the build, commit, push. Pages redeploys in about a minute.

All works, images, texts and films: (c) Rufino Q. Jimenez. All rights reserved. See /rights/.
