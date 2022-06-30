#!/usr/bin/env python3

from typing import Any, Optional


class Node:
    """Trida Node slouzi pro reprezentaci objektu v obousmerne
    spojovanem seznamu.

    Atributy:
        value   reprezentuje ulozenou hodnotu/objekt
        next    reference na nasledujici prvek v seznamu
        prev    reference na predchazejici prvek v seznamu
    """

    def __init__(self, value: Any = None, prev: Optional['Node'] = None) -> None:
        self.value: Any = value
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = prev


class LinkedList:
    """Trida LinkedList reprezentuje spojovany seznam.

    Atributy:
        first   reference na prvni prvek seznamu
        last    reference na posledni prvek seznamu
    """

    def __init__(self) -> None:
        self.first: Optional[Node] = None
        self.last: Optional[Node] = None


def insert(linked_list: LinkedList, value: Any) -> Node:
    """Metoda insert() vlozi na konec seznamu linked_list (za prvek last)
    novy uzel s hodnotou value. Vraci nove vlozeny objekt.
    """
    node = Node(value, linked_list.last)
    if not linked_list.first:
        linked_list.first = node
    else:
        linked_list.last.next = node
    linked_list.last = node
    return node


def print_list(linked_list: LinkedList) -> None:
    """Metoda print_list() vypise seznam linked_list."""
    node = linked_list.first
    while node:
        print(node.value, end=" ")
        node = node.next


def search(linked_list: LinkedList, value: Any) -> Optional[Node]:
    """Metoda search() vraci referenci na prvni vyskyt uzlu s hodnotou
    value v seznamu linked_list. Pokud se hodnota v seznamu nenachazi,
    vraci None.
    """
    node = linked_list.first
    while node:
        if node.value == value:
            return node
        node = node.next
    return node


def delete(linked_list: LinkedList, node: Node) -> None:
    """Metoda delete() smaze uzel node v seznamu linked_list."""
    if not node.prev:
        linked_list.first = node.next
    else:
        node.prev.next = node.next

    if not node.next:
        linked_list.last = node.prev
    else:
        node.next.prev = node.prev


# Testy implementace
def test_insert_empty() -> None:
    print("Test 1. Vkladani do prazdneho seznamu: ", end="")

    list1 = LinkedList()
    insert(list1, 1)

    if list1.first is None or list1.last is None:
        print("FAIL")
        return

    if (list1.first.value == 1 and list1.last.value == 1 and
            list1.first.next is None and list1.first.prev is None):
        print("OK")
    else:
        print("FAIL")


def test_insert_nonempty() -> None:
    print("Test 2. Vkladani do neprazdneho seznamu: ", end="")

    list2 = LinkedList()
    node = Node()
    node.value = 1
    node.next = None
    list2.first = node
    list2.last = node

    insert(list2, 2)

    if list2.last is None:
        print("FAIL")
        return

    if (list2.last.value == 2 and list2.last.prev is not None and
            list2.last.prev == list2.first and list2.first.value == 1):
        print("OK")
    else:
        print("FAIL")


def test_search_exist() -> None:
    print("Test 3. Hledani existujiciho prvku v seznamu: ", end="")

    list3 = LinkedList()
    node1 = Node()
    node2 = Node()
    node1.value = 1
    node1.next = node2
    node1.prev = None
    node2.value = 2
    node2.next = None
    node2.prev = node1
    list3.first = node1
    list3.last = node2

    result = search(list3, 2)

    if result == node2:
        print("OK")
    else:
        print("FAIL")


def test_search_not_exist() -> None:
    print("Test 4. Hledani neexistujiciho prvku v seznamu: ", end="")

    list4 = LinkedList()
    node1 = Node()
    node2 = Node()
    node1.value = 1
    node1.next = node2
    node1.prev = None
    node2.value = 2
    node2.next = None
    node2.prev = node1
    list4.first = node1
    list4.last = node2

    result = search(list4, 3)

    if result is None:
        print("OK")
    else:
        print("FAIL")


def test_delete_first() -> None:
    print("Test 5. Odstraneni prvniho prvku v seznamu: ", end="")

    list5 = LinkedList()
    node1 = Node()
    node2 = Node()
    node1.value = 1
    node1.next = node2
    node1.prev = None
    node2.value = 2
    node2.next = None
    node2.prev = node1
    list5.first = node1
    list5.last = node2

    delete(list5, node1)

    if list5.first == node2 and node2.prev is None:
        print("OK")
    else:
        print("FAIL")


def test_delete_mid() -> None:
    print("Test 6. Odstraneni prostredniho prvku v seznamu: ", end="")

    list6 = LinkedList()
    node1 = Node()
    node2 = Node()
    node3 = Node()
    node1.value = 1
    node1.next = node2
    node1.prev = None
    node2.value = 2
    node2.next = node3
    node2.prev = node1
    node3.value = 3
    node3.next = None
    node3.prev = node2
    list6.first = node1
    list6.last = node3

    delete(list6, node2)

    if (list6.last != node3 or list6.last.prev != node1 or
            list6.first.next != node3):
        print("FAIL")
    else:
        print("OK")


def test_delete_last() -> None:
    print("Test 7. Odstraneni posledniho prvku v seznamu: ", end="")

    list7 = LinkedList()
    node1 = Node()
    node2 = Node()
    node3 = Node()
    node1.value = 1
    node1.next = node2
    node1.prev = None
    node2.value = 2
    node2.next = node3
    node2.prev = node1
    node3.value = 3
    node3.next = None
    node3.prev = node2
    list7.first = node1
    list7.last = node3

    delete(list7, node3)

    if (list7.last != node2 or list7.last.prev != node1 or
            list7.first.next != node2):
        print("FAIL")
    else:
        print("OK")


def test_delete_solo() -> None:
    print("Test 8. Odstraneni jedineho prvku v seznamu: ", end="")

    list8 = LinkedList()
    node1 = Node()
    node1.value = 1
    node1.next = None
    node1.prev = None
    list8.first = node1
    list8.last = node1

    delete(list8, node1)

    if list8.last is not None or list8.first is not None:
        print("FAIL")
    else:
        print("OK")


def test_insert_return() -> None:
    print("Test 9. Vraceni vlozeneho prvku: ", end="")

    list9 = LinkedList()
    node = insert(list9, 1)

    if node is None or node.value != 1:
        print("FAIL")
    else:
        print("OK")


if __name__ == '__main__':
    test_insert_empty()
    test_insert_nonempty()
    test_search_exist()
    test_search_not_exist()
    test_delete_first()
    test_delete_mid()
    test_delete_last()
    test_delete_solo()
    test_insert_return()