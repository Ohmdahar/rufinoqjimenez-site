"""Embed authorship and rights metadata (EXIF + IPTC + XMP) in site images, losslessly, with exiftool (exiftool.org).

    python build/embed_meta.py img/d01-dasein.jpg img/d01-dasein-full.jpg ...

The record for each file comes from build/works_meta.json (title, medium, note, alt text as on the site), keyed by the
file name without its -s / -full suffix. Add a new work to works_meta.json first, then run this on its files."""
import json, os, re, subprocess, glob, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
works = json.load(open(os.path.join(HERE, 'works_meta.json'), encoding='utf-8'))

CREATOR = 'Rufino Q. Jimenez'
COPYRIGHT = '© Rufino Q. Jimenez. All rights reserved.'
RIGHTS_URL = 'https://rufinoqjimenez.com/rights/'
SITE_URL = 'https://rufinoqjimenez.com'
USAGE = ('All rights reserved. This image may not be reproduced, distributed, adapted, exhibited or used for the '
         'training of machine-learning systems without written permission. Permissions: ' + RIGHTS_URL)
DATAMINING = 'DMI-PROHIBITED-AIMLTRAINING'   # exiftool adds the http://ns.useplus.org/ldf/vocab/ prefix

# the film poster carries the same record as the home image
works['r-poster'] = dict(works['home-poster'])
works['r-poster']['meta'] = '2026 · browser-based interactive work · filmed tour'

def record(name):
    w = works[name]
    meta = w['meta']
    year = re.match(r'(\d{4})', meta)
    meta_read = re.sub(r'\s*·\s*', ', ', meta)
    meta_read = re.sub(r'^\d{4}, ', '', meta_read)
    desc = w['alt'].rstrip('.') + '. ' + meta_read[0].upper() + meta_read[1:] + '.'
    if w['note']:
        desc += ' ' + w['note'].replace('The full account and a filmed tour are on the PhD Research page.', 'The full account and a filmed tour: rufinoqjimenez.com/research/.')
    if name.startswith('d') or name == 'c03-all-art':
        desc += ' Drawing by Rufino Q. Jimenez.'
    elif name == 'c04-sadness':
        desc += ' Sculpture by Rufino Q. Jimenez.'
    else:
        desc += (' The ECT Entanglement Map, part of the practice-research PhD The Ethics of Entropy at Goldsmiths, '
                 'University of London; the map is shown in person and is not published online. By Rufino Q. Jimenez.')
    kw = [CREATOR, 'systems aesthetics']
    m = meta.lower()
    if name.startswith('d') or name == 'c03-all-art':
        kw.append('drawing')
    if 'pastel' in m: kw.append('pastel')
    if 'charcoal' in m: kw.append('charcoal')
    if name == 'c04-sadness': kw += ['sculpture', 'salt crystal']
    if name in ('c01-map-bulk', 'home-poster', 'r-poster'):
        kw += ['The Ethics of Entropy', 'ECT Entanglement Map', 'browser-based interactive work', 'Goldsmiths, University of London']
    return dict(title=w['title'], desc=desc, year=year.group(1) if year else None, kw=kw)

def exif_args(r):
    a = ['-overwrite_original', '-codedcharacterset=utf8',
         f'-MWG:Creator={CREATOR}', f'-MWG:Copyright={COPYRIGHT}', f'-MWG:Description={r["desc"]}',
         f'-XMP-dc:Title={r["title"]}', f'-IPTC:ObjectName={r["title"][:64]}',
         '-XMP-xmpRights:Marked=True', f'-XMP-xmpRights:WebStatement={RIGHTS_URL}', f'-XMP-xmpRights:UsageTerms={USAGE}',
         f'-XMP-plus:LicensorName={CREATOR}', f'-XMP-plus:LicensorURL={RIGHTS_URL}',
         f'-XMP-plus:CopyrightOwnerName={CREATOR}', f'-XMP-plus:ImageCreatorName={CREATOR}',
         f'-XMP-plus:DataMining#={DATAMINING}',
         f'-XMP-iptcCore:CreatorWorkURL={SITE_URL}',
         f'-XMP-photoshop:Credit={CREATOR}', f'-IPTC:Credit={CREATOR}',
         '-XMP-photoshop:Source=rufinoqjimenez.com', '-IPTC:Source=rufinoqjimenez.com']
    if r['year']:
        a.append(f'-XMP-photoshop:DateCreated={r["year"]}')
    for k in r['kw']:
        a.append(f'-MWG:Keywords={k}')
    return a

if __name__ == '__main__':
    files = sys.argv[1:]
    if not files:
        print(__doc__); sys.exit(1)
    for p in files:
        name = re.sub(r'(-s|-full)?\.jpg$', '', os.path.basename(p))
        if name not in works:
            print('no record for', name, '(add it to works_meta.json)'); continue
        r = record(name)
        out = subprocess.run(['exiftool'] + exif_args(r) + [p], capture_output=True, text=True)
        print(os.path.basename(p), (out.stdout.strip() + ' ' + out.stderr.strip()).strip())
