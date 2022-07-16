# coding: utf-8
# author: Ray Shirohara

"""NovelConverter Tree module."""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class TreeElement(ABC):
    """Base class of all tree element.

    Attributes:
        default (str): Text returned if the corresponding renderer does not exists.
    """

    @property
    @abstractmethod
    def default(self) -> str:
        """Text returned if the corresponding renderer does not exists."""


@dataclass(frozen=True)
class ElementTree:
    """Tree storing elements of document.

    Attributes:
        elements (tuple[TreeElement]): Elements stored in document.
        meta (dict[str, Any]): Document metadata.
    """

    elements: tuple[TreeElement, ...] = field(default_factory=tuple[TreeElement, ...])
    meta: dict[str, Any] = field(default_factory=dict[str, Any])
