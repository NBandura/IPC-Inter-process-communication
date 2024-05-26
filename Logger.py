import datetime  # Importieren des datetime Moduls zum Erfassen der Zeit
import os  # Importieren des os Moduls, um Dateien zu erstellen und zu verwalten

class Logger:
    
    def __init__(self, playerId):
        self.playerId = playerId
        self.file = self._logCreateFile()

    def _logCreateFile(self):
        logsFolderName = "logs"
        if not os.path.exists(logsFolderName):
            os.makedirs(logsFolderName)
        
        time = datetime.datetime.now()
        filename = time.strftime(f"{logsFolderName}/%Y-%m-%d-%H-%M-%S") + f"-bingo-{self.playerId}.txt"
        with open(filename, "w") as file:
            pass
        return filename

    def logGameStart(self):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Start des Spiels\n")

    def logGameEnd(self):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Ende des Spiels\n")

    def logCrossedWord(self, word, buttonId):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + word + " (crossed) " + buttonId + "\n")

    def logUncrossedWord(self, word, buttonId):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + word + " (uncrossed) " + buttonId + "\n")

    def logBingoOpportunity(self):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Bingo möglich\n")

    def logGameResult(self, result):
        time = datetime.datetime.now()
        with open(self.file, "a") as file:
            if result == 0:
                file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Sieg\n")
            elif result == 1:
                file.write(time.strftime("%Y-%m-%d-%H-%M-%S ") + "Abbruch\n")
