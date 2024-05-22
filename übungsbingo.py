import random
from tabulate import tabulate
from textual import on
from textual.app import App
from textual.widgets import Input, Label, Footer, Button
from textual.reactive import reactive

dateipfad = "buzzwords.txt" # Dateipfad wird gespeichert
buzzword_Wörter = [] # Liste wird erstellt
with open(dateipfad, 'r') as file:
    buzzword_Wörter = [zeile.strip() for zeile in file]


def matrix_erstellen(y_achse, x_achse): # matrix erstellen einfach logik
    matrix = []
    benutzewörter = [] # damit es keine doppelten Wörter gibt

    for i in range(y_achse):
        row = []
        for j in range(x_achse):
            row.append("")  # Platzhalter für spätere Einträge
        matrix.append(row)

    if y_achse == 5 and x_achse == 5: # bei 5 bzw 7 Große Felder wird einer Joker festgelegt
        matrix[2][2] = "Joker Feld"
    elif y_achse == 7 and x_achse == 7:
        matrix[3][3] = "Joker Feld"
   



    for i in range(y_achse):
        for j in range(x_achse):
            if matrix[i][j] == "Joker Feld": # Joker überspringen
                continue
            while True:
                random_word = random.choice(buzzword_Wörter)  # Zufälliges Wort auswählen
                if random_word not in benutzewörter:  # falls noch nicht verwendet 
                    benutzewörter.append(random_word)
                    matrix[i][j] = random_word
                    break

    return matrix


class BingoApp(App): # hier wird das Programm gespeicher welches ausgeführt werden kann 
   
    spieler_Dran = 0
    spieler_labels = []
  

    BINDINGS = {
        ("q", "quit", "Quit"),
        ("c", "commit", "Commit"),
        ("a", "add_bingoSpieler", "Add"),
    }

    def compose(self): # alles was hier drin steht wird angezeigt auch das Label wird hier schon definiert ohne text und später erst überarbeitet 
        self.anzahl_Spieler_input = Input(placeholder="Anzahl der Spieler", name="anzahl_Spieler_input")
        self.y_input = Input(placeholder="Anzahl der Zeilen", name="y_input")
        self.x_input = Input(placeholder="Anzahl der Spalten", name="x_input") # input entgegennehmen und in einer Variable speichern
        self.matrix_label = Label("", id="matrix_label")
        self.zufallswort_label = Label("", id="zufallswort_label")
        yield self.anzahl_Spieler_input
        yield self.y_input # mit yield wird es angezeigt
        yield self.x_input
        yield self.matrix_label
        yield self.zufallswort_label
        yield Button("Wort generiern", id="zufallswort")
        yield Button("Wort weg machen", id="clear")
        yield Footer() # Bodenzeiel wird angezeigt in dieser sieht man welche key Bidnungen es gibt 
    
    @on(Button.Pressed, "#zufallswort") # wenn der Button gedrückt wird wird die Methode ausgeführt
    def zufallswort_generieren(self):
        benutzte_wörter = [] # damit es keine doppelten Wörter gibt
        while True:
            zufallswort = random.choice(buzzword_Wörter)  # zufälliges Wort auswählen
            if zufallswort not in benutzte_wörter:  # sicherstellen, dass das Wort noch nicht verwendet wurde
                benutzte_wörter.append(zufallswort)
                break
        self.zufallswort_label.update(zufallswort) # Label erstellen
        



         # zufälliges Wort auswählen
        
        

    @on(Button.Pressed, "#clear") # wenn der Button gedrückt wird wird die Methode ausgeführt
    def clear_label(self):
        self.zufallswort_label.update("") # Label leeren
       

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.y_input.value.strip() and self.x_input.value.strip():
            try: # das ganze überprüft einfach nur, dass es eine eingabe gibt, welche auch eine ganze Zahl ist
                y_value = int(self.y_input.value)
                x_value = int(self.x_input.value)
                spieler_value = int(self.anzahl_Spieler_input.value)
            except ValueError:
                self.compose_error_message("Bitte geben Sie gültige Ganzzahlen ein.")
                return
 
            if y_value > 7 or x_value > 7: # das überprüft, dass die Anzahl der Zeilen und Spalten nicht größer als 7 oder 5 ist
                self.compose_error_message("Die Anzahl der Zeilen und Spalten darf nicht größer als 7 sein.")
                return
            elif y_value < 3 or x_value < 3:
                self.compose_error_message("Die Anzahl der Zeilen und Spalten darf nicht kleiner als 3 sein.")
                return

            self.clear_matrix_labels() # leert die Matrix Labels, damit sie dannach gefüllt werden kann
            

            for i in range(spieler_value):
                matrix = matrix_erstellen(y_value, x_value) # erstellt für jeden Spieler eine Matrix
                matrix_str = f"Spieler {i+1}\n" # speichert die Matrix als String
                matrix_str += tabulate(matrix, tablefmt="fancy_grid")
                self.matrix_str_list.append(matrix_str) # für jeden Spieler wird ein Matrix String in der Matrix Liste hinzugefügt, auf diese kann dann später zugegriffen wernde

            self.spieler_Dran = 0 # bei jedem neuen Spiel wird der Spieler zurückgesetzt
            self.update_matrix_label() # aktualisiert das Label mit der Matrix des ersten Spielers

    def clear_matrix_labels(self): # leert die Matrix Labels
        self.matrix_str_list = []
        self.matrix_label.update("")

    def update_matrix_label(self):
        if self.matrix_str_list: # wenn die Matrix Liste nicht leer ist, wird das Label aktualisiert mit dem Spieler der zuzusagen als nächstes dran ist 
            self.matrix_label.update(self.matrix_str_list[self.spieler_Dran]) # das passiert hier per einfacher Index zugriff 

    def compose_error_message(self, message): #falls ein Fehler auftritt bei der Eingabe wird eine Fehlermeldung ausgegeben
        error_label = Label(message, id="error_label")
        self.mount(error_label)

    def action_quit(self):
        self.exit() # Programm beenden

    def action_commit(self):
        self.spieler_Dran += 1 
        if self.spieler_Dran >= len(self.matrix_str_list): # wenn alle Spieler durch sind wird das Spiel zurückgesetzt
            self.spieler_Dran = 0
        self.update_matrix_label()

    def action_add_bingoSpieler(self): # mit dieser Methode kann man in dem Spiel jeder Zeit einen Spieler hinzufügen 
        y_value = int(self.y_input.value) # muss man erst wieder definierern, damit python die eingegbenen Werte erkennt und hier verwendet
        x_value = int(self.x_input.value)
        new_matrix = matrix_erstellen(y_value, x_value) # matrix erstellen
        matrix_str = f"Spieler {len(self.matrix_str_list) + 1}\n" # matrix als String speichern
        matrix_str += tabulate(new_matrix, tablefmt="fancy_grid")  #hier wird formatier
        self.matrix_str_list.append(matrix_str) # der Stringliste über die über die comitfunktion iteriert wird hinzufügen
        self.spieler_Dran = len(self.matrix_str_list) - 1 # der Ort an der die Matrix gespeicher wird die hier länge der Liste minus eins da es der 5 Wert der Liste ist die aber den Index 4 hat
        self.update_matrix_label() 


if __name__ == "__main__":
    BingoApp().run()

#was noch gemacht werden muss: Streichen und Gewonnen? sowie nach dem der Input eingelesen wurd muss dieser versteckt werden