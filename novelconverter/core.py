# coding: utf-8
# author: Ray Shirohara


from typing import Any, overload


@overload
def convert(src: str, from_format: str, to_format: str) -> str:
    ...


@overload
def convert(src: str, from_format: Any, to_format: Any) -> str:
    ...


def convert(src: str, from_format: Any, to_format: Any) -> str:
    ...
