"""Remove embedded C2PA / JUMBF content-credential blocks that the file transfer adds:
JPEG APP11 'JP' segments, and the c2pa:manifest element in the SVG part."""
import sys, os, re, glob

def strip_jpeg(path):
    b = open(path, 'rb').read()
    if b[:2] != b'\xff\xd8':
        return False
    out = bytearray(b[:2]); i = 2; removed = 0
    while i < len(b):
        if b[i] != 0xFF:
            out += b[i:]; break
        marker = b[i+1]
        if marker == 0xD8 or (0xD0 <= marker <= 0xD7) or marker == 0x01:
            out += b[i:i+2]; i += 2; continue
        if marker == 0xDA:          # start of scan: the rest is entropy-coded data, copy through
            out += b[i:]; break
        seglen = int.from_bytes(b[i+2:i+4], 'big')
        seg = b[i:i+2+seglen]
        if marker == 0xEB and seg[4:6] == b'JP':   # APP11 JUMBF (C2PA)
            removed += 1
        else:
            out += seg
        i += 2 + seglen
    if removed:
        open(path, 'wb').write(bytes(out))
    return removed

def strip_svg(path):
    t = open(path, encoding='utf-8').read()
    n = t
    n = n.replace(' xmlns:c2pa="http://c2pa.org/manifest"', '')
    n = re.sub(r'<c2pa:manifest>.*?</c2pa:manifest>', '', n, flags=re.S)
    if n != t:
        open(path, 'w', encoding='utf-8', newline='').write(n)
        return True
    return False

root = sys.argv[1]
for p in glob.glob(os.path.join(root, 'img', '*.jpg')):
    r = strip_jpeg(p)
    if r: print('jpeg', os.path.basename(p), 'removed', r)
for p in [os.path.join(root, 'build', 'schematic.svg.part')]:
    if os.path.exists(p) and strip_svg(p): print('svg', p, 'cleaned')
# report anything left
left = [p for p in glob.glob(os.path.join(root, '**', '*'), recursive=True) if os.path.isfile(p) and '.git' not in p and b'c2pa' in open(p, 'rb').read()]
print('files still containing c2pa:', left)
