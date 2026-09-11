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

`LICENSE-Basteleur.txt` and `LICENSE-Sligoil.txt` came with those faces. The
Google-hosted four are all OFL; see fonts.google.com for each family's licence.
