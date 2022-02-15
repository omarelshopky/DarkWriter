from UI.writingWindowUI import Ui_WritingWindow
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 

class WritingWindow(QMainWindow, Ui_WritingWindow):
    def __init__(self, widget):
        super().__init__()
        self.mainWidget = widget
        self.setupUi(self)
        self.UiComponentsEvent()
        self.hideEndSessionBtns()
        #loadUi('file', self)
  

    def UiComponentsEvent(self):
        # Closes the app when quit button pressed
        self.saveAndQuitBtn.clicked.connect(lambda:self.closeApp())
    

    # Sets Blocking Attributes from the calling Windows
    def setBlocking(self, amount, isTime):
        self.blockingAmount = amount
        self.blockingInTime = isTime

        self.startTimers()


    # Set the file path to read and write
    def setFilePath(self, path):
        self.filePath = path


    # Start All needed timers
    def startTimers(self):
        if self.blockingInTime:
            self.startProgressTimer(self.blockingAmount)
        
        self.updateProgressTimer = QTimer()
        if self.blockingAmount != 0:
            self.startUpdateProgressTimer()


    def startUpdateProgressTimer(self):
        self.updateProgressTimer.start(1000)
        self.updateProgressTimer.timeout.connect(lambda: self.stopUpdateProgressTimer())


    # Update the progress color and value and restart the timer if not 100%
    def stopUpdateProgressTimer(self):
        self.updateProgressTimer.stop()

        amount = self.updateProgressValue()
        self.updateProgressColor(amount)

        if amount != 100:
            self.startUpdateProgressTimer()
        

    def updateProgressValue(self):
        if self.blockingInTime:
            remain = self.progressTimer.remainingTime() / 60000
        else:
            # remain = self.wordsTyped
            pass

        amount = 100 - ((remain / int(self.blockingAmount)) * 100)
        self.progressBar.setValue(amount)

        return amount


    # Updates the progress bar's color according to its amount
    def updateProgressColor(self, amount):
        
        if amount <= 25:
            color = 'ED2938'
        elif amount <= 50:
            color = 'FF8C01'
        elif amount <= 75:
            color = 'FFE733'
        else:
            color = '37DD5C'

        self.progressBar.setStyleSheet("QProgressBar"
            "{"
            "border: solid grey;"
            "color: black;"
            "height: 5px"
            "}"
            "QProgressBar::chunk"
            "{"
            f"background-color: #{color};"
            "} ")


    def startProgressTimer(self, timeInMin):
        self.progressTimer = QTimer()
        self.progressTimer.start(int(timeInMin) * 60000)
        self.progressTimer.timeout.connect(lambda: self.stopProgressTimer())


    def stopProgressTimer(self):
        self.progressTimer.stop()
        self.showEndSessionBtns()


    # Show snooze and Quit buttons with hiding progress bar
    def showEndSessionBtns(self):
        self.progressBar.hide()
        self.snoozeBtn.show()
        self.saveAndQuitBtn.show()


    # Hide snooze and Quit buttons with showing progress bar
    def hideEndSessionBtns(self):
        self.progressBar.show()
        self.snoozeBtn.hide()
        self.saveAndQuitBtn.hide()


    # Close the app
    def closeApp(self):
        self.SaveFile()

        self.close()
        self.mainWidget.close()


    # Open browse files dialog to save the file
    def SaveFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save File', self.filePath, 'Text Files (*.txt)')
        

