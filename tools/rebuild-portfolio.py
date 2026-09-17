#!/usr/bin/env python3
"""
GOPROJECT - portfolio markup rebuilder.

Rewrites the hero and gallery of every project page from docs/image-manifest.json,
and repoints the portfolio cards on index.html / projekty.html at the new heroes.

What it fixes:
  * no more fixed h-64 / object-cover cropping - images render at native aspect
  * width/height on every image, so nothing shifts while loading (CLS)
  * srcset + sizes, so a phone never downloads a 1600px render
  * loading="lazy" everywhere except the hero, which gets fetchpriority="high"
  * a "Wizualizacja / Koncepcja / Realizacja" badge on every tile
  * the "Pliki: ..." internal filename list is replaced by a fact bar
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'docs', 'image-manifest.json')

LABELS = {
    'hero': 'Widok główny',
    'sytuacja-dzialki': 'Sytuacja działki',
    'widok-od-ulicy': 'Widok od ulicy',
    'widok-od-ogrodu': 'Widok od ogrodu',
    'widok-od-ogrodu-02': 'Widok od ogrodu II',
    'widok-od-ogrodu-03': 'Widok od ogrodu III',
    'widok-ogolny': 'Widok ogólny',
    'widok-nocny': 'Widok nocny',
    'widok-frontowy': 'Widok frontowy',
    'widok-dodatkowy': 'Widok dodatkowy',
    'widok-z-lotu-ptaka-02': 'Z lotu ptaka',
    'widok-nad-morzem': 'Bryła od strony morza',
    'widok-polnocno-wschodni': 'Widok płn.-wsch.',
    'widok-polnocno-zachodni': 'Widok płn.-zach.',
    'widok-poludniowo-zachodni': 'Widok płd.-zach.',
    'elewacja-frontowa': 'Elewacja frontowa',
    'elewacja-frontowa-szeregowa': 'Elewacja frontowa',
    'elewacja-poludniowa': 'Elewacja południowa',
    'elewacja-polnocno-wschodnia': 'Elewacja płn.-wsch.',
    'elewacja-polnocno-zachodnia': 'Elewacja płn.-zach.',
    'strefa-rekreacji': 'Strefa rekreacji',
    'parking': 'Parking i komunikacja',
    'perspektywa-01': 'Perspektywa',
    'plansza-konkursowa': 'Plansza konkursowa',
    'plan-sytuacyjny': 'Plan sytuacyjny',
    'wizualizacja-zima': 'Wizualizacja zimowa',
    'realizacja-01': 'Realizacja',
}

BADGE_CLASS = {
    'Realizacja': 'bg-accent text-black',
    'Koncepcja': 'bg-white/90 text-black',
    'Wizualizacja': 'bg-white/90 text-black',
}


def label_for(role):
    return LABELS.get(role, role.replace('-', ' ').capitalize())


def load_tiles():
    with open(MANIFEST) as fh:
        data = json.load(fh)
    grouped = {}
    for tile in data:
        project = tile['project']
        stem = tile['file'].rsplit('-', 1)[0]
        tile['url'] = './img/projects/%s/' % project
        tile['stem'] = stem
        tile['label'] = label_for(tile['role'])
        grouped.setdefault(project, []).append(tile)
    for tiles in grouped.values():
        tiles.sort(key=lambda t: t['order'])
    return grouped


def match_close(html, start, tag='div'):
    """Return the index just past the closing </tag> of the element at `start`."""
    pattern = re.compile(r'<%s\b|</%s>' % (tag, tag))
    depth = 0
    for m in pattern.finditer(html, start):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    raise ValueError('unbalanced <%s> at %d' % (tag, start))


def replace_element(html, marker, new_html):
    """Replace the first element (div or figure) that follows `marker`.

    Tag-agnostic so the pass is idempotent: the rewritten hero is a <figure>,
    the original was a <div>.
    """
    i = html.index(marker)
    candidates = []
    for tag in ('div', 'figure'):
        j = html.find('<%s' % tag, i)
        if j != -1:
            candidates.append((j, tag))
    if not candidates:
        raise ValueError('no element follows marker at %d' % i)
    start, tag = min(candidates)
    end = match_close(html, start, tag)
    return html[:start] + new_html + html[end:], end - start


def replace_inner(html, open_tag_index, new_inner, tag='div'):
    """Replace the children of the element whose opening tag is at open_tag_index."""
    open_end = html.index('>', open_tag_index) + 1
    end = match_close(html, open_tag_index, tag) - len('</%s>' % tag)
    return html[:open_end] + new_inner + html[end:]


def render_hero(tile):
    u = tile['url']
    big = '%s-%d.webp' % (tile['stem'], tile['large_px'])
    small = '%s-%d.webp' % (tile['stem'], tile['small_px'])
    alt = tile['caption']
    if tile['placeholder']:
        alt += ' — wizualizacja do wygenerowania'
    return (
        '      <!-- MAIN HERO IMAGE -->\n'
        '      <figure class="mb-16 border border-gray-200 shadow-2xl overflow-hidden relative group"%s>\n'
        '        <img src="%s%s"\n'
        '          srcset="%s%s %dw, %s%s %dw"\n'
        '          sizes="(min-width:1280px) 1200px, 100vw"\n'
        '          width="%d" height="%d"\n'
        '          loading="eager" fetchpriority="high" decoding="async"\n'
        '          alt="%s"\n'
        '          class="w-full h-auto" />\n'
        '        <figcaption class="absolute bottom-6 left-6 bg-black/80 text-white font-mono text-xs px-4 py-2 flex items-center gap-2">\n'
        '          <span class="text-accent font-bold">%s</span>\n'
        '          <span>&middot;</span>\n'
        '          <span>%s</span>\n'
        '        </figcaption>\n'
        '      </figure>'
    ) % (
        ' data-placeholder="1"' if tile['placeholder'] else '',
        u, small, u, small, tile['small_px'], u, big, tile['large_px'],
        tile['width'], tile['height'], alt, tile['kind'], tile['caption'],
    )


def render_tile(tile):
    u = tile['url']
    big = '%s-%d.webp' % (tile['stem'], tile['large_px'])
    small = '%s-%d.webp' % (tile['stem'], tile['small_px'])
    alt = tile['caption']
    if tile['placeholder']:
        alt += ' — wizualizacja do wygenerowania'
    return (
        '          <figure class="border border-gray-200 bg-studio-surface overflow-hidden group flex flex-col"%s>\n'
        '            <div class="relative overflow-hidden">\n'
        '              <img src="%s%s"\n'
        '                srcset="%s%s %dw, %s%s %dw"\n'
        '                sizes="(min-width:1024px) 33vw, (min-width:640px) 50vw, 100vw"\n'
        '                width="%d" height="%d"\n'
        '                loading="lazy" decoding="async"\n'
        '                alt="%s"\n'
        '                class="w-full h-auto group-hover:scale-[1.03] transition-transform duration-500" />\n'
        '              <div class="absolute top-3 left-3 bg-black/80 text-white font-mono text-[10px] px-2.5 py-1">%s</div>\n'
        '              <div class="absolute top-3 right-3 %s font-mono text-[10px] px-2.5 py-1">%s</div>\n'
        '            </div>\n'
        '            <figcaption class="p-4 font-mono text-xs border-t border-gray-200 mt-auto">\n'
        '              <div class="font-bold text-black mb-1">%s</div>\n'
        '              <p class="text-gray-500 text-[11px] font-sans">%s</p>\n'
        '            </figcaption>\n'
        '          </figure>'
    ) % (
        ' data-placeholder="1"' if tile['placeholder'] else '',
        u, small, u, small, tile['small_px'], u, big, tile['large_px'],
        tile['width'], tile['height'], alt,
        tile['label'], BADGE_CLASS[tile['kind']], tile['kind'], tile['label'], tile['caption'],
    )


def render_gallery(tiles):
    parts = []
    for tile in tiles[1:]:
        parts.append(render_tile(tile))
    return '\n\n'.join(parts)

GALLERY_CLASS = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 items-start'

PAGE_NAMES = {
    'budynek-wielorodzinny': 'projekt-budynek-mieszkalny-wielorodzinny.html',
    'obiekt-uzytecznosci-publicznej': 'projekt-obiekt-uzytecznosci-publicznej.html',
    'dom-jednorodzinny': 'projekt-dom-jednorodzinny.html',
    'osiedle-budynkow-dwulokalowych': 'projekt-osiedle-budynkow-dwulokalowych.html',
}


def find_gallery_grid(html):
    """The container that holds the gallery tiles.

    Idempotent: on a re-run the original h-64 tiles are already gone, so the
    rewritten container is recognised by its own class first.
    """
    exact = '<div class="%s">' % GALLERY_CLASS
    if exact in html:
        start = html.index(exact)
        return start, match_close(html, start, 'div')
    pattern = re.compile(r'<div class="grid grid-cols-1 md:grid-cols-2[^"]*"[^>]*>')
    for m in pattern.finditer(html):
        end = match_close(html, m.start(), 'div')
        if 'h-64' in html[m.start():end]:
            return m.start(), end
    raise ValueError('gallery grid not found')


def summary(tiles):
    counts = {}
    for t in tiles:
        counts[t['kind']] = counts.get(t['kind'], 0) + 1
    order = [('Wizualizacja', 'wizualizacji'), ('Koncepcja', 'plansz koncepcyjnych'),
             ('Realizacja', 'zdjęcie z realizacji')]
    bits = []
    for kind, noun in order:
        if counts.get(kind):
            n = counts[kind]
            if kind == 'Realizacja':
                bits.append(noun)
            else:
                bits.append('%d %s' % (n, noun))
    return ' &#183; '.join(bits)


def rebuild_page(path, tiles):
    with open(path, encoding='utf-8') as fh:
        html = fh.read()
    original = html

    # 1. hero
    html, _ = replace_element(html, '<!-- MAIN HERO IMAGE -->', render_hero(tiles[0]))

    # 2. gallery container (class + tiles)
    start, end = find_gallery_grid(html)
    html = html[:start] + '<div class="%s">\n%s\n\n        </div>' % (
        GALLERY_CLASS, render_gallery(tiles)) + html[end:]

    # 3. internal filename dump -> editorial fact bar
    html = re.sub(r'Pliki(?: powi&#261;zane| powi\u0105zane)?:[^<]*', summary(tiles), html, count=1)

    # 4. og:image -> this project's own hero, absolute so social scrapers resolve it
    hero_abs = 'https://goproject.com.pl/%s%s-%d.webp' % (
        tiles[0]['url'][2:], tiles[0]['stem'], tiles[0]['large_px'])
    html = re.sub(r'(property="og:image" content=")[^"]*(")',
                  lambda m: m.group(1) + hero_abs + m.group(2), html, count=1)

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    return len(original), len(html)


def repoint_cards(grouped):
    """Point the portfolio cards at each project's own hero (shared for recognition)."""
    heroes = {}
    for slug, tiles in grouped.items():
        heroes[slug] = '%s%s-%d.webp' % (tiles[0]['url'], tiles[0]['stem'], tiles[0]['small_px'])
    legacy = {
        './img/projects/infocentrum/wielorodzinny-infocentrum.webp': 'obiekt-uzytecznosci-publicznej',
        './img/projects/mieszkalny/budynek-mieszkalny-wielorodzinny-widok-poludniowo-zachodni.webp': 'budynek-wielorodzinny',
        './img/projects/osiedle-dwulokalowe/osiedle-dwulokalowe-lot-ptaka.webp': 'osiedle-budynkow-dwulokalowych',
        './img/projects/dom-jednorodzinny/dom-jednorodzinny-z-garazem-i-ogrodem-wizualizacja.webp': 'dom-jednorodzinny',
    }
    # Parked projects are absent from the manifest - skip them rather than fail.
    legacy = {old: heroes[slug] for old, slug in legacy.items() if slug in heroes}
    changed = 0
    for name in ('index.html', 'projekty.html'):
        path = os.path.join(ROOT, name)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        for old, new in legacy.items():
            if old in html:
                changed += html.count(old)
                html = html.replace(old, new)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
    return changed


if __name__ == '__main__':
    grouped = load_tiles()
    for slug, tiles in sorted(grouped.items()):
        print('%-38s %2d tiles (%d placeholders)' % (
            slug, len(tiles), sum(1 for t in tiles if t['placeholder'])))
    for slug, tiles in sorted(grouped.items()):
        path = os.path.join(ROOT, PAGE_NAMES[slug])
        before, after = rebuild_page(path, tiles)
        print('rebuilt  %-46s %d -> %d bytes' % (PAGE_NAMES[slug], before, after))
    print('card images repointed: %d' % repoint_cards(grouped))
