import datetime #Importieren des Time moduls zum erfassen der Zeit
import os #Importieren des OS Moduls, um Dateien zu erstellen und zu verwalten

class Logger:
    
    def __init__(self, playerId): #Konstruktor für ein Logger Objekt
        self.file = self.createFile(playerId)

    def createFile(self, playerId): #Methode um Datei für Spieler zu erstellen
        time = datetime.datetime.now()
        file = open(f"{time} PlayerId: {playerId}.txt", "w")
        return file
        
        

        