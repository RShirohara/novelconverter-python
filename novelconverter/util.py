# -*- coding: utf-8 -*-
# author: @RShirohara
"""NovelConverter Utility module.

Attributes:
    Registry: A list sorted by priority.
"""

from typing import Iterator, overload


class Registry:
    """A list sorted by priority.

    Registry is a list-like data structure.
    Registry is sorted of priority (ascending order).
    """

    def __init__(self) -> None:
        self.__data: dict[str, any] = {}
        self.__priority: dict[str, int] = {}
        self.__key_cache: list[str] = []
        self.__is_sorted: bool = False

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

    def __delitem__(self, key: int | str) -> None:
        self.__sort()
        target: str = ""
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

    @overload
    def __getitem__(self, key: int) -> any:
        pass

    @overload
    def __getitem__(self, key: str) -> any:
        pass

    @overload
    def __getitem__(self, key: slice) -> "Registry[any]":
        pass

    def __getitem__(self, key: int | str | slice) -> any:
        self.__sort()
        match key:
            case int() if type(key) != bool:
                return self.__data[self.__key_cache[key]]
            case str():
                if key not in self.__priority.keys():
                    raise KeyError(key)
                return self.__data[key]
            case slice():
                reg = Registry()
                for k in self.__key_cache[key]:
                    reg.add(k, self.__priority[k], self.__data[k])
                return reg
            case _:
                raise TypeError(
                    "registry indices must be integers, strings or slices"
                )

    def __iter__(self) -> Iterator[any]:
        self.__sort()
        return iter(self.__data[key] for key in self.__key_cache)

    def __len__(self) -> int:
        return len(self.__priority)

    def __sort(self) -> None:
        if not self.__is_sorted:
            sorted_priority: list[tuple[str, int]] = sorted(
                self.__priority.items(), key=lambda x: x[1]
            )
            self.__key_cache = [key for key, _ in sorted_priority]
            self.__is_sorted = True

    def add(self, key: str, priority: int, item: any) -> None:
        """Add an item to the registry with the given name and priority.

        Args:
            key (str): key of item.
            priority (int): priority of item.
            item (any): item.
        """

        if key in self.__priority:
            self.__delitem__(key)
        self.__is_sorted = False
        self.__data[key] = item
        self.__priority[key] = priority
