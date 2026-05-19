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

    def handleConnessi(self, e): # deve restituire aeroporti connessi
        # questo metodo termina il primo punto dell'esame (tempo stimato: 1h)
        if self._choicePartenza is None:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Attenzione! Selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return
        viciniT = self._model.getViciniOrdinati(self._choicePartenza)
        self._view._txt_results.controls.clear()
        self._view._txt_results.controls.append(ft.Text(f"Gli aeroporti raggiungibili da {self._choicePartenza} sono: "))
        for v in viciniT:
            self._view._txt_results.controls.append(ft.Text(f"{v[0]} - peso {v[1]}"))
        self._view.update_page()

    def handleCercaItinerario(self, e):
        t = self._view._txtInTratteMax.value

        try:
            tInt = int(t)
        except ValueError:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(
                ft.Text("Attenzione! Inserire un valore numerico intero", color="red"))
            self._view.update_page()
            return

        if tInt < 0:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(
                ft.Text("Attenzione! Inserire un valore numerico intero positivo", color="red"))
            self._view.update_page()
            return

        if self._choicePartenza is None:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Attenzione! Selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return

        if self._choiceDestinazione is None:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Attenzione! Selezionare un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return

        # volendo posso vedere quanto tempo ci mette -> all'inizio mettere valori piccoli
        path, score = self._model.getCamminoOttimo(self._choicePartenza, self._choiceDestinazione, tInt)
        self._view._txt_results.controls.clear()
        self._view._txt_results.controls.append(ft.Text(f"Cammino tra {self._choicePartenza} e {self._choiceDestinazione}."))
        self._view._txt_results.controls.append(ft.Text(f"Costo complessivo: {score}. Contiene i seguenti nodi:"))
        for p in path:
            self._view._txt_results.controls.append(ft.Text(f"- {p}"))
        self._view.update_page()


    def handleTestConnessione(self, e):
        # stampare percorso tra due aeroporti (se esiste)
        if self._choicePartenza is None:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Attenzione! Selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return
        if self._choiceDestinazione is None:
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(ft.Text("Attenzione! Selezionare un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return

        if not self._model.hasPath(self._choicePartenza, self._choiceDestinazione):
            self._view._txt_results.controls.clear()
            self._view._txt_results.controls.append(
                ft.Text(f"Non esiste un cammino tra {self._choicePartenza} e {self._choiceDestinazione}.", color = "orange"))
            self._view.update_page()
            return

        path = self._model.getPath(self._choicePartenza, self._choiceDestinazione)
        self._view._txt_results.controls.clear()
        self._view._txt_results.controls.append(
            ft.Text(f"Esiste un cammino tra {self._choicePartenza} e {self._choiceDestinazione}. Di seguito il cammino:", color = "green"))
        for p in path:
            self._view._txt_results.controls.append(ft.Text(p))
        self._view.update_page()



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
