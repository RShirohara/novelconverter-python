# -*- coding: utf-8 -*-
# author: @RShirohara

"""NovelConverter Processor module."""


from typing import Callable, TypeAlias

from .util import Registry

Processor: TypeAlias = Callable[[str], str]


def process(source: str, processors: Registry[Processor]) -> str:
    """Process string using processor.

    Args:
        source (str): Source string.
        processors (Registry[Processor]): Registry containing processor.

    Returns:
        str: Processed source string.
    """

    result: str = source

    for processor in processors.values():
        result = processor(result)

    return result
