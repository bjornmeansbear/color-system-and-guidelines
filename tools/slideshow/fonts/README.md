# Fonts

All OFL (SIL Open Font License), self-hosted per RULES.md in
`~/Code/color-system-and-guidelines`: "every font used is either an open/libre
license (OFL etc., self-hosted) or the system font stack."

They are base64-embedded into the built HTML rather than linked, so a built
file is self-contained and needs no network. That matters here: the gallery
build runs from a local file on a projector, and a CDN link would mean losing
the typography if venue wifi drops mid-show.

| File | Family | Source |
|---|---|---|
| `Basteleur-Bold.woff2` | Basteleur | Velvetyne — copied from `~/Code/oblique` |
| `Sligoil-Micro.woff2` | Sligoil Micro | Velvetyne — copied from `~/Code/oblique` |
| `SpaceGrotesk.woff2` | Space Grotesk | Google Fonts (OFL), latin subset |
| `WorkSans.woff2` | Work Sans | Google Fonts (OFL), latin subset |
| `LibreFranklin.woff2` | Libre Franklin | Google Fonts (OFL), latin subset |
| `CormorantGaramond.woff2` | Cormorant Garamond | Google Fonts (OFL), latin subset |
| `Feroniapi-MediumItalic.woff2` | Feroniapi | Velvetyne (OFL), from `~/Code/libreFontLibrary` |
| `Anthony.woff2` | Anthony | Velvetyne (OFL), from `~/Code/libreFontLibrary` |
| `LeMurmure.woff2` | Le Murmure | Velvetyne (OFL), from `~/Code/libreFontLibrary` |
| `Compagnon-Roman.woff2` | Compagnon | Velvetyne (OFL), from `~/Code/libreFontLibrary` |
| `Combat.woff2` | Combat | Velvetyne (OFL), from `~/Code/libreFontLibrary` |
| `TerminalGrotesque.woff2` | Terminal Grotesque | Velvetyne (OFL), from `~/Code/libreFontLibrary` |
| `Director-Regular.woff2`, `FT88-*.woff2`, `Louise-Regular.woff2`, `Latitude-Regular.woff2`, `Equateur-Regular.woff2`, `Abordage-Regular.woff2` | Degheest collection | Velvetyne (OFL), from `~/Code/libreFontLibrary` |
| `Spectral-200…800.woff2` | Spectral (7 statics) | Google Fonts (OFL), latin subset |
| `Overpass-VF.woff2` | Overpass, wght 100–900 | Google Fonts (OFL), latin subset, variable |
| `Newsreader-VF.woff2` | Newsreader, wght 200–800, opsz | Google Fonts (OFL), latin subset, variable |
| `AtkinsonHyperlegibleNext-VF.woff2` | Atkinson Hyperlegible Next, wght 200–800 | Google Fonts (OFL), latin subset, variable |
| `BioRhyme-VF.woff2` | BioRhyme (incl. Expanded), wght 200–800, wdth 100–125 | Google Fonts (OFL), latin subset, variable |
| `ClimateCrisis-VF.woff2` | Climate Crisis, YEAR 1979–2050 | Google Fonts (OFL), latin subset, variable |
| `Oi.woff2`, `Fruktur.woff2`, `YatraOne.woff2`, `YoungSerif.woff2` | Oi, Fruktur, Yatra One, Young Serif | Google Fonts (OFL), latin subset |
| `Astloch-400.woff2`, `Astloch-700.woff2` | Astloch | google/fonts repo, full file (Reserved Font Name, so not subset) |

`LICENSE-*` files: one per family (Degheest shares one). The Velvetyne ones came
with the fonts; the Google ones are `OFL.txt` from the google/fonts repo.
The Velvetyne files were converted to woff2 with fontTools and not subset:
under the OFL a subset counts as a modified font, which trips the Reserved
Font Name clause.

Which faces are display (short quotes only) is set in `QUOTE_FACES` in
`build_slideshow.py`. The
Google-hosted four are all OFL; see fonts.google.com for each family's licence.
