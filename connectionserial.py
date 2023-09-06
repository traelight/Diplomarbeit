# Diplomarbeit: Atomuhr Genauigkeit 
#
# Name:         Eren Karkin 
# Studiengang:  HF Elektrotechnik 
# Schule:       TEKO Glattbrugg
#
# Hauptprogramm: Connection Serial 
# Kurzbeschreib: Das Programm verbindet sich mit der zugewiesenen Schnittstelle und 
#                empfängt die Frequenzabweichungs-Daten der Atomuhr. Schliesslich findet 
#                eine Berechnung/Vergleich statt ob die Abweichung zur Hersteller Toleranz 
#                innerhalb ist und die Genauigkeit noch gewährleistet wird.  
#
# Hilfe Links: 
#   Website von File handling python 
#   https://www.w3schools.com/python/python_file_handling.asp
#   PySerial Definition: 
#   https://pyserial.readthedocs.io/en/latest/pyserial_api.html
#------------------------------------------------------------------------------------------------------
#   Rev 1.0 Eren Karkin 6.09.23 
#       - OHNE GUI
#------------------------------------------------------------------------------------------------------
# Python Library Imports
import time 
import serial 
import struct

# Header Files Imports
from calculationdata import check_atomuhr_accuracy
from definitions_functions import *

 # Serielle Einstellungen
ser = serial.Serial(       
   port='COM1',
   baudrate=9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
)

#-----------------------------Main---------------------------------------------------------------------
while True:  # Endlosschleife
    
    data = read_serial(ser)                               # Einlesen der Daten 
    found = check_for_character(file_path, target_character)    # Schlusszeichen'0a0a' bzw. '\n\n' suchen
    
    if data != '':                                        # Solange Daten gesendet werden 
        if found:                                         # Wenn Alle Daten empfangen wurden 
            print(f"Character '{target_character}' wurde gefunden in der Datei.")
       
            hex_data = str (find_and_write_target(file_path, target_character))    # Konvertierung in String für Umrechnung in Double Float  
            print(hex_data)          
            result = check_atomuhr_accuracy(hex_data)     # Berechnung ob Abweichung innerhalb Toleranz ist             
            print(result)
            
            countdown_timer(10)           # 10 Sec Aktualisierungszeit
        
        else:
            print(f"Character '{target_character}' noch nicht gefunden in der Datei.")
            f = open("data_test.txt", "a")                  # öffne Datei, falls es nicht gibt, kreiren der Datei 
            f.write(data)                                   # Schreibe in Datei
            f.close()                                       # Schliesse Datei
                                            
                
            