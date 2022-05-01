# -*- coding: utf-8 -*-
# author: @RShirohara

"""NovelConverter Renderer module."""

from typing import Callable, TypeAlias

from .tree import DocumentTree, TreeElement
from .util import Registry

Renderer: TypeAlias = Callable[[TreeElement], str]


def render(tree: DocumentTree, renderers: Registry[Renderer]) -> str:
    """Render DocumentTree using renderer.

    Args:
        tree (DocumentTree): Tree storing elemensts of document.
        renderers (Registry[Renderer]): Registry containing renderer.

    Returns:
        str: Rendered elements.
    """

    result: str = ""

    for element in tree.elements:
        element_type: str = element.__class__.__name__
        if element_type in renderers.keys():
            result += renderers[element_type](element)
        else:
            result += element.__str__()

    return result
