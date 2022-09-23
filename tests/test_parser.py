"""The test module of novelconverter.parser."""

from dataclasses import dataclass, field
from pytest import fixture

from pyparsing import ParserElement, Word, lineEnd, unicode, Opt, Group
from pyparsing.results import ParseResults

from novelconverter.tree import NovelNode, NovelParentNode, NovelTextNode
from novelconverter.parser import parse

ParserElement.set_default_whitespace_chars(" \t")


@dataclass
class Inline(NovelTextNode):
    type: str = field(init=False, default="Inline")
    raw: str
    value: str


@dataclass
class Ruby(NovelTextNode):
    type: str = field(init=False, default="Ruby")
    raw: str
    value: str
    ruby: str


@dataclass
class Para(NovelParentNode):
    type: str = field(init=False, default="Para")
    raw: str
    children: tuple[Ruby | Inline, ...]


@dataclass
class Root(NovelParentNode):
    type: str = field(init=False, default="Root")
    raw: str
    children: tuple[Para, ...]


def parse_inline(tokens: ParseResults) -> Inline:
    return Inline(raw="".join(tokens), value=tokens[0])


def parse_ruby(tokens: ParseResults) -> Ruby:
    return Ruby(
        raw="".join(tokens.as_list()), value=tokens["value"], ruby=tokens["ruby"]
    )


def parse_para(tokens: ParseResults) -> Para:
    raws: list[str] = []
    for token in tokens[0]:
        match token:
            case NovelNode():
                raws.append(token.raw)
    return Para(raw="".join(raws), children=tuple(tokens[0]))


def parse_root(source: str, loc: int, tokens: ParseResults) -> Root:
    return Root(raw=source, children=tuple(tokens))


line_end: ParserElement = lineEnd.suppress()

inline: ParserElement = (
    Word(unicode.CJK.printables)
    .set_results_name("Inline")
    .set_parse_action(parse_inline)
)
ruby: ParserElement = (
    (
        "{"
        + Word(unicode.Japanese.Kanji.printables).set_results_name("value")
        + "|"
        + Word(unicode.Japanese.Hiragana.printables).set_results_name("ruby")
        + "}"
    )
    .set_results_name("Ruby")
    .set_parse_action(parse_ruby)
)
para: ParserElement = (
    Group((inline ^ ruby)[1, ...]).set_results_name("Para").set_parse_action(parse_para)
)

line: ParserElement = Opt(line_end) & para & Opt(line_end)
root: ParserElement = (
    (line)[1, ...].set_results_name("Root").set_parse_action(parse_root)
)


@fixture
def source() -> str:
    return """
たとえば{私|わたし}はこの{文章|ぶんしょう}を書く。
これは二つ目の{文章|ぶんしょう}。

これが{最後|さいご}の文章。
"""


class TestParse:
    """test parser.parse"""

    def test(self, source: str) -> None:
        expected: Root = Root(
            raw=source,
            children=(
                Para(
                    raw="たとえば{私|わたし}はこの{文章|ぶんしょう}を書く。",
                    children=(
                        Inline(raw="たとえば", value="たとえば"),
                        Ruby(raw="{私|わたし}", value="私", ruby="わたし"),
                        Inline(raw="はこの", value="はこの"),
                        Ruby(raw="{文章|ぶんしょう}", value="文章", ruby="ぶんしょう"),
                        Inline(raw="を書く。", value="を書く。"),
                    ),
                ),
                Para(
                    raw="これは二つ目の{文章|ぶんしょう}。",
                    children=(
                        Inline(raw="これは二つ目の", value="これは二つ目の"),
                        Ruby(raw="{文章|ぶんしょう}", value="文章", ruby="ぶんしょう"),
                        Inline(raw="。", value="。"),
                    ),
                ),
                Para(
                    raw="これが{最後|さいご}の文章。",
                    children=(
                        Inline(raw="これが", value="これが"),
                        Ruby(raw="{最後|さいご}", value="最後", ruby="さいご"),
                        Inline(raw="の文章。", value="の文章。"),
                    ),
                ),
            ),
        )
        actual: Root = parse(source, root)
        assert expected == actual
