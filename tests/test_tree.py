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


class TestTreeBuilder:
    """Test class of TreeBuilder."""

    def test_add_meta(self) -> None:
        """Test TreeBuilder.add_meta."""
        builder: TreeBuilder = (
            TreeBuilder()
            .add_meta("foo", "Test string.")
            .add_meta("bar", 123)
            .add_meta("baz", True)
        )

        assert "foo" in builder.meta.keys()
        assert "bar" in builder.meta.keys()
        assert "baz" in builder.meta.keys()

        assert "Test string." == builder.meta["foo"]
        assert 123 == builder.meta["bar"]
        assert True is builder.meta["baz"]

    def test_add_element(self) -> None:
        """Test TreeBuilder.add_element."""

        builder: TreeBuilder = (
            TreeBuilder()
            .add_element(TestElement("foo", "Test string."))
            .add_element(TestElement("bar", 123))
            .add_element(TestElement("baz", True))
        )

        assert TestElement("foo", "Test string.") in builder.elements
        assert TestElement("bar", 123) in builder.elements
        assert TestElement("baz", True) in builder.elements

        assert TestElement("foo", "Test string.") == builder.elements[0]
        assert TestElement("bar", 123) == builder.elements[1]
        assert TestElement("baz", True) == builder.elements[2]

    def test_build(self) -> None:
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

        assert TestElement("foo", "Test string.") == tree.elements[0]
        assert TestElement("bar", 123) == tree.elements[1]
        assert TestElement("baz", True) == tree.elements[2]
