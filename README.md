# color-system-and-guidelines
Personal Color system, as well as typography and other image, etc. branding guidelines for all my projects (OOKB, Wjerk, Etc.)

Original OOKB colors:

/* Color Palette */
@ookb-pink:          rgba(236,64,121,1);
@ookb-brown:         rgba(47,41,38,1);
@ookb-gray:          rgba(132,132,120,1);
@ookb-darkgray:      rgba(96,103,103,1);
@ookb-lightgray:     rgba(194,211,186,1);

@ookb-red:           rgba(183,80,81,1);
@ookb-orange:        rgba(195,115,99,1);
@ookb-yellow:        rgba(197,192,101,1);
@ookb-green:         rgba(140,165,115,1);
@ookb-blue:          rgba(157,178,176,1);
@ookb-purple:        rgba(174,139,164,1);

(I have more now somewhere else!)

/* ─────────────────────────────────────────────
   Shared color palette
   Source of truth — import this into any project
   ───────────────────────────────────────────── */
:root {
  /* red */
  --red-0: rgb(255,222,218); --red-1: rgb(255,207,204); --red-2: rgb(255,185,182);
  --red-3: rgb(253,155,152); --red-4: rgb(222,116,115); --red-5: rgb(187,74,76);
  --red-6: rgb(142,42,47);   --red-7: rgb(98,9,21);     --red-8: rgb(57,0,0);
  --red-9: rgb(31,0,0);

  /* orange */
  --orange-0: rgb(255,229,216); --orange-1: rgb(255,215,201); --orange-2: rgb(255,194,179);
  --orange-3: rgb(240,165,149); --orange-4: rgb(208,128,112); --orange-5: rgb(173,88,72);
  --orange-6: rgb(130,57,43);   --orange-7: rgb(89,27,17);    --orange-8: rgb(50,0,0);
  --orange-9: rgb(26,0,0);

  /* yellow */
  --yellow-0: rgb(254,251,187); --yellow-1: rgb(241,238,171); --yellow-2: rgb(221,218,147);
  --yellow-3: rgb(195,191,113); --yellow-4: rgb(162,156,67);  --yellow-5: rgb(127,120,0);
  --yellow-6: rgb(92,85,0);     --yellow-7: rgb(59,52,0);     --yellow-8: rgb(29,22,0);
  --yellow-9: rgb(11,5,0);

  /* green */
  --green-0: rgb(235,255,217); --green-1: rgb(221,242,202); --green-2: rgb(201,222,181);
  --green-3: rgb(173,196,151); --green-4: rgb(137,162,113); --green-5: rgb(101,126,73);
  --green-6: rgb(69,91,44);    --green-7: rgb(39,57,17);    --green-8: rgb(13,27,0);
  --green-9: rgb(2,8,0);

  /* blue */
  --blue-0: rgb(235,251,249); --blue-1: rgb(221,238,236); --blue-2: rgb(201,218,216);
  --blue-3: rgb(172,191,189); --blue-4: rgb(137,157,155); --blue-5: rgb(100,122,120);
  --blue-6: rgb(68,87,85);    --blue-7: rgb(39,54,53);    --blue-8: rgb(12,25,24);
  --blue-9: rgb(1,7,7);

  /* purple */
  --purple-0: rgb(255,237,255); --purple-1: rgb(252,224,244); --purple-2: rgb(234,203,225);
  --purple-3: rgb(208,175,198); --purple-4: rgb(174,140,165); --purple-5: rgb(139,103,130);
  --purple-6: rgb(102,71,94);   --purple-7: rgb(67,41,60);    --purple-8: rgb(34,14,29);
  --purple-9: rgb(14,2,11);

  /* pink */
  --pink-0: rgb(255,203,232); --pink-1: rgb(255,187,218); --pink-2: rgb(255,163,197);
  --pink-3: rgb(255,129,169); --pink-4: rgb(250,81,134);  --pink-5: rgb(214,0,97);
  --pink-6: rgb(164,0,65);    --pink-7: rgb(116,0,37);    --pink-8: rgb(69,0,11);
  --pink-9: rgb(40,0,1);

  /* brown */
  --brown-0: rgb(251,245,242); --brown-1: rgb(238,232,229); --brown-2: rgb(219,212,209);
  --brown-3: rgb(192,185,181); --brown-4: rgb(158,151,147); --brown-5: rgb(122,115,111);
  --brown-6: rgb(88,81,78);    --brown-7: rgb(55,50,47);    --brown-8: rgb(25,21,19);
  --brown-9: rgb(8,5,4);

  /* gray (warm green-gray) */
  --gray-0: rgb(247,248,238); --gray-1: rgb(234,234,224); --gray-2: rgb(215,215,204);
  --gray-3: rgb(187,187,176); --gray-4: rgb(153,153,141); --gray-5: rgb(117,117,105);
  --gray-6: rgb(83,83,72);    --gray-7: rgb(52,51,42);    --gray-8: rgb(23,23,15);
  --gray-9: rgb(6,6,2);

  /* dark-gray (cool blue-gray) */
  --dark-gray-0: rgb(242,248,248); --dark-gray-1: rgb(229,235,235); --dark-gray-2: rgb(209,215,215);
  --dark-gray-3: rgb(181,188,188); --dark-gray-4: rgb(147,154,154); --dark-gray-5: rgb(110,118,118);
  --dark-gray-6: rgb(77,84,84);    --dark-gray-7: rgb(46,52,52);    --dark-gray-8: rgb(19,23,23);
  --dark-gray-9: rgb(4,6,6);

  /* light-gray (green-tinted) */
  --light-gray-0: rgb(239,251,233); --light-gray-1: rgb(225,238,219); --light-gray-2: rgb(205,219,199);
  --light-gray-3: rgb(177,192,170); --light-gray-4: rgb(142,158,135); --light-gray-5: rgb(106,122,98);
  --light-gray-6: rgb(73,88,66);    --light-gray-7: rgb(43,55,37);    --light-gray-8: rgb(16,25,11);
  --light-gray-9: rgb(3,8,1);
}

Color palette stuff:

this is scope creep, but I did start playing around with a wider, improved OOKB color palette based on the work of Jxnblk and MrMrs

https://www.a11yproject.com/
https://clrs.cc/
https://colorable.jxnblk.com/
https://randoma11y.com/
https://jxnblk.com/hello-color

https://github.com/jxnblk/colorable
https://github.com/jxnblk/colorable-app
https://github.com/jxnblk/palx
https://github.com/jxnblk/contrast-swatch
https://github.com/jxnblk/hello-color
https://github.com/jxnblk/hello10k

https://mrmrs.cc/writing/counting-accessible-color-combinations/
https://mrmrs.cc/writing/design-reading/

https://github.com/mrmrs/color-systems
https://github.com/mrmrs/randoma11y-js
https://github.com/mrmrs/css-colors
https://github.com/mrmrs/css-border-colors
https://github.com/mrmrs/skill.color-expert
https://github.com/mrmrs/colors
https://github.com/mrmrs/colors-saturated

https://github.com/johno/css.gui
https://github.com/johno/random-hex-color
https://github.com/johno/random-a11y-api
https://github.com/johno/css-color-list
https://github.com/johno/random-a11y-combo
https://github.com/johno/random-a11y-combo-api
https://github.com/johno/random-a11y-nn
https://github.com/johno/random-a11y-api
https://github.com/johno/colorable
https://github.com/johno/flexbox
https://github.com/johno/clrs
https://github.com/johno/get-contrast
https://github.com/johno/gray
https://github.com/johno/is-named-css-color
https://github.com/johno/named-colors
https://github.com/johno/scrutinize

This should probably break into its own repo