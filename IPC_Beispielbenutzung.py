import IPC
print()
print()
print()
print()


print("Ausgangssituation:")

print("Bingo-Status:", IPC.checkIfBingo())

print("Dateipfad:", IPC.getDateipfad())

print("Größe:", IPC.getGroesse())

print("Wortliste:", IPC.getWortListe())

print("Letztes Wort:", IPC.getLastWort())

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

wortliste = IPC.getWortListe()
print("Methode getWortListe() aufgerufen")
print("Wortliste:", wortliste)
print()

letztes_wort = IPC.getLastWort()
print("Methode getLastWort() aufgerufen")
print("Letztes Wort:", letztes_wort)
print()

print("------------------------------")

print("Darstellung des Speicherinhalts (wird so nicht benutzt, dient nur dem Verständnis):")
print(IPC._read())

print("------------------------------")

IPC.speicherFreigeben()
print("Methode speicherFreigeben() aufgerufen")
