# -*- coding: utf-8 -*-
# author: RShirohara


from collections import namedtuple


# "Registry"内で使用されるタプルの定義
_PriorityItem = namedtuple("PriorityItem", ["name", "priority"])


class Registry:
    """優先度順にソートされたレジストリ。

    "register"を使用してアイテムを追加し、
    "deregister"を使用してアイテムを削除する。
    読み込み後はリストのように振る舞う。
    例えば:
        reg = Registry()
        reg.register(hoge(), "Hoge", 20)
        # インデックスで取得する
        item = reg[0]
        # アイテム名で取得する
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
        # 同じインスタンスが存在するかを確認
        return item in self.data.values()

    def __iter__(self):
        self._sort()
        return iter([self._data[k] for k, p in self._priority])

    def __getitem__(self, key):
        self._sort()
        if isinstance(key, slice):
            # スライスで指定した場合
            data = Registry()
            for k, p in self._priority[key]:
                data.register(self._data[k], k, p)
            return data
        if isinstance(key, int):
            # インデックスで指定した場合
            return self._data[self._priority[key].name]
        # 文字列で指定された場合
        return self._data[key]

    def __len__(self):
        return len(self._priority)

    def __repr__(self):
        return f"<{self.__class__.__name__}({list(self)})>"

    def _sort(self):
        """レジストリを優先度順に並べ替える。"""
        if not self._is_sorted:
            self._priority.sort(key=lambda item: item.priority, reverse=True)
            self._is_sorted = True

    def get_index(self, name):
        """指定された名前のインデックスを返す。

        Args:
            name (str): インデックス名
        """
        if name in self:
            self._sort()
            return self._priority.index(
                [x for x in self._priority if x.name is name][0]
            )
        raise ValueError(f"No item named {name} exists.")

    def register(self, item, name, priority):
        """指定した名前と優先度でアイテムをレジストリに追加。

        同名のアイテムが存在した場合は上書きされる。

        Args:
            item (def): アイテム
            name (str): アイテム名
            priority (int): 優先度
        """
        if name in self:
            # 同名のアイテムがある場合削除
            self.deregister(name)
        self._is_sorted = False
        self._data[name] = item
        self._priority.append(_PriorityItem(name, priority))

    def deregister(self, name, strict=True):
        """指定したアイテムをレジストリから削除

        Args:
            name (str): アイテム名
        """
        try:
            index = self.get_index(name)
            del self._priority[index]
            del self._data[name]
        except ValueError:
            if strict:
                raise
