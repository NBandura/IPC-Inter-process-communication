import posix_ipc
import mmap

# Shared memory erstellen/öffnen (Wenn es den Namen bereits gibt, wird es geöffnet, sonst erstellt)
shared_memory = posix_ipc.SharedMemory(name="BuzzWordBingo", size=1024,flags=posix_ipc.O_CREAT)


fortfahren=True

while fortfahren:
    #Der letzte Prozess, der sich vom sharedMemory trennt muss den Speicher freigeben
    eingabe=input("SharedMemory lesen (l) oder schreiben (s) Verbindung beenden (b) oder Speicher freigeben(f): ")
    if eingabe=="l":
        # Shared memory lesen
        shared_memory_mmap=mmap.mmap(shared_memory.fd, shared_memory.size,mmap.MAP_SHARED,mmap.PROT_READ)
        text=shared_memory_mmap.read(shared_memory.size)
        text=text.decode()
        shared_memory_mmap.close()
        print("Shared Memory: ", text)
    elif eingabe=="s":
        # Shared memory schreiben
        text=input("Text eingeben: ")
        text=text.encode()
        shared_memory_mmap=mmap.mmap(shared_memory.fd, shared_memory.size,mmap.MAP_SHARED,mmap.PROT_WRITE)
        shared_memory_mmap.write(text)
        shared_memory_mmap.close()
    elif eingabe=="b":
        # Shared memory Verbindung beenden
        shared_memory.unlink()
        fortfahren=False
    elif eingabe=="f":
        # Shared memory freigeben
        shared_memory.close_fd()
        shared_memory.unlink()
        fortfahren=False
    else:
        print("Ungültige Eingabe")