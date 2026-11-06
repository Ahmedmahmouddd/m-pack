import fitz

NAVY = '#092a57'
RED = '#b30101'
GAP = 700

drawings = fitz.open('logo.pdf')[0].get_drawings()


def f(v):
    return f'{v:.1f}'


def path(d):
    out, last = [], None
    for it in d['items']:
        kind = it[0]
        if kind == 're':
            r = it[1]
            out.append(f'M{f(r.x0)} {f(r.y0)}H{f(r.x1)}V{f(r.y1)}H{f(r.x0)}Z')
            last = None
            continue
        a = it[1]
        if last is None or abs(a.x - last.x) > 0.05 or abs(a.y - last.y) > 0.05:
            if out:
                out.append('Z')
            out.append(f'M{f(a.x)} {f(a.y)}')
        if kind == 'l':
            b = it[2]
            out.append(f'L{f(b.x)} {f(b.y)}')
            last = b
        elif kind == 'c':
            c1, c2, b = it[2], it[3], it[4]
            out.append(f'C{f(c1.x)} {f(c1.y)} {f(c2.x)} {f(c2.y)} {f(b.x)} {f(b.y)}')
            last = b
    out.append('Z')
    return ''.join(out)


P = {i: path(d) for i, d in enumerate(drawings)}

# Drawing 0 is the white page background; 6 and 7 are the white counters of "P" and "A".
def body(navy, mask_id):
    return (
        f'<defs><mask id="{mask_id}" maskUnits="userSpaceOnUse" x="-10" y="-40" width="1830" height="640">'
        f'<rect x="-10" y="-40" width="1830" height="640" fill="#fff"/>'
        f'<path fill="#000" d="{P[6]}{P[7]}"/></mask></defs>'
        f'<path fill="{RED}" d="{P[4]}"/>'
        f'<g fill="{navy}" mask="url(#{mask_id})">'
        f'<path d="{P[1]}"/><path d="{P[3]}"/><path d="{P[5]}"/><path d="{P[2]}"/></g>'
    )


def logo(navy, mask_id):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -22 1805 601" role="img" aria-label="M PACK">'
            f'{body(navy, mask_id)}</svg>')


def tile(navy, mask_id):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -22 {1805 + GAP} 601">'
            f'<circle cx="{GAP / 2}" cy="279" r="38" fill="{RED}"/>'
            f'<g transform="translate({GAP} 0)">{body(navy, mask_id)}</g></svg>')


files = {
    'logo.svg': logo(NAVY, 'm'),
    'logo-white.svg': logo('#ffffff', 'mw'),
    'strap-tile.svg': tile(NAVY, 't'),
    'strap-tile-white.svg': tile('#ffffff', 'tw'),
}
for name, svg in files.items():
    with open(f'../assets/{name}', 'w') as fh:
        fh.write(svg)
    print(name, len(svg))
