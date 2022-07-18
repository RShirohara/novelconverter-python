# coding: utf-8
# author: Ray Shirohara

"""novelconverter.util test module.

This test will be run using pytest.
"""

from typing import Any, Generator
from pytest import fixture, raises

from novelconverter.util import RegistryKey, Registry

test_data: tuple[tuple[RegistryKey, Any], ...] = (
    (RegistryKey("foo", 10), "Test string."),
    (RegistryKey("bar", 30), 123),
    (RegistryKey("baz", 20), True),
    (RegistryKey("hoge", 40), [1, 2, 3]),
    (RegistryKey("fuga", 60), ("Test", "String")),
    (RegistryKey("piyo", 60), {"test": "string"}),
)


@fixture
def registry() -> Generator[Registry[Any], None, None]:
    """Build Test data.

    Yields:
        Generator[Registry[Any], None, None]: Test data.
    """

    yield Registry(test_data)


class TestRegistry:
    """Test class of Registry."""

    def test_iter(self, registry: Registry[Any]) -> None:
        """Test Registry.__iter__

        Args:
            registry (Registry[Any]): Test data.
        """

        expected: tuple[RegistryKey, ...] = tuple(sorted((key for key, _ in test_data)))
        actual: tuple[RegistryKey, ...] = tuple(x for x in registry)
        assert expected == actual

    def test_len(self, registry: Registry[Any]) -> None:
        """Test Registry.__len__

        Args:
            registry (Registry[Any]): Test data.
        """

        assert 6 == len(registry)

        # if delete item, len() will decrease.
        del registry["piyo"]
        assert 5 == len(registry)

    def test_delitem(self, registry: Registry[Any]) -> None:
        """Test Registry.__delitem__.

        Args:
            registry (Registry[Any]): Test data.
        """

        # if try to delete item by key, it will success.
        del registry["foo"]
        assert "foo" not in registry.keys()
        assert "Test string." not in registry.values()

        # if try to delete item by index, it will success.
        del registry[1]
        assert "bar" not in registry.keys()
        assert 123 not in registry.values()

        # if try to delete item by non-exist key, it will fail.
        with raises(KeyError):
            del registry["testKey"]

        # if try to delete item by value, it will fail.
        with raises(TypeError):
            del registry[True]

        # if try to delete item by index out of range, it will fail.
        with raises(IndexError):
            del registry[123]

    def test_getitem(self, registry: Registry[Any]) -> None:
        """Test Registry.__getitem__.

        Args:
            registry (Registry[Any]): Test data.
        """

        # if access using an exist key, return value.
        assert "Test string." == registry["foo"]
        assert 123 == registry["bar"]
        assert True is registry["baz"]

        # if access using an exist key and priority, return value.
        assert "Test string." == registry[("foo", 10)]
        assert 123 == registry[("bar", 30)]
        assert True is registry[("baz", 20)]

        # if access using an index in range, return value.
        assert "Test string." == registry[0]
        assert True is registry[1]
        assert 123 == registry[2]

        # if access using an slice, return registry.
        expected: tuple[Any, ...] = tuple(
            value for _, value in sorted(test_data, key=lambda x: x[0])
        )[0:4:2]
        actual: tuple[Any, ...] = tuple(registry[0:4:2].values())

        assert expected == actual

        # if access using an non-existing key, raise KeyError.
        with raises(KeyError):
            registry["testKey"]

        # if access using an key and not-match priority, raise KeyError.
        with raises(KeyError):
            registry[("foo", 100)]

        # if access using index out of range, raise IndexError.
        with raises(IndexError):
            registry[123]

        # if access using other-type values, raise TypeError.
        with raises(TypeError):
            registry[True]

    def test_setitem(self, registry: Registry[Any]) -> None:
        """Test Registry.__setitem__

        Args:
            registry (Registry[Any]): Test data.
        """

        # if add item by non-exist key and priority, it will success.
        registry[("testKey1", 15)] = ["Test", "values"]
        assert "testKey1" in registry.keys()
        assert ["Test", "values"] in registry.values()
        assert ["Test", "values"] == registry["testKey1"]
        assert ["Test", "values"] == registry[(("testKey1", 15))]
        assert ["Test", "values"] == registry[1]

        # if add item by non-exist key, it will success.
        registry["testKey2"] = "This is test string. link to 'testKey2'."
        assert "testKey2" in registry.keys()
        assert "This is test string. link to 'testKey2'." in registry.values()
        assert "This is test string. link to 'testKey2'." == registry["testKey2"]
        assert "This is test string. link to 'testKey2'." == registry[("testKey2", 61)]
        assert "This is test string. link to 'testKey2'." == registry[-1]

        # if add item by exist-key, Overwrite to value.
        registry[("bar", 40)] = ("Test", 123)
        assert "bar" in registry.keys()
        assert ("Test", 123) in registry.values()
        assert ("Test", 123) == registry["bar"]
        assert ("Test", 123) == registry[3]

        # if add item by other then tuple and string, raise TypeError.
        with raises(TypeError):
            registry[123] = ("Test", 712)

        # if add item by non-string key, raise TypeError.
        with raises(TypeError):
            registry[(True, 123)] = ("Test", 456)

        # if add item by non-int priority, raise TypeError.
        with raises(TypeError):
            registry[("bar", "test")] = ("Test", 789)

    def test_keys(self, registry: Registry[Any]) -> None:
        """Test Registry.keys

        Args:
            registry (Registry[Any]): Test data.
        """

        expected: tuple[str, ...] = tuple(
            key.key for key, _ in sorted(test_data, key=lambda x: x[0])
        )
        actual: tuple[str, ...] = tuple(registry.keys())
        assert expected == actual

    def test_priorities(self, registry: Registry[Any]) -> None:
        """Test Registry.priorities.

        Args:
            registry (Registry[Any]): Test data.
        """

        expected: tuple[RegistryKey, ...] = tuple(
            key for key, _ in sorted(test_data, key=lambda x: x[0])
        )
        actual: tuple[RegistryKey, ...] = tuple(registry.priorities())
        assert expected == actual

    def test_values(self, registry: Registry[Any]) -> None:
        """Test Registry.values

        Args:
            registry (Registry[Any]): Test data.
        """

        expected: tuple[Any, ...] = tuple(
            value for _, value in sorted(test_data, key=lambda x: x[0])
        )
        actual: tuple[Any, ...] = tuple(registry.values())
        assert expected == actual

    def test_items(self, registry: Registry[Any]) -> None:
        """Test Registry.items

        Args:
            registry (Registry[Any]): Test data.
        """

        expected: tuple[tuple[RegistryKey, Any], ...] = tuple(
            sorted(test_data, key=lambda x: x[0])
        )
        actual: tuple[tuple[RegistryKey, Any], ...] = tuple(registry.items())
        assert expected == actual
