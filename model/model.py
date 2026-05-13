import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._grafo = nx.Graph() # va bene per la traccia
        self._airports = DAO.getAllAirports()

        self._idMap = {}
        for el in self._airports:
            self._idMap[el.ID] = el

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMap)
        # ottengo nodi già filtrati
        self._grafo.add_nodes_from(nodes)
        self.addEdges2()

    def addEdges(self): # SQL più facile, python più difficile
        allTratte = DAO.getAllEdgesV1(self._idMap)
        # 1. problema: ho archi diretti e inversi (devo fare somma a mano)
        # 2. problema: ho archi fra aeroporti che avevo filtrato

        for t in allTratte:
            if t.aeroportoP in self._grafo and t.aeroportoA in self._grafo: # per risolvere il 2. problema
                if self._grafo.has_edge(t.aeroportoP, t.aeroportoA): # per risolvere il 1. problema
                    self._grafo[t.aeroportoP][t.aeroportoA]["weight"] += t.peso
                else:
                    self._grafo.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def addEdges2(self): # SQL più difficile, python più facile
        allTratte = DAO.getAllEdgesV2(self._idMap)
        for t in allTratte:
            if t.aeroportoP in self._grafo and t.aeroportoA in self._grafo:
                self._grafo.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getAllNodes(self):
        nodes = list(self._grafo.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes
