from __future__ import annotations

from enum import StrEnum


class HtmlTag(StrEnum):
    A = "a"
    ASIDE = "aside"
    BUTTON = "button"
    DETAILS = "details"
    DIALOG = "dialog"
    DIV = "div"
    FOOTER = "footer"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    LI = "li"
    LINK = "link"
    META = "meta"
    NAV = "nav"
    P = "p"
    PATH = "path"
    SCRIPT = "script"
    SUMMARY = "summary"
    SVG = "svg"
    TIME = "time"
    TITLE = "title"
    UL = "ul"


# Class Names
CLASS_TOOLTIP = "tooltip"

# HTML Attributes
ATTR_D = "d"
ATTR_DATA_TIP = "data-tip"
ATTR_HREF = "href"
ATTR_ONCLICK = "onclick"
ATTR_TARGET = "target"
ATTR_VIEW_BOX = "viewbox"


class Language(StrEnum):
    ENGLISH = "en"
    SPANISH = "es"
