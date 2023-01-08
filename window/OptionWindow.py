from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFileDialog
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
    components: dict
        Dictionary contains tabs related components
    """
    def __init__(self, mainStack: QStackedWidget):
        super().__init__()
        self.mainStack = mainStack
        self.pathResolver = PathResolver()
        self.setupUi(self)
        self._setupEvents()
        self._enableInputValidation()
        self.components = self._prepareTabComponents()

    def _setupEvents(self) -> None:
        """Setup all events in the UI components"""
        # Open writing window
        self.ndStartBtn.clicked.connect(lambda: self._openWritingWindow())
        self.odStartBtn.clicked.connect(lambda: self._openWritingWindow(False))

        # Closes the app when quit button pressed
        self.odQuitBtn.clicked.connect(lambda: self._closeApp())
        self.ndQuitBtn.clicked.connect(lambda: self._closeApp())

        # Browse button event
        self.odBrowseBtn.clicked.connect(lambda: self._browseFile())

        # Enable Start Writing Events
        self.odFilePathTxt.textChanged.connect(lambda: self._enableStart())
        self.ndFreeRadioBtn.toggled.connect(lambda: self._enableStart())
        self.odFreeRadioBtn.toggled.connect(lambda: self._enableStart())
        self.ndBlockInput.textChanged.connect(lambda: self._handleChangeBlockingAttribute())
        self.odBlockInput.textChanged.connect(lambda: self._handleChangeBlockingAttribute())
        self.ndSessionInput.textChanged.connect(lambda: self._handleChangeBlockingAttribute())
        self.odSessionInput.textChanged.connect(lambda: self._handleChangeBlockingAttribute())

    def _enableInputValidation(self) -> None:
        """Make blocking input box accept only integers"""
        self.ndBlockInput.setValidator(QIntValidator())
        self.odBlockInput.setValidator(QIntValidator())
        self.ndSessionInput.setValidator(QIntValidator())
        self.odSessionInput.setValidator(QIntValidator())

    def _prepareTabComponents(self) -> dict:
        """Prepare dictionary contains the similar components in each tab

        Returns:
        ----------
        dict:
            contains the components of each tab
        """
        return {
            OptionTab.NEW_DRAFT.name: {
                "BlockInput": self.ndBlockInput,
                "SessionInput": self.ndSessionInput,
                "TotalBlockTxt": self.ndTotalBlockTxt,
                "FreeRadioBtn": self.ndFreeRadioBtn,
                "TimeRadioBtn": self.ndMntRadioBtn,
                "WordRadioBtn": self.ndWordRadioBtn,
                "StartBtn": self.ndStartBtn,
                "QuitBtn": self.ndQuitBtn
            },
            OptionTab.OPEN_DRAFT.name: {
                "BlockInput": self.odBlockInput,
                "SessionInput": self.odSessionInput,
                "TotalBlockTxt": self.odTotalBlockTxt,
                "FreeRadioBtn": self.odFreeRadioBtn,
                "TimeRadioBtn": self.odMntRadioBtn,
                "WordRadioBtn": self.odWordRadioBtn,
                "StartBtn": self.odStartBtn,
                "QuitBtn": self.odQuitBtn
            }
        }

    def _getCurrentTabComponents(self) -> dict:
        """Get the components of the current tab

        Returns:
        ----------
        dict:
            Dictionary contains all the component of the current tab
        """
        return self.components[OptionTab(self.tabWidget.currentIndex()).name]

    def _openWritingWindow(self, isNewDraft: bool = True) -> None:
        """Open the writing window

        Parameters
        ----------
        isNewDraft: bool
            Is new draft or open existing one
        """
        filePath = self.pathResolver.getNewFilePath() if self.tabWidget.currentIndex() == OptionTab.NEW_DRAFT.value else self.odFilePathTxt.text()
        blockingAttributes = self._getBlockingAttributes()
        self.mainStack.widget(AppWindow.WRITING_WINDOW.value).startBlockingSessions(filePath, isNewDraft, blockingAttributes)

    def _getBlockingAttributes(self) -> dict:
        """Get blocking attributes from input fields

        Returns:
        ----------
        dict:
            the blocking attributes like amount and is time or words count
        """
        components = self._getCurrentTabComponents()
        amount = components["BlockInput"].text()
        isTime = not components["WordRadioBtn"].isChecked()
        numOfSessions = [components["SessionInput"].text(), 1][components["SessionInput"].text() == ""]

        if components["FreeRadioBtn"].isChecked():
            amount = 0
            numOfSessions = 1

        return {"blockingAmount": amount, "isTimeBlocking": isTime, "numOfSessions": numOfSessions}

    def _closeApp(self) -> None:
        """Close the app"""
        self.mainStack.close()

    def _browseFile(self) -> None:
        """Open browse files dialog"""
        fname = QFileDialog.getOpenFileName(self, "Open file", ".", "Text Files (*.txt)")
        self.odFilePathTxt.setText(fname[0])

    def _enableStart(self) -> None:
        """Enable Start Writing Button"""
        components = self._getCurrentTabComponents()
        isAbleToStart = components["BlockInput"].text() != "" or components["FreeRadioBtn"].isChecked()

        if self.tabWidget.currentIndex() == OptionTab.OPEN_DRAFT.value:
            isAbleToStart = isAbleToStart and self.odFilePathTxt.text() != ""

        components["StartBtn"].setEnabled(isAbleToStart)

    def _calculateTotalBlockGoal(self) -> None:
        """Calculate total block goal"""
        components = self._getCurrentTabComponents()
        blockAmount = components["BlockInput"].text()
        NumOfSession = components["SessionInput"].text()

        if blockAmount and NumOfSession:
            components["TotalBlockTxt"].setText(str(int(blockAmount) * int(NumOfSession)))
        elif blockAmount:
            components["TotalBlockTxt"].setText(blockAmount)
        else:
            components["TotalBlockTxt"].setText("0")

    def _handleChangeBlockingAttribute(self) -> None:
        """Handle changing text for any of the blocking attributes"""
        self._calculateTotalBlockGoal()
        self._enableStart()
