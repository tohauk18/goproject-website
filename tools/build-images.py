#!/usr/bin/env python3
"""
GOPROJECT - image system builder.

Generates img/projects/<project>/NN-<role>-{1600,800}.webp from the best
available source render, and neutral placeholders where no usable source
exists. Never crops and never upscales: native aspect is preserved so the
browser reserves exact space (no CLS) and no part of the architecture is cut.

Run from the repo root:  python3 tools/build-images.py
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Source tree for renders. The archive is preferred so this script stays
# re-runnable after it has already reorganised img/projects once.
SRC_CANDIDATES = [
    os.environ.get('GOPROJECT_SRC', ''),
    os.path.expanduser('~/Desktop/goproject-original-images/img/projects'),
    os.path.join(ROOT, 'img', 'projects'),
]
CUR = next((p for p in SRC_CANDIDATES if p and os.path.isdir(p)), '')
REC = '/tmp/mainimgs/img/projects'
OUT = os.path.join(ROOT, 'img', 'projects')
if not CUR:
    raise SystemExit('No source render tree found. Set GOPROJECT_SRC.')

C = lambda p: os.path.join(CUR, p)
R = lambda p: os.path.join(REC, p)

# Material harvested from the live one-page site (see
# ~/Desktop/goproject-imported/IMPORT-NOTES.md). Highest-resolution authoring
# the practice owns: 2040px photographs and 760px drawing sheets.
IMP = os.path.expanduser('~/Desktop/goproject-imported/originals')
I = lambda p: os.path.join(IMP, p)

W = 'Wizualizacja'
REAL = 'Realizacja'
KON = 'Koncepcja'
RY = 'Rysunek'   # drawings - not a visualisation, and not a concept

# Parked projects: temporarily out of the portfolio. Their definitions below are
# kept intact, so bringing one back is a one-line edit - remove the slug from this
# set, restore the page and folder from ~/Desktop/goproject-parked, then re-run
# build-images.py and rebuild-portfolio.py.
PARKED_SLUGS = {'obiekt-uzytecznosci-publicznej'}

# Folder names use building typology only - no invented client facts.
# Proper project names live in docs/projects.md and need studio sign-off.
PROJECTS = [
    {
        'slug': 'budynek-wielorodzinny',
        'page': 'projekt-budynek-mieszkalny-wielorodzinny.html',
        'tiles': [
            ('hero', W, C('mieszkalny/budynek-mieszkalny-wielorodzinny-widok-poludniowo-zachodni.webp'),
             'Widok od strony południowo-zachodniej'),
            ('sytuacja-dzialki', W, C('mieszkalny/budynek-mieszkalny-sytuacja-dzialki-widok-polnocno-zachodni.webp'),
             'Usytuowanie budynku na działce'),
            ('widok-od-ulicy', W, C('mieszkalny/budynek-mieszkalny-sytuacja-dzialki-widok-poludniowo-wschodni.webp'),
             'Widok od strony wjazdu'),
            ('widok-od-ogrodu', W, C('mieszkalny/budynek-mieszkalny-sytuacja-dzialki-widok-poludniowo-zachodni.webp'),
             'Widok od strony terenów zielonych'),
            ('elewacja-polnocno-wschodnia', W, C('mieszkalny/budynek-mieszkalny-wielorodzinny-widok-polnocno-wschodni.webp'),
             'Elewacja północno-wschodnia'),
            ('elewacja-polnocno-zachodnia', W, R('mieszkalny/budynek-mieszkalny-wielorodzinny-widok-polnocno-zachodni.webp'),
             'Elewacja północno-zachodnia'),
            ('widok-ogolny', W, C('infocentrum/wielorodzinny-sniadeckich-hq.webp'),
             'Widok ogólny bryły budynku'),
            ('perspektywa-01', W, R('infocentrum/wielorodzinny-perspektywa-1.webp'),
             'Perspektywa z poziomu pieszego'),
        ],
    },
    {
        'slug': 'obiekt-uzytecznosci-publicznej',
        'page': 'projekt-obiekt-uzytecznosci-publicznej.html',
        'tiles': [
            ('hero', KON, C('infocentrum/wielorodzinny-infocentrum.webp'),
             'Widok ogólny obiektu'),
            ('wizualizacja-zima', KON, C('infocentrum/infocentrum-budynek-uzytecznosci-publicznej-wizualizacja-zima.webp'),
             'Widok obiektu w kontekście zimowym'),
            ('plansza-konkursowa', KON, None, 'Plansza konkursowa — układ funkcjonalny'),
            ('elewacja-poludniowa', KON, None, 'Elewacja południowa'),
            ('widok-od-ulicy', KON, None, 'Widok od strony ulicy'),
            ('plan-sytuacyjny', KON, None, 'Plan sytuacyjny i zagospodarowanie terenu'),
        ],
    },
    {
        # One finished house, not a catalogue. Material: the practice's own
        # published project "Projekt domu jednorodzinnego w Chojnicach" - three
        # 2040px photographs of the built house plus its drawing sheet.
        'slug': 'dom-jednorodzinny',
        'page': 'projekt-dom-jednorodzinny.html',
        'tiles': [
            ('hero', REAL, I('goprojecthouse_adam_kubat1.jpg'),
             'Dom jednorodzinny w Chojnicach — bryła od strony wjazdu'),
            ('widok-od-ogrodu', REAL, I('goprojecthouse_adam_kubat7.jpg'),
             'Elewacja od strony ogrodu'),
            ('elewacja-boczna', REAL, I('goprojecthouse_adam_kubat8.jpg'),
             'Elewacja boczna z oknami dachowymi'),
            ('wnetrze-01', W, None,
             'Strefa dzienna — wizualizacja do wygenerowania'),
            ('detal-01', W, None,
             'Detal — wejście lub okap — do wygenerowania'),
            ('wizualizacja-koncepcja', W, None,
             'Wizualizacja koncepcyjna bryły — do wygenerowania'),
            ('rzut-parter', RY, I('Projekt5inside.jpg'),
             'Rzut parteru ze zestawieniem stolarki', (760, 640)),
            ('elewacje', RY, I('Projekt5front.jpg'),
             'Elewacje: frontowa, tylna i boczna', (760, 640)),
        ],
    },
    {
        'slug': 'osiedle-budynkow-dwulokalowych',
        'page': 'projekt-osiedle-budynkow-dwulokalowych.html',
        'tiles': [
            ('hero', W, C('osiedle-dwulokalowe/osiedle-dwulokalowe-lot-ptaka.webp'),
             'Zespół budynków dwulokalowych — widok z lotu ptaka'),
            ('widok-frontowy', W, C('osiedle-dwulokalowe/osiedle-dwulokalowe-widok-front.webp'),
             'Elewacja frontowa zespołu'),
            ('elewacja-frontowa-szeregowa', W, R('osiedle-dwulokalowe/domy-szeregowe-elewacja-frontowa-wizualizacja.webp'),
             'Układ szeregowy — elewacja frontowa'),
            ('strefa-rekreacji', W, R('osiedle-dwulokalowe/domy-szeregowe-ogrodki-plac-zabaw-wizualizacja.webp'),
             'Strefa rekreacji i place zabaw'),
            ('parking', W, R('osiedle-dwulokalowe/domy-szeregowe-parking-wizualizacja.webp'),
             'Parking i układ komunikacyjny'),
            ('widok-z-lotu-ptaka-02', W, R('osiedle-dwulokalowe/osiedle-domow-szeregowych-widok-z-lotu-ptaka.webp'),
             'Zagospodarowanie terenu — ujęcie z lotu ptaka'),
            ('widok-polnocno-wschodni', W, C('osiedle-dwulokalowe/osiedle-dwulokalowe-widok-ne.webp'),
             'Widok północno-wschodni'),
            ('widok-polnocno-zachodni', W, C('osiedle-dwulokalowe/osiedle-dwulokalowe-widok-nw.webp'),
             'Widok północno-zachodni'),
            ('widok-poludniowo-zachodni', W, C('osiedle-dwulokalowe/osiedle-dwulokalowe-widok-sw.webp'),
             'Widok południowo-zachodni'),
            ('widok-dodatkowy', W, C('osiedle-dwulokalowe/osiedle-dwulokalowe-widok-nw-2.webp'),
             'Widok dodatkowy — do identyfikacji'),
        ],
    },
]
# ---------------------------------------------------------------- export helpers
QUALITY = 78
# Hero renders span the full column; gallery tiles never exceed about half of it.
# Shipping a 1600px variant for a 390px tile was the single biggest waste.
HERO_EDGES = (1600, 800)
TILE_EDGES = (1000, 640)
FONT_CANDIDATES = [
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    '/Library/Fonts/Arial.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
]


def get_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def load_flat(src):
    """Open an image and flatten to RGB (WebP export friendly)."""
    im = Image.open(src)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    return im


def export_variant(im, dest, max_edge):
    """Resize so the long edge is max_edge, preserving aspect. Never upscales."""
    w, h = im.size
    scale = max_edge / float(max(w, h))
    out = im
    if scale < 1:
        out = im.resize((max(1, int(round(w * scale))), max(1, int(round(h * scale)))),
                        Image.LANCZOS)
    out.save(dest, 'WEBP', quality=QUALITY, method=6)
    return out.size


def make_placeholder(dest, role, caption, long_edge=1600):
    """Neutral 3:2 card stating exactly what has to be generated.

    Placeholders are the spec, not a downgrade: the filename is already the
    final one, so a new render drops in with no code change.
    """
    s = long_edge / 1600.0
    w = long_edge
    h = int(round(long_edge * 2 / 3.0))
    im = Image.new('RGB', (w, h), (243, 244, 246))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(203, 206, 210), width=max(2, int(4 * s)))
    lines = [
        ('WIZUALIZACJA DO WYGENEROWANIA', int(44 * s), (24, 24, 27), int(-60 * s)),
        (role, int(34 * s), (113, 113, 122), int(10 * s)),
        (caption, int(30 * s), (113, 113, 122), int(56 * s)),
        ('docelowo %d x %d px - proporcja 3:2' % (w, h), int(24 * s), (161, 161, 170), int(112 * s)),
    ]
    for text, font, colour, dy in lines:
        tw = d.textlength(text, font=get_font(font))
        d.text(((w - tw) / 2, h / 2 + dy), text, font=get_font(font), fill=colour)
    im.save(dest, 'WEBP', quality=QUALITY, method=6)
    return im.size

# ---------------------------------------------------------------- build
import shutil

STAGE = os.path.join(OUT, '_new')
OLD_DIRS = ['mieszkalny', 'infocentrum', 'osiedle-dwulokalowe', 'dom-jednorodzinny']


def build():
    shutil.rmtree(STAGE, ignore_errors=True)
    manifest = []
    for project in PROJECTS:
        slug = project['slug']
        if slug in PARKED_SLUGS:
            continue
        dest_dir = os.path.join(STAGE, slug)
        os.makedirs(dest_dir, exist_ok=True)
        for index, tile in enumerate(project['tiles'], 1):
            role, kind, src, caption = tile[:4]
            stem = '%02d-%s' % (index, role)
            # A source path that was written but does not exist is a typo, not a
            # request for a placeholder. Fail loudly instead of shipping a grey box.
            if src is not None and not os.path.exists(src):
                raise SystemExit('Source render missing: %s' % src)
            made_placeholder = src is None
            # a 5th element overrides the size pair (drawings are only 760px wide,
            # so naming them -1000.webp would be a lie)
            edges = tile[4] if len(tile) > 4 else (HERO_EDGES if index == 1 else TILE_EDGES)
            names = {}
            for edge in edges:
                name = '%s-%d.webp' % (stem, edge)
                names[edge] = name
                dest = os.path.join(dest_dir, name)
                if made_placeholder:
                    size = make_placeholder(dest, role, caption, edge)
                else:
                    size = export_variant(load_flat(src), dest, edge)
                if edge == edges[0]:
                    big_size = size
            manifest.append({
                'project': slug,
                'file': names[edges[0]],
                'order': index,
                'role': role,
                'kind': kind,
                'caption': caption,
                'source': os.path.relpath(src, ROOT) if src and not made_placeholder else None,
                'placeholder': made_placeholder,
                'width': big_size[0],
                'height': big_size[1],
                'ratio': round(big_size[0] / float(big_size[1]), 3),
                'large_px': edges[0],
                'small_px': edges[1],
                'kb_large': os.path.getsize(os.path.join(dest_dir, names[edges[0]])) // 1024,
                'kb_small': os.path.getsize(os.path.join(dest_dir, names[edges[1]])) // 1024,
            })
    return manifest


def promote():
    for old in OLD_DIRS:
        shutil.rmtree(os.path.join(OUT, old), ignore_errors=True)
    for slug in os.listdir(STAGE):
        target = os.path.join(OUT, slug)
        shutil.rmtree(target, ignore_errors=True)
        shutil.move(os.path.join(STAGE, slug), target)
    shutil.rmtree(STAGE, ignore_errors=True)


if __name__ == '__main__':
    data = build()
    promote()
    with open(os.path.join(ROOT, 'docs', 'image-manifest.json'), 'w') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    total = sum(t['kb_large'] + t['kb_small'] for t in data)
    ph = sum(1 for t in data if t['placeholder'])
    print('tiles built      : %d' % len(data))
    print('placeholders     : %d' % ph)
    print('total payload    : %.1f MB (hero 1600+800, tiles 1000+640)' % (total / 1024.0))
    print('manifest written : docs/image-manifest.json')
