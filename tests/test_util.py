# -*- coding: utf-8 -*-
# author: @RShirohara
"""novelconverter.util test module.

This module is test of novelconverter.util.
This test will be run using pytest.
"""


from novelconverter.util import Registry
from pytest import fixture, raises


datas: tuple[tuple[str, int, any]] = (
    ("foo", 10, "Test string."),
    ("bar", 30, 123),
    ("baz", 20, True),
)


@fixture
def registry() -> Registry:
    reg: Registry[any] = Registry()
    reg.add_items(datas)
    yield reg


class TestRegistry:
    def test_getitem(self, registry: Registry) -> None:
        # if access using an existing key, return values.
        assert datas[0][1:] == registry["foo"]
        assert datas[1][1:] == registry["bar"]
        assert datas[2][1:] == registry["baz"]

        # if access using an index in range, return values.
        assert datas[0] == registry[0]
        assert datas[2] == registry[1]
        assert datas[1] == registry[2]

        # if access using an slice, return registry.
        assert datas[0] == registry[0:2][0]
        assert datas[2] == registry[0:2][1]
        assert datas[1] == registry[0:3:2][1]

        # if access using an non-existing key, raise KeyError.
        with raises(KeyError):
            registry["hoge"]

        # if access using index out of range, raise IndexError.
        with raises(IndexError):
            registry[123]

        # if access using other-type values, raise TypeError.
        with raises(TypeError):
            registry[("foo", "Bar")]

    def test_delitem(self, registry: Registry) -> None:
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

    def test_iter(self, registry: Registry) -> None:
        assert tuple(sorted(datas, key=lambda x: x[1])) == tuple(
            x for x in registry
        )

    def test_contains(self, registry: Registry) -> None:
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

    def test_add(self, registry: Registry) -> None:
        add_data: tuple[tuple[str, int, any]] = (
            ("hoge", 15, [1, 2, 3]),
            ("bar", 40, ("Test", 123)),
        )

        registry.add(add_data[0][0], add_data[0][1], add_data[0][2])
        assert add_data[0][0] in registry
        assert add_data[0][2] in registry
        assert add_data[0][1:] == registry["hoge"]
        assert add_data[0] == registry[1]

        registry.add(add_data[1][0], add_data[1][1], add_data[1][2])
        assert add_data[1][0] in registry
        assert add_data[1][2] in registry
        assert add_data[1][1:] == registry["bar"]
        assert add_data[1] == registry[3]

    def test_add_items(self, registry: Registry) -> None:
        pass
