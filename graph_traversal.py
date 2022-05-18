#!/usr/bin/env python3
from collections import deque
from typing import List, Optional, TextIO


# V teto uloze mate implementovat zakladni funkce pro pruchod grafu.
#
# V prikladech pouzivame orientovany neohodnoceny graf, ktery je reprezentovan
# matici sousednosti. Matice je indexovana od [0][0], vrcholum tedy odpovidaji
# cisla 0 .. n - 1, kde n je velikost grafu (pocet vrcholu). V matici je
# na indexu [u][v] hodnota True nebo False, podle toho, jestli graf obsahuje
# hranu u -> v.
#
# Ve vypisech matic pro usporu mista pouzivame 0/1 misto False/True.


class Graph:
    def __init__(self, size: int) -> None:
        """Vytvori orientovany graf se 'size' vrcholy a bez jakychkoli hran.
        Atributy:
            size: pocet vrcholu v grafu
            matrix: maticova reprezentace grafu popsana vyse

            parent, distance: pro pouziti v algoritmu BFS, viz nize
            parent, visited, discovery_time, finishing_time:
                pro pouziti v algoritmu DFS, viz nize
        """
        self.size: int = size
        self.matrix: List[List[bool]] = [[False] * size for _ in range(size)]
        self.clear_flags()

    def clear_flags(self) -> None:
        self.parent: List[Optional[int]] = [None] * self.size
        self.distance: List[Optional[int]] = [None] * self.size
        self.discovery_time: List[Optional[int]] = [None] * self.size
        self.finishing_time: List[Optional[int]] = [None] * self.size

        self.visited: List[bool] = [False] * self.size


def is_edge(graph: Graph, u: int, v: int) -> bool:
    """Pokud v matici vzdalenosti 'matrix' existuje hrana (u, v), vraci
    True, jinak False.
    """
    return graph.matrix[u][v]


def bfs(graph: Graph, start: int) -> None:
    """Prochazeni grafu do sirky (BFS) z vrcholu start.
    Pri vyberu nasledniku vybirejte vzdy nejdrive naslednika s mensim cislem.

    vstup: 'graph' typu Graph, v nemz maji pomocna pole vsechny prvky
           nastaveny na None (visited na False)
           'start' pocatecni vrchol, z nejz ma zacit prohledavani
    vystup: nic, do pomocnych poli parent a distance se ulozi informace:
        parent[u] = rodic vrcholu u ve vyslednem BFS stromu
                    (None pokud u nebyl nalezen nebo u = start)
        distance[u] = vzdalenost od start do u ve vyslednem BFS stromu
                      (None pokud u nebyl nalezen)
    """
    queue = deque([start])
    graph.distance[start] = 0
    while queue:
        u = queue.popleft()
        for v in range(graph.size):
            if is_edge(graph, u, v) and graph.distance[v] is None:
                graph.distance[v] = graph.distance[u] + 1
                graph.parent[v] = u
                queue.append(v)


def _dfs(graph: Graph, u: int, time: int) -> int:
    graph.visited[u] = True
    time += 1
    graph.discovery_time[u] = time

    for v in range(graph.size):
        if is_edge(graph, u, v) and not graph.visited[v]:
            graph.parent[v] = u
            time = _dfs(graph, v, time)

    time += 1
    graph.finishing_time[u] = time
    return time


def dfs(graph: Graph, start: int) -> None:
    """Prochazeni grafu do hloubky (DFS) z vrcholu start; vcetne casovych znamek.
    Pri vyberu nasledniku vybirejte vzdy nejdrive naslednika s mensim cislem.

    vstup: 'graph' typu Graph, v nemz maji pomocna pole vsechny prvky
           nastaveny na None (visited na False)
           'start' pocatecni vrchol, z nejz ma zacit prohledavani
    vystup: nic, do pomocnych poli se ulozi informace:
        parent[u] = rodic vrcholu u ve vyslednem DFS stromu
                    (None pokud u nebyl nalezen nebo u = start)
        discovery_time[u] = casova znamka objeveni vrcholu u
        finishing_time[u] = casova znamka ukonceni zpracovani vrcholu u
        (casove znamky neobjevenych vrcholu jsou None)

    Tip: Vyuzijte pomocne pole 'visited' pro uchovavani informace o tom, ktere
    vrcholy byly navstiveny.

    Je podstatne jednodussi tuto funkci naprogramovat rekurzivne. Jako bonus
    muzete zkusit napsat iterativni verzi.
    """
    _dfs(graph, start, 0)


def convert_to_list(graph: Graph) -> List[List[int]]:
    """Vytvori seznam nasledniku z grafu zadaneho matici sousednosti 'matrix'.
    V seznamech nasledniku se vyskytuji indexy sousedu, nic jineho.
    Pokud vrchol nema nasledniky, je jeho seznam nasledniku prazdny.
    Pro implementaci seznamu pouzijte bezne Pythonovske seznamy.

    Napr. pro graf zadany matici:
        0 0 1
        1 1 1
        0 0 0
    ma byt vysledkem [[2], [0, 1, 2], []]
    """
    res = []
    for i in range(graph.size):
        row = []
        for j in range(graph.size):
            if is_edge(graph, i, j):
                row.append(j)
        res.append(row)
    return res


# Dodatek k graphvizu:
# Graphviz je nastroj, ktery vam umozni vizualizaci datovych struktur, coz se
# hodi predevsim pro ladeni.Vygenerovane soubory nahrajte do online nastroje
# pro zobrazeni graphvizu:
# http://sandbox.kidstrythisathome.com/erdos/
# nebo http://www.webgraphviz.com/ - zvlada i vetsi grafy.
#
# Alternativne si muzete nainstalovat prekladac z jazyka dot do obrazku na
# svuj pocitac.
def make_graph(graph: Graph, filename: str) -> None:
    with open(filename, 'w') as f:
        f.write("digraph MyGraph {\n")
        make_graphviz(graph, f)
        f.write("}\n")


def make_graphviz(graph: Graph, f: TextIO) -> None:
    for u in range(graph.size):
        for v in range(graph.size):
            if graph.matrix[u][v]:
                f.write('"{}" -> "{}"\n'.format(u, v))


def print_matrix(graph: Graph) -> None:
    for u in range(graph.size):
        for v in range(graph.size):
            print(1 if graph.matrix[u][v] else 0, end=" ")
        print()


def create_test_graph() -> Graph:
    graph = Graph(5)
    graph.matrix[0][1] = True
    graph.matrix[0][3] = True
    graph.matrix[2][0] = True
    graph.matrix[2][1] = True
    graph.matrix[3][4] = True
    graph.matrix[4][0] = True
    graph.matrix[4][3] = True

    return graph


def test_is_edge() -> None:
    print("Test 1. kontrola existence hrany:")

    graph1 = create_test_graph()
    if not is_edge(graph1, 0, 3):
        print("NOK - z vrcholu 0 do vrcholu 3 je hrana, vy vracite False.")
        print("Testovany graf je:")
        print_matrix(graph1)
        return

    graph2 = create_test_graph()
    if is_edge(graph2, 3, 0):
        print("NOK - z vrcholu 3 do vrcholu 0 neni hrana, vy vracite True.")
        print("Testovany graf je:")
        print_matrix(graph2)
        return

    print("OK")


def check_bfs(
        graph: Graph,
        start: int,
        parent: List[Optional[int]],
        distance: List[Optional[int]]
) -> bool:
    bfs(graph, start)

    ok = True

    if graph.parent != parent:
        print("NOK - pole parent ma byt {},".format(parent))
        print("        Vase reseni dava {}".format(graph.parent))
        ok = False

    if graph.distance != distance:
        print("NOK - pole distance ma byt {},".format(distance))
        print("          Vase reseni dava {}".format(graph.distance))
        ok = False

    if not ok:
        print("Testovany graf je:")
        print_matrix(graph)
        print("Pocatecni vrchol byl", start)

    return ok


def test_bfs() -> None:
    print("Test 2. prohledavani do sirky (BFS):")

    graph1 = Graph(3)
    graph1.matrix[1][0] = True
    graph1.matrix[0][1] = True
    graph1.matrix[0][0] = True
    graph1.matrix[1][1] = True

    if not check_bfs(graph1, 0, [None, 0, None], [0, 1, None]):
        return

    graph2 = create_test_graph()

    if not check_bfs(graph2, 0, [None, 0, None, 0, 3], [0, 1, None, 1, 2]):
        return

    graph3 = create_test_graph()

    if not check_bfs(graph3, 2, [2, 2, None, 0, 3], [1, 1, 0, 2, 3]):
        return

    graph4 = create_test_graph()

    if not check_bfs(graph4, 3, [4, 0, None, None, 3], [2, 3, None, 0, 1]):
        return

    graph5 = create_test_graph()

    if not check_bfs(graph5, 4, [4, 0, None, 4, None], [1, 2, None, 1, 0]):
        return

    print("OK")


def check_dfs(
        graph: Graph,
        start: int,
        parent: List[Optional[int]],
        discovery_time: List[Optional[int]],
        finishing_time: List[Optional[int]]
) -> bool:
    dfs(graph, start)

    ok = True

    if graph.parent != parent:
        print("NOK - pole parent ma byt {},".format(parent))
        print("        Vase reseni dava {}".format(graph.parent))
        ok = False

    if graph.discovery_time != discovery_time:
        print("NOK - pole discovery_time ma byt {},".format(discovery_time))
        print("                Vase reseni dava {}"
              .format(graph.discovery_time))
        ok = False

    if graph.finishing_time != finishing_time:
        print("NOK - pole finishing_time ma byt {},".format(finishing_time))
        print("                Vase reseni dava {}"
              .format(graph.finishing_time))
        ok = False

    if not ok:
        print("Testovany graf je:")
        print_matrix(graph)
        print("Pocatecni vrchol byl", start)

    return ok


def test_dfs() -> None:
    print("Test 3. prohledavani do hloubky (DFS):")

    graph1 = Graph(3)
    graph1.matrix[1][0] = True
    graph1.matrix[0][1] = True
    graph1.matrix[0][0] = True
    graph1.matrix[1][1] = True

    if not check_dfs(graph1, 0, [None, 0, None], [1, 2, None], [4, 3, None]):
        return

    graph2 = create_test_graph()

    if not check_dfs(graph2, 0,
                     [None, 0, None, 0, 3],
                     [1, 2, None, 4, 5], [8, 3, None, 7, 6]):
        return

    graph3 = create_test_graph()

    if not check_dfs(graph3, 2,
                     [2, 0, None, 0, 3],
                     [2, 3, 1, 5, 6], [9, 4, 10, 8, 7]):
        return

    graph4 = create_test_graph()

    if not check_dfs(graph4, 3,
                     [4, 0, None, None, 3],
                     [3, 4, None, 1, 2], [6, 5, None, 8, 7]):
        return

    graph5 = create_test_graph()

    if not check_dfs(graph5, 4,
                     [4, 0, None, 0, None],
                     [2, 3, None, 5, 1], [7, 4, None, 6, 8]):
        return

    print("OK")


def test_convert_to_list() -> None:
    print("Test 4. prevod reprezentace grafu na seznam nasledniku: ")

    graph1 = Graph(5)
    lists1 = convert_to_list(graph1)

    if lists1 != [[]] * 5:
        print("NOK - matice neodpovida vracenemu seznamu nasledniku")
        print("Testovany graf je:")
        print_matrix(graph1)
        print("Vas seznam nasledniku:")
        print(lists1)
        return

    graph2 = Graph(5)
    graph2.matrix[1][0] = True
    graph2.matrix[0][1] = True
    lists2 = convert_to_list(graph2)

    if lists2 != [[1], [0], [], [], []]:
        print("NOK - matice neodpovida vracenemu seznamu nasledniku")
        print("Testovany graf je:")
        print_matrix(graph2)
        print("Vas seznam nasledniku:")
        print(lists2)
        return

    graph3 = create_test_graph()
    lists3 = convert_to_list(graph3)

    if lists3 != [[1, 3], [], [0, 1], [4], [0, 3]]:
        print("NOK - matice neodpovida vracenemu seznamu nasledniku")
        print("Testovany graf je:")
        print_matrix(graph3)
        print("Vas seznam nasledniku:")
        print(lists3)
        return

    print("OK")


if __name__ == '__main__':
    test_is_edge()
    print()
    test_bfs()
    print()
    test_dfs()
    print()
    test_convert_to_list()
    # make_graph(create_test_graph(), "test11.dot")
