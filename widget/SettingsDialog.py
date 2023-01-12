from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QMainWindow, QFileDialog
from designPy.settingsDialogUI import Ui_SettingsDialog
from util.ImagesChecker import ImagesChecker
from util.SettingsReader import SettingsReader

class SettingsDialog(QDialog, Ui_SettingsDialog):
    """Booster images feature settings dialog

    Methods
    -------
    _setupEvents()
        Setup all events in the UI components
    _enableInputValidation()
        Make numerical input box accept only integers
    _loadSettings()
        Loads the settings to the dialog inputs
    _browseImageFolder()
        Open browse folder dialog to get images folder
    _saveSettings()
        Saves the settings modified in dialog
    _getBoosterImgIsEnabled()
        Getter for booster image is enabled
    _getBoosterImgWordGoal()
        Getter for booster image words goal
    _getBoosterImgFolder()
        Getter for booster image folder
    """
    def __init__(self, parentWindow: QMainWindow):
        super().__init__(parentWindow)
        self.settingsReader = SettingsReader()
        self.imagesChecker = ImagesChecker()
        self.setupUi(self)
        self._setupEvents()
        self._enableInputValidation()
        self._loadSettings()

    def setupUi(self, SettingsDialog):
        super().setupUi(SettingsDialog)
        # disable whatIsThat from toolbar
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def _setupEvents(self) -> None:
        """Setup all events in the UI components"""
        self.buttonBox.accepted.connect(lambda: self._saveSettings())
        self.BImageFolderBrowseBtn.clicked.connect(lambda: self._browseImageFolder())

    def _enableInputValidation(self) -> None:
        """Make numerical input box accept only integers"""
        self.BIwordCountInput.setValidator(QIntValidator())

    def _loadSettings(self) -> None:
        """Loads the settings to the dialog inputs"""
        boosterImgSettings = self.settingsReader.getBoosterImagesSettings()
        self.BoosterImgSettingsGBox.setChecked(boosterImgSettings["enabled"])
        self.BIwordCountInput.setText(str(boosterImgSettings["words-goal"]))
        self.BImageFolderPathLbl.setText(boosterImgSettings["images-folder"])

    def _browseImageFolder(self) -> None:
        """Open browse folder dialog to get images folder"""
        folderPath = QFileDialog.getExistingDirectory(self, "Select Booster Images Folder")
        imgsCount = self.imagesChecker.checkImagesDir(folderPath)

        if imgsCount > 0:
            self.BImageFolderPathLbl.setText(folderPath)
            self.errorLbl.hide()
        else:
            self.BImageFolderPathLbl.setText("")
            self.errorLbl.setText("The folder you selected doesn't contain any images, please select another one")
            self.errorLbl.show()

    def _saveSettings(self) -> None:
        """Saves the settings modified in dialog"""
        isEnabled = self._getBoosterImgIsEnabled()
        wordGoal = self._getBoosterImgWordGoal()
        imgsFolder = self._getBoosterImgFolder()
        imgsCount = self.imagesChecker.checkImagesDir(imgsFolder)

        if wordGoal and imgsFolder and imgsCount > 0:
            self.settingsReader.setBoosterImagesSettings(isEnabled, int(wordGoal), imgsFolder)

    def _getBoosterImgIsEnabled(self) -> bool:
        """Getter for booster image is enabled

        Returns
        -------
        bool:
            Booster image feature is enabled or not
        """
        return self.BoosterImgSettingsGBox.isChecked()

    def _getBoosterImgWordGoal(self) -> str:
        """Getter for booster image words goal

        Returns
        -------
        str:
            Booster image words goal
        """
        wordGoal = self.BIwordCountInput.text()

        if not wordGoal:
            wordGoal = self.settingsReader.getBoosterImagesSettings()["words-goal"]
            self.BIwordCountInput.setText(wordGoal)

        return wordGoal

    def _getBoosterImgFolder(self) -> str:
        """Getter for booster image folder

        Returns
        -------
        str:
            Booster image folder path
        """
        return self.BImageFolderPathLbl.text()