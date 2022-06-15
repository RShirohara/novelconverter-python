# -*- coding: utf-8 -*-
# author: @RShirohara

from re import MULTILINE, Match, compile
from sys import maxsize
from typing import Optional

from novelconverter.lexer import Token, tokenize
from novelconverter.parser import ElementParser
from novelconverter.util import Registry

src: str = """# This is header

This is first paragraph.
This is second line

## Second level header

This is second paragraph.

> ## Quote header
>
> This is third paragraph.

### Nested header

This is last paragraph.
"""

parsers = Registry(
    (
        ("quote", 1, ElementParser(compile(r"(^(> ?)+(.*?)$)+", MULTILINE))),
        ("header", 2, ElementParser(compile(r"^(#{1,6}) (.*?)$", MULTILINE))),
        (
            "paragraph&Default",
            maxsize,
            ElementParser(compile(r"(^.+$)+", MULTILINE)),
        ),
    )
)


class TestLexer:
    def test_tokenize(self) -> None:
        res: tuple[Token, ...] = tokenize(src, parsers)
        res_token: tuple[str, ...] = tuple(token.value for token in res)

        assert res_token == (
            "# This is header",
            "This is first paragraph.",
            "This is second line",
            "## Second level header",
            "This is second paragraph.",
            "> ## Quote header",
            ">",
            "> This is third paragraph.",
            "### Nested header",
            "This is last paragraph.",
        )
