# -*- coding: utf-8 -*-
# author: @RShirohara
"""novelconverter.tree test module.

This test will be run using pytest.
"""


from dataclasses import dataclass
from novelconverter.tree import DocumentTree, TreeBuilder, TreeElement


@dataclass(frozen=True)
class TestElement(TreeElement):
    """TreeElement used for test."""

    key: str
    value: str | int | bool

    def __str__(self) -> str:
        return f"{self.key}: {self.value}"


class TestTreeElement:
    """Test class for TreeElement."""

    def test_str(self):
        """Test TreeElement.__str__."""
        assert "foo: Test string." == TestElement("foo", "Test string.").__str__()


class TestTreeBuilder:
    """Test class of TreeBuilder."""

    def test_build(self):
        """Test TreeBuilder.build."""

        tree: DocumentTree = (
            TreeBuilder()
            .add_element(TestElement("foo", "Test string."))
            .add_element(TestElement("bar", 123))
            .add_element(TestElement("baz", True))
            .build()
        )

        assert TestElement("foo", "Test string.") in tree.elements
        assert TestElement("bar", 123) in tree.elements
        assert TestElement("baz", True) in tree.elements
