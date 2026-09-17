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
| GP-2023-02 | «Infocentrum» — obiekt użyteczności publicznej | użyteczności publicznej | — | 2023 | konkurs architektoniczny | koncepcja | `obiekt-uzytecznosci-publicznej` | `projekt-obiekt-uzytecznosci-publicznej.html` |
| GP-2024-01 | Dom jednorodzinny «Nad morzem» | jednorodzinny | Pomorze | 2024 | projekt + nadzór | w realizacji | `dom-jednorodzinny` | `projekt-dom-jednorodzinny.html` |
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
