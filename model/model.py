import copy

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._grafo = nx.Graph() # va bene per la traccia
        self._airports = DAO.getAllAirports()

        self._idMap = {}
        for el in self._airports:
            self._idMap[el.ID] = el

        self._bestCammino = []
        self._bestScore = 0

    # RICORSIONE
    def getCamminoOttimo(self, v0, v1, t):
        self._bestCammino = []
        self._bestScore = 0

        parziale = [v0] # so già che devo partire da v0

        self._ricorsione(parziale, v1, t)

        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1, t):
        # parziale è una soluzione valida? se sì, la salvo
        if parziale[-1] == v1: # per essere valido, ultimo elemento deve essere v1 -> potenzialmente accettabile
            # guardo se soluzione migliore di prima
            if self._getScore(parziale) > self._bestScore: # controllo ottimalità
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        # ha senso continuare ad aggiungere elementi in parziale? altrimenti esco
        if len(parziale) == t+1: # se condizione è vera, allora parziale ha già raggiunto numero massimo di tratte
            return # ritorno e interrompo

        # la if è falsa -> espando parziale e faccio ricorsione con backtracking
        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale: # non ha senso ripassare nello stesso nodo
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()

    def _getScore(self, parziale):
        sumPesi = 0
        for i in range(0, len(parziale)-1):
            sumPesi += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return sumPesi


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

    def getViciniOrdinati(self, source): # aeroporti che posso raggiungere da nodo di partenza
        # restituisce vicini di source, ordinati per peso dell'arco che li collega
        vicini = self._grafo.neighbors(source)
        # creo tupla con peso e ordino
        viciniT = []
        for v in vicini:
            viciniT.append((v, self._grafo[source][v]["weight"]))
            # sono sicuro che arco esista perchè ho preso vicini
        viciniT.sort(key=lambda x: x[1], reverse=True)
        return viciniT

    def hasPath(self, v0, v1):
        # presi due nodi, restituisce True se esiste cammino
        # calcolo componente connessa e verifico se c'è altro nodo
        # nx.connected_components() # restituisce tutte le componenti connesse
        return v1 in nx.node_connected_component(self._grafo, v0) # restituisce componente connessa di un nodo
        # mi restituisce True se c'è, altrimenti False

    def getPath(self, v0, v1):
        # 1. possibilità: BFS
        dictOfPredecessors = dict(nx.bfs_predecessors(self._grafo, v0)) # cerca cammini minimi in numero di archi
        # raggruppo in dizionario -> nodo: chiave, nodo precedente: valore
        pathBFS = [v1]
        while pathBFS[0] != v0:
            pathBFS.insert(0, dictOfPredecessors[pathBFS[0]])
            # finché non arrivo a v0 aggiungo predecessore
        # path = [v0 , ... , v1] parto da v1 e torno indietro

        # 2. possibilità: DFS (cammino più lungo)
        dictOfPredecessors = dict(nx.dfs_predecessors(self._grafo, v0))
        pathDFS = [v1]
        while pathDFS[0] != v0:
            pathDFS.insert(0, dictOfPredecessors[pathDFS[0]])

        # 3. Possibilià: metodo presente in nx -> minimizza numero archi (in questo caso non benissimo)
        path = nx.shortest_path(self._grafo, v0, v1) # usa dijkstra

        # 4. Possibilità: dijkstra -> minimizza numero archi
        pathD = nx.dijkstra_path(self._grafo, v0, v1, weight = None)
        # weight = None, considera nulla gli archi

        # 5. Possibilità
        pathDW = nx.dijkstra_path(self._grafo, v0, v1) # considero il peso

        return pathD


    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getAllNodes(self):
        nodes = list(self._grafo.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes
