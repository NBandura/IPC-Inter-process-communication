# Buzzword Bingo – IPC praktisch erlernen

## Überblick
Buzzword Bingo wurde im Rahmen des Moduls „Betriebssysteme und Rechnernetze“ im Studiengang Wirtschaftsinformatik entwickelt. Das Projekt demonstriert praxisnah die **Interprozesskommunikation (IPC)** mithilfe von POSIX Shared Memory. Ziel ist es, zu verstehen, wie mehrere Prozesse miteinander synchronisiert und Daten ausgetauscht werden können.

## Projektziel
- **Interprozesskommunikation verstehen:** Erlernen, wie Prozesse über einen gemeinsamen Speicherbereich (Shared Memory) Daten austauschen.
- **Praktische Anwendung:** Umsetzung eines spielerischen Szenarios (Buzzword Bingo), in dem jeder Spieler als eigener Prozess agiert und über IPC miteinander kommuniziert.

## Kernkomponenten der IPC
- **SpielIPC-Klasse:**  
  Diese Klasse übernimmt die Verwaltung der Verbindung zum Shared Memory. Sie ermöglicht das Senden und Empfangen zentraler Spielinformationen wie:
  - Bingo-Status
  - Dateipfad zur Buzzword-Liste
  - Spielfeldgröße und Wörter
- **Shared Memory:**  
  Ein von der POSIX-Bibliothek bereitgestellter, zentraler Speicherbereich, in dem Daten als serialisierte Liste (mittels Pickle in Python) abgelegt und regelmäßig aktualisiert werden.
- **Synchronisation:**  
  Durch kontinuierliches Auslesen und Überschreiben des Shared Memorys wird sichergestellt, dass alle Prozesse stets den aktuellen Spielstand abrufen und darauf reagieren können.

## Technischer Überblick
- **Mechanismus:** POSIX Shared Memory zur Realisierung der IPC
- **Datenübertragung:** Serialisierung von Daten (z. B. mit Pickle in Python)
- **Herausforderungen:**  
  - Gewährleistung der Datenaktualität trotz häufiger Updates  
  - Fehlerbehandlung beim Serialisieren/Deserialisieren  
  - Koordination mehrerer, gleichzeitig agierender Prozesse

## Fazit
Buzzword Bingo bietet einen praxisnahen Einstieg in die Interprozesskommunikation. Durch die Arbeit mit Shared Memory und der Synchronisation mehrerer Prozesse wird ein tiefes Verständnis für IPC-Konzepte und deren Herausforderungen vermittelt.

