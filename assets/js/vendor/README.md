# Third-party notices

`assets/js/fastsearch.js` began as the search script of the
[PaperMod theme](https://github.com/adityatelange/hugo-PaperMod/tree/3e5362100777a9426e05ef30e972800cabb54f21);
`PaperMod-LICENSE` retains that theme's MIT notice.

Search used to bundle Fuse.js 7.0.0 for fuzzy matching. It was removed on
2026-10-26: the script now matches every space-separated keyword literally
and ranks by the field it occurs in, so no third-party code is bundled.
