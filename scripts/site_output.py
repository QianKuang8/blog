"""Read generated Hugo pages for the site checker."""

from __future__ import annotations

from functools import cached_property
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit

LEARNING_CONTROLS = {"data-learning-record", "data-learning-status", "data-learning-edit", "data-learning-back"}


class Page(HTMLParser):
    """Links, references, head metadata and learning groups of one HTML page."""

    def __init__(self, html: str = "") -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[dict[str, str | None], str]] = []
        self.references: list[tuple[str, str, str]] = []
        self.canonical_urls: list[str] = []
        self.meta: list[dict[str, str | None]] = []
        self.json_ld: list[str] = []
        self.learning_groups: list[dict] = []
        self.learning_controls: list[dict[str, str | None]] = []
        self._containers: list[dict | None] = []
        self._json_ld: list[str] | None = None
        self._link: dict[str, str | None] | None = None
        self._link_text: list[str] = []
        self._link_groups: list[dict] = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if LEARNING_CONTROLS.intersection(attributes):
            self.learning_controls.append(attributes)
        for name in ("href", "src"):
            if attributes.get(name) and tag != "base":
                self.references.append((tag, name, attributes[name]))
        if tag == "link" and "canonical" in (attributes.get("rel") or "").split():
            self.canonical_urls.append(attributes.get("href") or "")
        elif tag == "meta":
            self.meta.append(attributes)
        elif tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_ld = []
        elif tag == "a":
            self._link, self._link_text = attributes, []
            self._link_groups = [group for group in self._containers if group is not None]
        if tag in {"section", "details"}:
            group = None
            if "data-learning-group" in attributes:
                group = {"tag": tag, "attrs": attributes, "links": []}
                self.learning_groups.append(group)
            self._containers.append(group)

    def handle_data(self, data: str) -> None:
        if self._json_ld is not None:
            self._json_ld.append(data)
        if self._link is not None:
            self._link_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_ld is not None:
            self.json_ld.append("".join(self._json_ld).strip())
            self._json_ld = None
        elif tag == "a" and self._link is not None:
            link = (self._link, "".join(self._link_text).strip())
            self.links.append(link)
            for group in self._link_groups:
                group["links"].append(link)
            self._link = None
        elif tag in {"section", "details"} and self._containers:
            self._containers.pop()

    @property
    def canonical_url(self) -> str | None:
        return self.canonical_urls[0] if self.canonical_urls else None

    @property
    def is_redirect(self) -> bool:
        return any((item.get("http-equiv") or "").lower() == "refresh" for item in self.meta)

    @property
    def is_noindex(self) -> bool:
        return any(
            item.get("name") == "robots" and "noindex" in (item.get("content") or "")
            for item in self.meta
        )

    def links_with(self, attribute: str) -> list[tuple[dict[str, str | None], str]]:
        return [(attrs, text) for attrs, text in self.links if attribute in attrs]


class Site:
    """A generated site directory, addressed by paths relative to its root."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._pages: dict[str, Page] = {}

    def exists(self, relative_path: str) -> bool:
        return (self.root / relative_path).is_file()

    def read(self, relative_path: str) -> str:
        path = self.root / relative_path
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def page(self, relative_path: str) -> Page:
        if relative_path not in self._pages:
            self._pages[relative_path] = Page(self.read(relative_path))
        return self._pages[relative_path]

    def html_paths(self) -> list[str]:
        return sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob("*.html"))

    @cached_property
    def home_url(self) -> str:
        return self.page("index.html").canonical_url or ""

    @cached_property
    def base_path(self) -> str:
        return unquote(urlsplit(self.home_url).path).rstrip("/") + "/"

    def url_of(self, relative_path: str) -> str:
        """Public URL of an output file; index.html files are served as their directory."""
        path = relative_path.removesuffix("index.html")
        return urljoin(self.home_url, quote(path))

    def resolve(self, url: str, page_path: str = "") -> str | None:
        """Output file for a URL on this site, or None when it points elsewhere."""
        target = urlsplit(urljoin(self.url_of(page_path), url))
        home = urlsplit(self.home_url)
        if (target.scheme, target.netloc) != (home.scheme, home.netloc):
            return None
        path = unquote(target.path)
        if path + "/" == self.base_path:
            path = self.base_path
        if not path.startswith(self.base_path):
            return None
        relative = path[len(self.base_path):]
        return relative + "index.html" if relative == "" or relative.endswith("/") else relative

    def same_url(self, first: str | None, second: str) -> bool:
        return first is not None and unquote(urljoin(self.home_url, first)) == unquote(urljoin(self.home_url, second))
