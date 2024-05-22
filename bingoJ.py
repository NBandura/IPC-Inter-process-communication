import random
from textual import on
from textual.app import App
from textual.widgets import Input, Label, Footer, Button, Static

dateipfad = "buzzwords.txt"  # Wörter werden eingelesen und in einer Liste gespeichert
buzzword_Wörter = []
with open(dateipfad, 'r') as file:
    buzzword_Wörter = [zeile.strip() for zeile in file]

class Bingo(App):
    CSS_PATH = "styles.tcss" # hier wird beschrieben wie die Buttons im Bingofeld aussehen werden
    benutzte_wörter = []
    zufallswort = ""
    gewähltes_wort = "" 

    def compose(self): # alles was hier drin passieret wird mit yield auf die Console gemalt
        self.y_input = Input(placeholder="Anzahl der Zeilen", name="y_input")
        self.x_input = Input(placeholder="Anzahl der Spalten", name="x_input")
        self.zufallswort_label = Label("", id="zufallswort_label")
        self.error_message = Label("", id="error_message")
        self.zufallswort_button = Button("Wort generieren", id="zufallswort")
        self.clear_button = Button("Wort weg machen", id="clear")
        self.grid_container = Static(classes="bingo-grid")
        self.sieg = Label("", id="gewonnen_label")

        yield self.y_input
        yield self.x_input
        yield self.error_message
        yield self.zufallswort_label
        yield self.zufallswort_button
        yield self.clear_button
        yield self.grid_container
        yield self.sieg
        yield Footer() # Fußzeile kann aber eigentlich auch weggelassen werden

    def bingo_felder_erstellen(self, y_input_value, x_input_value):
        button_name = ""
        self.button_name_Liste = []  # Liste zum Speichern der Wörter
        self.button_status = {}  # Dictionary zum Speichern des Status der Buttons

        self.y_value = y_input_value  # Speichert die Werte, damit sie später verwendet werden können
        self.x_value = x_input_value
        
        self.grid_container.remove()  # Entfernt das alte Grid
        self.grid_container = Static(classes="bingo-grid")  # Erstellt ein neues Grid
        
        benutzte_wörter = []  # Liste zum Speichern der bereits verwendeten Wörter
        for y in range(y_input_value):
            for x in range(x_input_value):
                if (y_input_value == 5 and x_input_value == 5) or (y_input_value == 7 and x_input_value == 7): # ist jetzt die vereifcht bzw zusammengefasst
                    mitte_y = y_input_value // 2 # mitte der Zeilen
                    mitte_x = x_input_value // 2 # mitte der Spalten
                    if y == mitte_y and x == mitte_x: # joker Feld wird platziert
                        button_name = "Joker Feld"
                        self.button_name_Liste.append(button_name)
                    else:
                        while True: # ansonten zufälliges Wort
                            button_name = random.choice(buzzword_Wörter)
                            if button_name not in benutzte_wörter:
                                benutzte_wörter.append(button_name)
                                self.button_name_Liste.append(button_name)
                                break
                else:
                    while True: # wenn nicht 5 mal 5 oder 7 mal 7 dann zufälliges Wort
                        button_name = random.choice(buzzword_Wörter) 
                        if button_name not in benutzte_wörter:
                            benutzte_wörter.append(button_name)
                            self.button_name_Liste.append(button_name)
                            break

                button_id = f"button_{y}_{x}" # button id wird erstellt darüber ist jeder Button ansprechbar
                self.button_status[button_id] = False  # Status also ob durchgestrichen oder nicht 
                button = Button(button_name, id=button_id, classes="bingo-button") # bennenung button
                self.grid_container.mount(button) # button wird zum register hinzugefügt
        
        self.grid_container.styles.grid_size_columns = x_input_value  # Formatiert in CSS
        self.grid_container.styles.grid_size_rows = y_input_value
        self.mount(self.grid_container) # das Register wird der Console hinzugefügt
    
    def compose_error_message(self, message): # für Fehlermeldungen 
        self.error_message.update(message)

    def überprüfe_bingo(self):
        # Horizontale Überprüfung
        for y in range(self.y_value): # kann euch erkläre wie das funktioniert ist aber einfacher als ihr denkt
            if all(self.button_status.get(f"button_{y}_{x}", False) and self.query_one(f"#button_{y}_{x}").disabled for x in range(self.x_value)): # der zweite Teil überprüft, ob die Buttons auch disabled sind 
                return True
        
        # Vertikale Überprüfung
        for x in range(self.x_value):
            if all(self.button_status.get(f"button_{y}_{x}", False) and self.query_one(f"#button_{y}_{x}").disabled for y in range(self.y_value)):
                return True
        
        # Diagonale Überprüfung (von links oben nach rechts unten)
        if all(self.button_status.get(f"button_{i}_{i}", False) and self.query_one(f"#button_{i}_{i}").disabled for i in range(min(self.y_value, self.x_value))):
            return True
        
        # Diagonale Überprüfung (von rechts oben nach links unten)
        if all(self.button_status.get(f"button_{i}_{self.x_value-1-i}", False) and self.query_one(f"#button_{i}_{self.x_value-1-i}").disabled for i in range(min(self.y_value, self.x_value))):
            return True
        
        return False

    @on(Button.Pressed)  # Behandelt das Ereignis, wenn ein beliebiger Button gedrückt wird
    def wort_Streiche(self, event: Button.Pressed):
        button_id = event.button.id  # Damit man genau diesen Button anspricht, keinen anderen
        button_name = str(event.button.label)  # muss in einen String umgewandelt werden
        # Überprüft, ob der Button Teil des Grids ist
        if button_id.startswith("button_"):  # Nur die Buttons, die wirklich auch in der Grid also Tabelle sind
            if button_id in self.button_status and not event.button.disabled:
                if button_name == self.gewähltes_wort or button_name == "Joker Feld": # wenn das Wort das zufallswort ist oder das Jokerfeld ist
                    event.button.disabled = True  # Button wird deaktiviert und bleibt gestrichen
                    self.button_status[button_id] = True
                    event.button.add_class("strikethrough")  # Fügt dem Button die Klasse "strikethrough" hinzu
                else:
                    self.button_status[button_id] = not self.button_status[button_id]  # Ändert den Status des Buttons
                    if self.button_status[button_id]:
                        event.button.add_class("strikethrough")  # Fügt dem Button die Klasse "strikethrough" hinzu
                    else:
                        event.button.remove_class("strikethrough")  # Entfernt die Klasse "strikethrough" vom Button
            if self.überprüfe_bingo():
                self.sieg.update("Bingo! Sie haben gewonnen!")

    @on(Button.Pressed, "#zufallswort") # zufalls wort wird generiert
    def zufallswort_generieren(self, event: Button.Pressed):
        if len(self.benutzte_wörter) == len(buzzword_Wörter):
            self.compose_error_message("Alle Wörter wurden bereits verwendet.") # funktioniert irgendiwe nocch  nicht
            return 
        
        while True:
            self.zufallswort = random.choice(buzzword_Wörter) # zufälliges Wort wird ausgewählt
            if self.zufallswort not in self.benutzte_wörter: # geprüft wird, ob das Wort bereits verwendet wurde
                self.gewähltes_wort = self.zufallswort # Das Wort wird als gewählt markiert -> meine idee ist, das man darüber ermittelt ob der gedrückte Button dem ZUfallswort entspricht 
                self.zufallswort_label.update(self.zufallswort)
                self.benutzte_wörter.append(self.zufallswort)
                break

    @on(Button.Pressed, "#clear") # löscht das zufallswort
    def clear_label(self, event: Button.Pressed):
        self.zufallswort_label.update("")
        self.error_message.update("")
    
    def gewonnen_label(self, message): # für die Gewinnnachricht
        self.sieg.update(message)

    async def on_input_submitted(self, event: Input.Submitted) -> None: # durch enter bestätigen
        if self.y_input.value.strip() and self.x_input.value.strip(): # wird versucht in Integer umzuwandeln, wenn das nicht klappt fehlermeldung
            try:
                y_value = int(self.y_input.value)
                x_value = int(self.x_input.value) # formatierung
                if y_value > 0 and x_value > 0:
                    if y_value <= 7 and x_value <= 7: # Fehlermeldung, wenn kleiner als drei oder größer 7 eingegeben wird -> kann nich angepasst werden
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

if __name__ == "__main__":
    Bingo().run()
