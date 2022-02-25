from UI.optionWindowUI import Ui_optionWindow
from components.PathSolver import PathSolver
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 


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
        self.odStartBtn.clicked.connect(lambda:self.openWrintingWindow(False))

        # Closes the app when quit button pressed
        self.odQuitBtn.clicked.connect(lambda:self.closeApp())
        self.ndQuitBtn.clicked.connect(lambda:self.closeApp())

        # Browse button event
        self.odBrowseBtn.clicked.connect(lambda:self.browseFile())

        # Enable Start Writing Events
        self.ndFreeRadioBtn.toggled.connect(lambda:self.enableStart())
        self.odFreeRadioBtn.toggled.connect(lambda:self.enableStart())
        self.odFilePathTxt.textChanged.connect(lambda:self.enableStart())
        self.ndBlockInput.textChanged.connect(lambda:self.enableStart())
        self.odBlockInput.textChanged.connect(lambda:self.enableStart())


    # Make blocking input box accept only integers
    def enableInputValidation(self):
        self.ndBlockInput.setValidator(QIntValidator())
        self.odBlockInput.setValidator(QIntValidator())


    # Open the writing window
    def openWrintingWindow(self, isNew = True):
        # Current Index = 0 at New Draft Tab
        filePath = self.pathSolver.getNewFilePath() if self.tabWidget.currentIndex() == 0 else self.odFilePathTxt.text()
        self.setBlocking()
        self.mainWidget.widget(1).setFilePath(filePath)

        self.mainWidget.setCurrentIndex(1)
        self.mainWidget.widget(1).calculateLineHeight()

        if isNew == False:
            self.mainWidget.widget(1).fileHandler.loadFromFile()
            self.mainWidget.widget(1).currentParLbl.setText(str(len(self.mainWidget.widget(1).contentLines)-1))
            self.mainWidget.widget(1).updateContent()
            self.mainWidget.widget(1).setCursor(self.mainWidget.widget(1).textEdit.document().characterCount() - 1)
            self.mainWidget.widget(1).saving = True


    # Set Blocking period and Type
    def setBlocking(self):
        if self.tabWidget.currentIndex() == 0:  # New Draft Tab
            if self.ndFreeRadioBtn.isChecked():
                amount = 0
                isTime = True
            elif self.ndMntRadioBtn.isChecked():
                amount = self.ndBlockInput.text()
                isTime = True
            elif self.ndWordRadioBtn.isChecked():
                amount = self.ndBlockInput.text()
                isTime = False
            
        else:           # Open Draft Tab
            if self.odFreeRadioBtn.isChecked():
                amount = 0
                isTime = True
            elif self.odMntRadioBtn.isChecked():
                amount = self.odBlockInput.text()
                isTime = True
            elif self.odWordRadioBtn.isChecked():
                amount = self.odBlockInput.text()
                isTime = False

        self.mainWidget.widget(1).setBlocking(amount, isTime)
        

    # Close the app
    def closeApp(self):
        self.close()
        self.mainWidget.close()


    # Open browse files dialog
    def browseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.', 'Text Files (*.txt)')
        self.odFilePathTxt.setText(fname[0])


    # Enable Start Writing Button
    def enableStart(self):

        if self.tabWidget.currentIndex() == 0:  # New Draft Tab
            if self.ndBlockInput.text() != '' or self.ndFreeRadioBtn.isChecked():
                self.ndStartBtn.setEnabled(True)
            else:
                self.ndStartBtn.setEnabled(False)

        else:           # Open Draft Tab
            if (self.odBlockInput.text() != '' or self.odFreeRadioBtn.isChecked()) and self.odFilePathTxt.text() != '':
                self.odStartBtn.setEnabled(True)
            else:
                self.odStartBtn.setEnabled(False)

        