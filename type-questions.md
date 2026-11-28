# Type questions for prose books

Bjook's rules for poems, newspapers and shelves are in RULES.md ("Bjook"). Prose books (essays, journals, the teaching philosophy, EssayADay) don't have rules yet. `kind = "prose"` is planned in NOTES.md (2026-11-13). These are the decisions a prose book needs that the rules don't settle.

**How to answer:** after each question, write a word, a letter, or "yes" to my guess. Leave any you don't care about blank, and my guess stands. When you answer, the answers move into RULES.md as rules, and this file shrinks.

**Faster than answering:**
- **React to specimens.** `bjook specimen` sets one passage in several faces. The first prose specimen (2026-11-28) sets "Change Over Time" from *Slowing Down Graphic Design* in six roster faces at 10/15pt. Say which ones you'd read a whole book in.
- **Name books you like the look of.** Three to five from your shelf, or library.wjerk.shop. Photograph a spread with a ruler in it, or just name them. Trim, margins, measure, size and leading can be measured off a page, and a rule that starts from a real book you like will be closer than any guess.
- **Mark up a proof.** Circle and scribble on any of the PDFs in `sentence-a-day/books/`. A photo of the page is enough.

---

## The page

1. **Trim size.** Half letter (5.5 × 8.5in) folds from office paper and matches the poems. 6 × 9in is a trade book (the lectureScripts essay pipeline uses it). A5 is the European pocket size. *My guess: half letter for booklets, 6 × 9 for anything over ~80 pages.*
2. **Margins.** Classical proportions (inside narrowest, then top, outside, bottom widest, in roughly 2:3:4:6), or the modern even margin with a deeper foot for the folio? *My guess: classical-leaning, built on the leading grid.*
3. **Measure.** Characters per line for body text: 55–65 (book), up to 75 (looser)? *My guess: about 60.*

## The text

4. **Text face for prose.** The roster's book serifs: Gentium, EB Garamond, Crimson Pro, Newsreader. Or a sans (Libre Franklin, Work Sans) as a deliberate choice? *My guess: one house serif for prose, with others allowed per book. Which one is the house face?*
5. **Size by x-height, not points.** On the specimen, 10pt EB Garamond and Crimson Pro look much smaller than 10pt Gentium or Work Sans. Should a book's size be set so the lowercase matches across faces (EB Garamond nearer 11.5pt), or does each book choose its own size by eye? *My guess: match the x-height to Gentium at 10pt.*
6. **Leading.** Poems use 10/15. Prose usually runs tighter (10/13.5 to 10/14). *My guess: tighter than the poems, still a whole number of lines in the text block.*
7. **Justified or ragged?** The poems are ragged. Most books justify prose and hyphenate it. *My guess: ragged right, hyphenated lightly. That's closer to the kit's web pages and avoids rivers. But it's a taste call.*
8. **New paragraphs.** First-line indent (1em, none after a heading), or a blank line between paragraphs? *My guess: indent. A blank line is the web habit.*
9. **Widows and orphans.** Allow none, or allow one line? *My guess: none.*

## Inside a piece

10. **Headings inside an essay.** Same face in italic (like the poem titles), small caps, the display face (Basteleur), or the sans? *My guess: text-face italic or small caps. Basteleur only for titles.*
11. **Chapter openings.** New page or run on? Sunk start (the title a third of the way down)? Any drop cap? *My guess: new recto page, sunk start, no drop cap.*
12. **Numerals.** Old-style figures (1925 sits in the lowercase) in running text, lining figures in tables? *My guess: old-style in text, where the face has them.*
13. **Small caps** for acronyms (CO₂, WCAG, MICA) and the first words of a chapter? *My guess: yes for acronyms, where the face has real small caps.*
14. **Quotations.** Indented block for anything over ~3 lines, at the text size or a step down? Your wiki's `<<<` blocks come out as these. *My guess: indented 1em both sides, same size, no quote marks around the block.*
15. **Notes.** Footnotes at the foot of the page, endnotes at the back, or sidenotes in the outside margin (Tufte style)? The essay pipeline groups footnotes already. *My guess: footnotes for essays, a Sources list at the end of each piece (your wiki rule: every fact has a checked source).*
16. **Links from the wiki.** Drop them, print them as "(see p. 12)" when the target is in the same book, or print the URL in a note? *My guess: page references inside the book, nothing otherwise.*
17. **Images and captions.** Full measure, or allowed into the margin? Captions in the sans at 0.8 of text, as in the newspaper? *My guess: yes to the newspaper caption rule.*

## The furniture

18. **Running heads.** RULES.md says they earn their place in a prose book: author on the left, title on the right. In prose, should the right-hand head be the chapter title instead of the book title? *My guess: chapter title.*
19. **Folio.** Bottom-outside, as in the poems, or top-outside with the running head? *My guess: keep bottom-outside, so every Bjook book matches.*
20. **The end mark (‡).** At the end of every essay, as in the poems? *My guess: yes.*
21. **Colophon.** Always the faces (with designer and license), the paper, the tool, and the license of the text? *My guess: yes. It's already the rule ("Treat type like a specimen").*
22. **Covers.** Type only, in Basteleur, on a kit tint, the same family as the poems? Or can a prose book carry an image? *My guess: type only, for now.*

## Ink and paper

23. **Paper for prose.** Office white, warm/natural, or the risograph's paper? *My guess: natural/cream where it's an option, which does the kit's warm-ground job.*
24. **One color or two?** Black only, or pink for one thing per book (a heading, the end mark, the folio)? *My guess: black only in print. Pink is a screen accent.*
