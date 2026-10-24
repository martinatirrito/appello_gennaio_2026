import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapC = {}

    def buildGraph(self, year1, year2):
        self._graph.clear()
        nodi = DAO.getAllNodes(year1, year2)
        for n in nodi:
            self._idMapC[n.constructorId] = n
        self._graph.add_nodes_from(nodi)

        edges = DAO.getAllEdges(year1, year2, self._idMapC)
        for e in edges:
            self._graph.add_edge(e.c1, e.c2, weight = e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop3Archi(self):
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:3]

    def getComponentiConnesse(self):
        # nx.number_connected_components(self._graph) anche cosi per numero componente connessa

        components = list(nx.connected_components(self._graph))  # len --> numero componenti connesse
        num_components = len(components)
        largest = max(components, key=len)  # usa la dimensione della componente per decidere qual è la più grande. Mi da tutti i nodi
        # len largest mi da quanti ce ne sono
        #STAMPARE NODI DI LARGEST ORDINATI IN SENSO DECRESCENTE DI GRADO DI NODI
        largestOrdinata = sorted(largest, key=lambda n: self._graph.degree(n), reverse=True)
        return num_components, largest, largestOrdinata

    def getAllYears(self):
        return DAO.getAllYears()

