import traceback

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        year1 = self._view._ddAnno1.value
        year2 = self._view._ddAnno2.value #.value restituisce stringa

        if year1 is None or year2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione seleziona anno prima di creare il grafo", color="red"))
            self._view._page.update()
            return

        if int(year1) > int(year2):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione anno di inizio deve essere minore di anno di fine.", color="red"))
            self._view._page.update()
            return

        try:
            self._model.buildGraph(year1, year2)
            self._view._btnstampa.disabled = False
            self._view.txt_result.controls.clear()
            Nnodi, Narchi = self._model.getGraphDetails()
            self._view.txt_result.controls.append(
                ft.Text("Grafo correttamente creato.")
            )
            self._view.txt_result.controls.append(
                ft.Text(f"Numero di nodi: {Nnodi}")
            )
            self._view.txt_result.controls.append(
                ft.Text(f"Numero di archi: {Narchi}")
            )

            self._view._page.update()

        except Exception as ex:
            traceback.print_exc()
            #self._view.create_alert(f"Errore nella creazione del grafo: {ex}") non ho il metodo nella view
            self._view.txt_result.controls.append(ft.Text(f"Errore nella creazione del grafo: {ex}"))
            self._view._page.update()

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()

        nNodi, nArchi = self._model.getGraphDetails()
        if nNodi == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            top3 = self._model.getTop3Archi()
            self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore", color = "red"))
            for a in top3:
                self._view.txt_result.controls.append(ft.Text(f'{a[0]} -> {a[1]} ({a[2]["weight"]} piloti condivisi)'))

            num_components, largest, largestOrdinata = self._model.getComponentiConnesse()
            self._view.txt_result.controls.append(ft.Text(f'Il grafo ha {num_components} componenti connesse.', color = "red"))

            self._view.txt_result.controls.append(ft.Text(f'Componente connessa più grande ({len(largest)} nodi)', color="red"))
            for c in largest:
                self._view.txt_result.controls.append(ft.Text(str(c)))

            self._view.txt_result.controls.append(ft.Text(f'Componente connessa in ordine decrescente', color="red"))
            for c in largestOrdinata:
                self._view.txt_result.controls.append(ft.Text(f'{str(c)} (grado = {self._model._graph.degree(c)})'))

            self._view._page.update()


        except Exception as ex:
            traceback.print_exc()
            self._view.txt_result.controls.append(ft.Text(f"Errore nella stampa delle info: {ex}"))
            self._view._page.update()


    def handleCerca(self, e):
        pass

    def fillDDYear1(self):
        anni = self._model.getAllYears()
        for a in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def fillDDYear2(self):
        anni = self._model.getAllYears()
        for a in anni:
            self._view._ddAnno2.options.append(ft.dropdown.Option(a))
        self._view.update_page()
