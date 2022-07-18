# coding: utf-8
# author: Ray Shirohara

"""NovelConverter Utility module."""

from dataclasses import InitVar, dataclass, field
from typing import (
    Any,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    MutableMapping,
    NamedTuple,
    Optional,
    TypeVar,
    ValuesView,
    overload,
)

T = TypeVar("T")


class RegistryKey(NamedTuple):
    """Key-Priority pair to reference an item in registry.

    Attributes:
        key (str): Key used to reference item in registry.
        priority (int): Priority used for sort items in registry.
    """

    key: str
    priority: int

    def __eq__(self, __o: object) -> bool:
        equals: bool = False
        match __o:
            case RegistryKey():
                equals = (self.key, self.priority) == (__o.key, __o.priority)
            case tuple() if __o.__len__() == 3:
                equals = (self.key, self.priority) == (__o[0], __o[1])
            case _:
                equals = False
        return equals

    def __lt__(self, __x: tuple[Any, ...]) -> bool:
        match __x:
            case RegistryKey():
                return (self.priority, self.key) < (__x.priority, __x.key)
            case tuple() if len(__x) == 2 and isinstance(__x[0], str) and isinstance(
                __x[1], int
            ):
                return (self.priority, self.key) < (__x[1], __x[0])
            case _:
                return False

    def __hash__(self) -> int:
        return hash((self.key, self.priority))


@dataclass
class Registry(MutableMapping[(str | RegistryKey), T]):
    """Map-like object sorted by priority.

    Registry is map-like data structure.
    Registry items is sorted in ascending order of priority. If the item priorities are
    duplicated, the items sorted in ascending order of key.

    Args:
        init_items (Iterable[tuple[RegistryKey, T]]):
    """

    __data: dict[str, T] = field(default_factory=dict[str, T], init=False)
    __priorities: dict[str, int] = field(default_factory=dict[str, int], init=False)
    __key_cache: tuple[str, ...] = field(
        default_factory=tuple[str, ...], init=False, hash=False, compare=False
    )
    __is_sorted: bool = field(default=False, init=False, hash=False, compare=False)
    init_items: InitVar[Optional[Iterable[tuple[RegistryKey, T]]]] = None

    def __post_init__(
        self, init_items: Optional[Iterable[tuple[RegistryKey, T]]]
    ) -> None:
        if not init_items:
            return
        for (key, priority), value in init_items:
            self.__setitem__((key, priority), value)

    def __iter__(self) -> Iterator[RegistryKey]:
        self.__sort()
        return iter(
            RegistryKey(key, self.__priorities[key]) for key in self.__key_cache
        )

    def __len__(self) -> int:
        return len(self.__priorities)

    def __delitem__(self, key: int | str | tuple[str, int]) -> None:
        target: str = ""

        self.__sort()
        match key:
            case int() if type(key) != bool:
                target = self.__key_cache[key]
            case str():
                target = key
            case tuple() if len(key) == 2:
                target = key[0]
            case _:
                raise TypeError("registry indices on delete must be entegers or string")

        if (target not in self.__priorities.keys()) or (
            isinstance(key, tuple) and key[1] != self.__priorities[target]
        ):
            raise KeyError(key)

        self.__is_sorted = False
        del self.__priorities[target]
        del self.__data[target]

    @overload
    def __getitem__(self, key: int) -> T:
        ...

    @overload
    def __getitem__(self, key: str) -> T:
        ...

    @overload
    def __getitem__(self, key: tuple[str, int]) -> T:
        ...

    @overload
    def __getitem__(self, key: slice) -> "Registry[T]":
        ...

    def __getitem__(self, key: int | str | tuple[str, int] | slice) -> Any:
        self.__sort()
        match key:
            case int() if type(key) != bool:
                return self.__data[self.__key_cache[key]]
            case str():
                if key not in self.__priorities.keys():
                    raise KeyError(key)
                return self.__data[key]
            case tuple() if len(key) == 2:
                if (key[0] not in self.__priorities.keys()) or (
                    key[1] != self.__priorities[key[0]]
                ):
                    raise KeyError(key)
                return self.__data[key[0]]
            case slice():
                items: tuple[tuple[RegistryKey, T], ...] = tuple(
                    (RegistryKey(k, self.__priorities[k]), self.__data[k])
                    for k in self.__key_cache[key]
                )
                reg: Registry[T] = Registry(items)
                return reg
            case _:
                raise TypeError("registry indices must be integers, strings or slices")

    @overload
    def __setitem__(self, key: str, value: T) -> None:
        ...

    @overload
    def __setitem__(self, key: tuple[str, int], value: T) -> None:
        ...

    def __setitem__(self, key: str | tuple[str, int], value: T) -> None:
        value_key: str
        value_priority: int

        match key:
            case str():
                value_key = key
                priorities: tuple[int, ...] = tuple(self.__priorities.values())
                value_priority = (
                    sorted(priorities, reverse=True)[0] + 1
                    if len(priorities) > 0
                    else 0
                )
            case tuple() if len(key) == 2:
                value_key: str = key[0]
                value_priority: int = key[1]
            case _:
                raise TypeError("registry indices on add must be str or tuple")

        if not isinstance(value_key, str):
            raise TypeError("registry key indices must be string")
        if not isinstance(value_priority, int):
            raise TypeError("registry priority indices must be int")

        self.__is_sorted = False
        self.__data[value_key] = value
        self.__priorities[value_key] = value_priority

    def __sort(self) -> None:
        if self.__is_sorted:
            return
        sorted_priority: list[tuple[str, int]] = sorted(
            self.__priorities.items(), key=lambda x: (x[1], x[0])
        )
        self.__key_cache = tuple(key for key, _ in sorted_priority)
        self.__is_sorted = True

    def keys(self) -> KeysView[str]:
        """Return keys registered in Registry.

        Returns:
            KeysView[RegistryKey]: Keys registered in Registry.
        """

        self.__sort()
        return {key: key for key in self.__key_cache}.keys()

    def priorities(self) -> KeysView[RegistryKey]:
        """Return key and priority pairs registered in Registry.

        Returns:
            KeysView[RegistryKey]: Key and priority pairs.
        """

        self.__sort()
        return {
            RegistryKey(key, self.__priorities[key]): key for key in self.__key_cache
        }.keys()

    def values(self) -> ValuesView[T]:
        """Return items registered in Registry.

        Returns:
            ValuesView[T]: Items registered in Registry.
        """

        self.__sort()
        return {key: self.__data[key] for key in self.__key_cache}.values()

    def items(self) -> ItemsView[RegistryKey, T]:
        """Return key and item pairs registered in Registry.

        Returns:
            ItemsView[RegistryKey, T]: key-priority tuple and item pairs.
        """

        self.__sort()
        return {
            RegistryKey(key, self.__priorities[key]): self.__data[key]
            for key in self.__key_cache
        }.items()
