import tkinter as tk
from tkinter import filedialog

def einlesen():
    #Auswählen der Datei
    print("-----------------------------------------")
    print("Bitte wählen Sie die Datei mit den BuzzWords aus.")
    print("-----------------------------------------")
    dateipfad=filedialog.askopenfilename()
        
    #Lesen, speichern der Datei und TryCatch falls Pfad ungültig
    try:
        with open (dateipfad,"r") as buzzWordDatei:
            inhaltString = buzzWordDatei.read()
        BuzzWordsArray=inhaltString.split(",")
    except Exception:
        BuzzWordsArray=["Ungültige BuzzWordDatei"]

    #Zurückgeben
    return BuzzWordsArray