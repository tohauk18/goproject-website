# GOPROJECT — Portfolio Naming & Image System

**Deliverable:** naming system for projects + image organisation system + creator/entity wiring
**Prepared for:** GOPROJECT Pracownia Projektowa (mgr inż. Adam Kubat) + the site creator
**Version:** v1.0 proposal · audited against the live HTML and the `img/` tree in this repo
**Status:** untracked working doc — do not ship to production hosting

---

## 1. Audit — what the portfolio says today

Facts taken from the four project pages, `projekty.html`, `index.html` and `img/`.

| # | Finding | Evidence |
|---|---|---|
| 1 | **Projects have no names — only building types.** All four titles are `[typ] — [opis procesu]`. | `Dom jednorodzinny — od koncepcji do realizacji`, `Budynek mieszkalny wielorodzinny — od koncepcji do realizacji`, `Osiedle budynków jednorodzinnych dwulokalowych — kompleksowy projekt osiedlowy`, `Obiekt użyteczności publicznej — projekt konkursowy` |
| 2 | **Three of four titles end in the same process phrase**, so nothing distinguishes them in a search result or a shared link. | `<title>` of each project page |
| 3 | **They compete with your own service pages** for `dom jednorodzinny` / `budynek wielorodzinny`, so six pages fight over one intent instead of one page owning each. | `projekt-*.html` vs `uslugi-*.html` |
| 4 | **The folder taxonomy mixes three naming axes.** | `dom-jednorodzinny` (typology) · `mieszkalny` (typology, generic) · `osiedle-dwulokalowe` (typology+scale) · `infocentrum` (proper noun) |
| 5 | **`img/projects/infocentrum/` is a dumping ground for two different projects.** | public-building renders (`infocentrum-…-zima`, `nowoczesny-budynek-biurowy-…`) sit next to multi-family renders (`wielorodzinny-perspektywa-1…4`, `wielorodzinny-sniadeckich-hq`) |
| 6 | **A single-family page shows multi-family images.** Three gallery tiles pull from `mieszkalny/` while their alt text claims "Projekt domu jednorodzinnego". | `projekt-dom-jednorodzinny.html` (~lines 443/455) → `img/projects/mieszkalny/budynek-mieszkalny-sytuacja-dzialki-widok-*.webp` |
| 7 | **Portfolio is thin: 4 projects, 4 card images**, each reused on `index.html`, `projekty.html` and its own page. | `osiedle-dwulokalowe-lot-ptaka`, `wielorodzinny-infocentrum`, `budynek-mieszkalny-wielorodzinny-widok-poludniowo-zachodni`, `dom-jednorodzinny-z-garazem-i-ogrodem-wizualizacja` |
| 8 | **Two renders ship but are never displayed** — dead weight. | `dom-parterowy-szkłana-szczytowa-sciana-wizualizacja.webp` (212 KB), `wielorodzinny-sniadeckich-hq.webp` (540 KB) |
| 9 | **The hero is repeated as gallery tile #1 on the same page.** | `projekt-dom-jednorodzinny.html`: hero and `<!-- File 1 -->` both use `dom-jednorodzinny-z-garazem-i-ogrodem-wizualizacja.webp` |
| 10 | **Filenames are full Polish sentences up to 78 characters**, duplicating alt text. | `budynek-mieszkalny-sytuacja-dzialki-widok-poludniowo-wschodni.webp` |
| 11 | **`-2` versioning anti-pattern** — two "north-west" views, no way to tell which is canonical. | `osiedle-dwulokalowe-widok-nw.webp` vs `…-widok-nw-2.webp` |
| 12 | **Compass abbreviations are used as public labels.** | gallery chips `Widok NW` / `Widok SE` |
| 13 | **No `width`/`height` on any gallery image** → layout shift (CLS) on every portfolio page. Only logos have them. | galleries report `-x-`; logos `290x24` |
| 14 | **Inconsistent lazy-loading**: `projekty.html` cards use `loading="lazy"`, project galleries do not. | `projekty.html` `load=lazy` vs `projekt-*.html` `load=-` |
| 15 | **Fixed `h-64` + `object-fit: cover` crops the architecture.** | `class="h-64"` wrapper + `class="w-full h-full object-cover"` |
| 16 | **Aspect ratios are chaotic** — 3.69:1, 1.78:1, 1.71:1, 1.44:1, 1.41:1, 1.33:1, 0.78:1, 0.75:1 inside single galleries. | measured in §1.1 |
| 17 | **Files are overweight**: 844 KB, 616 KB, 600 KB, 598 KB served as-is; a 1195×896 render weighs 537 KB. | repo sizes |
| 18 | **Renders and real photos are mixed with no label**, destroying the trust signal an architect sells on. | `dom-drewniany-z-tarasem-zdjecie-realizacji.webp` sits beside 3D renders |
| 19 | **`keywords` in structured data are hashtags** — not a valid keyword list. | `"keywords": ["#domjednorodzinny", "#mieszkalny", …]` on every project page |
| 20 | **`creator` and `author` contradict each other and are not connected.** Architect = `author`, studio = `creator`, no `@id` anywhere. | JSON-LD block, all 4 project pages |
| 21 | **Orphan scratch file in the web root** — 19 broken internal links, never referenced. | `_live.html` |
| 22 | **macOS `.DS_Store` inside `img/` subfolders** — git-ignored, but leaks into ZIP exports. | `img/.DS_Store`, `img/projects/*/.DS_Store` |

### 1.1 Measured image inventory

| File | Pixels | Ratio | Size |
|---|---|---|---|
| `mieszkalny/budynek-mieszkalny-wielorodzinny-widok-polnocno-wschodni.webp` | 1920x1440 | 1.33 | 92 KB |
| `mieszkalny/budynek-mieszkalny-wielorodzinny-widok-poludniowo-zachodni.webp` | 1920x1123 | 1.71 | 80 KB |
| `mieszkalny/budynek-mieszkalny-sytuacja-dzialki-widok-polnocno-zachodni.webp` | 1920x1338 | 1.44 | 140 KB |
| `mieszkalny/budynek-mieszkalny-sytuacja-dzialki-widok-poludniowo-wschodni.webp` | 1920x1363 | 1.41 | 104 KB |
| `mieszkalny/budynek-mieszkalny-sytuacja-dzialki-widok-poludniowo-zachodni.webp` | 1920x1363 | 1.41 | 112 KB |
| `dom-jednorodzinny/dom-jednorodzinny-z-garazem-i-ogrodem-wizualizacja.webp` | 1108x1420 | **0.78 portrait** | 172 KB |
| `dom-jednorodzinny/dom-parterowy-szkłana-szczytowa-sciana-wizualizacja.webp` | 1427x1102 | 1.29 | 212 KB *(unused)* |
| `dom-jednorodzinny/dom-drewniany-z-tarasem-zdjecie-realizacji.webp` | 1039x583 | 1.78 | 128 KB |
| `dom-jednorodzinny/dom-jednorodzinny-bialy-z-ogrodem-wizualizacja.webp` | 506x321 | 1.58 but **only 506 px wide** | 36 KB |
| `infocentrum/wielorodzinny-infocentrum.webp` | 1195x896 | 1.33 | 556 KB |
| `infocentrum/wielorodzinny-sniadeckich-hq.webp` | 1195x896 | 1.33 | 540 KB *(unused)* |
| `infocentrum/infocentrum-budynek-uzytecznosci-publicznej-wizualizacja-zima.webp` | 1039x282 | **3.69 banner** | 64 KB |
| `osiedle-dwulokalowe/osiedle-dwulokalowe-lot-ptaka.webp` | 1402x1122 | 1.25 | 844 KB |
| `osiedle-dwulokalowe/osiedle-dwulokalowe-widok-front.webp` | 1388x1133 | 1.23 | 456 KB |
| `osiedle-dwulokalowe/osiedle-dwulokalowe-widok-ne.webp` | 896x1195 | **0.75 portrait** | 616 KB |
| `osiedle-dwulokalowe/osiedle-dwulokalowe-widok-nw.webp` | 896x1195 | **0.75 portrait** | 576 KB |
| `osiedle-dwulokalowe/osiedle-dwulokalowe-widok-nw-2.webp` | 896x1195 | **0.75 portrait** | 600 KB |
| `osiedle-dwulokalowe/osiedle-dwulokalowe-widok-sw.webp` | 896x1195 | **0.75 portrait** | 540 KB |

**Five of the eight `osiedle-dwulokalowe` images are portrait** and are rendered inside a `h-64` landscape window, so over half that gallery is cropped rather than composed.

### 1.2 Renders already available but not used

Branch `restructure` does **not** include 16 renders that still exist on the older `main` branch. They are genuine portfolio material:

- `dom-jednorodzinny/`: `dom-jednorodzinny-ceglany-wizualizacja`, `dom-jednorodzinny-widok-noca-wizualizacja`, `dom-parterowy-z-garazem-wizualizacja`, `dwupietrowy-dom-z-ogrodem-wizualizacja`, `nowoczesny-dom-jednorodzinny-nad-morzem-wizualizacja`
- `infocentrum/`: `nowoczesny-budynek-biurowy-wizualizacja`, `nowoczesny-budynek-publiczny-fasada-wizualizacja`, `wielorodzinny-perspektywa-1` … `-4`
- `mieszkalny/`: `budynek-mieszkalny-wielorodzinny-widok-polnocno-zachodni` (the missing third elevation)
- `osiedle-dwulokalowe/`: `domy-szeregowe-elewacja-frontowa-wizualizacja`, `domy-szeregowe-ogrodki-plac-zabaw-wizualizacja`, `domy-szeregowe-parking-wizualizacja`, `osiedle-domow-szeregowych-widok-z-lotu-ptaka`

> Retrieval: `git checkout origin/main -- img/projects/` from the repo root — but only **after** the taxonomy in §3 is agreed, so nothing is imported into the old structure.

---

## 2. Project naming system

### 2.1 Principle — a project is a place, not a category

Today every project is named after its **building type**. A visitor can browse the whole portfolio and never learn a single thing that only GOPROJECT can say. A portfolio project should be named so it can be spoken out loud to a future client:

> "To robiliśmy przy Śniadeckich" / "Ten dom nad morzem to nasz"

**Template for display:**

```
[Typ] «Nazwa własna lub ulica» — [Miejscowość], [rok]
```

**Rules of use**

| Element | Rule |
|---|---|
| Typ | Exactly one. `Dom jednorodzinny`, never `Dom jednorodzinny i osiedle` |
| Nazwa własna | Street, estate name, or competition name. Quote it with Polish « » |
| Miejscowość | Always. Your two markets are Chojnice and Gdańsk — say which |
| rok | Year of realisation or competition. Real years are credibility |
| Process phrases | **Banned from names.** `— od koncepcji do realizacji` is a claim, not a title. Say it once, on the homepage, where it has room to land |

### 2.2 Decision tree — how to name a project that has no name yet

1. **Realised for a client** → street or estate name + town + completion year.
   `Osiedle «Brzozowa» — Chojnice, 2024`
2. **Competition entry** → project name + competition + year + result if any.
   `Infocentrum — konkurs SARP, 2023 (wyróżnienie)`
3. **Own study / no client yet** → studio code + descriptive name + explicit `Koncepcja` label, so it never reads as a misrepresentation.
   `GP-2024-07 «Dom nad morzem» — koncepcja`
4. **Developer order under confidentiality** → type + town + scope only, and say so.
   `Budynek wielorodzinny — Gdańsk, 48 lokali (szczegóły objęte poufnością)`

**Rule:** no project may receive its first render export until it has a name recorded in the register (§2.4). Naming after the fact is how the `-nw` / `-nw-2` mess happens.

### 2.3 Proposed rename table — **requires confirmation by Adam Kubat**

Names marked `«…»` are placeholders inferred from your own filenames; confirm or correct them.

| Current URL | Current title | Proposed display name | Proposed H1 |
|---|---|---|---|
| `projekt-dom-jednorodzinny.html` | Dom jednorodzinny — od koncepcji do realizacji | **Dom jednorodzinny «Nad morzem» — Pomorze** *(placeholder — a `nowoczesny-dom-jednorodzinny-nad-morzem-wizualizacja` render exists)* | Dom jednorodzinny z garażem dwustanowiskowym — projekt i nadzór |
| `projekt-budynek-mieszkalny-wielorodzinny.html` | Budynek mieszkalny wielorodzinny — od koncepcji do realizacji | **Budynek wielorodzinny, ul. Śniadeckich — Chojnice** *(placeholder — a `wielorodzinny-sniadeckich-hq` render exists)* | Budynek wielorodzinny przy ul. Śniadeckich — od koncepcji po odbiór |
| `projekt-osiedle-budynkow-dwulokalowych.html` | Osiedle budynków jednorodzinnych dwulokalowych — kompleksowy projekt osiedlowy | **Osiedle budynków dwulokalowych «…», [miasto], [N] budynków** | Osiedle [N] budynków dwulokalowych — projekt zespołu i infrastruktury |
| `projekt-obiekt-uzytecznosci-publicznej.html` | Obiekt użyteczności publicznej — projekt konkursowy | **Infocentrum — projekt konkursowy, [rok]** *(placeholder — an `infocentrum-…-wizualizacja-zima` render exists)* | Infocentrum — obiekt użyteczności publicznej, projekt konkursowy |

### 2.4 Slug convention (URLs)

Keep the type keyword for search, add the location, drop the process phrase:

```
projekt-<typ>-<lokalizacja>.html

dom-jednorodzinny-nad-morzem.html
budynek-wielorodzinny-sniadeckich-chojnice.html
osiedle-budynkow-dwulokalowych-<miasto>.html
infocentrum-obiekt-uzytecznosci-publicznej.html
```

*If any of these four URLs is already indexed in Google, keep the existing URL and change only the visible name, then add a 301 to the new slug when you are ready. The site is new, so renaming now is cheaper than renaming later.*

### 2.5 Title tag and meta formula

```
<title>{Nazwa} | {Typ} {Miejscowość} — GOPROJECT</title>

Budynek wielorodzinny ul. Śniadeckich, Chojnice — GOPROJECT
Infocentrum — projekt konkursowy obiektu publicznego — GOPROJECT
```

Why: `GOPROJECT` last is fine for brand recall, but the **name and place must come first**, because that is what a client is searching for and what makes four projects distinguishable in a list of results. Today all four titles open with a generic type and three end with the same phrase — that is the single cheapest SEO and positioning win available.

### 2.6 Project register (create it now)

Keep one `docs/projects.md` table as the source of truth, and derive folder names, slugs and schema from it:

| Code | Name | Type | Place | Year | Scope | Status | Slug |
|---|---|---|---|---|---|---|---|
| GP-2023-01 | Budynek wielorodzinny, ul. Śniadeckich | wielorodzinny | Chojnice | 2023 | projekt + kierownik budowy | zrealizowany | `budynek-wielorodzinny-sniadeckich-chojnice` |
| GP-2023-02 | Infocentrum | użyteczności publicznej | — | 2023 | konkurs | koncepcja | `infocentrum-obiekt-uzytecznosci-publicznej` |
| GP-2024-01 | Dom «Nad morzem» | jednorodzinny | Pomorze | 2024 | projekt + nadzór | zrealizowany | `dom-jednorodzinny-nad-morzem` |
| GP-2024-02 | Osiedle «…» | dwulokalowe | — | 2024 | zespół + infrastruktura | w toku | `osiedle-budynkow-dwulokalowych-…` |

---

## 3. Image organisation system

### 3.1 Folder taxonomy — one folder = one project

```
img/
  studio/                     # studio-wide assets only, never project-specific
    logo-light.svg
    logo-dark.svg
    adam-kubat.jpg
    og-default.jpg            # social share fallback (1200x630)
  projects/
    <slug>/                   # 1:1 with the register in §2.6
      01-hero.webp
      02-sytuacja-dzialki.webp
      ...
```

**Two hard rules**

1. **An image lives in exactly one project folder.** If one image is needed by two projects, the projects are the same project — merge them.
2. **Folder name = the slug in the register.** No exceptions, no synonyms.

### 3.2 Migration map for the folders you have now

| Today | Action |
|---|---|
| `dom-jednorodzinny/` | Rename to `dom-jednorodzinny-nad-morzem/`. **Remove the 3 misfiled `budynek-mieszkalny-sytuacja-dzialki-*` images** (see below). |
| `mieszkalny/` | **Dissolve.** `budynek-mieszkalny-wielorodzinny-widok-poludniowo-zachodni` + `…-polnocno-wschodni` → `budynek-wielorodzinny-sniadeckich-chojnice/`. |
| `infocentrum/` | **Split.** `infocentrum-…-zima`, `nowoczesny-budynek-publiczny-fasada`, `nowoczesny-budynek-biurowy` → `infocentrum-obiekt-uzytecznosci-publicznej/`. `wielorodzinny-*` (infocentrum, sniadeckich-hq, perspektywa-1…4) → `budynek-wielorodzinny-sniadeckich-chojnice/`. |
| `osiedle-dwulokalowe/` | Rename to `osiedle-budynkow-dwulokalowych-<miasto>/`. |

**The one unresolved decision — resolve it first.**

`projekt-dom-jednorodzinny.html` displays three images from `mieszkalny/` labelled "Sytuacja Działki — Widok NW/SE/SW" with alt text claiming *Projekt domu jednorodzinnego*. Either:

- **(a)** they are site studies of the **multi-family** building → move them to `budynek-wielorodzinny-sniadeckich-chojnice/` and **delete those three tiles from the single-family page** (it then needs 3 replacements from the 5 unused single-family renders in §1.2), or
- **(b)** they really are the **house** on its plot → they must be re-exported under the house's slug and the alt text becomes true.

Do not leave a single-family page showing `/mieszkalny/` images: it is the clearest tell that the portfolio is not curated.

### 3.3 Filename convention

```
NN-<rola>.webp
```

| Part | Rule |
|---|---|
| `NN` | Two-digit gallery order: `01`, `02`, `03`. This **replaces** `-2` suffixes — order lives in the name, so nothing is ever "version 2" |
| `<rola>` | One value from the closed vocabulary below |
| no `-wizualizacja` on every file | Mark the **minority** instead: real photos get `realizacja-*`, everything else is understood to be a render |
| max 40 characters | lowercase, ASCII, hyphens, no spaces |

**Closed role vocabulary** — use exactly these, nothing else:

`hero` · `z-lotu-ptaka` · `sytuacja-dzialki` · `plan-sytuacyjny` · `widok-od-ulicy` · `widok-od-ogrodu` · `elewacja-frontowa` · `elewacja-tylna` · `elewacja-boczna` · `rzut-parter` · `rzut-pietro` · `przekroj` · `wnetrze-01…` · `detal-01…` · `realizacja-01…` · `makieta`

**Kill the compass letters.** `widok-nw` / `widok-ne` / `widok-sw` mean nothing to a client, cannot be checked without opening the file, and gave you the `-nw` vs `-nw-2` collision. Name what is visible: `widok-od-ogrodu`, `widok-od-ulicy`, `widok-od-parkingu`.

**Example set for one project**

```
01-hero.webp
02-sytuacja-dzialki.webp
03-z-lotu-ptaka.webp
04-widok-od-ulicy.webp
05-widok-od-ogrodu.webp
06-wnetrze-01.webp
07-realizacja-01.webp
```

### 3.4 Export and delivery spec

| Item | Standard |
|---|---|
| Master | 3:2 **landscape**, 2400 px long edge, sRGB. Masters live outside the repo (`img-master/`, not committed) |
| Web exports | 1600 px and 800 px wide, WebP quality 78. AVIF later if wanted |
| Hero weight | ≤ 250 KB |
| Gallery tile | ≤ 120 KB |
| Card / thumbnail | ≤ 60 KB |
| Upscaling | **Never.** Re-export from the master instead |
| Portrait renders | Two acceptable answers: (a) **re-render landscape** — the 3D scene exists, this is preferred; (b) display them in a genuinely tall card (`aspect-[3/4]`) in a masonry column. **Never** squeeze a 0.75 portrait into a 16:9 window with `object-cover` |
| Ultra-wide renders (e.g. the 1039x282 winter banner) | Use as a full-width band across the page, not as a grid tile |
| Small originals (e.g. 506x321) | Too small for a 2x tile. Re-export at ≥ 1100 px or drop it |

### 3.5 Weight — what you ship today vs the target

| Gallery | Ships today | Target after re-export |
|---|---|---|
| `projekt-osiedle-budynkow-dwulokalowych` | **3.6 MB** (844 + 616 + 600 + 576 + 540 + 456 KB) | ≤ 700 KB |
| `projekt-obiekt-uzytecznosci-publicznej` | 620 KB (556 + 64) | ≤ 350 KB |
| `projekt-dom-jednorodzinny` | 692 KB | ≤ 600 KB |
| `projekt-budynek-mieszkalny-wielorodzinny` | **172 KB for only 2 tiles** | ≈ 400 KB across 6 tiles |

A 1195x896 render currently costs 537 KB. At a correct export it should be roughly 150 KB — a **3.5x** saving on that file alone, with no visible difference.

Also: `wielorodzinny-sniadeckich-hq.webp` (540 KB) is shipped and never displayed. Either promote it to the multi-family hero — which finally gives that project its own identity — or delete it.

### 3.6 Markup — the CLS fix, ready to paste

Replace the `h-64` + `object-cover` wrapper with an intrinsic-ratio box:

```html
<div class="relative aspect-[3/2] overflow-hidden bg-zinc-100">
  <img src="./img/projects/<slug>/01-hero-1600.webp"
       srcset="./img/projects/<slug>/01-hero-800.webp 800w,
               ./img/projects/<slug>/01-hero-1600.webp 1600w"
       sizes="(min-width:1024px) 33vw, (min-width:768px) 50vw, 100vw"
       width="1600" height="1067"
       loading="lazy" decoding="async"
       alt="Dom jednorodzinny z garażem dwustanowiskowym — widok od ogrodu"
       class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
  <div class="absolute top-3 left-3 bg-black/80 text-white font-mono text-[10px] px-2.5 py-1">Widok od ogrodu</div>
  <div class="absolute top-3 right-3 bg-white/90 text-black font-mono text-[10px] px-2.5 py-1">Wizualizacja</div>
</div>
```

- **Only the hero** gets `loading="eager" fetchpriority="high"`; everything else is lazy. Today the project galleries are all eager and `projekty.html` is lazy — pick one rule and apply it everywhere.
- The right-hand badge (`Wizualizacja` / `Realizacja 2024`) is the credibility fix from audit item 18.

### 3.7 Gallery composition rules

1. **Minimum 5 tiles, maximum 12.** `projekt-obiekt-uzytecznosci-publicznej` ships **2** — it reads as unfinished, which is worse than not listing it. The 16 unused renders in §1.2 exist precisely to fix this.
2. **Use the same six-beat running order for every project:**

   | Beat | Role | Answers the question |
   |---|---|---|
   | 1 | `01-hero` | What is it? |
   | 2 | `02-sytuacja-dzialki` / `plan-sytuacyjny` | Where does it stand? |
   | 3 | `03-elewacja-frontowa` or `widok-od-ulicy` | What does the street see? |
   | 4 | `04-rzut-parter` / `wnetrze-01` | How does it work inside? |
   | 5 | `05-detal-01` / second view | Why is it good architecture? |
   | 6 | `06-realizacja-01` | Does it actually exist? |

   A visitor then learns the same thing from every project, and comparing them becomes possible.
3. **Never repeat the hero inside its own gallery** (audit item 9).
4. **Label every tile** with its role in plain Polish, plus the `Wizualizacja` / `Realizacja RRRR` badge.
5. **Alternate the formats on purpose.** Today every tile is the same `h-64` box, so the page reads as a contact sheet rather than a portfolio. A rhythm that works: one full-bleed wide shot → a 2-up → a 3-up → one tall tile for a portrait render.
6. **If a project has no realisation photo, stop at concept and label it.** `Obiekt użyteczności publicznej — projekt konkursowy` must not sit visually equal to a built multi-family block. Honesty here is what sells the *od koncepcji do realizacji* claim you already make on the homepage.

### 3.8 Portfolio index rules (`projekty.html` / `index.html`)

- **Card image = the project hero.** That is correct and good for recognition; keep it. The problem is not the reuse across pages, it is that four cards are the *entire* visible portfolio.
- **Give each card depth:** a 2-image card (hero + one detail) or a 3-image hover stack. Right now a visitor sees four photos and nothing else.
- **Add a fact bar per card:** `typ · miejscowość · rok · zakres`. Four words that turn a picture into an entry.
- **Separate Realizacje from Koncepcje.** This is the single biggest credibility win available: a competition concept and a completed building must not be presented as equals. Two labelled groups, or a filter.
- **Have the filters ready:** `Wszystkie / Domy / Osiedla / Wielorodzinne / Publiczne`. With 4 projects filters are premature, but the taxonomy must already support them so projects 5–10 slot in without a rebuild.
- **Fix the thinness:** importing the 16 renders from §1.2 takes `projekt-obiekt-uzytecznosci-publicznej` from 2 tiles to 6, `projekt-budynek-mieszkalny-wielorodzinny` from 2 to 6 (including the missing north-west elevation), and `projekt-dom-jednorodzinny` from 6 to 8–9 once the misfiled images are removed.

---

## 4. Connecting the creator — one entity graph

### 4.1 What is wrong with the schema today

Every project page declares:

```json
"author":  { "@type": "Person", "name": "mgr inż. Adam Kubat" },
"creator": { "@type": "ProfessionalService", "name": "GOPROJECT Pracownia Projektowa" }
```

The intent is right, the wiring is not:

| Issue | Consequence | Fix |
|---|---|---|
| No `@id` on either entity | Google cannot know that the `Person` on project A is the same person as on project B, or that the studio here is the studio on the homepage | Define each entity **once**, with an `@id`, on the page that owns it; reference by `{"@id": …}` everywhere else |
| `creator` = the studio | Semantically a *person* creates; the studio **publishes**. Right now your own architect is demoted to `author` | `creator` + `author` = the Person; `publisher` + `copyrightHolder` = the Organization |
| `keywords` are hashtags | `#domjednorodzinny` is not a keyword list | Plain terms: `["dom jednorodzinny", "Chojnice", "kierownik budowy"]` |
| No `image`, no dates, no place | Projects are anonymous, undated, unplaced — no portfolio entity is actually built | `image` array (ImageObject), `dateCreated`, `locationCreated` |
| No `isPartOf` / `hasPart` | Four projects float freely instead of forming one portfolio | `CollectionPage` with `hasPart` → each project `@id` |

### 4.2 The model — define once, reference everywhere

```
index.html      defines  #organization  (GOPROJECT)
                defines  #adam-kubat    (mgr inż. Adam Kubat)
                defines  #website

o-nas.html      references  #organization + #adam-kubat   (founder, employee)

projekty.html   defines   #portfolio  (CollectionPage)
                hasPart →  each project  @id

projekt-*.html  references  #adam-kubat   as  creator + author
                references  #organization as publisher + copyrightHolder
                isPartOf    #portfolio
```

That is the whole trick: **one definition per entity, `@id` links everywhere else.** It is what makes the architect, the studio and the projects one connected graph instead of nine unrelated fragments.

### 4.3 Templates — ready to paste

**A. `index.html` — the entity home (defines everything once)**

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ProfessionalService",
      "@id": "https://goproject.com.pl/#organization",
      "name": "GOPROJECT Pracownia Projektowa",
      "alternateName": "GOPROJECT",
      "url": "https://goproject.com.pl/",
      "logo": { "@type": "ImageObject", "@id": "https://goproject.com.pl/#logo",
                "url": "https://goproject.com.pl/img/studio/logo-dark.svg" },
      "image": { "@id": "https://goproject.com.pl/#logo" },
      "founder": { "@id": "https://goproject.com.pl/#adam-kubat" },
      "employee": { "@id": "https://goproject.com.pl/#adam-kubat" },
      "knowsAbout": ["projektowanie architektoniczne", "projekty budowlane",
                     "kierownik budowy", "nadzór inwestorski",
                     "świadectwa energetyczne", "odbiory mieszkań"],
      "areaServed": [
        { "@type": "City", "name": "Chojnice" },
        { "@type": "City", "name": "Gdańsk" },
        { "@type": "AdministrativeArea", "name": "województwo pomorskie" }
      ],
      "address": [
        { "@type": "PostalAddress", "streetAddress": "<ulica i nr>", "postalCode": "89-600",
          "addressLocality": "Chojnice", "addressRegion": "pomorskie", "addressCountry": "PL" },
        { "@type": "PostalAddress", "addressLocality": "Gdańsk", "addressCountry": "PL" }
      ],
      "sameAs": [
        "https://www.google.com/maps/place/<wizytówka>",
        "https://www.facebook.com/<profil>",
        "https://www.instagram.com/<profil>"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://goproject.com.pl/#adam-kubat",
      "name": "Adam Kubat",
      "honorificPrefix": "mgr inż.",
      "jobTitle": "Architekt, kierownik budowy, założyciel GOPROJECT",
      "image": "https://goproject.com.pl/img/studio/adam-kubat.jpg",
      "worksFor": { "@id": "https://goproject.com.pl/#organization" },
      "knowsAbout": ["projektowanie budowlane", "nadzór inwestorski", "odbiory techniczne"],
      "sameAs": ["https://www.linkedin.com/in/<profil>"]
    },
    {
      "@type": "WebSite",
      "@id": "https://goproject.com.pl/#website",
      "url": "https://goproject.com.pl/",
      "name": "GOPROJECT Pracownia Projektowa",
      "inLanguage": "pl-PL",
      "publisher": { "@id": "https://goproject.com.pl/#organization" }
    }
  ]
}
```

**B. `projekty.html` — the portfolio container**

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "@id": "https://goproject.com.pl/projekty.html#portfolio",
      "name": "Portfolio projektów — GOPROJECT",
      "isPartOf": { "@id": "https://goproject.com.pl/#website" },
      "about": { "@id": "https://goproject.com.pl/#organization" },
      "hasPart": [
        { "@id": "https://goproject.com.pl/budynek-wielorodzinny-sniadeckich-chojnice.html#projekt" },
        { "@id": "https://goproject.com.pl/infocentrum-obiekt-uzytecznosci-publicznej.html#projekt" },
        { "@id": "https://goproject.com.pl/dom-jednorodzinny-nad-morzem.html#projekt" },
        { "@id": "https://goproject.com.pl/osiedle-budynkow-dwulokalowych-<miasto>.html#projekt" }
      ]
    }
  ]
}
```

**C. `projekt-*.html` — the project, connected to its creator**

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["CreativeWork", "Project"],
      "@id": "https://goproject.com.pl/budynek-wielorodzinny-sniadeckich-chojnice.html#projekt",
      "name": "Budynek wielorodzinny, ul. Śniadeckich — Chojnice",
      "headline": "Optymalizacja PUM, konstrukcji i instalacji w jednym procesie",
      "creator": { "@id": "https://goproject.com.pl/#adam-kubat" },
      "author":  { "@id": "https://goproject.com.pl/#adam-kubat" },
      "publisher":       { "@id": "https://goproject.com.pl/#organization" },
      "copyrightHolder": { "@id": "https://goproject.com.pl/#organization" },
      "dateCreated": "2023",
      "locationCreated": {
        "@type": "Place",
        "name": "Chojnice",
        "address": { "@type": "PostalAddress", "addressLocality": "Chojnice", "addressCountry": "PL" }
      },
      "about": { "@type": "Place", "name": "Chojnice" },
      "description": "Kompleksowa realizacja mieszkaniowa — od pierwszego spotkania z inwestorem po zakończenie budowy.",
      "keywords": ["budynek wielorodzinny", "Chojnice", "kierownik budowy", "nadzór inwestorski"],
      "isPartOf": { "@id": "https://goproject.com.pl/projekty.html#portfolio" },
      "mainEntityOfPage": {
        "@id": "https://goproject.com.pl/budynek-wielorodzinny-sniadeckich-chojnice.html"
      },
      "image": [
        { "@type": "ImageObject",
          "contentUrl": "https://goproject.com.pl/img/projects/budynek-wielorodzinny-sniadeckich-chojnice/01-hero-1600.webp",
          "width": 1600, "height": 1067,
          "caption": "Widok od ulicy", "representativeOfPage": true },
        { "@type": "ImageObject",
          "contentUrl": "https://goproject.com.pl/img/projects/budynek-wielorodzinny-sniadeckich-chojnice/02-sytuacja-dzialki-1600.webp",
          "width": 1600, "height": 1067,
          "caption": "Sytuacja działki" }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Główna", "item": "https://goproject.com.pl/" },
        { "@type": "ListItem", "position": 2, "name": "Portfolio", "item": "https://goproject.com.pl/projekty.html" },
        { "@type": "ListItem", "position": 3, "name": "Budynek wielorodzinny, ul. Śniadeckich",
          "item": "https://goproject.com.pl/budynek-wielorodzinny-sniadeckich-chojnice.html" }
      ]
    }
  ]
}
```

### 4.4 Visible credit — because schema is invisible

Structured data does not sell architecture; a visible credit line does. Add to every project page, directly under the H1:

```html
<p class="font-mono text-xs text-gray-500">
  Projekt i nadzór: mgr inż. Adam Kubat &nbsp;·&nbsp; GOPROJECT, Chojnice
  &nbsp;·&nbsp; <span>Realizacja 2023</span>
</p>
```

and a fact bar with `Lokalizacja · Rok · Zakres · Powierzchnia / liczba lokali`. A portfolio where every entry states who made it, when and where is the difference between a picture gallery and an architectural practice.

### 4.5 The other reading of "connect creator"

If you also mean the **person or studio who built the site** (the developer handing this over), the clean way is a single `WebPage` entity with a `contributor`, not a footer name glued onto every page:

```json
{ "@type": "WebPage",
  "@id": "https://goproject.com.pl/projekty.html#webpage",
  "isPartOf": { "@id": "https://goproject.com.pl/#website" },
  "contributor": { "@type": "Organization", "name": "<studio>, Gdańsk" } }
```

Keep it in one place so it can be edited in one place. Do not put a developer credit on all 14 pages — it dilutes the architect's credit and ages badly.

---

## 5. Roadmap

### P0 — this week (no new content required, all code and renaming)

| # | Action | Effort | Why now |
|---|---|---|---|
| 1 | Resolve the single-family / multi-family image decision (§3.2) | 30 min | A wrong image on a page is worse than a missing one |
| 2 | Add `width`/`height` + one lazy-loading rule to every gallery (§3.6) | 1 h | Removes layout shift from all 4 portfolio pages |
| 3 | Re-export the 6 `osiedle` renders + the 556 KB file; delete or promote the unused 540 KB one | 2 h | −3 MB, same visual result |
| 4 | Rename the 4 projects + slugs (§2.3) | 2 h | Cheapest positioning & SEO win available |
| 5 | Fix `keywords`, link `creator`/`author` by `@id` (§4) | 2 h | Turns 9 fragments into one entity graph |
| 6 | Add the `Wizualizacja` / `Realizacja RRRR` badge (§3.6) | 1 h | Largest single credibility gain |
| 7 | Move or delete `_live.html`; strip `.DS_Store` from `img/` | 10 min | Removes the only broken-link file and ZIP noise |

### P1 — next two weeks

- Import the 16 unused renders (§1.2) and rebuild every gallery to **≥ 6 tiles** in the six-beat order (§3.7)
- Execute the folder split and rename to `NN-<rola>.webp` (§3.1–3.3)
- Add card depth + fact bars to `projekty.html`; separate **Realizacje** from **Koncepcje** (§3.8)
- Publish the register as `docs/projects.md` (already drafted in §2.6)
- Per-project `og:image` (1200x630 crop of the hero) so shared links stop looking generic

### P2 — the studio layer (this is where the real difference is)

1. **Write the case study, not the caption.** 150 words per project in the shape: *brief → constraint → decision → result*. Your differentiator is that the architect also runs the site supervision — that is buried today in one sentence of a JSON-LD description, when it should be the spine of every project story. No competitor in Chojnice can claim it.
2. **Publish drawings.** You ship 6 renders and 1 site photo, and **zero plans**. Architecture practices are judged on `rzut parteru`, `przekrój` and `plan sytuacyjny`. Adding two drawings per project is the strongest remaining "this is a real pracownia" signal left on the table — and it costs you nothing, because the drawings already exist in your project documentation.
3. **Show the process.** Construction-stage photos for built projects; they prove the *od koncepcji do realizacji* claim instead of asserting it.
4. **Surface the project code** (`GP-2024-01`) as a small mono label in the UI. It ties the register to the site and reads unmistakably as an architecture office.

### Targets to hold the system honest

| Metric | Target |
|---|---|
| Largest gallery payload | < 700 KB |
| CLS on portfolio pages | < 0.1 |
| Tiles per project | ≥ 6 |
| Images serving two projects | 0 |
| Projects with a proper name, place and year | 100% |

---

## Studio summary

The portfolio's problem is not the images. It is that the portfolio does not yet say **who** you are. Four projects named after building types, four photographs reused across three pages, no dates, no locations, no drawings, and the architect credited only in invisible markup.

Fix the naming and connect the creator, and the photographs you already own will work twice as hard. Add the drawings and the supervision story, and no competitor in the region can present the same offer.

### Immediate next step

P0 items 1–7 are all implementable in this repo without new material. On approval, the studio can execute them in a single pass: reorganise `img/`, rename the four projects, replace the gallery markup, and rewire the JSON-LD.
