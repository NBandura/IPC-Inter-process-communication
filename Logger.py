import datetime #Modul zum erfassen der aktuellen Zeit
import os #Modul zum Interagieren mit dem System

class Logger:
    def __init__(self, playerId):
        self.playerId = playerId #Speichern von playerId im Objekt
        self.filename = self._logCreateFile() #Erstellen der Log-Datei direkt bei erstellen eines Logger-Objekts

    def _logCreateFile(self):
        time = datetime.datetime.now() #Erfassen der aktuellen Zeit
        filename = time.strftime("logs/" + "%Y-%m-%d-%H-%M-%S") + f"-bingo-{self.playerId}.txt" #Erstellen des Dateinamens über Pfad
        file = open(filename, "w") #Erstellen der Datei
        file.close #Schließen der Datei um die Datei zu initialisieren
        return filename

    #Schreiben des Spielstarts in die Log-Datei
    def logGameStart(self):
        time = datetime.datetime.now()
        file = open(self.filename, "a")
        file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Start des Spiels\n")
        file.close

    #Schreiben des Spielendes in die Log-Datei
    def logGameEnd(self):
        time = datetime.datetime.now()
        file = open(self.filename, "a")
        file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Ende des Spiels\n")
        file.close

    #Schreiben eines markierten Wortes mit Koordinaten in die Log-Datei 
    def logWord(self, word, x, y):
        time = datetime.datetime.now()
        file = open(self.filename, "a") 
        file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + word + f" ({x}/{y})\n")
        file.close

    #Schreibt das Spielergebnis über eine Statusvariable
    def logGameResult(self, result):
        time = datetime.datetime.now()
        file = open(self.filename, "a")
        if result == 0:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Sieg\n")
        elif result == 1:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Abbruch\n")
        file.close()