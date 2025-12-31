from __future__ import annotations

from enum import StrEnum


class HtmlTag(StrEnum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    DIV = "div"
    P = "p"
    A = "a"
    UL = "ul"
    LI = "li"
    NAV = "nav"
    FOOTER = "footer"
    TIME = "time"
    DIALOG = "dialog"
    SVG = "svg"
    PATH = "path"
    BUTTON = "button"
    DETAILS = "details"
    SUMMARY = "summary"


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
