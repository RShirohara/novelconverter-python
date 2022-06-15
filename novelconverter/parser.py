# -*- coding: utf-8 -*-
# author: @RShirohara

"""NovelConverter parser module.

Attributes:
    ElementParser
"""

from dataclasses import dataclass
from re import Pattern


@dataclass(frozen=True)
class ElementParser:
    pattern: Pattern
