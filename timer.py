#!/usr/bin/python3

import sys
import datetime
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QDialog, QApplication, QGridLayout, QPushButton, QLabel)

class MainWindow(QDialog):
    lastTick = datetime.datetime.now()
    timeAccum = lastTick - lastTick
    timer = QTimer()
    timeLabel = None # QLabel
    timesLabel = None # QLabel
    
    times = []

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.OriginalPalette = QApplication.palette()

        self.setWindowTitle("Timer")
        self.timeLabel = QLabel(str(self.timeAccum))
        self.timesLabel = QLabel("")

        buttonStart = QPushButton("&Start")
        buttonStart.clicked.connect(self.timerStart)
        buttonReset = QPushButton("&Reset")
        buttonReset.clicked.connect(self.timerReset)
        buttonStop = QPushButton("Sto&p")
        buttonStop.clicked.connect(self.timerStop)

        buttonRegister = QPushButton("R&egister")
        buttonRegister.clicked.connect(self.registerTime)
        buttonRegisterAndReset = QPushButton("Re&gister && Reset")
        buttonRegisterAndReset.clicked.connect(self.registerTimeAndReset)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.timeLabel, 0, 0)
        mainLayout.addWidget(buttonStart, 1, 0)
        mainLayout.addWidget(buttonReset, 2, 0)
        mainLayout.addWidget(buttonStop, 3, 0)
        mainLayout.addWidget(buttonRegister, 1, 1)
        mainLayout.addWidget(buttonRegisterAndReset, 2, 1)
        mainLayout.addWidget(self.timesLabel, 4, 0)
        self.setLayout(mainLayout)

        self.timer.timeout.connect(self.timerUpdate)

    def timerUpdate(self):
        now = datetime.datetime.now()
        self.timeAccum += now - self.lastTick
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
        self.times.append(self.timeAccum)
        txt = ""
        for i, t in enumerate(self.times):
            if i > 0:
                txt += "\n"
            txt += "#" + str(i) + ": " + str(t)

        self.timesLabel.setText(txt)

    def registerTimeAndReset(self):
        self.registerTime()
        self.timerReset()

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())