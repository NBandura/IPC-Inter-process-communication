import random
from textual import on
from textual.app import App
from textual.widgets import Label, Footer, Button, Static
import sys

import argparse

# ArgumentParser erstellen
parser = argparse.ArgumentParser(description="Bingo-Spiel")

# Argument hinzufügen
parser.add_argument('-d', '--datei', type=str, required=True, help="Pfad zur Datei mit den Buzzwords")
parser.add_argument('-s', '--size', type=int, required=True, help="Größe des Spielfelds")
# Argumente parsen
args = parser.parse_args()

# Dateipfad aus den Argumenten extrahieren
dateipfad = args.datei
size = args.size

# Überprüfen, ob die Größe des Spielfelds zwischen 3 und 7 liegt
if size < 3 or size > 7:
    print("Die Größe des Spielfelds muss zwischen 3 und 7 liegen.")
    sys.exit(1)


# Wörter werden eingelesen und in einer Liste gespeichert
buzzword_Wörter = []
with open(dateipfad, 'r') as file:
    buzzword_Wörter = [zeile.strip() for zeile in file]

class Bingo(App):
    CSS_PATH = "stylesMBW.tcss"
    
    def compose(self):
        self.zufallswort_label = Label("", id="zufallswort_label")
        self.error_message = Label("", id="error_message")
        self.zufallswort_button = Button("Wort generieren", id="zufallswort")
        self.clear_button = Button("Wort weg machen", id="clear")
        self.grid_container = Static(classes="bingo-grid")
        self.gewonnen_label = Label("", id="gewonnen_label")
        self.bingo_confirm_button = Button("Bingo bestätigen", id="bingo_confirm") 
        self.quit_button = Button("Quit", id="quit", classes="quit-button")  # Neuer Quit-Button


        yield self.error_message
        yield self.zufallswort_label
        yield self.zufallswort_button
        yield self.clear_button
        yield self.grid_container
        yield self.gewonnen_label
        yield self.bingo_confirm_button  # Bingo-Bestätigungsbutton hinzufügen
        yield self.quit_button  # Quit-Button hinzufügen
        yield Footer()
      

        self.bingo_felder_erstellen(size)  # Erstellen Sie das Bingo-Feld beim Start

    def bingo_felder_erstellen(self, size):
        self.grid_container.remove_children()  # Entfernt das alte Grid
        
        self.button_name_Liste = []  # Liste zum Speichern der Wörter
        self.button_status = {}  # Dictionary zum Speichern des Status der Buttons

        benutzte_wörter = []
        for y in range(size):
            for x in range(size):
                if size in {5, 7} and y == size // 2 and x == size // 2:
                    button_name = "Joker Feld"
                else:
                    while True:
                        button_name = random.choice(buzzword_Wörter)
                        if button_name not in benutzte_wörter:
                            benutzte_wörter.append(button_name)
                            break
                self.button_name_Liste.append(button_name)
                button_id = f"button_{y}_{x}"
                self.button_status[button_id] = False  # Initialer Status des Buttons ist False (nicht durchgestrichen)
                button = Button(button_name, id=button_id, classes="bingo-button")
                self.grid_container.mount(button)
        
        self.grid_container.styles.grid_size_columns = size  # Formatiert in CSS
        self.grid_container.styles.grid_size_rows = size

    def überprüfe_bingo(self):
        # Horizontale Überprüfung
        for y in range(size):
            if all(self.button_status.get(f"button_{y}_{x}", False) for x in range(size)):
                self.bingo_confirm_button.add_class("bingoconf")  # Fügt die "bingoconf"-Klasse zum Button hinzu
                return True
    
        # Vertikale Überprüfung
        for x in range(size):
            if all(self.button_status.get(f"button_{y}_{x}", False) for y in range(size)):
                self.bingo_confirm_button.add_class("bingoconf")  # Fügt die "bingoconf"-Klasse zum Button hinzu
                return True
    
        # Diagonale Überprüfung (von links oben nach rechts unten)
        if all(self.button_status.get(f"button_{i}_{i}", False) for i in range(size)):
            self.bingo_confirm_button.add_class("bingoconf")  # Fügt die "bingoconf"-Klasse zum Button hinzu
            return True
    
        # Diagonale Überprüfung (von rechts oben nach links unten)
        if all(self.button_status.get(f"button_{i}_{size-1-i}", False) for i in range(size)):
            self.bingo_confirm_button.add_class("bingoconf")  # Fügt die "bingoconf"-Klasse zum Button hinzu
            return True
    
        self.bingo_confirm_button.remove_class("bingoconf")  # Entfernt die "bingoconf"-Klasse vom Button
        return False
    
      
         

    @on(Button.Pressed)  # Behandelt das Ereignis, wenn ein beliebiger Button gedrückt wird
    def wort_streiche(self, event: Button.Pressed):
        button_id = event.button.id  # Damit man eben genau diesen Button anspricht, keinen anderen 
        # Überprüft, ob der Button Teil des Grids ist
        if button_id.startswith("button_"):  # Nur die Buttons, die wirklich auch in der Grid, also Tabelle, sind
            if button_id in self.button_status:
                self.button_status[button_id] = not self.button_status[button_id]  # Ändert den Status des Buttons
                if self.button_status[button_id]:
                    event.button.add_class("strikethrough")  # Fügt dem Button die Klasse "strikethrough" hinzu
                else:
                    event.button.remove_class("strikethrough")  # Entfernt die Klasse "strikethrough" vom Button
                if self.überprüfe_bingo():
                    self.update_gewonnen_label("Bingo! Du hast gewonnen!")

    @on(Button.Pressed, "#zufallswort")
    def zufallswort_generieren(self):
        zufallswort = random.choice(buzzword_Wörter)
        self.zufallswort_label.update(zufallswort)

    @on(Button.Pressed, "#bingo_confirm")  # Event-Handler für den Bingo-Bestätigungsbutton
    def on_bingo_confirm(self, event):
        if self.überprüfe_bingo():
            self.update_gewonnen_label("Bingo!") 
            #Message für Bingo gewonnen nach dem Button gedrückt wurde 
        else:
            self.update_gewonnen_label("Noch kein Bingo. Versuche es weiter!")

    @on(Button.Pressed, "#clear")
    def clear_label(self):
        self.zufallswort_label.update("")
        self.error_message.update("")
    
    def update_gewonnen_label(self, message):
        self.gewonnen_label.update(message)

    @on(Button.Pressed, "#quit")  # Event-Handler für den Quit-Button
    def on_quit(self, event):
        self.quit()

if __name__ == "__main__":
    Bingo().run()
