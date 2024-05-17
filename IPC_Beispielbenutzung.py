import IPC
print()
print()
print()
print()


print("Ausgangssituation:")

print("Bingo-Status:", IPC.checkIfBingo())

print("Dateipfad:", IPC.getDateipfad())

print("Größe:", IPC.getGroesse())

print("------------------------------")

IPC.setDateipfad("Test.txt")
print("Methode setDateipfad('Test.txt') aufgerufen")

IPC.setGroesse(100)
print("Methode setGroesse(100) aufgerufen")

IPC.bingo()
print("Methode bingo() aufgerufen")

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

IPC.beenden()
print("Methode beenden() aufgerufen")
