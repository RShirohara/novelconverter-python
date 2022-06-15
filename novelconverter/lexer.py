# -*- coding: utf-8 -*-
# author: @RShirohara

"""NovelConverter Lexer module.

Attributes:
    Token:
"""


from dataclasses import InitVar, dataclass, field
from re import Match, Pattern, compile
from sys import maxsize
from typing import Iterator, NamedTuple, Optional

from .parser import ElementParser
from .util import Registry


class TokenizeError(Exception):
    pass


class Token(NamedTuple):
    type: str
    priority: int
    value: str
    start: int
    end: int

    def __lt__(self, __x: "Token") -> bool:
        return (self.start, self.priority, self.end) < (
            __x.start,
            __x.priority,
            __x.end,
        )


@dataclass(frozen=True)
class MatchIterator(Iterator):

    src: str
    reg: InitVar[Registry[ElementParser]]
    pos: int = 0
    matches: Registry[Iterator[Match]] = field(default_factory=Registry, init=False)
    current: dict[str, Token] = field(default_factory=dict, init=False)

    def __post_init__(self, reg: Registry[ElementParser]) -> None:
        # Build Iterators
        iters = Registry(
            (
                (
                    key,
                    pri,
                    item.pattern.finditer(self.src, pos=self.pos),
                )
                for key, pri, item in reg
            )
        )
        object.__setattr__(self, "matches", iters)

    def __next__(self) -> tuple[Optional[Token], ...]:
        return self.next(pos=self.pos + 1)

    def next(self, pos: int) -> tuple[Optional[Token], ...]:
        # Check pos.
        if (pos <= self.pos) and (pos >= len(self.src)):
            raise IndexError("string index out of range")
        # Get tokens.
        result: list[Optional[Token]] = []
        if self.current:
            for key, token in self.current.items():
                if pos < token.start:
                    result.append(token)
                else:
                    pri = self.matches.priorities()[key]
                    item = self.matches[key]
                    result.append(get_token(key, pri, item, pos))
        else:
            result = [
                get_token(key, pri, item, pos) for key, pri, item, in self.matches
            ]
        result = sorted(result, key=lambda x: (x is None, x))
        if all(r is None for r in result):
            raise StopIteration
        # Set result.
        object.__setattr__(
            self, "current", {token.type: token for token in result if token}
        )
        return tuple(result)


def build_token(type: str, priority: int, match: Match) -> Token:
    return Token(
        type=type,
        priority=priority,
        value=match.group(0),
        start=match.start(),
        end=match.end(),
    )


def get_token(
    type: str, priority: int, match: Iterator[Match], pos: int
) -> Optional[Token]:
    result: Optional[Token] = None
    while True:
        try:
            result = build_token(type, priority, match.__next__())
        except StopIteration:
            result = None
            break
        if result and (result.end >= pos):
            break
    return result


def get_default_parser(
    reg: Registry[ElementParser],
) -> tuple[Optional[ElementParser], Registry[ElementParser]]:
    key_pattern: Pattern = compile(r"(?P<key>.*?)&Default$")
    key: Optional[str] = None
    parser: Registry[ElementParser] = reg[:]
    default: Optional[ElementParser] = None

    # Search Key
    for k in parser.keys():
        match: Optional[Match] = key_pattern.fullmatch(k)
        if match and (max(parser.priorities().values()) == maxsize):
            key = k
            break
    # Get default parser
    if key:
        default = parser.pop(key)

    return (default, parser)


def tokenize(src: str, parsers: Registry[ElementParser]) -> tuple[Token, ...]:
    default_parser: Optional[ElementParser] = None
    pos: int = 0
    tokens: list[Token] = []
    result: list[Token] = []
    old: Optional[Token] = None
    current: Optional[Token] = None

    # Get parsers.
    default_parser, parsers = get_default_parser(parsers)
    # Get tokens.
    match_iter: MatchIterator = MatchIterator(src, parsers, pos)
    while pos <= len(src):
        # Get current.
        try:
            current, *_ = match_iter.next(pos)
        except StopIteration:
            current = None
        # Add old to result.
        if old and (not current or (old.priority >= current.priority)):
            tokens.append(old)
        # Check current.
        if not current:
            break
        elif not old or (old.end <= current.start) or (old.priority < current.priority):
            old = current
            pos = current.start + 1
    # Check tokens.
    for i in range(len(tokens) + 1):
        old_end: int = tokens[i - 1].end if i > 0 else 0
        cur_start: int = tokens[i].start if i < len(tokens) else len(src) - 1
        if (cur_start - old_end) > 1:
            if default_parser:
                match: Optional[Match] = default_parser.pattern.search(
                    src, pos=old_end, endpos=cur_start
                )
                if match:
                    result.append(
                        build_token(
                            default_parser.__class__.__name__,
                            maxsize,
                            match,
                        )
                    )
                else:
                    raise TokenizeError(tokens[i])
            else:
                raise TokenizeError(tokens[i])
        # Add matched token to result.
        if i < len(tokens):
            result.append(tokens[i])
    return tuple(result)
