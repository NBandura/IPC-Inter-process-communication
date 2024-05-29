from IPC import SpielIPC
print()
print()
print()
print()
spielname="test"
IPC=SpielIPC(spielname)
print("Mit Spiel "+spielname+" verbunden")

print("Ausgangssituation:")

print("Bingo-Status:", IPC.checkIfBingo())

print("Dateipfad:", IPC.getDateipfad())

print("Größe:", IPC.getGroesse())

print("Wortliste:", IPC.getWortString())

print("Letztes Wort:", IPC.getLastWort())

print("Start-Status:", IPC.checkIfStarted())

print("------------------------------")

IPC.setDateipfad("Test.txt")
print("Methode setDateipfad('Test.txt') aufgerufen")

IPC.setGroesse(100)
print("Methode setGroesse(100) aufgerufen")

IPC.bingo()
print("Methode bingo() aufgerufen")

IPC.addWord("Testwort")
print("Methode addWort('Testwort') aufgerufen")
IPC.addWord("Testwort2")
print("Methode addWort('Testwort2') aufgerufen")

IPC.startGame()
print("Methode startGame() aufgerufen")

print("------------------------------")

bingo_status = IPC.checkIfBingo()
print("Methode checkIfBingo() aufgerufen: Rückgabewert ist boolenischer Wert")
print("Bingo-Status:", bingo_status)
print()

dateipfad = IPC.getDateipfad()
print("Methode getDateipfad() aufgerufen")
print("Dateipfad:", dateipfad)
print()

groesse = IPC.getGroesse()
print("Methode getGroesse() aufgerufen")
print("Größe:", groesse)
print()

wortliste = IPC.getWortString()
print("Methode getWortListe() aufgerufen")
print("Wortliste:", wortliste)
print()

letztes_wort = IPC.getLastWort()
print("Methode getLastWort() aufgerufen")
print("Letztes Wort:", letztes_wort)
print()

start_status = IPC.checkIfStarted()
print("Methode checkIfStarted() aufgerufen: Rückgabewert ist boolenischer Wert")
print("Start-Status:", start_status)
print()

print("------------------------------")

print("Darstellung des Speicherinhalts (wird so nicht benutzt, dient nur dem Verständnis):")
print(IPC._read())

print("------------------------------")

IPC.speicherFreigeben()
print("Methode speicherFreigeben() aufgerufen")
