from __future__ import annotations

from typing import TYPE_CHECKING

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdown import Markdown, markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

register = template.Library()


class _ExternalLinkTreeprocessor(Treeprocessor):
    def run(self, root: Element) -> None:
        for link in root.iter("a"):
            link.set("target", "_blank")
            link.set("rel", "noopener noreferrer")


class _ExternalLinkExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:  # noqa: N802 (override)
        md.treeprocessors.register(_ExternalLinkTreeprocessor(md), "external_links", 0)


@register.filter
@stringfilter
def md(value: str) -> str:
    return mark_safe(markdown(value, extensions=[_ExternalLinkExtension()]))
