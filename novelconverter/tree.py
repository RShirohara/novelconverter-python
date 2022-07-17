# coding: utf-8
# author: Ray Shirohara

"""NovelConverter Tree module."""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class TreeElement(ABC):
    """Base class of all tree element."""

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @abstractmethod
    def __str__(self) -> str:
        """Get the text if the corresponding renderer does not exists.

        Returns:
            str: text displayed if the corresponding renderer does not exists.
        """


@dataclass(frozen=True)
class ElementTree:
    """Tree storing elements of document.

    Attributes:
        elements (tuple[TreeElement]): Elements stored in document.
        meta (dict[str, Any]): Document metadata.
    """

    elements: tuple[TreeElement, ...] = field(default_factory=tuple[TreeElement, ...])
    meta: dict[str, Any] = field(default_factory=dict[str, Any])
