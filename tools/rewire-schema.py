#!/usr/bin/env python3
"""
GOPROJECT - structured-data rewiring.

Turns the site's separate, disconnected JSON-LD fragments into one entity graph:

    index.html      defines  #organization, #adam-kubat, #website
    projekty.html   defines  #portfolio (CollectionPage) with hasPart -> each project
    projekt-*.html  references #adam-kubat as creator+author,
                    #organization as publisher+copyrightHolder, isPartOf #portfolio

Before: every project page inlined its own copy of the architect as `author` and the
studio as `creator` - semantically backwards (a person creates, a studio publishes),
with no @id anywhere, so nothing was actually connected.

Run from the repo root:  python3 tools/rewire-schema.py
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://goproject.com.pl/'
ORG = BASE + '#organization'
PERSON = BASE + '#adam-kubat'
WEBSITE = BASE + '#website'
PORTFOLIO = BASE + 'projekty.html#portfolio'

MANIFEST = os.path.join(ROOT, 'docs', 'image-manifest.json')

# page -> (manifest project, canonical url, keywords)
PROJECTS = {
    'projekt-budynek-mieszkalny-wielorodzinny.html': (
        'budynek-wielorodzinny',
        BASE + 'projekt-budynek-mieszkalny-wielorodzinny.html',
        ['budynek wielorodzinny', 'projekt budowlany', 'kierownik budowy',
         'nadzór inwestorski', 'Chojnice']),
    'projekt-dom-jednorodzinny.html': (
        'dom-jednorodzinny',
        BASE + 'projekt-dom-jednorodzinny.html',
        ['dom jednorodzinny', 'projekt budowlany', 'kierownik budowy',
         'nadzór inwestorski']),
    'projekt-osiedle-budynkow-dwulokalowych.html': (
        'osiedle-budynkow-dwulokalowych',
        BASE + 'projekt-osiedle-budynkow-dwulokalowych.html',
        ['osiedle domów dwulokalowych', 'projekt osiedla', 'urbanistyka',
         'zagospodarowanie terenu']),
}


def find_org(payload):
    """The organization node, whether the block is flat or already a @graph."""
    if payload.get('@type') == 'ProfessionalService':
        return payload, None
    for node in payload.get('@graph', []):
        if 'ProfessionalService' in type_names(node):
            return node, payload
    return None, payload


def find_ld_blocks(html):
    return [(m.start(), m.end(), m.group(1)) for m in
            re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


def replace_ld_block(html, span, payload):
    start, end, _ = span
    head = html[:start].rstrip(' \t')
    text = json.dumps(payload, ensure_ascii=False, indent=2).replace('\n', '\n  ')
    new = '  <script type="application/ld+json">\n  ' + text + '\n  </script>'
    return head + new + html[end:]


def type_names(node):
    t = node.get('@type')
    return t if isinstance(t, list) else [t]


def load_images():
    """Hero + one supporting image per project, with real pixel dimensions."""
    with open(MANIFEST) as fh:
        tiles = json.load(fh)
    out = {}
    for t in tiles:
        slug = t['project']
        entry = out.setdefault(slug, [])
        if len(entry) < 3:
            entry.append({
                '@type': 'ImageObject',
                'contentUrl': BASE + 'img/projects/%s/%s' % (slug, t['file']),
                'width': t['width'],
                'height': t['height'],
                'caption': t['caption'],
            })
    if out:
        for slug in out:
            out[slug][0]['representativeOfPage'] = True
    return out


def rewire_project(page, slug, canonical, keywords, images):
    path = os.path.join(ROOT, page)
    html = io.open(path, encoding='utf-8').read()
    for span in find_ld_blocks(html):
        payload = json.loads(span[2])
        graph = payload.get('@graph', [])
        work = next((n for n in graph if 'CreativeWork' in type_names(n)), None)
        if work is None:
            continue
        new_work = {
            '@type': ['CreativeWork', 'Project'],
            '@id': canonical + '#projekt',
            'name': work.get('name'),
        }
        if work.get('headline'):
            new_work['headline'] = work['headline']
        # a person creates; the studio publishes and holds copyright
        new_work['creator'] = {'@id': PERSON}
        new_work['author'] = {'@id': PERSON}
        new_work['publisher'] = {'@id': ORG}
        new_work['copyrightHolder'] = {'@id': ORG}
        if work.get('description'):
            new_work['description'] = work['description']
        # hashtags are not keywords
        new_work['keywords'] = keywords
        new_work['isPartOf'] = {'@id': PORTFOLIO}
        new_work['mainEntityOfPage'] = canonical
        if images:
            new_work['image'] = images
        # NOTE: dateCreated / locationCreated deliberately omitted until the studio
        # confirms the year and place for each project - see docs/projects.md
        # NB: compare via type_names() - the rewritten node carries a LIST @type,
        # so a plain `!= 'CreativeWork'` comparison silently kept it and appended a
        # duplicate on every run.
        others = [n for n in graph if 'CreativeWork' not in type_names(n)]
        payload['@graph'] = [new_work] + others
        html = replace_ld_block(html, span, payload)
        break
    io.open(path, 'w', encoding='utf-8').write(html)
    return True


def rewire_portfolio():
    path = os.path.join(ROOT, 'projekty.html')
    html = io.open(path, encoding='utf-8').read()
    for span in find_ld_blocks(html):
        payload = json.loads(span[2])
        if payload.get('@type') != 'CollectionPage':
            continue
        payload['@id'] = PORTFOLIO
        payload['isPartOf'] = {'@id': WEBSITE}
        payload['about'] = {'@id': ORG}
        payload['hasPart'] = [
            {'@id': canonical + '#projekt'}
            for _, canonical, _ in PROJECTS.values()
        ]
        # reorder so the container fields read before the item list
        ordered = {}
        for key in ('@context', '@type', '@id', 'name', 'url', 'isPartOf', 'about',
                    'hasPart', 'mainEntity'):
            if key in payload:
                ordered[key] = payload[key]
        html = replace_ld_block(html, span, ordered)
        break
    io.open(path, 'w', encoding='utf-8').write(html)


def fix_about_page():
    """o-nas.html invented a second @id for the architect (#founder).

    Two @ids for one person is exactly the disconnect this pass exists to remove,
    so the Person is now defined once on index.html and referenced here.
    """
    path = os.path.join(ROOT, 'o-nas.html')
    html = io.open(path, encoding='utf-8').read()
    for span in find_ld_blocks(html):
        payload = json.loads(span[2])
        graph = payload.get('@graph') or []
        person = next((n for n in graph if 'Person' in type_names(n)), None)
        if person is None or person.get('@id') != BASE + '#founder':
            continue
        page = next((n for n in graph if 'AboutPage' in type_names(n)), None)
        if page is not None:
            page['isPartOf'] = {'@id': WEBSITE}
            page['about'] = {'@id': PERSON}
            page['mainEntity'] = {'@id': PERSON}
        payload['@graph'] = [n for n in graph if 'Person' not in type_names(n)]
        html = replace_ld_block(html, span, payload)
        break
    io.open(path, 'w', encoding='utf-8').write(html)


def rewire_index():
    path = os.path.join(ROOT, 'index.html')
    html = io.open(path, encoding='utf-8').read()
    for span in find_ld_blocks(html):
        payload = json.loads(span[2])
        org, _ = find_org(payload)
        if org is None:
            continue
        org.pop('@context', None)          # belongs only at the top level
        org.pop('founder', None)
        org['logo'] = {'@type': 'ImageObject', '@id': BASE + '#logo',
                       'url': BASE + 'img/goprojekt_logo_dark.svg'}
        # one definition of the architect, referenced by @id from everywhere else
        org['founder'] = {'@id': PERSON}
        org['employee'] = {'@id': PERSON}
        org.setdefault('email', 'biuro@goproject.com.pl')
        person = {
            '@type': 'Person',
            '@id': PERSON,
            'name': 'Adam Kubat',
            'honorificPrefix': 'mgr inż.',
            # wording taken verbatim from the site's own existing schema - "Architekt"
            # is a protected professional title in Poland and is not ours to assert
            'jobTitle': 'Główny Inżynier Projektant i Kierownik Budowy',
            'image': BASE + 'img/adam-kubat.jpg',
            'worksFor': {'@id': ORG},
            'knowsAbout': [
                'Projekty budowlane',
                'Kierownictwo budowy',
                'Nadzór inwestorski',
                'Adaptacje MPZP i WZ',
                'Odbiory mieszkań od dewelopera',
                'Świadectwa energetyczne',
            ],
        }
        website = {
            '@type': 'WebSite',
            '@id': WEBSITE,
            'url': BASE,
            'name': 'GOPROJECT Pracownia Projektowa',
            'inLanguage': 'pl-PL',
            'publisher': {'@id': ORG},
        }
        html = replace_ld_block(html, span,
                                {'@context': 'https://schema.org',
                                 '@graph': [org, person, website]})
        break
    io.open(path, 'w', encoding='utf-8').write(html)


if __name__ == '__main__':
    images = load_images()
    for page, (slug, canonical, keywords) in PROJECTS.items():
        rewire_project(page, slug, canonical, keywords, images.get(slug, []))
        print('rewired  %-46s %d image refs' % (page, len(images.get(slug, []))))
    rewire_portfolio()
    print('rewired  projekty.html                              -> #portfolio + hasPart')
    rewire_index()
    print('rewired  index.html                                -> #organization, #adam-kubat, #website')
    fix_about_page()
    print('rewired  o-nas.html                                -> #founder merged into #adam-kubat')
