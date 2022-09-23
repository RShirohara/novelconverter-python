"""Parse string to NovelConverter AST."""

from typing import Callable

from pyparsing import ParserElement
from pyparsing.results import ParseResults

from .tree import NovelNode, NovelParentNode

NodeBuilder = Callable[[ParseResults], NovelNode]


def parse(source: str, root_parser: ParserElement) -> NovelParentNode:
    """Parse string to NovelNode.

    Args:
        source (str): Source string.
        root_parser (ParserElement): The Parser for root element.

    Returns:
        NovelParentNode: Tho NovelNode rendered py NovelNode parsers.
    """

    result: NovelParentNode = root_parser.parse_string(source)[0]
    return result
