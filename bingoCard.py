from asciimatics.exceptions import StopApplication  
from asciimatics.screen import Screen 
from asciimatics.exceptions import ResizeScreenError 
from asciimatics.event import KeyboardEvent, MouseEvent  
from tkinter import Tk  
from tkinter.filedialog import askopenfilename  
import random 
import argparse  
import time  

def read_words():
    Tk().withdraw()  # Verhindert das Anzeigen eines leeren Tkinter-Fensters
    filename = askopenfilename()  # Zeigt einen Dateiauswahldialog an
    with open(filename, 'r') as file:  # Öffnet die ausgewählte Datei zum Lesen
        words = file.read().splitlines()  # Liest die Wörter aus der Datei | splitlines() trennt die Wörter an den Zeilenumbrüchen
    return words  # Gibt die Liste der Wörter zurück

def create_bingo_board(words, size):
    random.shuffle(words)  # Mischen Sie die Wörter in zufälliger Reihenfolge
    return [words[i*size:i*size+size] for i in range(size)]  # Erstellt das Bingo-Brett mit unserer Struktur für die Wörter und gibt es zurück

def draw_board(screen, board, max_word_length):
    for i, row in enumerate(board):  # Geht durch jede Zeile des Bretts
        for j, word in enumerate(row):  # Geht durch jedes Wort in der Zeile
            screen.print_at('|' + word.center(max_word_length) + '|', j*(max_word_length+4), i*3)  # Zeichnet das Wort auf dem Bildschirm | j = Spaltennummer | i = Zeilennummer
            screen.print_at('-'*(len(board[0])*(max_word_length+3)), 0, i*3+1) # Zeichnet eine Trennlinie auf dem Bildschirm
    screen.refresh()  # Aktualisiert den Bildschirm

def cross_out_word(board, word):
    for i, row in enumerate(board):  # Geht durch jede Zeile des Bretts
        for j, cell in enumerate(row):  # Geht durch jedes Wort in der Zeile
            if cell.strip() == word:  # Wenn das Wort in der Zelle dem ausgewählten Wort entspricht
                board[i][j] = ' X '  # Kreuzt das Wort aus

def check_bingo(board):
    # Prüft jede Zeile
    for row in board:
        if all(cell == ' X ' for cell in row):
            return True
    # Prüft jede Spalte
    for col in zip(*board):
        if all(cell == ' X ' for cell in col):
            return True
    # Prüft die Hauptdiagonale (nur für quadratische Bretter)
    if len(board) == len(board[0]) and all(board[i][i] == ' X ' for i in range(len(board))):
        return True
    # Prüft die Nebendiagonale (nur für quadratische Bretter)
    if len(board) == len(board[0]) and all(board[i][len(board)-i-1] == ' X ' for i in range(len(board))):
        return True
    return False

def validate_words(words, size, screen):
    if len(words) < size * size:  # Wenn es nicht genug Wörter gibt, um das Brett zu füllen
        screen.print_at("Es sind nicht genug Wörter vorhanden, um ein Brett dieser Größe zu erstellen.", 0, 0)  # Gibt eine Fehlermeldung aus
        screen.refresh()  # Aktualisiert den Bildschirm
        time.sleep(5)  # Wartet 5 Sekunden
        return False  # Gibt False zurück, wenn nicht genug Wörter vorhanden sind
    if size < 3:  # Wenn die Dimensionen des Bretts zu klein sind
        screen.print_at("Die Dimensionen des Bretts sind zu klein. Mindestgröße ist 3x3.", 0, 0)  # Gibt eine Fehlermeldung aus
        screen.refresh()  # Aktualisiert den Bildschirm
        time.sleep(5)  # Wartet 5 Sekunden
        return False  # Gibt False zurück, wenn die Dimensionen des Bretts zu klein sind
    return True  # Gibt True zurück, wenn genug Wörter vorhanden sind und die Dimensionen des Bretts gültig sind


def handle_event(event, screen, board, max_word_length):
    if isinstance(event, KeyboardEvent):  # Wenn das Ereignis eine Tastatureingabe ist
        if event.key_code == ord('q'):  # Wenn die 'q'-Taste gedrückt wurde
            raise StopApplication("Spiel beendet")  # Beendet das Spiel
        # mit Tasten kann man nur Q zum beenden drücken sonst geht alles nur mit der maus
    elif isinstance(event, MouseEvent):  # Wenn das Ereignis eine Mausaktion ist
        if event.buttons == MouseEvent.LEFT_CLICK:  # Wenn die linke Maustaste geklickt wurde
            x = event.x // (max_word_length + 4)  # Berechnet die x-Position des geklickten Wortes
            y = event.y // 3  # Berechnet die y-Position des geklickten Wortes
            if 0 <= x < len(board[0]) and 0 <= y < len(board):  # Wenn die geklickte Position innerhalb des Bretts liegt
                board[y][x] = ' X '  # Markiert das Wort als ausgewählt
                draw_board(screen, board, max_word_length)  # Zeichnet das Brett erneut
                if check_bingo(board):  # Überprüft, ob ein Bingo erreicht wurde
                    screen.print_at("Bingo erreicht!", 0, len(board)*3+1)  # Gibt eine Nachricht aus
                    screen.refresh()  # Aktualisiert den Bildschirm
                    
                   

def main(screen,size):
    words = read_words()  # Liest die Wörter aus der Datei
    if not validate_words(words, size, screen):  # Überprüft, ob genug Wörter vorhanden sind
        return  # Beendet die Funktion
    bingo_board = create_bingo_board(words, size)  # Erstellt das Bingo-Brett
    max_word_length = max(len(word) for row in bingo_board for word in row)  # Findet die Länge des längsten Wortes | ausbauen dort wird das Board angepasst an die länge des längsten wortes
    draw_board(screen, bingo_board, max_word_length)  # Zeichnet das Brett auf dem Bildschirm
    while True:  # Startet eine Endlosschleife
        event = screen.get_event()  # Holt das nächste Ereignis
        if event is None:  # Wenn es kein Ereignis gibt
            continue  # Geht zur nächsten Iteration der Schleife
        handle_event(event, screen, bingo_board, max_word_length)  # Verarbeitet das Ereignis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bingo-Spiel.')  # Erstellt einen ArgumentParser
    parser.add_argument('-s', '--size', type=int, required=True, help='Die Größe des Bingobretts.')  # Fügt ein Argument für die Größe hinzu
    args = parser.parse_args()  # Verarbeitet die Befehlszeilenargumente
    try:
        Screen.wrapper(main, arguments=(args.size,))  # Startet das Spiel
    except ResizeScreenError:  # Wenn ein ResizeScreenError auftritt
        pass  # Ignoriert den Fehler


    # funktion mit dem Joker bei größeren feldern 
    # clean machen 
    # das man mit den pfeil Tasten auswählen kann muss noch realisiert werden. Bis jetzt geht nur maus und q zum beenden
    # Bingo board falsch man was flasch ankreuzt das rückgängig machen kann
    # Bingoboard abgehakte Wörter anders darstellen

    # Hier ist jetzt schon in der Main ein beispiel zum direkt ausführen. Wir müssen natürlich eine weiter eigen Klasse bingo Game noch erstellen die dann imm er auf BingoCard zugreifen kann.
    # Außerdem sollten wir nochmal schauen ob wir das so machen wollen, wie in Line 117 beschrieben wird. Also wie Baun uns das Auf dem Blatt gegeben hat, oder ob wir das auch in Asciimatics und die art GUI einbauen wollen.

    # python bingoCard.py -s 4 bzw. python bingoCard.py -s ' ' startet das Programm im Terminal
    # module installieren: pip install asciimatics | alles andere sollte schon in der Base von Anaconda vorhanden sein

    # Also erst asciimatics instalieren und dann bingoCard.py ausführen mit line 117 und dann könnt ihr die einzelenen Felder anklicken und es wird ein X reingeschrieben.
    # Ist eine reihe voll steht unten dann Bingo erreicht.
    # Unser erster BingoBoard - Teil mit dem wir dann soweit weiter arbeiten können.