import tkinter as tk
from tkinter import filedialog

class buzzWordsEinlesenMethoden:

    @staticmethod
    def einlesen():
        #Auswählen der Datei
        print("-----------------------------------------")
        print("Bitte wählen Sie die Datei mit den BuzzWords aus.")
        print("-----------------------------------------")
        dateipfad=filedialog.askopenfilename()
        
        #Lesen der Datei und speichern
        with open (dateipfad,"r") as buzzWordDatei:
             inhaltString = buzzWordDatei.read()
        BuzzWordsArray=inhaltString.split(",")

        #Zurückgeben
        return BuzzWordsArray

       