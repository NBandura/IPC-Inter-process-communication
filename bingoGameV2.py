import random
from textual import on
from textual.app import App
from textual.dom import DOMNode
from textual.widgets import Label, Footer, Button, Static
import sys
import os
from Logger import Logger
from IPC import SpielIPC
import argparse

print()
print()
print()
print()
print()

print("<......Bingo Game......>")
spielname = input("Bitte geben Sie den Spielnamen ein, mit dem Sie sich verbinden wollen: ")
IPC= SpielIPC(spielname) #IPC für das Spiel erstellen
logger = Logger(os.getpid()) #Logger für jeden Prozess erstellen
logger.logGameStart()

if(IPC.checkIfStarted()):
    size=IPC.getGroesse()
    dateipfad=IPC.getDateipfad()
    istStartProzess=False
    buzzword_Wörter = []
    # Wörter werden eingelesen und in einer Liste gespeichert
    with open(dateipfad, 'r') as file:
        buzzword_Wörter = [zeile.strip() for zeile in file]
else:
    size=0
    while(True):
        try:
            size=int(input("Bitte gebe die Spielfeldgröße ein: "))
        except ValueError:
            None
        if(size < 3 or size > 7 ):
            print("Ungültige Größe: Erlaubt ist eine Größe von 3 - 7 und sie darf keine Dezimalzahl sein")
        else:
            break
    
    while (True):
        try:
            dateipfad=input("Bitte gebe den Dateipfad ein: ")
            buzzword_Wörter = []
            # Wörter werden eingelesen und in einer Liste gespeichert
            with open(dateipfad, 'r') as file:
                buzzword_Wörter = [zeile.strip() for zeile in file]
            break
        except Exception:
            print("Der Dateipfad ist ungültig!")

    IPC.setDateipfad(dateipfad)
    IPC.setGroesse(size)
    IPC.startGame()
    istStartProzess=True
    
# Startprozess ist fertig
# Noch zu machen:
# Prozess muss solange laufen bis (IPC.checkIfBingo) true ist, dann müssen alle die es nicht gesendet haben, ein Verloren Feld bekommen
# Und so lange auch, die Sachen dauerhaft aktualisieren:
#   Wortliste anzeigen (IPC.getWortliste)
#   Letztes Wort anzeigen (IPC.getLastWord)
# Speicher Freigeben Button in "Spiel Abbrechen" umbennen
# Sonst bei Bingo 5 sec. warten, dann speicher automatisch freigeben



class Bingo(App):
    CSS_PATH = "StylesMBW.tcss"
    
    def compose(self):
        self.zufallswort_label = Label("", id="zufallswort_label")
        self.error_message = Label("", id="error_message")
        self.zufallswort_button = Button("Wort generieren", id="zufallswort")
        self.grid_container = Static(classes="bingo-grid")
        self.gewonnen_label = Label("", id="gewonnen_label")
        self.bingo_confirm_button = Button("Bingo bestätigen", id="bingo_confirm") 
        self.quit_button = Button("Quit", id="quit", classes="quit-button")  # Neuer Quit-Button
        self.speicher_freigeben_button = Button("Speicher freigeben", id="speicher_freigeben", classes="freigeben")  # speicher freigeben
        self.getWort = Label("", id="getWort", classes="getWort")
        self.wortliste_label = Label("", id="wortliste_label")
        self.CheckBingo_label = Label("", id="CheckBingo_label")


        yield self.error_message
        if(istStartProzess):
            yield self.zufallswort_label
            yield self.zufallswort_button
            yield self.speicher_freigeben_button
        else:
            yield self.getWort
            yield self.wortliste_label
        yield self.grid_container
        yield self.CheckBingo_label
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
        buttonName = str(event.button.label)
        button_id = str(event.button.id)  # Damit man eben genau diesen Button anspricht, keinen anderen 
        logger.logWord(buttonName, button_id)
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
        IPC.addWord(zufallswort)
        self.zufallswort_label.update(zufallswort)

    @on(Button.Pressed, "#bingo_confirm")  # Event-Handler für den Bingo-Bestätigungsbutton
    def on_bingo_confirm(self, event):
        if self.überprüfe_bingo():
            logger.logGameResult(0)
            self.update_gewonnen_label("Bingo!") 
            IPC.bingo()
            #Message für Bingo gewonnen nach dem Button gedrückt wurde 
        else:
            self.update_gewonnen_label("Noch kein Bingo. Versuche es weiter!")
    
    def update_gewonnen_label(self, message):
        self.gewonnen_label.update(message)

    def update_lastWort(self):
        self.getWort.update(IPC.getLastWort())
    
    def update_Wortliste(self):
        self.wortliste_label.update((IPC.getWortString()).replace(";", ", "))

    def update_checkBingo(self):
        if IPC.checkIfBingo():
            self.CheckBingo_label.update("Es hat jemand gewonnen!")
        else:
            self.CheckBingo_label.update("Es hat noch niemand gewonnen!")
    
    def on_mount(self):
        self.set_interval(0.1, self.update_lastWort)
        self.set_interval(0.1, self.update_Wortliste)
        self.set_interval(0.1, self.update_checkBingo)
    
    


    @on(Button.Pressed, "#quit")  # Event-Handler für den Quit-Button
    def on_quit(self, event):
        logger.logGameEnd()
        self.exit()

    @on(Button.Pressed, "#speicher_freigeben") 
    def speicher_freigeben(self):
        IPC.speicherFreigeben() # Event-Handler für den Speicher freigeben-Button

    

if __name__ == "__main__": 
    Bingo().run()
