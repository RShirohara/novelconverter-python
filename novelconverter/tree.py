"""The definition for NovelConverter AST node types."""

from typing import Protocol


class NovelNode(Protocol):
    """Basic NovelNode.

    Real NovelNode implemention has more attributes.
    """

    type: str
    raw: str


class NovelTextNode(NovelNode, Protocol):
    """Text Node.

    Text Node has inline value.
    """

    value: str


class NovelParentNode(NovelNode, Protocol):
    """Parent Node.

    Parent Node has children nodes that are consist of `NovelNode` or `NovelTextNode`.
    """

    children: tuple[NovelNode, ...]
