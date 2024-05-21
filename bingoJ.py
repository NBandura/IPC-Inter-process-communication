import random
from textual import on
from textual.app import App
from textual.widgets import Input, Label, Footer, Button, Static
from textual.reactive import reactive

dateipfad = "buzzwords.txt"  # Wörter werden eingelesen und in einer Liste gespeichert
buzzword_Wörter = []
with open(dateipfad, 'r') as file:
    buzzword_Wörter = [zeile.strip() for zeile in file]

class Bingo(App):
    CSS_PATH = "styles.tcss"
    
    def compose(self):
        self.y_input = Input(placeholder="Anzahl der Zeilen", name="y_input")
        self.x_input = Input(placeholder="Anzahl der Spalten", name="x_input")
        self.zufallswort_label = Label("", id="zufallswort_label")
        self.error_message = Label("", id="error_message")
        self.zufallswort_button = Button("Wort generieren", id="zufallswort")
        self.clear_button = Button("Wort weg machen", id="clear")
        self.grid_container = Static(classes="bingo-grid")
        self.gewonnen_label = Label("", id="gewonnen_label")

        yield self.y_input
        yield self.x_input
        yield self.error_message
        yield self.zufallswort_label
        yield self.zufallswort_button
        yield self.clear_button
        yield self.grid_container
        yield self.gewonnen_label
        yield Footer()

    def bingo_felder_erstellen(self, y_input_value, x_input_value):
        button_name = ""
        self.button_name_Liste = []  # Liste zum Speichern der Wörter
        self.button_status = {}  # Dictionary zum Speichern des Status der Buttons
        
        self.grid_container.remove()  # Entfernt das alte Grid
        self.grid_container = Static(classes="bingo-grid")  # Erstellt ein neues Grid
        
        benutzte_wörter = []
        for y in range(y_input_value):
            for x in range(x_input_value):
                if (y_input_value == 5 and x_input_value == 5) or (y_input_value == 7 and x_input_value == 7):
                    mitte_y = y_input_value // 2
                    mitte_x = x_input_value // 2
                    if y == mitte_y and x == mitte_x:
                        button_name = "Joker Feld"
                        self.button_name_Liste.append(button_name)
                    else:
                        while True:
                            button_name = random.choice(buzzword_Wörter)
                            if button_name not in benutzte_wörter:
                                benutzte_wörter.append(button_name)
                                self.button_name_Liste.append(button_name)
                                break
                else:
                    while True:
                        button_name = random.choice(buzzword_Wörter)
                        if button_name not in benutzte_wörter:
                            benutzte_wörter.append(button_name)
                            self.button_name_Liste.append(button_name)
                            break

                button_id = f"button_{y}_{x}"
                self.button_status[button_id] = False  # Initialer Status des Buttons ist False (nicht durchgestrichen)
                button = Button(button_name, id=button_id, classes="bingo-button")
                self.grid_container.mount(button)
        
        self.grid_container.styles.grid_size_columns = x_input_value # formatiert in css
        self.grid_container.styles.grid_size_rows = y_input_value
        self.mount(self.grid_container)

    def überprüfe_bingo(self):
    # Horizontale Überprüfung
        for y in range(self.y_value):
            row_bingo = True
            for x in range(self.x_value):
                button_id = f"button_{y}_{x}"
                if not self.button_status.get(button_id, False):
                    row_bingo = False
                    break
            if row_bingo:
                return True
    
    # Vertikale Überprüfung
        for x in range(self.x_value):
            col_bingo = True
            for y in range(self.y_value):
                button_id = f"button_{y}_{x}"
                if not self.button_status.get(button_id, False):
                    col_bingo = False
                    break
            if col_bingo:
                return True
    
    # Diagonale Überprüfung (von links oben nach rechts unten)
        diagonal_bingo1 = all(self.button_status.get(f"button_{i}_{i}", False) for i in range(min(self.y_value, self.x_value)))
        if diagonal_bingo1:
            return True
    
    # Diagonale Überprüfung (von rechts oben nach links unten)
        diagonal_bingo2 = all(self.button_status.get(f"button_{i}_{self.x_value-1-i}", False) for i in range(min(self.y_value, self.x_value)))
        if diagonal_bingo2:
            return True
    
        return False

# Wo immer Sie überprüfen möchten, ob ein Bingo erzielt wurde, rufen Sie diese Methode auf


    @on(Button.Pressed)  # Behandelt das Ereignis, wenn ein beliebiger Button gedrückt wird
    def wort_Streiche(self, event: Button.Pressed):
        button_id = event.button.id  # damit man eben genau diesen Butoon anspricht keinen andern 
        # Überprüft, ob der Button Teil des Grids ist
        if button_id.startswith("button_"): # nur die Buttons die wirklich auch in der Grid also Tabelle sind
            if button_id in self.button_status:
                self.button_status[button_id] = not self.button_status[button_id]  # Ändert den Status des Buttons
                if self.button_status[button_id]:
                    event.button.add_class("strikethrough")  # Fügt dem Button die Klasse "strikethrough" hinzu
                else:
                    event.button.remove_class("strikethrough")  # Entfernt die Klasse "strikethrough" vom Button

    @on(Button.Pressed, "#zufallswort")
    def zufallswort_generieren(self):
        benutzte_wörter2 = []

        
        while True:
            zufallswort = random.choice(buzzword_Wörter)
            if zufallswort not in benutzte_wörter2:
                self.zufallswort_label.update(zufallswort)
                benutzte_wörter2.append(zufallswort)
                break
            elif len(benutzte_wörter2) == len(buzzword_Wörter):
                self.error_message.update("Alle Wörter wurden benutzt.")
                break
            
            
            else: 
                continue

            

    @on(Button.Pressed, "#clear")
    def clear_label(self):
        self.zufallswort_label.update("")
        self.error_message.update("")
    
    def gewonnen_label(self, message):
        self.gewonnen_label.update(message)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.y_input.value.strip() and self.x_input.value.strip():
            try:
                y_value = int(self.y_input.value)
                x_value = int(self.x_input.value)
                if y_value > 0 and x_value > 0:
                    if y_value <= 7 and x_value <= 7:
                        if y_value >= 3 and x_value >= 3:
                            self.bingo_felder_erstellen(y_value, x_value)
                        else:
                            self.compose_error_message("Die Anzahl der Zeilen und Spalten darf nicht kleiner als 3 sein.")
                    else:
                        self.compose_error_message("Die Anzahl der Zeilen und Spalten darf nicht größer als 7 sein.")
                else:
                    self.compose_error_message("Die Anzahl der Zeilen und Spalten muss größer als Null sein.")
            except ValueError:
                self.compose_error_message("Bitte geben Sie gültige Ganzzahlen ein.")

    def compose_error_message(self, message):
        self.error_message.update(message)

if __name__ == "__main__":
    Bingo().run()
