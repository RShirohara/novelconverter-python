"""Render NovelConverter AST with renderer."""

from dataclasses import dataclass
from typing import Callable, TypeVar

from .tree import NovelNode

T_co = TypeVar("T_co", bound=NovelNode, covariant=True)
NodeRenderer = Callable[[T_co, dict[str, "NodeRenderer[T_co]"]], str]


@dataclass
class RenderError(Exception):
    """A error in rendering process.

    Attributes:
        message (str): Error message.
        node (NovelNode): Node being processed when the error occurred.
    """

    message: str
    node: NovelNode

    def __str__(self) -> str:
        return f'{self.message}\nnode: {self.node.type}, raw: "{self.node.raw}"'


def render(root: NovelNode, renderers: dict[str, NodeRenderer[NovelNode]]) -> str:
    """Render root NovelNode with NodeRenderer.

    Args:
        root (NovelNode): The rendered root node.
        renderers (dict[str, NodeRenderer]): Node name and Node renderer pairs.

    Returns:
        str: A document rendered from root node.
    """

    if not root.type in renderers.keys():
        raise RenderError("Renderer corresponding to Node does not exist", root)

    return renderers[root.type](root, renderers)
