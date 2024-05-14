import random
felder = []
dateipfad = '/Users/jandillemuth/Documents/buzzwörter.txt'
buzzword_Wörter = []
#Methode für Bingo Feld erstellen
def bingofeldeerErstellen(matrix):
    benutze_Woerter = []
    bingo_felder = []  # Liste zum Speichern der Bingo-Felder
    for row in matrix:
        temp_row = []  # Liste für die aktuelle Zeile der Bingo-Felder
        for element in row:
            if element == "frei":
                temp_row.append("")  # leeres Element für freies Feld
            else:
                while True:
                    random_word = random.choice(buzzword_Wörter)
                    if random_word not in benutze_Woerter:
                        benutze_Woerter.append(random_word)
                        temp_row.append(random_word)  # zufälliges Wort
                        break
        bingo_felder.append(temp_row)  
    return bingo_felder  


       
       
# Methode für die markierung            
def markieren():
     wort_haben = input("Falls sie das Wort nicht haben drücken sie s (skippen)")
     while True: #falls falsche Eingabe mehrer Versuchte
        if wort_haben == "s": 
            print("Sie haben geskippt")
            break
        feldX = int(input("Geben sie hier die Spalte an: "))
        feldY = int(input("Geben sie hier die Riehe an: "))
        if felder[i][feldX-1][feldY-1] == tem: # überschreibung des Feldes bei einem Treffer durch ein x
            felder[i][feldX-1][feldY-1] = "x"
            print(matrix_ausgeben(felder[i]))
            break
        else: 
            wort_haben = input("Sind sie sich sicher, dass sie das Wort haben? Falls nicht drücken sie s")


#Methode um Matrizen auszugeben
def matrix_ausgeben(bingo_Felder):
     for row in bingo_Felder:
        for word in row:
            print("\t" + word.ljust(20), end=" ")  # Formatieren so das es gut aussieht 
        print() #" ".ljust(15)

#den Spieler entsprechend die Spielfelder erstellen 
def spieler_abfrage(): 
    for i in range(anzahlSpieler):
        print("Spieler", i+1)
        spielerfeld = bingofeldeerErstellen(matrix)
        felder.append(spielerfeld)
        matrix_ausgeben(spielerfeld)
    





# Datei öffnen und Zeilen in die Liste speichern
with open(dateipfad, 'r') as file:
    buzzword_Wörter = [zeile.strip() for zeile in file]



# matrix wird erstellt
matrix = [
    ['', '', ''],
    ['' , "frei", ''],
    ['', '', '']
]                            
                            
        
#Anzahl der Spieler abfragen      
while True:
    anzahlSpieler = input("Bitte geben Sie die Anzahl der Spieler ein: ")
    try:
        anzahlSpieler = int(anzahlSpieler)
        print("Die eingegebene Zahl ist:", anzahlSpieler)
        break  
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")


spieler_abfrage()
#5 mal durchführen des Markierens
for i in range(5):
    tem = random.choice(buzzword_Wörter) # hier wird das wort der Rudne angezeigt 
    for i in range(anzahlSpieler): # spielablauf sp das jeder in jeder Runde dran kommt
        print(f"Spieler: ", i+1 , "\nHier ist das Wort der Runde: ", tem.upper(), "\nHier ist ihr Bingofeld:\n ")
        print(matrix_ausgeben(felder[i]))
        markieren()
   
   




#Das vorgegbene Wort zum Streichen wird bis jetzt leider nur einmal am Rundenanfang angezigt, methoden implementieren die die große in kleinere aufteillen 