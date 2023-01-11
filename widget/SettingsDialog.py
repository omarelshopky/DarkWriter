from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtCore import Qt
from designPy.settingsDialogUI import Ui_SettingsDialog

class SettingsDialog(QDialog, Ui_SettingsDialog):
    """Booster images feature settings dialog

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
    """
    def __init__(self, parentWindow: QMainWindow):
        super().__init__(parentWindow)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)