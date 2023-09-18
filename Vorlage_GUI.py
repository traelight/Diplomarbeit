# Diplomarbeit: Atomuhr Genauigkeit 
#
# Name:         Eren Karkin 
# Studiengang:  HF Elektrotechnik 
# Schule:       TEKO Glattbrugg
#
# Programm:      Vorlage_GUI.py
# Kurzbeschreib: Eine Vorlage der Atomuhr Genauigkeits GUI (Graphic User Interface). 
#                Ein GUI ermöglicht den Nutzer das Programm verständlicher darzustellen und zu nutzen.
#                Das programmierte GUI beinhaltet: Neue/ Alte Daten Erkennung, Anzeige der jetztigen Abweichung,
#                Statusanzeige (Grün/Rot) der Genauigkeit und die nächste Aktualiserungszeit der Daten  
#
# Hilfe Links: 
#   Video Beginner PyQt5- Fenster generieren, Label, Buttons etc. 
#   https://www.youtube.com/watch?v=MOItX2aKTGc
#
#   PyQt5 Designer Tutorial: 
#   https://www.tutorialspoint.com/pyqt5/pyqt5_using_qt_designer.htm
#
#   Pyqt5 CountdownTimer Code Examples
#   https://stackoverflow.com/questions/40994187/pyqt-showing-countdown-timer
#   https://pythonpyqt.com/qtimer/  
#  
#   PyQt5 PopUp Fenster -QMessagebox
#   https://www.youtube.com/watch?v=GkgMTyiLtWk
#------------------------------------------------------------------------------------------------------
#   Rev 1.0 Eren Karkin 09.09.23 
#       - MIT GUI
#   Rev 1.1 Eren Karkin 09.09.23 
#        - Mail Versand Erkennung - Variable Mailstatus + Email PopUp Fenster hinzugefügt
#        - Vor Beginn des Countdown, Daten initialisieren
#   Rev 1.2 Eren Karkin 13.09.23 
#           - Log Editor
#------------------------------------------------------------------------------------------------------

# PyQt5 Library Imports
from threading import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *

# HeaderFile Imports
from calculationdata_GUI import *
from definitions_functions_GUI import *



# Config der Seriellenschnittstelle
 # Serielle Einstellungen
ser = serial.Serial(       
   port='COM1',
   baudrate=9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
)


#--------------------- Einlesen der Daten Funktion ---------------------
def read_data(): 
    data = read_serial(ser)                               # Einlesen der Daten 
    global found
    found = check_for_character(file_path, target_character)    # Schlusszeichen'0a0a' bzw. '\n\n' suchen
    
    if data != '':                                        # Solange Daten gesendet werden 
        if found:                                         # Wenn Alle Daten empfangen wurden 
            
            #print(f"Character '{target_character}' wurde gefunden in der Datei.")
            hex_data = str (find_and_write_target(file_path, target_character))    # Konvertierung in String für Umrechnung in Double Float  
            print(hex_data)          
                        
            global float_value          
            float_value = check_atomuhr_accuracy (hex_data)         #  double float Zahl (Abweichung) wird exportiert
            global  old_float_value                                 
            old_float_value = float_value                           #  vorherige double float Zahl wird gespeichert

            global result 
            global Mailstatus   
            result = check_status(float_value)                      #  double float Zahl (Abweichung) wird verglichen mit Toleranz ob nicht erfüllt/erfüllt 
            if result != False:
                Mailstatus = False
            else:
                Mailstatus = True
        
            print(result)
    
        else:
            print(f"Character '{target_character}' noch nicht gefunden in der Datei.")
            f = open("data_test.txt", "a")                  # öffne Datei, falls es nicht gibt, kreiren der Datei 
            f.write(data)                                   # Schreibe in Datei
            f.close()                                       # Schliesse Datei    
    return result


#--------------------------------- Hauptfenster Klasse-----------------------------------
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 160, 421, 151))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        #---------Jetztige Frequenzabweichung label-----------------------
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label)
        #--------- ------- Data label -------------------------------------
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 350, 661, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        #-------------Nächste Aktualisierung label-------------------------
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        #--------------Status Atomuhr Genauigkeit label--------------------
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        #--------------Titel Atomuhr Genauigkeit label---------------------
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 431, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        #--------------Mittige Design Linie ------------------------------
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 330, 771, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        #--------------Titel Design Linie ------------------------------
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setGeometry(QtCore.QRect(10, 50, 771, 16))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        #--------------Keine neuen Daten wurden erkannt label-------------
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(50, 40, 551, 131))     #(50, 40, 351, 41)) 
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)    
        
        #----------------LOG Text Editor -----------------------------
        
        #Titel Schreibstil
        self.textEditTitel = QtWidgets.QLabel(self.centralwidget)
        self.textEditTitel.setGeometry(QtCore.QRect(550, 30, 100, 100))   
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        self.textEditTitel.setFont(font)
        self.textEditTitel.setObjectName("textEditTitel")
        #-------- Generierung des QTextedit Box---------
        MainWindow.setCentralWidget(self.centralwidget)  
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(550, 95, 200, 200))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.textEdit.setStyleSheet ("background-color: lightgray;")  #("background-color: rgba(0, 0, 0, 0);")
        #Inhalt Schreibstil
        self.textEdit.setReadOnly(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.textEdit.setFont(font)
        
        #----------------INFO BAR Menüleiste -----------------------------
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuInfo = QtWidgets.QMenu(self.menubar)
        self.menuInfo.setObjectName("menuInfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionMade_by = QtWidgets.QAction(MainWindow)
        self.actionMade_by.setObjectName("actionMade_by")
        self.menuInfo.addAction(self.actionMade_by)
        self.menubar.addAction(self.menuInfo.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #------------ Create a label for the LED------------------
        self.led_label = QtWidgets.QLabel(self.centralwidget)
        self.led_label.setGeometry(QtCore.QRect(500, 370, 100, 50))  # Adjust the position and size as needed
        self.led_label.setAutoFillBackground(True)
        self.set_led_color(False)  # Set the initial color to red (False)
    
        #----------- Create a label for the countdown timer--------
        self.countdown_label = QtWidgets.QLabel(self.centralwidget)
        self.countdown_label.setGeometry(QtCore.QRect(390, 470, 300, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        self.countdown_label.setFont(font)
        self.countdown_label.setObjectName("countdown_label")
        self.countdown_label.setAlignment(QtCore.Qt.AlignCenter)  # Center align the text
      
        # Generiere den Countdown Timer mit dem QTimer Modul
        self.countdown_timer = QTimer(MainWindow)
        self.countdown_timer.timeout.connect(self.update_countdown) # Binde den Countdown Timer mit der "update_countdown" Funktion
        # Initialisiere Dauer in Sekunden (Bei Änderung: Hier und in der Funktion [Reset Countdown Dauer] )
        self.countdown_duration = 10
       
        self.start_countdown()
        
        
    
   #------------------START Nachricht für Logging der Abweichung FUNKTION--------------------------
    def add_message(self):                  
        current_datetime = QtCore.QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")
        message = f"----------------------------\n{formatted_datetime}: Abweichung ausserhalb: {str(float_value)}"  
        self.textEdit.append(message)
        
          
    #------------------START LED FUNKTION--------------------------
        # Generiere Funktion die LED 
    def set_led_color(self, is_active):
        if is_active:                                               # Wenn Abweichung innerhalb setze LED(pallete) auf Grün/ Rot
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 255, 0))  # Grün
            #self.label_status.setText("Status - Erfüllt")
            self.led_label.setPalette(palette)

        else:
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0))  # Rot
            #self.label_status.setText("Status: Nicht Erfüllt")
            self.led_label.setPalette(palette)
    #----------------- END LED FUNKTION-----------------------------
       
    #-----------------START COUNTDOWN TIMER FUNKTION----------------
    def start_countdown(self):
        self.countdown_timer.start(1000)  # Sekunden Takt [in ms]

    def update_countdown(self):
        if self.countdown_duration >= 0:                         # Countdown Timer
            mins, secs = divmod(self.countdown_duration, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)      # Countdown Timer Format
            self.countdown_label.setText(f"{timeformat}")
            self.countdown_duration -= 1
        else:
            self.countdown_timer.stop()                          # Countdown Timer Stop                     
            self.countdown_label.setText(" Daten neu lesen ")
            read_data()                                          # Daten neu lesen
            if found:                                            # Sobald alle Daten gelesen wurden vergleiche ob es neue Daten gibt und
                if float_value != old_float_value:
                    self.label_7.setText((" Neuen Daten wurden erkannt "))
                    self.label_7.setStyleSheet("color: blue;")
                    ui.set_led_color(result)                     # LED Farbe ändern bei result innerhalb = True --> Grün andern falls Rot
                    if result == False:                           #FALSE TESTZWECKE-->TRUE   # Loggen der Abweichung 
                        self.add_message()
                    if Mailstatus == False:                       # Warnmeldung Pop Up Fenster öffnen
                        self.show_popup()   
                        
                else: 
                    self.label_7.setText((" Keine neuen Daten wurden erkannt "))
                    self.label_7.setStyleSheet("color: red;")
                    ui.set_led_color(result)      
                    if result == True: #FALSE TESTZWECKE-->TRUE  # Loggen der Abweichung 
                        self.add_message()
                    if Mailstatus == True:                       # Warnmeldung Pop Up Fenster öffnen
                        self.show_popup()  
                        
                self.label_2.setText(str(float_value))           # Anzeige der jetztige Abweichung
                self.countdown_duration = 10  # Reset Countdown Dauer 
                self.countdown_timer.start(1000)  # Wiederhole Countdown Timer
            else:
                read_data()
                self.countdown_label.setText(" Daten werden neu gelesen ")         
                time.sleep(5)
                
                
    #----------------- END COUNTDOWN TIMER FUNKTION-----------------
        
    def retranslateUi(self, MainWindow):
        #----------- Alle Titel-------------
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Jetztige Frequenzabweichung:"))
        self.label_4.setText(_translate("MainWindow", "Nächste Aktualisierung: "))
        self.label_3.setText(_translate("MainWindow", "Status Atomuhr Genauigkeit: "))
        self.textEditTitel.setText(_translate("MainWindow", "Log Editor: "))
        #------------------
        self.label_5.setText(_translate("MainWindow", "Atomuhr Genauigkeit"))
        #------------------
        self.menuInfo.setTitle(_translate("MainWindow", "Info"))
        self.actionMade_by.setText(_translate("MainWindow", "Made by Eren Karkin"))
    
    #-----------------START POP UP FENSTER FUNKTION----------------
    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle ("Warnmeldung Mail")
        msg.setText (" Atomuhr Genauigkeit wurde nicht erfüllt! \n Warnmeldung geschickt an:\n erenkarkin210300@gmail.com ")
        msg.setIcon (QMessageBox.Warning)
       
        # Create a QTimer to close the message box after 10 seconds (10000 milliseconds)
        timer = QTimer()
        timer.timeout.connect(msg.accept)  # Close the message box
        timer.start(5000)  # 5 seconds
        msg.exec_()
    #----------------- END POP UP FENSTER FUNKTION----------------
    
#--------------------------------------- GUI MAIN-----------------------------------------
if __name__ == "__main__":
    # Standard pyqt5 Konfiguartionen um Fenster zu generieren
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow ()  
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())                           # Fenster schliessen

    
