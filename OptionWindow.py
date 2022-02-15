from UI.optionWindowUI import Ui_optionWindow
from PyQt5.QtWidgets import * 


class OptionWindow(QMainWindow, Ui_optionWindow):
    def __init__(self, widget):
        super().__init__()
        self.mainWidget = widget
        self.setupUi(self)
        self.UiComponentsLogic()
        self.show()
        #loadUi('file', self)
  
  
    def UiComponentsLogic(self):
        # Open writing window
        self.ndStartBtn.clicked.connect(lambda:self.openWrintingWindow())
        self.odStartBtn.clicked.connect(lambda:self.openWrintingWindow())

        # Closes the app when quit button pressed
        self.odQuitBtn.clicked.connect(lambda:self.closeApp())
        self.ndQuitBtn.clicked.connect(lambda:self.closeApp())

        # Browse button event
        self.odBrowseBtn.clicked.connect(lambda:self.browseFile())

        # Radion Buttons event
        self.ndWordRadioBtn.toggled.connect(lambda:self.handleRadioButton())
        self.ndMntRadioBtn.toggled.connect(lambda:self.handleRadioButton())
        self.ndFreeRadioBtn.toggled.connect(lambda:self.handleRadioButton())
        self.odWordRadioBtn.toggled.connect(lambda:self.handleRadioButton())
        self.odMntRadioBtn.toggled.connect(lambda:self.handleRadioButton())
        self.odFreeRadioBtn.toggled.connect(lambda:self.handleRadioButton())


    # Open the writing window
    def openWrintingWindow(self):
        self.mainWidget.setCurrentIndex(1)


    # Close the app
    def closeApp(self):
        self.close()
        self.mainWidget.close()


    # Open browse files dialog
    def browseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.', 'Text Files (*.txt)')
        self.odFilePathTxt.setText(fname[0])


    def handleRadioButton(self):
        index = self.tabWidget.currentIndex()

        if index == 0:  # New Draft Tab
            self.ndStartBtn.setEnabled(self.ndFreeRadioBtn.isChecked())

        else:           # Open Draft Tab
            if self.odFreeRadioBtn.isChecked() and self.odFilePathTxt.text() != '':
                self.odStartBtn.setEnabled(True)
