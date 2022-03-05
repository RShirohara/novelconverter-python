# -*- coding: utf-8 -*-
# author: @RShirohara

"""NovelConverter Utility module.

Attributes:
    Registry: A list sorted by priority.
"""

from dataclasses import dataclass, field
from typing import Container, Iterable, Iterator, NamedTuple, overload


class RegistryItem(NamedTuple):
    """A tuple to store registry item information.

    Attributes:
        key (str): Key used to reference item.
        priority (int): Priority used for sort in registry.
        item (any): Item added to registry.
    """

    key: str
    priority: int
    item: any


@dataclass(repr=False)
class Registry(Container):
    """A registry sorted by priority.

    Registry is a list-like data structure.
    Registry item is sorted of prioritry (ascending order).
    """

    __data: dict[str, any] = field(default_factory=dict[str, any], init=False)
    __priority: dict[str, int] = field(
        default_factory=dict[str, int], init=False
    )
    __key_cache: tuple[str] = field(
        default_factory=tuple[str], init=False, hash=False, compare=False
    )
    __is_sorted: bool = field(
        default=False, init=False, hash=False, compare=False
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" + tuple(self.__iter__()).__repr__()

    def __len__(self) -> int:
        return len(self.__priority)

    @overload
    def __getitem__(self, key: int) -> RegistryItem:
        pass

    @overload
    def __getitem__(self, key: str) -> RegistryItem:
        pass

    @overload
    def __getitem__(self, key: slice) -> "Registry[any]":
        pass

    def __getitem__(self, key: int | str | slice) -> any:
        self.__sort()
        match key:
            case int() if type(key) != bool:
                k: str = self.__key_cache[key]
                return RegistryItem(k, self.__priority[k], self.__data[k])
            case str():
                if key not in self.__priority.keys():
                    raise KeyError(key)
                return RegistryItem(
                    key, self.__priority[key], self.__data[key]
                )
            case slice():
                items: tuple[tuple[str, int, any]] = tuple(
                    RegistryItem(k, self.__priority[k], self.__data[k])
                    for k in self.__key_cache[key]
                )
                reg: Container[any] = Registry()
                reg.add_items(items)
                return reg
            case _:
                raise TypeError(
                    "registry indices must be integers, strings or slices"
                )

    def __delitem__(self, key: int | str) -> any:
        target: str

        self.__sort()
        match key:
            case int() if type(key) != bool:
                target = self.__key_cache[key]
            case str():
                target = key
            case _:
                raise TypeError(
                    "registry indices on delete must be integers or strings"
                )
        if target not in self.__priority.keys():
            raise KeyError(target)

        self.__is_sorted = False
        del self.__priority[target]
        del self.__data[target]

    def __iter__(self) -> Iterator[tuple[str, int, any]]:
        self.__sort()
        return iter(
            (key, self.__priority[key], self.__data[key])
            for key in self.__key_cache
        )

    def __contains__(self, item: any) -> bool:
        self.__sort()
        match item:
            case str():
                res: bool = item in self.__priority.keys()
                if not res:
                    res = item in self.__data.values()
                return res
            case _:
                return item in self.__data.values()

    def __sort(self) -> None:
        if not self.__is_sorted:
            sorted_priority: list[tuple[str, int]] = sorted(
                self.__priority.items(), key=lambda x: x[1]
            )
            self.__key_cache = tuple(key for key, _ in sorted_priority)
            self.__is_sorted = True

    def add(self, key: str, priority: int, item: any) -> None:
        """Add an item to the registry.

        Args:
            key (str): Key used to reference item.
            priority (int): Priority used for sort in registry.
            item (any): Item added to registry.
        """

        # Block duplicates with existing items.
        if key in self.__priority:
            self.__delitem__(key)

        self.__is_sorted = False
        self.__data[key] = item
        self.__priority[key] = priority

    def add_items(self, items: Iterable[tuple[str, int, any]]) -> None:
        """Add items to the registry all at once.

        Args:
            items (Iterable[tuple[str, int, any]]): Items added to registry.
        """

        for key, priority, item in items:
            self.add(key, priority, item)
