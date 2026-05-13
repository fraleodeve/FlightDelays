import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza = None
        self._choiceDestinazione = None

    def handleAnalizzaAeroporti(self, e):
        nMintxt = self._view._txtInCMin.value
        if nMintxt == "":
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Inserire un valore numerico", color = "red"))
            self._view.update_page()
            return

        try:
            valore = int(nMintxt)
        except ValueError:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Inserire un valore intero", color="red"))
            self._view.update_page()
            return

        if valore <= 0:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Inserire un valore intero positivo", color = "red"))
            self._view.update_page()
            return

        self._model.buildGraph(valore)
        numNodi = self._model.getNumNodes()
        numArchi = self._model.getNumEdges()

        self._view._txt_results.controls.clear()
        self._view._txt_results.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view._txt_results.controls.append(ft.Text(f"Il grafo contiene {numNodi} nodi e {numArchi} archi."))

        allNodes = self._model.getAllNodes()
        self.fillDropdown(allNodes)

        self._view.update_page()

    def handleConnessi(self, e):
        pass

    def handleCercaItinerario(self, e):
        pass

    def fillDropdown(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data = n,
                                                                       # key = n.AIRPORT,
                                                                       key = n.IATA_CODE,
                                                                       on_click = self._choiceDDaP))
            self._view._ddAeroportoD.options.append(ft.dropdown.Option(data = n,
                                                                       # key = n.AIRPORT,
                                                                       key = n.IATA_CODE,
                                                                       on_click=self._choiceDDaD))
    def _choiceDDaP(self, e):
        self._choicePartenza = e.control.data
        print(f"Aeroporto di partenza: {self._choicePartenza}")

    def _choiceDDaD(self, e):
        self._choiceDestinazione = e.control.data
        print(f"Aeroporto di destinazione: {self._choiceDestinazione}")
