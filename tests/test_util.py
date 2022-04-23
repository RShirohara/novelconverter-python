# -*- coding: utf-8 -*-
# author: @RShirohara
"""novelconverter.util test module.

This module is test of novelconverter.util.
This test will be run using pytest.
"""


from typing import Any, Generator
from pytest import fixture, raises

from novelconverter.util import Registry, RegistryItem

datas: tuple[RegistryItem, ...] = (
    RegistryItem("foo", 10, "Test string."),
    RegistryItem("bar", 30, 123),
    RegistryItem("baz", 20, True),
)


@fixture
def registry() -> Generator[Registry[Any], None, None]:
    """Build test data.

    Yields:
        Registry[Any]: Test data.
    """

    yield Registry(datas)


class TestRegistry:
    """Test class of Registry."""

    def test_contains(self, registry: Registry) -> None:
        """Test Registry.__contains__.

        Args:
            registry (Registry): Test data.
        """

        # if registry contains key, return True.
        assert "foo" in registry
        assert "bar" in registry
        assert "baz" in registry

        # if registry contains value, return True.
        assert "Test string." in registry
        assert 123 in registry
        assert True in registry

        # if registry not contains key, return False.
        assert "hoge" not in registry

        # if registry not contains value, return False.
        assert "This is test string" not in registry
        assert 456 not in registry
        assert False not in registry

    def test_delitem(self, registry: Registry) -> None:
        """Test Registry.__delitem__

        Args:
            registry (Registry): Test data.
        """

        # if try to delete item by key, it will success.
        del registry["foo"]
        assert "Test string." not in registry

        # if try to delete item by index, it will success.
        del registry[1]
        assert 456 not in registry

        # if try to delete item by non-exist key, it will fail.
        with raises(KeyError):
            del registry["hoge"]

        # if try to delete item by value, it will fail.
        with raises(TypeError):
            del registry[True]

        # if try to delete item by index out of range, it will fail.
        with raises(IndexError):
            del registry[123]

    def test_getitem(self, registry: Registry):
        """Test Registry.__getitem__.

        Args:
            registry (Registry): Test data.
        """

        # if access using an existing key, return values.
        assert "Test string." == registry["foo"]
        assert 123 == registry["bar"]
        assert True is registry["baz"]

        # if access using an index in range, return values.
        assert "Test string." == registry[0]
        assert True is registry[1]
        assert 123 == registry[2]

        # if access using an slice, return registry.
        assert "Test string." == registry[0:2][0]
        assert True is registry[0:2][1]
        assert 123 == registry[0:3:2][1]

        # if access using an non-existing key, raise KeyError.
        with raises(KeyError):
            registry["hoge"]

        # if access using index out of range, raise IndexError.
        with raises(IndexError):
            registry[123]

        # if access using other-type values, raise TypeError.
        with raises(TypeError):
            registry[("foo", "Bar")]

    def test_iter(self, registry: Registry):
        """Test Registry.__iter__

        Args:
            registry (Registry): Test data.
        """

        assert tuple(sorted(datas, key=lambda x: x[1])) == tuple(x for x in registry)

    def test_len(self, registry: Registry):
        """Test Registry.__len__

        Args:
            registry (Registry): Test data.
        """

        assert 3 == len(registry)

    def test_repr(self, registry: Registry):
        """Test Registry.__repr__

        Args:
            registry (Registry): Test data.
        """

        assert (
            "Registry(\
RegistryItem(key='foo', priority=10, value='Test string.'), \
RegistryItem(key='baz', priority=20, value=True), \
RegistryItem(key='bar', priority=30, value=123))"
            == repr(registry)
        )

    def test_setitem(self, registry: Registry):
        """Test Registry.__setitem__

        Args:
            registry (Registry): Test data.
        """

        # if add item by non-exist key, it will success.
        registry[("hoge", 15)] = [1, 2, 3]
        assert "hoge" in registry
        assert [1, 2, 3] in registry
        assert [1, 2, 3] == registry["hoge"]
        assert [1, 2, 3] == registry[1]

        # if add item by exist key, Overwrite to value.
        registry[("bar", 40)] = ("Test", 123)
        assert "bar" in registry
        assert ("Test", 123) in registry
        assert ("Test", 123) == registry["bar"]
        assert ("Test", 123) == registry[3]

        # if add item by other then tuple, raise TypeError.
        with raises(TypeError):
            registry["bar"] = ("Test", 123)

        # if add item by non-string key, raise TypeError.
        with raises(TypeError):
            registry[(True, 123)] = ("Test", 123)

        # if add item by non-int priority, raise TypeError.
        with raises(TypeError):
            registry[("bar", "Test")] = ("Test", 123)

    def test_keys(self, registry: Registry):
        """Test Registry.keys

        Args:
            registry (Registry): Test data.
        """

        assert ("foo", "bar", "baz") == registry.keys()

    def test_pop(self, registry: Registry):
        """Test Registry.pop

        Args:
            registry (Registry): Test data.
        """

        # if try delete item by key, return deleted value.
        assert True is registry.pop("baz")
        assert True not in registry

        # if try delete item by non-exist key, raise KeyError.
        with raises(KeyError):
            registry.pop("bazFix")

    def test_priorities(self, registry: Registry):
        """Test Registry.priorities.

        Args:
            registry (Registry): Test data.
        """

        assert {"foo": 10, "bar": 30, "baz": 20} == registry.priorities()

    def test_values(self, registry: Registry):
        """Test Registry.values.

        Args:
            registry (Registry): Test data.
        """

        assert ("Test string.", True, 123) == registry.values()
