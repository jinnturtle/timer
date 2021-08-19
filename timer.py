#!/usr/bin/python3

import sys
import datetime
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
        QDialog, QApplication, QGridLayout, QPushButton, QLabel, QLineEdit)

class MainWindow(QDialog):
    lastTick = datetime.datetime.now()
    timeAccum = lastTick - lastTick
    timer = QTimer()
    currTimerNameLabel = None # QLabel
    timeLabel = None # QLabel
    timesLabel = None # QLabel
    renameTextLine = None # QLineEdit
    
    times = []

    def __init__(self, version, parent = None):
        super(MainWindow, self).__init__(parent)

        self.OriginalPalette = QApplication.palette()

        self.setWindowTitle("Timer " + str(version))
        self.currTimerNameLabel = QLabel("time 0")
        self.timeLabel = QLabel(str(self.timeAccum))
        self.timesLabel = QLabel("")
        self.renameTextLine = QLineEdit(self.currTimerNameLabel.text())

        buttonStart = QPushButton("&Start")
        buttonStart.clicked.connect(self.timerStart)
        buttonReset = QPushButton("&Reset")
        buttonReset.clicked.connect(self.timerReset)
        buttonStop = QPushButton("&Pause")
        buttonStop.clicked.connect(self.timerStop)

        buttonRegister = QPushButton("R&egister")
        buttonRegister.clicked.connect(self.registerTime)
        buttonRegisterAndReset = QPushButton("Re&gister && Reset")
        buttonRegisterAndReset.clicked.connect(self.registerTimeAndReset)
        buttonRename = QPushButton("Re&name")
        buttonRename.clicked.connect(self.renameTimer)


        mainLayout = QGridLayout()
        mainLayout.addWidget(self.currTimerNameLabel, 0, 0)
        mainLayout.addWidget(self.timeLabel, 0, 1)
        mainLayout.addWidget(buttonStart, 1, 0)
        mainLayout.addWidget(buttonReset, 2, 0)
        mainLayout.addWidget(buttonStop, 3, 0)
        mainLayout.addWidget(buttonRegister, 1, 1)
        mainLayout.addWidget(buttonRegisterAndReset, 2, 1)
        mainLayout.addWidget(buttonRename, 3, 1)
        mainLayout.addWidget(self.renameTextLine, 4, 1)
        mainLayout.addWidget(self.timesLabel, 5, 0)
        self.setLayout(mainLayout)

        self.timer.timeout.connect(self.timerUpdate)

    def timerUpdate(self):
        now = datetime.datetime.now()
        self.timeAccum += now - self.lastTick

        # timeTxt = str(self.timeAccum)
        # if self.currTimerNameLabel.text() != "":
        #     timeTxt = self.currTimerNameLabel.text() + ": " + timeTxt

        self.timeLabel.setText(str(self.timeAccum))

        self.lastTick = now

    def timerStart(self):
        self.lastTick = datetime.datetime.now()
        self.timer.start(1)

    def timerReset(self):
        self.timeAccum -= self.timeAccum

    def timerStop(self):
        self.timer.stop()

    def registerTime(self):
        self.times.append(TimeRecord(name = self.currTimerNameLabel.text(), time = self.timeAccum))
        txt = ""
        for i, t in enumerate(self.times):
            if i > 0: txt += "\n"

            if t.name != "": txt += t.name
            txt += ": " + str(t.time)

        self.timesLabel.setText(txt)

        self.renameTextLine.setText("time " + str(len(self.times)))
        self.renameTimer()

    def registerTimeAndReset(self):
        self.registerTime()
        self.timerReset()

    def renameTimer(self):
        self.currTimerNameLabel.setText(self.renameTextLine.text())

class TimeRecord:
    def __init__(self, name, time):
        self.name = name
        self.time = time

class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

#-------------------------------------------------------------------------------

version = Version(1,1,0)

app = QApplication(sys.argv)
mainWindow = MainWindow(version)
mainWindow.show()
sys.exit(app.exec_())
