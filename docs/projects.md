# Rejestr projektów / Project register

**Source of truth for project naming.** Folder names, slugs, page titles and
structured data are all derived from this table — change a name here first,
then apply it, so the site, the image folders and the schema never drift apart.

Status: **proposal** — the names marked `«…»` are placeholders inferred from
GOPROJECT's own render filenames and **require confirmation by mgr inż. Adam Kubat**.

---

## 1. Register

| Code | Nazwa (display) | Typ | Miejscowość | Rok | Zakres | Status | Image folder | Page |
|---|---|---|---|---|---|---|---|---|
| GP-2023-01 | Budynek wielorodzinny «Śniadeckich» | wielorodzinny | Chojnice | 2023 | projekt + kierownik budowy | zrealizowany | `budynek-wielorodzinny` | `projekt-budynek-mieszkalny-wielorodzinny.html` |
| GP-2023-02 | «Infocentrum» — obiekt użyteczności publicznej | użyteczności publicznej | — | 2023 | konkurs architektoniczny | **zaparkowany** — poza portfolio | `obiekt-uzytecznosci-publicznej` | `projekt-obiekt-uzytecznosci-publicznej.html` |
| GP-2024-01 | Dom jednorodzinny w Chojnicach | jednorodzinny | **Chojnice** | — | projekt + kierownik budowy + nadzór | **zrealizowany** | `dom-jednorodzinny` | `projekt-dom-jednorodzinny.html` |
| GP-2024-02 | Osiedle budynków dwulokalowych «…» | dwulokalowe | — | 2024 | zespół + infrastruktura | w toku | `osiedle-budynkow-dwulokalowych` | `projekt-osiedle-budynkow-dwulokalowych.html` |

### Evidence behind the placeholders

These were not invented — they were read off GOPROJECT's own asset names:

| Placeholder | Evidence in the repository |
|---|---|
| «Śniadeckich» | an unused 540 KB render named `wielorodzinny-sniadeckich-hq.webp` |
| «Infocentrum» | `wielorodzinny-infocentrum.webp` and `infocentrum-…-wizualizacja-zima.webp` |
| «Nad morzem» | `nowoczesny-dom-jednorodzinny-nad-morzem-wizualizacja.webp` |

### Open questions for the studio

1. **Confirm or correct the three names above** and give the estate in GP-2024-02 a name.
2. **Confirm the years** (2023 / 2024 are guesses derived from where the files sit).
3. **Confirm the municipality** for GP-2023-02 and GP-2024-02.
4. **`dom-jednorodzinny` is currently a set of different houses.** The folder holds
   renders of at least five distinct designs (`ceglany`, `drewniany`, `parterowy`,
   `dwupiętrowy`, `nad morzem`, `biały`). They cannot all be one project. Either
   pick the real project house and archive the rest, or promote each house to its
   own register row — which would take the portfolio from 4 entries to 9.

### Parked projects

**GP-2023-02 is parked** — held out of the portfolio deliberately, to be added back later.

**Why:** the public-building entry is a competition **concept** that carried only two real
renders (its other four tiles were placeholders). It weakened the portfolio rather than
strengthening it, and showing a concept beside built work blurs what the practice is
actually claiming. The `publiczny` filter button and the `Koncepcja` badges went with it.

**Where it lives now — outside the repo**, because `tohauk18/goproject-website` is a
**public** repository:

```
~/Desktop/goproject-parked/
  projekt-obiekt-uzytecznosci-publicznej.html
  obiekt-uzytecznosci-publicznej-images/      6 tiles x 2 sizes
```

**To bring it back:**

1. `mv ~/Desktop/goproject-parked/projekt-obiekt-uzytecznosci-publicznej.html .`
2. `mv ~/Desktop/goproject-parked/obiekt-uzytecznosci-publicznej-images img/projects/obiekt-uzytecznosci-publicznej`
3. Delete `'obiekt-uzytecznosci-publicznej'` from `PARKED_SLUGS` in `tools/build-images.py`
4. Re-add by hand: the portfolio card on `index.html` and `projekty.html`, the footer
   entry on all pages, the `<url>` block in `sitemap.xml`, the `ListItem` in the portfolio
   JSON-LD, and the `publiczny` filter button on both portfolio pages
5. `python3 tools/build-images.py && python3 tools/rebuild-portfolio.py`

**Before it returns, generate its renders.** Four of its six tiles were placeholders —
re-adding it as-is would put grey boxes back into a live portfolio.

The filter bar currently has four buttons:
`Wszystkie · Domy jednorodzinne · Osiedla dwulokalowe · Budynki wielorodzinne`

### The other house designs, from `projekt-dom-jednorodzinny`

That page used to display **nine images of at least six different houses** — a modern
barn, a brick house, a two-storey flat-roof house, a seaside pavilion, a small white
barn and a wooden house — presented as one project. They are now parked at:

```
~/Desktop/goproject-parked/dom-jednorodzinny-inne-koncepcje/      12 files
```

They are **not** wasted. Each is a candidate register entry, and promoting them would
take the portfolio from 3 to as many as 8 projects — each needing only renders.

| What it shows | Source render |
|---|---|
| night render | `dom-jednorodzinny-widok-noca-wizualizacja` |
| single-storey with garage | `dom-parterowy-z-garazem-wizualizacja` |
| two-storey, flat roof | `dwupietrowy-dom-z-ogrodem-wizualizacja` |
| seaside pavilion | `nowoczesny-dom-jednorodzinny-nad-morzem-wizualizacja` |
| white house with garden | `dom-jednorodzinny-bialy-z-ogrodem-wizualizacja` |
| wooden house with terrace | `dom-drewniany-z-tarasem-zdjecie-realizacji` **(real photograph)** |

**Note:** that wooden-house photograph was the *only* real image the page had. It is
parked with the rest — if it turns out to be a completed project, it deserves its own
entry rather than sitting inside a concept set.

### The page's own metadata already said Chojnice

Worth recording, because it settles the "which house" question. The page's parameter
table already read **167,12 m²**, **764,54 m³**, **Lokalizacja: Chojnice**, **Status:
Zrealizowany pod klucz** — exactly the figures published for *"Projekt domu
jednorodzinnego w Chojnicach"* on the old site. The page was always meant to be this
house; only its images were wrong. The table was missing two real values, now added:
**pow. zabudowy 120,00 m²** and **wysokość 7,86 m**.

### Confirm the photo / drawing pairing

The three photographs (`goprojecthouse_adam_kubat1/7/8`) and the drawing sheet
(`Projekt5front` / `Projekt5inside`) were paired by the **old site's own carousel**, so
the pairing is GOPROJECT's assertion rather than an invention here. It still deserves a
human eye: the elevation sheet shows a roof with a different dormer arrangement from
the photographs.

Also: those drawings are **760 px wide and carry a tiled GoProject watermark**. They
read as thumbnails only — the floor plan's dimension text is not legible at that size.
A re-export from the original CAD/PDF at 1600–2400 px is what would make the drawings
section genuinely persuasive.

---

## 2. Naming rules

**Template**

```
[Typ] «Nazwa własna lub ulica» — [Miejscowość], [rok]
```

**Rules**

| Element | Rule |
|---|---|
| Typ | Exactly one building type |
| Nazwa własna | Street, estate or competition name, in Polish « » quotes |
| Miejscowość | Always — the two markets are Chojnice and Gdańsk |
| rok | Year of realisation or competition |
| Process phrases | **Banned from names.** `— od koncepcji do realizacji` is a claim, not a title |

**Decision tree for a project that has no name yet**

1. Realised for a client → street or estate name + town + completion year
2. Competition entry → project name + competition + year + result
3. Own study, no client → studio code + descriptive name + explicit `Koncepcja` label
4. Confidential developer work → type + town + scope, and say it is confidential

**Rule:** no render export leaves the studio before the project has a register row.

---

## 3. Slug convention

Keep the building-type keyword for search, add the location, drop the process phrase:

```
dom-jednorodzinny-nad-morzem.html
budynek-wielorodzinny-sniadeckich-chojnice.html
osiedle-budynkow-dwulokalowych-<miasto>.html
infocentrum-obiekt-uzytecznosci-publicznej.html
```

**Not yet applied.** The four page URLs are deliberately unchanged, because a
street name and a year are factual claims about a real practice and must be
confirmed before they go live. Once the table above is signed off, renaming is
one pass: update this file, then run the rename step and re-run
`tools/rebuild-portfolio.py`.

---

## 4. How to apply a rename

1. Update the row here.
2. If the display name changed only: update the `<title>`, `<h1>` and the
   `name`/`headline` fields in the page's JSON-LD. Nothing else moves.
3. If the URL changed too: rename the file, add a redirect from the old URL, and
   update every internal link (`index.html`, `projekty.html`, nav, footer,
   `sitemap.xml`).
4. If the **image folder** changed: rename `img/projects/<old>` to the new slug,
   update the `project` value in the tile definitions in `tools/build-images.py`,
   then re-run `tools/build-images.py` and `tools/rebuild-portfolio.py`.
