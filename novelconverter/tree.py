"""The definition for NovelConverter AST node types."""

from abc import ABC
from typing import Optional


class NovelNode(ABC):
    """Basic NovelNode.

    Real NovelNode implemention has more attributes.
    """

    type: str
    raw: str
    parent: Optional["NovelNode"]


class NovelTextNode(NovelNode):
    """Text Node.

    Text Node has inline value.
    """

    value: str


class NovelParentNode(NovelNode):
    """Parent Node.

    Parent Node has children nodes that are consist of `NovelNode` or `NovelTextNode`.
    """

    children: tuple[NovelNode | NovelTextNode, ...]
