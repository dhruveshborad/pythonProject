import sys
import sqlite3
from PyQt5 import QtWidgets , QtCore
from PyQt5.QtWidgets import QDialog, QApplication,QMessageBox,QListWidgetItem, QCheckBox,QCalendarWidget
from PyQt5.uic import loadUi
import pymongo
import random
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import os.path
from email import encoders
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("form1.ui", self)
        self.pushButtonlogin.clicked.connect(self.loginfunction)
        self.lineEditpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButtonsignup.clicked.connect(self.gotocreate)
        self.pushButtonforegatepassword.clicked.connect(self.gotoforegotpass)

    def loginfunction(self):
        email = self.lineEditusername.text()
        password = self.lineEditpassword.text()
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb["people"]
        data = {'name': email, 'password': password}
        if mycol.find_one(data):
            print("Successfully logged in with email: ", email, "and password:", password)
            calendar = Calendar()
            widget.addWidget(calendar)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            global loginid
            loginid = ""
            loginid = self.lineEditusername.text()
            print(email)
        else:
            print("username not found")

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoforegotpass(self):
        forgotpass = ForgotPass()
        widget.addWidget(forgotpass)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("form.ui", self)
        self.pushButtonsignup1.clicked.connect(self.create_db)
        self.lineEditpassword1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditconfrimpassword1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.beackbutton.clicked.connect(self.beackfunc)
        self.pushButtonsendotp.clicked.connect(self.sendemail)

    def create_db(self):
        password = self.lineEditpassword1.text()
        email = self.lineEditusername1.text()
        if self.lineEditpassword1.text() == self.lineEditconfrimpassword1.text() and random_str1 == self.lineEditotp.text():
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            try:
                client = pymongo.MongoClient()
                mydb = client['mydb']
                mycol = mydb["people"]
                data = {'name': email, 'password': password}
                if mycol.insert_one(data):
                    print("Successfully created acc with email: ", email, "and password: ", password)
            except Exception as e:
                print("Something went wrong....", e)

    def beackfunc(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sendemail(self):
        digits = [i for i in range(0, 10)]
        global random_str1
        random_str1 = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str1 += str(digits[index])
        print(random_str1)
        msg = MIMEMultipart()
        domainemail = "dhruveshborad007@gmail.com"
        domainpass = "Dh@#$008"
        useremail = self.lineEditusername1.text()
        subject = "This mail send by vocadors"
        msg['From'] = domainemail
        msg['To'] = useremail
        msg['Subject'] = subject
        otpmsg = "your new account otp is: {}".format(random_str1)
        try:
            # Create your SMTP session
            msg.attach(MIMEText(otpmsg, 'plain'))
            filename = os.path.basename("C:\\Users\\Dhruvesh\\PycharmProjects\\pythonProject\\D1.jpg")
            attachment = open("C:\\Users\\Dhruvesh\\PycharmProjects\\pythonProject\\D1.jpg", "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(domainemail, domainpass)
            message = msg.as_string()
            smtp.sendmail(domainemail, useremail, message)
            smtp.quit()
            print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong....", ex)


class ForgotPass(QDialog):
    def __init__(self):
        super(ForgotPass, self).__init__()
        loadUi("form3.ui", self)
        self.lineEditpassword2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditconfrimpassword1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButtonSubmmite.clicked.connect(self.submmitepass)
        self.pushButtonsendotp.clicked.connect(self.sendemail)
        self.pushButtonBack.clicked.connect(self.Backlogin)

    def sendemail(self):
        email = self.lineEditusername2.text()
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb["people"]
        data = {'name': email}
        if (mycol.find_one(data)):
            digits = [i for i in range(0, 10)]
            global random_str
            random_str = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                random_str += str(digits[index])
            print(random_str)
            domainemail = "dhruveshborad007@gmail.com"
            domainpass = "Dh@#$008"
            useremail = self.lineEditusername2.text()
            subject = "vocadors sending a mail"
            msg = MIMEMultipart()
            msg['From'] = domainemail
            msg['To'] = useremail
            msg['Subject'] = subject
            otpmsg = 'Your Account OTP is: {}'.format(random_str)
            try:
                # Create your SMTP session
                msg.attach(MIMEText(otpmsg, 'plain'))
                filename = os.path.basename("C:\\Users\\Dhruvesh\\PycharmProjects\\pythonProject\\D1.jpg")
                attachment = open("C:\\Users\\Dhruvesh\\PycharmProjects\\pythonProject\\D1.jpg", "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(part)

                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                smtp.starttls()
                smtp.login(domainemail, domainpass)
                message = msg.as_string()
                smtp.sendmail(domainemail, useremail, message)
                smtp.quit()
                print("Email sent successfully!")
            except Exception as ex:
                print("Something went wrong....", ex)
        else:
            print("username is invelide....")

    def submmitepass(self):
        if (
                self.lineEditpassword2.text() == self.lineEditconfrimpassword1.text() and random_str == self.lineEditotp.text()):
            email = self.lineEditusername2.text()
            client = pymongo.MongoClient()
            mydb = client['mydb']
            mycol = mydb["people"]
            if (mycol.find_one_and_update({'name': email}, {'$set': {'password': self.lineEditpassword2.text()}})):
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                print("true")

    def Backlogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Calendar(QDialog):

    def __init__(self):
        super(Calendar, self).__init__()
        loadUi("form2.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)

    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.tasksListWidget.clear()
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb["people"]
        data = {str(date):[],'name':(loginid)}
        if mycol.find_one({'name':loginid}):
            mycol.insert_one(data)
    def saveChanges(self):
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb["people"]
        date = self.calendarWidget.selectedDate().toPyDate()
        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                mycol.find_one_and_update({'name':loginid},{'$set':{task:['Done']}})
            else:
                mycol.find_one_and_update({'name':loginid},{'$set':{task:['Not']}})

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb["people"]
        newTask = str(self.lineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()
        data = {str(date): [newTask], 'name': (loginid)}
        if mycol.find_one({'name': loginid}):
            mycol.insert_one(data)
        self.updateTaskList(date)

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1500)
widget.setFixedHeight(720)
widget.show()
app.exec_()
