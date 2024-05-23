import datetime #Importieren des Time moduls zum erfassen der Zeit
import os #Importieren des OS Moduls, um Dateien zu erstellen und zu verwalten

class Logger:
    
    def __init__(self, playerId): #Konstruktor für ein Logger Objekt
        self.playerId = playerId
        self.file = self._logCreateFile()

    def _logCreateFile(self): #Methode um Datei für Spieler zu erstellen
        time = datetime.datetime.now()
        filename = time.strftime("%Y-%m-%d-%H-%M-%S") + f"-bingo-{self.playerId}.txt"
        file = open(filename, "w")
        file.close
        return filename

    def logGameStart(self):
        time = datetime.datetime.now()
        file = open(self.file, "a")
        file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Start des Spiels\n")
        file.close

    def logGameEnd(self):
        time = datetime.datetime.now()
        file = open(self.file, "a")
        file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Ende des Spiels\n")
        file.close

    def logWord(self, word, buttonId):
        time = datetime.datetime.now()
        file = open(self.file, "a") 
        file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + word + " " + buttonId + "\n")
        file.close
    
    def logGameResult(self, result):
        time = datetime.datetime.now()
        file = open(self.file, "a")
        if result == 0:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Sieg\n")
        elif result == 1:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Abbruch\n")
        file.close()