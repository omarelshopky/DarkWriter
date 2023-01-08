from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIntValidator
from cenum.AppWindow import AppWindow
from cenum.OptionTab import OptionTab
from designPy.optionWindowUI import Ui_optionWindow
from util.PathResolver import PathResolver

class OptionWindow(QMainWindow, Ui_optionWindow):
    """Startup window that shows the available starting options and goal definitions

    Attributes
    ----------
    mainStack : QStackedWidget
        Main stacked widget that contains all the app windows
    pathResolver: PathResolver
        The path resolver object that handle creating new files

    Methods
    -------
    _setupEvents()
        Setup all events in the UI components
    _enableInputValidation()
        Make blocking input box accept only integers
    _openWritingWindow(isNewDraft=True)
        Open the writing window
    _setBlocking()
        Set Blocking period and Type
    _closeApp()
        Close the app
    _browseFile()
        Open browse files dialog
    _enableStart()
        Enable Start Writing Button
    """
    def __init__(self, mainStack: QStackedWidget):
        super().__init__()
        self.mainStack = mainStack
        self.pathResolver = PathResolver()
        self.setupUi(self)
        self._setupEvents()

    def _setupEvents(self) -> None:
        """Setup all events in the UI components"""
        self._enableInputValidation()

        # Open writing window
        self.ndStartBtn.clicked.connect(lambda: self._openWritingWindow())
        self.odStartBtn.clicked.connect(lambda: self._openWritingWindow(False))

        # Closes the app when quit button pressed
        self.odQuitBtn.clicked.connect(lambda: self._closeApp())
        self.ndQuitBtn.clicked.connect(lambda: self._closeApp())

        # Browse button event
        self.odBrowseBtn.clicked.connect(lambda: self._browseFile())

        # Enable Start Writing Events
        self.ndFreeRadioBtn.toggled.connect(lambda: self._enableStart())
        self.odFreeRadioBtn.toggled.connect(lambda: self._enableStart())
        self.odFilePathTxt.textChanged.connect(lambda: self._enableStart())
        self.ndBlockInput.textChanged.connect(lambda: self._enableStart())
        self.odBlockInput.textChanged.connect(lambda: self._enableStart())

    def _enableInputValidation(self) -> None:
        """Make blocking input box accept only integers"""
        self.ndBlockInput.setValidator(QIntValidator())
        self.odBlockInput.setValidator(QIntValidator())

    def _openWritingWindow(self, isNewDraft: bool = True) -> None:
        """Open the writing window

        Parameters
        ----------
        isNewDraft: bool
            Is new draft or open existing one
        """
        writingWindow = self.mainStack.widget(AppWindow.WRITING_WINDOW.value)
        filePath = self.pathResolver.getNewFilePath() if self.tabWidget.currentIndex() == OptionTab.NEW_DRAFT.value else self.odFilePathTxt.text()
        self._setBlocking()
        writingWindow.setFilePath(filePath)

        self.mainStack.setCurrentIndex(AppWindow.WRITING_WINDOW.value)
        writingWindow.calculateLineHeight()

        if isNewDraft == False:
            writingWindow.fileHandler.loadFromFile()
            writingWindow.currentParLbl.setText(str(len(writingWindow.contentLines) - 1))
            writingWindow.updateContent()
            writingWindow.setCursor(writingWindow.textEdit.document().characterCount() - 1)
            writingWindow.saving = True

    def _setBlocking(self) -> None:
        """Set Blocking period and Type"""
        if self.tabWidget.currentIndex() == OptionTab.NEW_DRAFT.value:
            if self.ndFreeRadioBtn.isChecked():
                amount = 0
                isTime = True
            elif self.ndMntRadioBtn.isChecked():
                amount = self.ndBlockInput.text()
                isTime = True
            elif self.ndWordRadioBtn.isChecked():
                amount = self.ndBlockInput.text()
                isTime = False
        else:# Open Draft Tab
            if self.odFreeRadioBtn.isChecked():
                amount = 0
                isTime = True
            elif self.odMntRadioBtn.isChecked():
                amount = self.odBlockInput.text()
                isTime = True
            elif self.odWordRadioBtn.isChecked():
                amount = self.odBlockInput.text()
                isTime = False

        self.mainStack.widget(AppWindow.WRITING_WINDOW.value).setBlocking(amount, isTime)

    def _closeApp(self) -> None:
        """Close the app"""
        self.close()
        self.mainStack.close()

    def _browseFile(self) -> None:
        """Open browse files dialog"""
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.', 'Text Files (*.txt)')
        self.odFilePathTxt.setText(fname[0])

    def _enableStart(self) -> None:
        """Enable Start Writing Button"""
        if self.tabWidget.currentIndex() == OptionTab.NEW_DRAFT.value:
            if self.ndBlockInput.text() != '' or self.ndFreeRadioBtn.isChecked():
                self.ndStartBtn.setEnabled(True)
            else:
                self.ndStartBtn.setEnabled(False)
        else:# Open Draft Tab
            if (self.odBlockInput.text() != '' or self.odFreeRadioBtn.isChecked()) and self.odFilePathTxt.text() != '':
                self.odStartBtn.setEnabled(True)
            else:
                self.odStartBtn.setEnabled(False)
