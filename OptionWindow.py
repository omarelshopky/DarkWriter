from UI.optionWindowUI import Ui_optionWindow
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import os
from datetime import datetime


class OptionWindow(QMainWindow, Ui_optionWindow):

    def __init__(self, widget):
        super().__init__()
        self.mainWidget = widget
        self.setupUi(self)
        self.UiComponentsEvent()
        self.pathSolver = PathSolver()

  
    # Set up all events in the UI components
    def UiComponentsEvent(self):
        self.enableInputValidation()

        # Open writing window
        self.ndStartBtn.clicked.connect(lambda:self.openWrintingWindow())
        self.odStartBtn.clicked.connect(lambda:self.openWrintingWindow())

        # Closes the app when quit button pressed
        self.odQuitBtn.clicked.connect(lambda:self.closeApp())
        self.ndQuitBtn.clicked.connect(lambda:self.closeApp())

        # Browse button event
        self.odBrowseBtn.clicked.connect(lambda:self.browseFile())

        # Enable Start writing without blocking
        self.ndFreeRadioBtn.toggled.connect(lambda:self.enableFreeStart())
        self.odFreeRadioBtn.toggled.connect(lambda:self.enableFreeStart())
        self.odFilePathTxt.textChanged.connect(lambda:self.enableFreeStart())

        # 
        self.ndBlockInput.textChanged.connect(lambda:self.enableBlockedStart())



    # Make blocking input box accept only integers
    def enableInputValidation(self):
        self.ndBlockInput.setValidator(QIntValidator())
        self.odBlockInput.setValidator(QIntValidator())


    # Open the writing window
    def openWrintingWindow(self):
        # Current Index = 0 at New Draft Tab
        filePath = self.pathSolver.getNewFilePath() if self.tabWidget.currentIndex() == 0 else self.odFilePathTxt.text()
        self.mainWidget.widget(1).setFilePath(filePath)
        self.mainWidget.widget(1).setBlocking(self.blockingAmount, self.blockingInTime)
        self.mainWidget.setCurrentIndex(1)


    # Close the app
    def closeApp(self):
        self.close()
        self.mainWidget.close()


    # Open browse files dialog
    def browseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.', 'Text Files (*.txt)')
        self.odFilePathTxt.setText(fname[0])


    # Enable start writing with blocking time = 0 min
    def enableFreeStart(self):
        
        if self.tabWidget.currentIndex() == 0:  # New Draft Tab
            self.ndStartBtn.setEnabled(self.ndFreeRadioBtn.isChecked())

        else:           # Open Draft Tab
            if self.odFreeRadioBtn.isChecked() and self.odFilePathTxt.text() != '':
                self.odStartBtn.setEnabled(True)
            else:
                self.odStartBtn.setEnabled(False)

        self.blockingInTime = True
        self.blockingAmount = 0


    def enableBlockedStart(self):

        if self.tabWidget.currentIndex() == 0:  # New Draft Tab
            if self.ndBlockInput.text() != '':
                self.ndStartBtn.setEnabled(True)
            else:
                self.ndStartBtn.setEnabled(False)

        else:           # Open Draft Tab
            pass



class PathSolver():

    # Gets the path of the new created file in default dir
    def getNewFilePath(self):
        defaultPath = os.path.expanduser('~/Documents/DarkTurkeyWriter/')

        filePath = os.path.join(defaultPath, self.getCurrentDateTime() + '.txt')
        if not os.path.exists(defaultPath):
            os.makedirs(defaultPath)
            
        return filePath


    def getCurrentDateTime(self):
        return datetime.now().strftime("%d-%m-%Y_%H-%M") # dd-mm-YY_H-M
        