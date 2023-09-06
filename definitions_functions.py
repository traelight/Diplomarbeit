# Diplomarbeit: Atomuhr Genauigkeit 
#
# Name:         Eren Karkin 
# Studiengang:  HF Elektrotechnik 
# Schule:       TEKO Glattbrugg
#
# Headerdatei:   Definitiones / Functions
# Kurzbeschreib: Hier werden die grundsätzlichen/gebräuchlichsten Definitionen und 
#                Funktionen definiert und deklariert
#
# Hilfe Links: 
#   Serial Verbindung
#   https://www.tutorialspoint.com/how-do-i-access-the-serial-rs232-port-in-python
#   
#   Website die das 1Byte problem gelöst hat Fehler Output war nur b'\n' sichtbar
#   https://devtut.github.io/python/python-serial-communication-pyserial.html#read-from-serial-port
#
# Code Referenzen: 
#   1 - Countdown_timer: https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
#   2 - Read_serial:     https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
#------------------------------------------------------------------------------------------------------
#   Rev 1.0 Eren Karkin 6.09.23 
#-----------------------------------------------------------------------------------------------------
# Python Library Imports
import time 
import serial 
import struct

# Alle Befehlssätze der 'GPS View' Software
command_opt = bytearray([0x2A, 0x6F, 0x70, 0x74, 0x3F, 0x0A]) #command --> *opt?\n
command_idn = bytearray([0x2A, 0x69, 0x64, 0x6E, 0x3F, 0x0A]) #command --> *idn?\n in bytes (hexformat)
#command --> Archiv Daten (24h)
command_24h = bytearray([0x74, 0x72, 0x61, 0x63, 0x3A,0x61,0x72,0x63,0x32,0x34,0x68,0x3F,0x20,0x63,0x68,0x31,0x0A])
# command --> Täglich Daten (1h)
command_1h  = bytearray([0x74, 0x72, 0x61, 0x63, 0x3A,0x64,0x65,0x76,0x31,0x68,0x3F,0x20,0x63,0x68,0x31,0x0A]) 
# command --> Phasenabweichung 
command_phasedevation = bytearray([0x74, 0x72, 0x61, 0x63, 0x3F,0x20,0x63,0x68,0x31,0x0A])

#--------------------------#Definition#------------------------------------------------------------------

file_path = "data_test.txt"         # Benamung der Datei für die Daten
target_character = "0a0a"           # Schlusszeichen Versenden der Daten
out = ''                            # Variabel der Ausgabe der Daten

#-------------------------#Funktionen#--------------------------------------------------------------------

# Countdown Timer (Referenz 1.0)
def countdown_timer(seconds):
    while seconds:                 # Solange 'seconds' übrig sind
        mins, secs = divmod(seconds, 60)        #
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f'Nächste Aktualisierung in:', timeformat, end='\r' ) # ohne (end='\r') schreibt er immer wieder neue Zeile standard = \n
        time.sleep(1)
        seconds -= 1
  
    print("\nTimer complete!")

# Suchfunktion der Daten in der Speicherdatei
def find_and_write_target(input_file, target):      # Funktion um letzte Daten zu extrahieren
    with open(input_file, 'r') as file:
        text = file.read()

    index = text.find(target)

    if index == -1:                             
        print(f"Charakter '{target}' im Text nicht gefunden.")
        return

    start_index = index - 40                        # 40 Charakter vor dem Endzeichnen wird gelesen
    end_index = start_index + 16

    if end_index > len(text):                       # Ausgabe nur in 16 Charakter 
        end_index = len(text)

    extracted_text = text[start_index:end_index]
    return extracted_text                           # Ausgabe in Hex

# Suchfunktion des Schlusszeichen    
def check_for_character(file_path, target_character):       # Funktion Überprüfung von spezifischen Charakter
    with open(file_path, "r") as file:                # öffne Speicherdatei 
        for line in file:                             # suche bis Schlusszeichen gefunden wird 
            if target_character in line:
                return True
    return False

# Schnittstellen verbinden und auslesen Funktion (Ausgabe in HEX) 
# (Referenz 2)                
def read_serial(ser): 
    global out  
    ser.write(command_24h)             # Befehl senden
    time.sleep(1.0)
    while ser.inWaiting() > 0:         # Solange Daten Empfangen bis nichts mehr gesendet wird
        out = ser.read(ser.inWaiting()).hex() 
    return out  
# muss hex konvertiert werden sonst ausgabe in bytes = anderes Format