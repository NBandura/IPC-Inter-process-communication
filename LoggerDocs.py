#Logger Modul aus Logger.py Datei importieren
from Logger import Logger 

#Initialisieren eines Loggers für Spieler über SpielerId und erstellen einer neuen Log-Datei
logger = Logger(12345)

#Spielstart in Log-Datei schreiben
logger.logGameStart()

#Spielende in Log-Datei schreiben
logger.logGameEnd()

#Spielausgang für konkreten Spieler in Log-Datei schreiben; (0) = Sieg, (1) = Abbruch
logger.logGameResult(1)

#Angekreuztes Wort in Log-Datei schreiben, x(1) und y(2) um Koordinaten zu übergeben
logger.logWord("Testwort", "button_1_2")