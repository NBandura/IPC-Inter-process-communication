import datetime  #Importieren des datetime Moduls zum Erfassen der Zeit
import os  #Importieren des os Moduls, um Dateien zu erstellen und zu verwalten

class IPCLogger:
    
    def __init__(self, gameName):
        self.gameName = gameName
        self.file = self._logCreateFile()

    def _logCreateFile(self): 
        logsFolderName = "ipc_logs"
        if not os.path.exists(logsFolderName):
            os.makedirs(logsFolderName)
        
        time = datetime.datetime.now()
        filename = time.strftime(f"{logsFolderName}/%Y-%m-%d-%H-%M-%S") + f"-ipc-{self.gameName}.txt"
        with open(filename, "w") as file:
            pass
        return filename

    def log(self, message):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + message + "\n")

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