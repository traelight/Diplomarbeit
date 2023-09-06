# Diplomarbeit: Atomuhr Genauigkeit 
#
# Name:         Eren Karkin 
# Studiengang:  HF Elektrotechnik 
# Schule:       TEKO Glattbrugg
#
# Headerdatei:   Calculation Data 
# Kurzbeschreib: Umwandlung von HEX Daten in Stringformat zu 64 Bit Double Float
#                + Berechnung/ Vergleich Funktion der Abweichung + Warn Mail Funktion 
#
# Hilfe Links:
#       Erste Variante, ohne Erfolg.
#           https://stackoverflow.com/questions/38831808/reading-hex-to-double-precision-float-python
#           https://blog.finxter.com/python-hex-to-float-conversion/ python hex to float
#           https://docs.python.org/3/library/struct.html#struct-format-strings struct functions  
#       INFOS über 'double float precision 64Bit' Zahlen           
#           https://de.wikipedia.org/wiki/IEEE_754  
#
# Code Referenzen: 
#   1  - send_email_alert: https://docs.python.org/3/library/email.examples.html
#----------------------------------------------------------------------------------------------------------
#   Rev 1.0  Eren Karkin 6.09.23
#----------------------------------------------------------------------------------------------------------
# Python Library Imports
import math
import struct 
# Py Mail Library Imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#-------------------------#Email Funktionen#----------------------------------------------------------------

# Email Konfiguration (Code Referenz 1)
sender_email = 'raspitesto@gmail.com'
sender_password = 'Raspi_testo_123'
receiver_email = 'erenkarkin210300@gmail.com'
subject = 'Warnmeldung: Atomuhr Genauigkeit'
message_text = 'Die Atomuhr Genauigkeit ist nicht mehr gewährleistet. Keine Kalibration durchführen. \n Dies ist ein automatisch generierte Mail des Raspis'

# Email versenden Funktion (Code Referenz 1)
def send_email_alert():
    try:
        # Mail Format generierung
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_text, 'plain'))

        # SMTP Server Konfiguration (Gmail)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Verbindung zu SMTP Server

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(" Warn-Email wurde an Laborleiter versandt ")

    except Exception as e:
        print(f"Es gab ein Error: {str(e)}")

    finally:
        # Schliesse SMTP Server
        server.quit()

#-------------------------#Berechnung Funktion#--------------------------------------------------------------------
# Toleranz definition
Toleranz = float(2.9e-14)
negativToleranz = float(-2.9e-14)

def check_atomuhr_accuracy (input_hex):
    final_value = float (struct.unpack('<d', bytes.fromhex(input_hex))[0])  # Umwandlung von string auf bytes + Verarbeitung/Speicherung des double float Wert für Berechnung
    print(final_value)
    
    #Berechnung/Vergleich von Toleranz und Abweichung
    if  final_value > 0: # positive Abweichung
        if Toleranz >= final_value:                                # Wenn Toleranz grössergleich Abweichung ist = gut
            return 'Atomuhr Genauigkeit ist gewährleistet'
        else:
            send_email_alert()                  # Warn Mail Sendung
            return 'Atomuhr Genauigkeit ist NICHT gewährleistet. Keine Kalibration durchführen !'
    elif final_value < 0: #negative Abweichung
        if negativToleranz <= final_value:                          # Wenn Toleranz kleinergleich Abweichung ist = gut/umgekehrt wegen negativabfrage
            return 'Atomuhr Genauigkeit ist gewährleistet'
        else:
            send_email_alert()                  # Warn Mail Sendung
            return 'Atomuhr Genauigkeit ist NICHT gewährleistet. Keine Kalibration durchführen!'
    else:
        return ('Berechnung fehlgeschlagen')



