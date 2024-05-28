from Logger import Logger
from IPCLogger import IPCLogger

spieler1 = Logger(239232)
spieler2 = Logger(4324)

spieler1.logGameStart()
spieler1.logCrossedWord("Test", "2, 2")
spieler1.logUncrossedWord("Test", "2, 2")
spieler1.logBingoOpportunity()
spieler1.logGameEnd()

spiel_logger = IPCLogger("TestSpiel")

spiel_logger.logGameCreation("Spieler1")
spiel_logger.logAddWord("Wort1")
spiel_logger.logConnect("Spieler2")
spiel_logger.logRead("Spieler3")
spiel_logger.logWrite("Spieler4")
spiel_logger.logGameDeletion()