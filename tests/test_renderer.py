# -*- coding: utf-8 -*-
# author: @RShirohara

"""novelconverter.renderer test module.

This test will be run using pytest.
"""

from dataclasses import dataclass

from novelconverter.tree import DocumentTree, TreeBuilder, TreeElement
from novelconverter.renderer import render
from novelconverter.util import Registry


@dataclass(frozen=True)
class TestElement(TreeElement):
    """TreeElement used for test."""

    key: str
    value: str | int | bool

    def __str__(self) -> str:
        return f"{self.key}: {self.value}\n"


@dataclass(frozen=True)
class TestDefaultElement(TreeElement):
    """DefaultElement used for test."""

    value: str | int | bool

    def __str__(self) -> str:
        return f"Default: {self.value}\n"


def renderer(element: TestElement) -> str:
    """Renderer for TestElement used for test."""
    return f"Test: {element.key}, {element.value}\n"


def test_render() -> None:
    """Test render."""

    tree: DocumentTree = (
        TreeBuilder()
        .add_element(TestElement("foo", "Test string."))
        .add_element(TestElement("bar", 123))
        .add_element(TestElement("baz", True))
        .add_element(TestDefaultElement("Default string."))
        .add_element(TestDefaultElement(456))
        .add_element(TestDefaultElement(False))
        .build()
    )
    result: str = """Test: foo, Test string.
Test: bar, 123
Test: baz, True
Default: Default string.
Default: 456
Default: False
"""

    assert result == render(tree, Registry((("TestElement", 1, renderer),)))
