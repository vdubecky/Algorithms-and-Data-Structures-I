#!/usr/bin/env python3


from typing import Any, Optional, List


class HashPair:
    """Trida reprezentujici dvojici klice 'key' a hodnoty 'data'."""

    def __init__(self, key: Any, data: Any) -> None:
        self.key: Any = key
        self.data: Any = data


class Node:
    """Trida Node slouzi pro reprezentaci objektu v obousmerne
    spojovanem seznamu.

    Atributy:
        pair    reprezentuje ulozenou dvojici (klic, data)
        next    reference na nasledujici prvek v seznamu
        prev    reference na predchazejici prvek v seznamu
    """

    def __init__(self, pair: HashPair = HashPair(0, 0)) -> None:
        self.pair: HashPair = pair
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None


class LinkedList:
    """Trida LinkedList reprezentuje spojovany seznam.

    Atributy:
        first   reference na prvni prvek seznamu
        last    reference na posledni prvek seznamu
    """

    def __init__(self) -> None:
        self.first: Optional[Node] = None
        self.last: Optional[Node] = None


SIZE = 10   # velikost hasovaci tabulky


class HashTable:
    """Trida HashTable reprezentujici hasovaci tabulku.

    Atributy:
        table   pole zretezenych seznamu
                zretezene seznamy obsahuji dvojice HashPair,
                ktere jsou indexovany podle indexu pole
    """

    def __init__(self) -> None:
        self.table: List[LinkedList] = [LinkedList() for x in range(SIZE)]


def insert_linked_list(linked_list: LinkedList, pair: HashPair) -> None:
    """Metoda insert_linked_list vlozi na konec (za prvek last) seznamu
    novy uzel s hodnotou pair.
    """
    node = Node(pair)
    node.prev = linked_list.last
    if linked_list.first is None:
        linked_list.first = node
    else:
        assert linked_list.last is not None
        linked_list.last.next = node
    linked_list.last = node


def search_linked_list(linked_list: LinkedList, key: Any) -> Optional[Node]:
    """Metoda search_linked_list vraci referenci na prvni vyskyt uzlu
    s klicem 'key'. Pokud se hodnota v seznamu nenachazi, vraci None.
    """
    node = linked_list.first
    while node is not None and node.pair.key is not key:
        node = node.next
    return node


def delete_linked_list(linked_list: LinkedList, node: Optional[Node]) -> None:
    """Metoda delete_linked_list smaze uzel node ze seznamu."""
    if node is None:
        return
    if node.prev is None:
        linked_list.first = node.next
    else:
        node.prev.next = node.next
    if node.next is None:
        linked_list.last = node.prev
    else:
        node.next.prev = node.prev


def hash(key: Any) -> Any:
    """Funkce vypocita hodnotu hasovaci funkce pro klic 'key'
    na zaklade velikosti tabulky.
    Hashovaci funkce f(n) = n mod 'SIZE'
    """
    return key % SIZE


def insert_hashtable(hashtable: HashTable, key: Any, data: Any) -> None:
    """Vytvori dvojici 'HashPair' z hodnot 'key' a 'data'. Pote vlozi
    vytvorenou dvojici do tabulky.
    """
    pair = HashPair(key, data)
    insert_linked_list(hashtable.table[hash(key)], pair)


def get_hashtable(hashtable: HashTable, key: Any) -> Optional[Any]:
    """Najde dvojici s klicem 'key' a vrati klici prirazenou
    hodnotu 'data'. Pokud se klic v tabulce nenachazi, vraci None.
    """
    pair = search_linked_list(hashtable.table[hash(key)], key)
    if pair:
        return pair.pair.data
    return None


def remove_hashtable(hashtable: HashTable, key: Any) -> None:
    """Odstrani prvni vyskyt dvojice s klicem 'key'."""
    hash_k = hash(key)
    delete_linked_list(hashtable.table[hash_k], search_linked_list(hashtable.table[hash_k], key))


def keys_hashtable(hashtable: HashTable) -> List[Any]:
    """Vrati seznam vsech klicu v tabulce."""
    keys = []
    for lst in hashtable.table:
        node = lst.first
        while node:
            keys.append(node.pair.key)
            node = node.next
    return keys


def values_hashtable(hashtable: HashTable) -> List[Any]:
    """Vrati seznam vsech hodnot v tabulce."""
    keys = []
    for lst in hashtable.table:
        node = lst.first
        while node:
            keys.append(node.pair.data)
            node = node.next
    return keys


# Testy implementace

def test_hash() -> None:
    print("Test 1. hasovaci funkce (hash): ")

    for key in 10, 5323, 65321:
        if hash(key) != key % SIZE:
            print("NOK - nekorektni hasovani.")
            print("Vase hodnota {} != {}".format(hash(key), key % SIZE))
            return

    print("OK")


def test_insert() -> None:
    print("Test 2. vkladani do tabulky (insert):")
    t = HashTable()
    key = SIZE - 1
    value = 'A'
    insert_hashtable(t, key, value)
    node = t.table[key % SIZE].first
    if node is None:
        print("NOK - nekorektni vkladani do tabulky")
        print("V tabulce je po vlozeni None")
        return
    if node.pair.data != value:
        print("NOK - nekorektni vkladani do tabulky")
        print("Na pozici hash({}) se na prvni pozici ".format(key), end="")
        print("v seznamu nenachazi hodnota '{}'".format(value))
        print("Ve vasi tabulce se na pozici hash({}) ".format(key), end="")
        print("nachazi '{}'".format(node.pair.data))
        return
    key = SIZE * 2
    value = 'B'
    insert_hashtable(t, key, value)
    node = t.table[key % SIZE].first
    if node is None:
        print("NOK - nekorektni vkladani do tabulky")
        print("V tabulce je po vlozeni None")
        return
    if node.pair.data != value:
        print("NOK - nekorektni vkladani do tabulky")
        print("Na pozici hash({}) se na prvni pozici ".format(key), end="")
        print("v seznamu nenachazi hodnota '{}'".format(value))
        print("Ve vasi tabulce se na pozici hash({}) ".format(key), end="")
        print("nachazi '{}'".format(node.pair.data))
        return
    key = 2 * SIZE - 1
    value = 'C'
    insert_hashtable(t, key, value)
    node = t.table[key % SIZE].first
    if node is None:
        print("NOK - nekorektni vkladani do tabulky")
        print("V tabulce je po vlozeni None")
        return
    if node.next is None:
        print("NOK - nekorektni vkladani do tabulky")
        print("V tabulce je po vlozeni None")
        return
    if node.next.pair.data != value:
        print("NOK - nekorektni vkladani do tabulky")
        print("Na pozici hash({}) se na prvni pozici ".format(key), end="")
        print("v seznamu nenachazi hodnota '{}'".format(value))
        print("Ve vasi tabulce se na pozici hash({}) ".format(key), end="")
        print("nachazi '{}'".format(node.next.pair.data))
        return
    key = 0
    value = 'D'
    insert_hashtable(t, key, value)
    node = t.table[key % SIZE].last
    if node is None:
        print("NOK - nekorektni vkladani do tabulky")
        print("V tabulce je po vlozeni None")
        return
    if node.pair.data != value:
        print("NOK - nekorektni vkladani do tabulky")
        print("Na pozici hash({}) se na prvni pozici ".format(key), end="")
        print("v seznamu nenachazi hodnota '{}'".format(value))
        print("Ve vasi tabulce se na pozici hash({}) ".format(key), end="")
        print("nachazi '{}'".format(node.pair.data))
        return
    print("OK")


def init_table() -> HashTable:
    t = HashTable()
    p1 = HashPair(0, 'A')
    p2 = HashPair(SIZE, 'B')
    p3 = HashPair(1, 'C')
    p4 = HashPair(2 * SIZE, 'D')
    p5 = HashPair(2 * SIZE - 2, 'E')

    insert_linked_list(t.table[0], p1)
    insert_linked_list(t.table[0], p2)
    insert_linked_list(t.table[0], p4)
    insert_linked_list(t.table[1], p3)
    insert_linked_list(t.table[SIZE - 2], p5)
    return t


def check_get(res: Any, correct: Any) -> Any:
    if res != correct:
        print("NOK - nekorektni hledani v tabulce")
        print("Tabulka vraci {} != {}".format(res, correct))

    return res == correct


def test_get() -> None:
    print("Test 3. hledani v tabulce (get):")
    t = init_table()

    res = get_hashtable(t, 0)
    if not check_get(res, 'A'):
        return

    res = get_hashtable(t, SIZE)
    if not check_get(res, 'B'):
        return

    res = get_hashtable(t, 1)
    if not check_get(res, 'C'):
        return

    res = get_hashtable(t, 2 * SIZE)
    if not check_get(res, 'D'):
        return

    res = get_hashtable(t, 2 * SIZE - 2)
    if not check_get(res, 'E'):
        return

    res = get_hashtable(t, 3 * SIZE - 2)
    if not check_get(res, None):
        return

    res = get_hashtable(t, SIZE - 3)
    if not check_get(res, None):
        return

    print("OK")


def test_remove() -> None:
    print("Test 4. odstranovani z tabulky (remove):")
    t = init_table()
    key = 1
    remove_hashtable(t, key)
    if t.table[key % SIZE].first is not None:
        print("NOK - nekorektni odebirani prvku s klicem {}".format(key))
        return
    key = 2 * SIZE - 2
    remove_hashtable(t, key)
    if t.table[key % SIZE].first is not None:
        print("NOK - nekorektni odebirani prvku s klicem {}".format(key))
        return
    key = 0
    remove_hashtable(t, key)
    node = t.table[key % SIZE].first
    if (node is None or
            node.pair.data != 'B'):
        print("NOK - nekorektni odebirani prvku s klicem {}".format(key))
        return
    key = 2 * SIZE
    remove_hashtable(t, key)
    node = t.table[key % SIZE].first
    if (node is None or
            node.pair.data != 'B'):
        print("NOK - nekorektni odebirani prvku s klicem {}".format(key))
        return
    key = SIZE
    remove_hashtable(t, key)
    if t.table[key % SIZE].first is not None:
        print("NOK - nekorektni odebirani prvku s klicem {}".format(key))
        return
    print("OK")


def test_keys() -> None:
    print("Test 5. seznam klicu (keys):")
    t = HashTable()
    res: List[Any] = []
    k = keys_hashtable(t)
    if k != res:
        print("NOK - nekorektni vypis klicu {}".format(res))
        print("Vas vystup: {}".format(k))
        return

    t = init_table()
    k = keys_hashtable(t)
    res = [0, SIZE, 2 * SIZE, 1, 2 * SIZE - 2]
    if k != res:
        print("NOK - nekorektni vypis klicu {}".format(res))
        print("Vas vystup: {}".format(k))
        return

    p = HashPair(SIZE // 2, 'G')
    insert_linked_list(t.table[SIZE // 2], p)
    k = keys_hashtable(t)
    res = [0, SIZE, 2 * SIZE, 1, SIZE // 2, 2 * SIZE - 2]
    if k != res:
        print("NOK - nekorektni vypis klicu {}".format(res))
        print("Vas vystup: {}".format(k))
        return

    print("OK")


def test_values() -> None:
    print("Test 6. seznam hodnot (value):")
    t = HashTable()
    res: List[Any] = []
    k = values_hashtable(t)
    if k != res:
        print("NOK - nekorektni vypis hodnot {}".format(res))
        print("Vas vystup: {}".format(k))
        return

    t = init_table()
    k = values_hashtable(t)
    res = ['A', 'B', 'D', 'C', 'E']
    if k != res:
        print("NOK - nekorektni vypis hodnot {}".format(res))
        print("Vas vystup: {}".format(k))
        return

    p = HashPair(SIZE // 2, 'G')
    insert_linked_list(t.table[SIZE // 2], p)
    res = ['A', 'B', 'D', 'C', 'G', 'E']
    k = values_hashtable(t)
    if k != res:
        print("NOK - nekorektni vypis hodnot {}".format(res))
        print("Vas vystup: {}".format(k))
        return

    print("OK")


if __name__ == '__main__':
    test_hash()
    print()
    test_insert()
    print()
    test_get()
    print()
    test_remove()
    print()
    test_keys()
    print()
    test_values()
    print()