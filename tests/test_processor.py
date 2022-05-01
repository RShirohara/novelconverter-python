# -*- coding: utf-8 -*-
# author: @RShirohara

"""novelconverter.processor test module.

This test will be run using pytest.
"""

from re import Match, Pattern, compile
from typing import Generator, Optional
from pytest import fixture

from novelconverter.processor import Processor, process
from novelconverter.util import Registry


def quote(source: str) -> str:
    """Processor used for test.

    Args:
        source (str): Source string.

    Returns:
        str: Processed string.
    """

    pattern: Pattern = compile(r"^This\W")
    result: list[str] = []

    for src in source.splitlines():
        match: Optional[Match] = pattern.match(src)
        if match:
            result.append(f"> {match.string}")
        else:
            result.append(src)

    return "\n".join(result)


@fixture
def processors() -> Generator[Registry[Processor], None, None]:
    """Build processor."""

    yield Registry((("quote", 1, quote),))


def test_process(processors: Registry[Processor]) -> None:
    """Test process."""

    source: str = """
Test string.
This is first paragraph.

This is second paragraph.
This is a pen.

This is last paragraph.
Bye."""
    result: str = """
Test string.
> This is first paragraph.

> This is second paragraph.
> This is a pen.

> This is last paragraph.
Bye."""

    assert result == process(source, processors)
