from model.model import Model

myModel = Model()
myModel.buildGraph(5)
print(f"Numero nodi: {myModel.getNumNodes()}") # se N = 5 -> 98 nodi
print(f"Numero archi: {myModel.getNumEdges()}") # se N = 5 -> 1522 archi
