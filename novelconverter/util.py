# -*- coding: utf-8 -*-
# author: @RShirohara

"""NovelConverter Utility module.

Attributes:
    Registry: A list sorted by priority.
"""

from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from typing import (
    Any,
    Container,
    Iterable,
    Iterator,
    NamedTuple,
    Optional,
    TypeVar,
    overload,
)


Unknown = TypeVar("Unknown")


class RegistryItem(NamedTuple):
    """A tuple to store registry item.

    Attributes:
        key (str): Key used to reference item.
        priority (int): Priority used for sort in registry.
        value (Any): Item added to registry.
    """

    key: str
    priority: int
    value: Any


@dataclass(repr=False)
class Registry(Container[Unknown]):
    """A registry sorted by priority.

    Registry is a list-like data structure.
    Registry item is sorted of prioritry (ascending order).
    """

    __data: dict[str, Unknown] = field(default_factory=dict[str, Unknown], init=False)
    __priority: dict[str, int] = field(default_factory=dict[str, int], init=False)
    __key_cache: tuple[str] = field(
        default_factory=tuple[str], init=False, hash=False, compare=False
    )
    __is_sorted: bool = field(default=False, init=False, hash=False, compare=False)
    items: InitVar[Optional[Iterable[tuple[str, int, Unknown]]]] = None

    def __post_init__(
        self, items: Optional[Iterable[tuple[str, int, Unknown]]]
    ) -> None:
        if not items:
            return
        for key, priority, value in items:
            self.__setitem__((key, priority), value)

    def __contains__(self, item: Unknown) -> bool:
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

    @overload
    def __getitem__(self, key: int) -> Unknown:
        pass

    @overload
    def __getitem__(self, key: str) -> Unknown:
        pass

    @overload
    def __getitem__(self, key: slice) -> "Registry[Unknown]":
        pass

    def __getitem__(self, key: int | str | slice) -> Any:
        self.__sort()
        match key:
            case int() if type(key) != bool:
                return self.__data[self.__key_cache[key]]
            case str():
                if key not in self.__priority.keys():
                    raise KeyError(key)
                return self.__data[key]
            case slice():
                items: tuple[RegistryItem] = tuple(
                    RegistryItem(k, self.__priority[k], self.__data[k])
                    for k in self.__key_cache[key]
                )
                reg: Container[Unknown] = Registry(items)
                return reg
            case _:
                raise TypeError("registry indices must be integers, strings or slices")

    def __iter__(self) -> Iterator[tuple[str, int, Unknown]]:
        self.__sort()
        return iter(
            RegistryItem(key, self.__priority[key], self.__data[key])
            for key in self.__key_cache
        )

    def __len__(self) -> int:
        return len(self.__priority)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" + tuple(self.__iter__()).__repr__()

    def __setitem__(self, key: tuple[str, int], value: Unknown) -> None:
        if not isinstance(key, tuple):
            raise TypeError("registry indices on add must be tuple")
        if not isinstance(key[0], str):
            raise TypeError("registry key indices must be string")
        if not isinstance(key[1], int):
            raise TypeError("registry priority indices must be int")

        # block duplicates with existing item.
        if key[0] in self.__priority:
            self.__delitem__(key[0])

        self.__is_sorted = False
        self.__data[key[0]] = value
        self.__priority[key[0]] = key[1]

    def __sort(self) -> None:
        if not self.__is_sorted:
            sorted_priority: list[tuple[str, int]] = sorted(
                self.__priority.items(), key=lambda x: x[1]
            )
            self.__key_cache = tuple(key for key, _ in sorted_priority)
            self.__is_sorted = True

    def keys(self) -> tuple[str]:
        """Return the keys registered in Registry.

        Returns:
            tuple[str]: Keys registered in Registry.
        """

        self.__sort()
        return tuple(self.__data.keys())

    def priorities(self) -> dict[str, int]:
        """Return the priorities of item registered in Registry.

        Returns:
            dict[str, int]: Key and priority pair registered in Registry.
        """

        self.__sort()
        return deepcopy(self.__priority)

    def values(self) -> tuple[Unknown]:
        """Return the items registered in Registry.

        Returns:
            tuple[Unknown]: Items registered in Registry.
        """

        self.__sort()
        return tuple(self.__data[key] for key in self.__key_cache)

    def pop(self, key: str) -> Unknown:
        """Remove specified key and return the corresponding value.

        Args:
            key (str): Key used to reference item.

        Raises:
            KeyError: If the key is not found, raise a KeyError.

        Returns:
            Unknown: Item corresponded to key.
        """

        if key not in self.__priority.keys():
            raise KeyError(key)
        item: Unknown = self.__getitem__(key)
        self.__delitem__(key)
        return item
