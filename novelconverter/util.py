# -*- coding: utf-8 -*-
# author: RShirohara


from collections import namedtuple


# "Registry"内で使用される名前付きタプルの定義
_PriorityItem = namedtuple("PriorityItem", ["name", "priority"])


class Registry:
    """A priority sorted by registry.

    Use "add to add items and "delete" to remove items.
    A "Registry" instance it like a list when reading data.

    For example:
        reg = Registry()
        reg.add(hoge(), "Hoge", 20)
        # by index
        item = reg[0]
        # by name
        item = reg["Hoge"]
    """

    def __init__(self):
        self._data = {}
        self._priority = []
        self._is_sorted = False

    def __contains__(self, item):
        if isinstance(item, str):
            # 同名のアイテムが存在するかを確認
            return item in self._data.keys()
        return item in self._data.values()

    def __iter__(self):
        self._sort()
        return iter([self._data[k] for k, v in self._priority])

    def __getitem__(self, key):
        self._sort()
        if isinstance(key, slice):
            # スライスで指定した場合
            reg = Registry()
            for k, v in self._priority[key]:
                reg.add(self._data[k], k, v)
            return reg
        if isinstance(key, int):
            # インデックスで指定した場合
            return self._data[self._priority[key].name]
        # 文字列で指定した場合
        return self._data[key]

    def __len__(self):
        return len(self._priority)

    def __repr__(self):
        return f"<{self.__class__.__name__}({list(self)})>"

    def _sort(self):
        """Sort the registry by priority."""
        if not self._is_sorted:
            self._priority.sort(key=lambda item: item.priority, reverse=True)
            self._is_sorted = True

    def get_index(self, name):
        """Return the index of the given name

        Args:
            name (str): index name
        """
        if name in self:
            self._sort()
            return self._priority.index(
                [x for x in self._priority if x.name is name][0]
            )
        raise ValueError(f"No item named {name} exists.")

    def add(self, item, name, priority):
        """Add an item to the registry with the given name and priority.

        If an item is registered with a "name" which already exists, the
        existing item is replaced with the new item.

        Args:
            item (function): item
            name (str): item name
            priority (int): priority
        """
        if name in self:
            # 同名のアイテムがある場合削除
            self.delete(name)
        self._is_sorted = False
        self._data[name] = item
        self._priority.append(_PriorityItem(name, priority))

    def delete(self, name, strict=True):
        """Delete an item to the registry with the given name.

        Args:
            name (str): item name
        """
        try:
            index = self.get_index(name)
            del self._priority[index]
            del self._data[name]
        except ValueError:
            if strict:
                raise
