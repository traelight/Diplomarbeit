# Diplomarbeit: Atomuhr Genauigkeit 
#
# Name:         Eren Karkin 
# Studiengang:  HF Elektrotechnik 
# Schule:       TEKO Glattbrugg
#
# Headerdatei:   Simulation Atomuhr
# Kurzbeschreib: Dies Stellt den zweit Aufbau der Atomuhr dar
#
# 
#------------------------------------------------------------------------------------------------------
#   Rev 1.0 Eren Karkin 05.10.23 
#-----------------------------------------------------------------------------------------------------

file_path_1 = "data_speicher_atomuhr.txt"                # Benamung der Datei
file_path_2 = "zwischenspeicher_alarmsystem.txt"         # Benamung der Datei 

# Öffne Daten File im Speicher der Atomuhr
with open(file_path_1, 'r') as speicheratomuhr_file:
    # Lese die Daten im Speicher der Atomuhr
    data = speicheratomuhr_file.read()

# Öffne Daten File im Zwischenspeicher des Alarmsystems
with open(file_path_2, 'w') as zwischenspeicher_alarm_file:
    # Schreibe die daten in Zwischenspeicher
    zwischenspeicher_alarm_file.write(data)

#Ausgabe 
print(f'Daten wurden empfangen von {file_path_1} zu {file_path_2}.')

    
        