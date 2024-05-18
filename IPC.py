import posix_ipc
import mmap
import pickle

# Funktion zum Verbinden mit dem Shared Memory
def _connect():
    # Erzeugen des Shared Memory Objekts mit dem Namen "BuzzWordBingo" und einer Größe von 1024 Bytes
    shared_memory = posix_ipc.SharedMemory(name="BuzzWordBingo", size=1024, flags=posix_ipc.O_CREAT)

    try:
        # Erzeugen einer mmap-Instanz, um auf den Shared Memory zuzugreifen
        shared_memory_mmap = mmap.mmap(shared_memory.fd, shared_memory.size, mmap.MAP_SHARED, mmap.PROT_READ)
        # Lesen der Daten aus dem Shared Memory und Umwandeln in eine Liste
        listeAlsCode = shared_memory_mmap.read(shared_memory.size)
        shared_memory_mmap.close()
        speicherListe = pickle.loads(listeAlsCode)
    except pickle.UnpicklingError:
        # Falls ein Fehler beim Entpacken der Daten auftritt, weil ohne keine Liste da ist, wird eine leere Liste erzeugt und in den Shared Memory geschrieben
        listeAlsCode = pickle.dumps(["", "", ""])
        shared_memory_mmap = mmap.mmap(shared_memory.fd, shared_memory.size, mmap.MAP_SHARED, mmap.PROT_WRITE)
        shared_memory_mmap.write(listeAlsCode)
        shared_memory_mmap.close()

    return shared_memory

# Funktion zum Lesen der Daten aus dem Shared Memory
def _read():
    shared_memory = _connect()
    shared_memory_mmap = mmap.mmap(shared_memory.fd, shared_memory.size, mmap.MAP_SHARED, mmap.PROT_READ)
    listeAlsCode = shared_memory_mmap.read(shared_memory.size)
    speicherListe = pickle.loads(listeAlsCode)
    shared_memory_mmap.close()
    return speicherListe

# Funktion zum Schreiben der Daten in den Shared Memory
def _write(speicherListe):
    listeAlsCode = pickle.dumps(speicherListe)
    speicherFreigeben() # Löschen des alten Shared Memory, damit es keine Probleme mit der Serialisierung gibt
    shared_memory = _connect()
    shared_memory_mmap = mmap.mmap(shared_memory.fd, shared_memory.size, mmap.MAP_SHARED, mmap.PROT_WRITE)
    shared_memory_mmap.write(listeAlsCode)
    shared_memory_mmap.close()

# Funktion zum Löschen des Shared Memory
def speicherFreigeben():
    shared_memory = _connect()
    try:
        shared_memory.unlink()
    except posix_ipc.ExistentialError:
        None

# Funktion zum Überprüfen, ob ein Bingo erreicht wurde
def checkIfBingo():
    speicherListe = _read()
    if speicherListe[0] == "Bingo":
        return True
    else:
        return False

# Funktion zum Abrufen des Dateipfads
def getDateipfad():
    speicherListe = _read()
    return speicherListe[1]

# Funktion zum Abrufen der Größe des Spielfeldes
def getGroesse():
    speicherListe = _read()
    return speicherListe[2]

# Funktion zum Setzen des Bingo-Status
def bingo():
    position0 = "Bingo"
    position1 = getDateipfad()
    position2 = getGroesse()
    speicherListe = [position0, position1, position2]
    _write(speicherListe)

# Funktion zum Setzen des Dateipfads
def setDateipfad(dateipfad):
    if checkIfBingo():
        position0 = "Bingo"
    else:
        position0 = ""
    position1 = dateipfad
    position2 = getGroesse()
    speicherListe = [position0, position1, position2]
    _write(speicherListe)

# Funktion zum Setzen der Größe des Spielfeldes
def setGroesse(groesse):
    if checkIfBingo():
        position0 = "Bingo"
    else:
        position0 = ""
    position1 = getDateipfad()
    position2 = groesse
    speicherListe = [position0, position1, position2]
    _write(speicherListe)

# Hauptprogramm
if __name__ == '__main__':
    None
