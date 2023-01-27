from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QLabel, QSpinBox, QComboBox, QTableWidget
from PyQt5 import QtGui, QtCore
from time import sleep
import pandas
import webbrowser
import traceback
import os, shutil
import glob
import mysql.connector as mysql
from PyQt5 import QtWidgets, uic
import sys,time,datetime
from subprocess import CREATE_NO_WINDOW

from config import CHROME_PROFILE_PATH

username = os.environ.get('USERNAME')

first_launch_date_filepath = "Res\.edc"
filename1 = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
filename = "Log\log.txt"


# Database info
HOST = 'mysql.stackcp.com'
PORT = 57664
DATABASE = 'wamdatabase-313333cd05'
USER = "wamuser"
PASSWORD = "bFeW2:gdI3jf"


try:
    db_connection = mysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DATABASE)
    # print("Connected to:", db_connection.get_server_info())
    c = db_connection.cursor()
    connection = 1
except:
    connection = 0
    
    
ID = ""
name = ""
email = ""
password = ""
act = ""
days = 0


class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(r'Res\GUI.ui', self) # Load the .ui file
        self.setWindowIcon(QtGui.QIcon('ico\web.png'))
        
        self.tableWidget = self.findChild(QTableWidget, "tableWidget")
        self.tableWidget.setColumnWidth(0,160)
        self.tableWidget.setColumnWidth(1,76)

        
        self.comboBox = self.findChild(QComboBox, "comboBox")
        self.comboBox.addItems(["", "+92"])
        ComboText=str(self.comboBox.currentText())
        
        self.textedit = self.findChild(QTextEdit, "textEdit")
        self.spinBox = self.findChild(QSpinBox, "spinBox")
        self.spinBox.setValue(10)
        
        self.warn = self.findChild(QLabel, "warn")

        self.label = self.findChild(QLabel, "total")
        
        self.sent = self.findChild(QLabel, "sent")
        
        self.notsent = self.findChild(QLabel, "notsent") 
        
        self.act_label = self.findChild(QLabel, "act_label")
             
        
        self.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Password)  
        self.setVisible(False) 

        self.button = self.findChild(QtWidgets.QPushButton, 'login')
        self.button.clicked.connect(self.LoginFunc)
        
        self.button = self.findChild(QtWidgets.QPushButton, 'Reload')
        self.button.clicked.connect(self.Refresh)
        self.button.setIcon(QtGui.QIcon('ico\loading.png'))
        self.button.setIconSize(QtCore.QSize(24,24))
        
        self.button = self.findChild(QtWidgets.QPushButton, 'Open')
        self.button.clicked.connect(self.OpenFile)
        self.button.setIcon(QtGui.QIcon('ico\contact.png'))
        self.button.setIconSize(QtCore.QSize(24,24))
        
        self.button = self.findChild(QtWidgets.QPushButton, 'Send')
        self.button.clicked.connect(self.SendMessege)
        self.button.setIcon(QtGui.QIcon('ico\send.png'))
        self.button.setIconSize(QtCore.QSize(24,24))
        
        self.button = self.findChild(QtWidgets.QPushButton, 'AttachFile')
        self.button.clicked.connect(self.Attachfile)
        self.button.setIcon(QtGui.QIcon('ico\paperclip.png'))
        self.button.setIconSize(QtCore.QSize(24,24))

        self.button = self.findChild(QtWidgets.QPushButton, 'clear')
        self.button.clicked.connect(self.logout)
        self.button.setIcon(QtGui.QIcon('ico\logout.png'))
        self.button.setIconSize(QtCore.QSize(24,24))
        
        self.button = self.findChild(QtWidgets.QPushButton, 'contactbtn')
        self.button.clicked.connect(self.ContactUs)
        self.button.setIcon(QtGui.QIcon('ico\info.png'))
        self.button.setIconSize(QtCore.QSize(24,24))

        self.show() # Show the GUI

        if connection == 1:
            self.act_label.setText("Connected")
        elif connection == 0:
            self.act_label.setText("Not Connected")
          
    def LoadUser(self):
        global email
        global ID
        global password
        global act
        global days
        global name
        c.execute("SELECT * FROM User WHERE email ='%s'"%str(self.EmailBox.text()))
        records = c.fetchall()
        for record in records:
            ID=str(record[0])
            name=str(record[1])
            email=str(record[2])
            password=str(record[3])
            act=str(record[4])
            days=int(record[5])
     
                
    def LoginFunc(self):
        self.LoadUser()
        self.is_program_expired()
        emailgot = self.EmailBox.text()
        passwordgot = self.PasswordBox.text()
        
        if emailgot=="" or passwordgot == "":
            self.warn.setText("Email Or Password field is Empty")
        else:
            if email == emailgot and password == passwordgot:
                if Expired!=True:
                    self.warn.setText("Hi, " + name)
                    self.act_label.setText("Activated")
                else:
                    self.act_label.setText("Expired")
                    self.warn.setText("Your Program is Expired")
            else:
                self.warn.setText("Email or Password is Incorrect")   
        
    def is_program_expired(self):
        global Expired
        Expired=False
        # Query date of first lauch in given file
        if os.path.exists(first_launch_date_filepath):
            with open(first_launch_date_filepath, 'r') as fileRead:
                time_as_str = fileRead.read()
                start_date = datetime.datetime.strptime(time_as_str, "%Y_%m_%d")
                # Check if current time is greater than time limit
                expire_date = start_date + datetime.timedelta(days=days)
                if datetime.datetime.now() > expire_date:
                    Expired=True
        else:
            start_date = datetime.datetime.now()
            with open(first_launch_date_filepath, 'w') as fileWrite:
                fileWrite.write(start_date.strftime("%Y_%m_%d"))
                
    def CheckExpired(self):
        self.is_program_expired()
        if Expired==True:
            self.act_label.setText("Expired")
        else:
            pass

    def ContactUs(self): 
        webbrowser.open('https://www.instagram.com/mkeykhan/?hl=en')
    
    def CheckContact(self):
        try:
            path
        except NameError:
            self.warn.setText(f'Please Select A Contact File')
        else:
            if path > "":
                self.warn.setText(f'Contact File Selected Successfully')
            else:
                self.warn.setText(f'No File Selected')
    
    def OpenFile(self):
        self.CheckExpired()
        global path
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                        'All Files (*.xlsx*)')
        if path != ('', ''):
            path=path[0]
            self.CheckContact()
            self.LoadFile()
            
    def LoadFile(self):
        contacts = pandas.read_excel(path, sheet_name='Recipients')
        row = 0
        total = self.tableWidget.setRowCount(len(contacts))
        for column in contacts['Contact'].tolist():
            ph = str(self.comboBox.currentText()) + str(contacts['Contact'][row])
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(ph))
            row += 1
        self.total.setText(str(row))
    
    def Refresh(self):
        try:
            self.LoadFile()
        except:
            self.CheckContact()
        
    def Attachfile(self):
        self.CheckExpired()
        global filepath
        filepath = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                        'All Files ()')
        if filepath != ('', ''):
            filepath = filepath[0]
            
    def SendText(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--profile-directory=Default')
        options.add_argument('--user-data-dir=C:/Temp/ChromeProfile')
        # options.add_argument(CHROME_PROFILE_PATH)
        excel_data = pandas.read_excel(path, sheet_name='Recipients')
        count = 0
        send = 0
        notsent = 0
        failed = 0
        count1 = []
        
        d_path = Service('Driver\chromedriver.exe')
        d_path.creationflags = CREATE_NO_WINDOW

        driver = webdriver.Chrome(service=d_path, options=options)
        driver.get('https://web.whatsapp.com')
        driver.maximize_window()
        with open(filename, 'w') as log:
            try:
                element = WebDriverWait(driver, 500).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_1RAKT")))
            finally:
                for column in excel_data['Contact'].tolist():
                    try:
                        url = 'https://web.whatsapp.com/send?phone=' + str(self.comboBox.currentText()) + str(excel_data['Contact'][count]) + '&text=' + self.textedit.toPlainText()                   
                        sent = False
                        driver.get(url)
                        
                        try:
                            click_btn = WebDriverWait(driver, self.spinBox.value()).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, '_1Ae7k')))
                        except Exception as e:
                            try:
                                driver.find_element(By.XPATH, '//div[@class="_26aja _1dEQH"]')
                            except:
                                driver.find_element(By.XPATH, '//div[@class="_20C5O _2Zdgs"]').click()
                                print('Sorry, Messege could not sent to: ' +'0'+ str(excel_data['Contact'][count]), file = log)
                                self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("Not Sent"))
                                notsent = notsent + 1
                                self.notsent.setText(str(notsent))
                            else:
                                click_btn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, '_1Ae7k')))
                                pass
                                
                        else:
                            click_btn.click()
                            sent = True
                            sleep(2)
                            print('Message sent to: ' +'0'+ str(excel_data['Contact'][count]), file = log)
                            self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("Sent"))
                            send += 1
                            self.sent.setText(str(send))

                        count = count + 1
                    
                    except Exception as e:
                        print('Failed to send message to ' +'0'+ str(excel_data['Contact'][count]) + str(e), file = log)
                        self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("Failed"))
                        count1.append(count)
                        count = count + 1
                print('ReTest', file = log)
                while len(count1) > 0:
                    for x in count1:
                        try:
                            url = 'https://web.whatsapp.com/send?phone=' + str(self.comboBox.currentText()) + str(excel_data['Contact'][x]) + '&text=' + self.textedit.toPlainText()                   
                            sent = False
                            driver.get(url)
                            
                            try:
                                click_btn = WebDriverWait(driver, self.spinBox.value()).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, '_1Ae7k')))
                            except Exception as e:
                                try:
                                    driver.find_element(By.XPATH, '//div[@class="_26aja _1dEQH"]')
                                except:
                                    driver.find_element(By.XPATH, '//div[@class="_20C5O _2Zdgs"]').click()
                                    print('Sorry, Messege could not sent to: ' +'0'+ str(excel_data['Contact'][x]), file = log)
                                    self.tableWidget.setItem(x, 1, QtWidgets.QTableWidgetItem("Not Sent"))
                                    notsent = notsent + 1
                                    self.notsent.setText(str(notsent))
                                    count1.remove(x)
                                else:
                                    click_btn = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, '_1Ae7k')))
                                    pass
                                    
                            else:
                                click_btn.click()
                                sent = True
                                sleep(2)
                                print('Message sent to: ' +'0'+ str(excel_data['Contact'][x]), file = log)
                                self.tableWidget.setItem(x, 1, QtWidgets.QTableWidgetItem("Sent"))
                                send += 1
                                self.sent.setText(str(send))
                                count1.remove(x)
                        
                        except Exception as e:
                            print('Failed to send message to ' +'0'+ str(excel_data['Contact'][x]) + str(e), file = log)

            print('Session Compleate', file = log)
            driver.quit()
            self.warn.setText(f'Session Completed')
    
    
    def SendImage(self):
        if len(self.textedit.toPlainText())>=1:
            setclass="_1Ae7k"
        else:
            setclass="_3HQNh"
        
        options = webdriver.ChromeOptions()
        options.add_argument('--profile-directory=Default')
        options.add_argument('--user-data-dir=C:/Temp/ChromeProfile')
        # options.add_argument(CHROME_PROFILE_PATH)
        excel_data = pandas.read_excel(path, sheet_name='Recipients')
        count = 0
        send = 0
        notsent = 0
        failed = 0
        count1 = []
        
        d_path = Service('Driver\chromedriver.exe')
        d_path.creationflags = CREATE_NO_WINDOW

        driver = webdriver.Chrome(service=d_path, options=options)
        driver.get('https://web.whatsapp.com')
        driver.maximize_window()
        with open(filename, 'w') as log:       
            try:
                element = WebDriverWait(driver, 500).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_1RAKT")))
            finally:
                for column in excel_data['Contact'].tolist(): 
                    # sleep(1)               
                    try:
                        url = 'https://web.whatsapp.com/send?phone=' + str(self.comboBox.currentText()) + str(excel_data['Contact'][count]) + '&text=' + self.textedit.toPlainText()                  
                        sent = False
                        driver.get(url)
                            
                        try:
                            WebDriverWait(driver, self.spinBox.value()).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, setclass)))
                                
                        except Exception as e:
                            try:
                                driver.find_element(By.XPATH, '//div[@class="_26aja _1dEQH"]')
                            except:
                                driver.find_element(By.XPATH, '//div[@class="_20C5O _2Zdgs"]').click()
                                print('Sorry, Messege could not sent to: ' +'0'+ str(excel_data['Contact'][count]), file = log)
                                self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("Not Sent"))
                                notsent = notsent + 1
                                self.notsent.setText(str(notsent))
                                
    
                            else:
                                click_btn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, setclass)))
                                pass
                            
                        else:
                                
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title = "Attach"]'))).click()
                            
                            image_box = driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(filepath)
                                
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_165_h'))).click()
                                
                            sent = True
                                
                            sleep(2)
                            print('Message sent to: ' +'0'+ str(excel_data['Contact'][count]), file = log)
                            self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("Sent"))
                            send += 1
                            self.sent.setText(str(send))

                        count = count + 1
                    except Exception as e:
                        print('Failed to send message to ' +'0'+ str(excel_data['Contact'][count]) + str(e), file = log)
                        self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("Failed"))
                        count1.append(count)
                        count = count + 1
                print('ReTest', file = log)    
                while len(count1) > 0:
                    for x in count1:
                        # sleep(1)               
                        try:
                            url = 'https://web.whatsapp.com/send?phone=' + str(self.comboBox.currentText()) + str(excel_data['Contact'][x]) + '&text=' + self.textedit.toPlainText()                  
                            sent = False
                            driver.get(url)
                                
                            try:
                                WebDriverWait(driver, self.spinBox.value()).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, setclass)))
                                    
                            except Exception as e:
                                try:
                                    driver.find_element(By.XPATH, '//div[@class="_26aja _1dEQH"]')
                                except:
                                    driver.find_element(By.XPATH, '//div[@class="_20C5O _2Zdgs"]').click()
                                    print('Sorry, Messege could not sent to: ' +'0'+ str(excel_data['Contact'][x]), file = log)
                                    self.tableWidget.setItem(x, 1, QtWidgets.QTableWidgetItem("Not Sent"))
                                    notsent = notsent + 1
                                    self.notsent.setText(str(notsent))
                                    count1.remove(x)
        
                                else:
                                    click_btn = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, setclass)))
                                    pass
                                
                            else:
                                    
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title = "Attach"]'))).click()
                                
                                image_box = driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(filepath)
                                    
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_165_h'))).click()
                                    
                                sent = True
                                    
                                sleep(2)
                                print('Message sent to: ' +'0'+ str(excel_data['Contact'][x]), file = log)
                                self.tableWidget.setItem(x, 1, QtWidgets.QTableWidgetItem("Sent"))
                                send += 1
                                self.sent.setText(str(send))
                                count1.remove(x)

                        except Exception as e:
                            print('Failed to send message to ' +'0'+ str(excel_data['Contact'][x]) + str(e), file = log)
         
            print('Session Completed', file = log)
            driver.quit()
            self.warn.setText(f'Session Completed')
        
    def SendMessege(self):
        # self.CheckExpired()
        if Expired==True:
            self.act_label.setText("Expired")
        else:
            try:
                path
            except NameError:
                self.CheckContact()
            else: 
                try:
                    filepath
                except NameError:
                    self.SendText()
                else:
                    self.SendImage()
            
    def logout(self):
        self.CheckExpired()
        LoginPath = 'C:\\Users\\' + username + '\\AppData\\Local\\Google\\Chrome\\User Data\\WAM'
        try:
            shutil.rmtree(LoginPath)
        
        except:
            self.warn.setText(f'No Login Info found') 
        else:
            self.warn.setText(f'Whatsapp Logout Successfull')
            
            
        
def main():
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui()# Create an instance of our class
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()