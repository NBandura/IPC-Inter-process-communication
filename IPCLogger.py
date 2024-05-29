import datetime  #Importieren des datetime Moduls zum Erfassen der Zeit
import os  #Importieren des os Moduls, um Dateien zu erstellen und zu verwalten

class IPCLogger:
    
    def __init__(self, gameName):
        self.gameName = gameName
        self.file = self._logCreateFile() #automatisches Erstellen der Log-Datei beim erstellen eines Logger Objektes

    def _logCreateFile(self): 
        logsFolderName = "ipc_logs" #Festlegen des Log-Ordner Namens
        if not os.path.exists(logsFolderName): #Erstellen eines neuen Log-Ordners, falls dieser nicht vorhanden ist
            os.makedirs(logsFolderName)
        
        filename = f"{logsFolderName}/ipc-{self.gameName}.txt"
        with open(filename, "w") as file: #"with open" um Datei nicht wieder schließen zu müssen
            pass #pass um Datei "nur" zu erstellen
        return filename #Rückgabe des Dateinamens um ihn im Objekt zu verwenden

    #Methode um Grundkonstrukt einer Log-Zeile zu realisieren
    def log(self, message):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + message + "\n") #Grundkonstrukt einer Log-Zeile + Nachricht

    #Methoden um IPC-Ereignisse zu loggen (selbsterklärend über Namen)
    def logGameCreation(self, spielerId):
        self.log(f"Spiel von {spielerId} erstellt")

    def logAddWord(self, word):
        self.log(f"Wort hinzugefügt: {word}")

    def logConnect(self, spielerId):
        self.log(spielerId + " hat sich mit Spiel verbunden")

    def logRead(self, spielerId):
        self.log(spielerId + " hat aus Shared Memory gelesen")

    def logWrite(self, spielerId):
        self.log(spielerId + " hat in Shared Memory geschrieben")

    def logGameDeletion(self):
        self.log("Shared Memory wurde gelöscht (Spielende)")