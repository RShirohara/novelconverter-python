# -*- coding: utf-8 -*-
# author: @RShirohara

"""NovelConverter Tree module.

Attributes:
    DocumentTree:
"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class TreeElement(metaclass=ABCMeta):
    """Base class of all elements stored in DocumentTree."""

    @abstractmethod
    def __str__(self) -> str:
        ...


@dataclass(frozen=True)
class DocumentTree:
    """Tree storing elements of document.

    Attributes:
        meta (dict[str, Any]): Document metadata.
        elements (tuple[TreeElement]): Elements stored in document.
    """

    meta: dict[str, Any] = field(default_factory=dict[str, Any])
    elements: tuple[TreeElement] = field(default_factory=tuple[TreeElement])


@dataclass
class TreeBuilder:
    """DocumentTree builder."""

    meta: dict[str, Any] = field(default_factory=dict[str, Any], init=False)
    elements: list[TreeElement] = field(default_factory=list[TreeElement], init=False)

    def add_meta(self, key: str, value: Any) -> "TreeBuilder":
        """Add metadata to tree.

        Args:
            key (str): Metadata type.
            value (Any): Metadata value.

        Returns:
            TreeBuilder: self.
        """
        self.meta[key] = value
        return self

    def add_element(self, value: TreeElement) -> "TreeBuilder":
        """Add element to tree.

        Args:
            value (TreeElement): Element add to tree.

        Returns:
            TreeBuilder: self.
        """
        self.elements.append(value)
        return self

    def build(self) -> DocumentTree:
        """Build DocumentTree

        Returns:
            DocumentTree: Tree storing added elements.
        """
        return DocumentTree(meta=self.meta, elements=tuple(self.elements))
