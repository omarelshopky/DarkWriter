from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QMainWindow, QFileDialog
from designPy.settingsDialogUI import Ui_SettingsDialog
from util.ImagesChecker import ImagesChecker
from util.SettingsReader import SettingsReader, IS_ENABLED, WORD_DISAPPEARING_INTERVAL, BOOSTER_IMAGES_WORDS_GOAL, BOOSTER_IMAGES_FOLDER_PATH

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
        self.WDintervalInput.setValidator(QIntValidator())

    def _loadSettings(self) -> None:
        """Loads the settings to the dialog inputs"""
        self._loadBoosterImageSettings()
        self._loadWordDisappearingSettings()

    def _loadBoosterImageSettings(self) -> None:
        boosterImgSettings = self.settingsReader.getBoosterImagesSettings()
        self.BoosterImgSettingsGBox.setChecked(boosterImgSettings[IS_ENABLED])
        self.BIwordCountInput.setText(str(boosterImgSettings[BOOSTER_IMAGES_WORDS_GOAL]))
        self.BImageFolderPathLbl.setText(boosterImgSettings[BOOSTER_IMAGES_FOLDER_PATH])

    def _loadWordDisappearingSettings(self) -> None:
        wordDisappearSettings = self.settingsReader.getWordDisappearingSettings()
        self.WordDisSettingsGBox.setChecked(wordDisappearSettings[IS_ENABLED])
        self.WDintervalInput.setText(str(wordDisappearSettings[WORD_DISAPPEARING_INTERVAL]))

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
        self._saveBoosterImageSettings()
        self._saveWordDisappearingSettings()

    def _saveBoosterImageSettings(self) -> None:
        isEnabled = self._getBoosterImgIsEnabled()
        wordGoal = self._getBoosterImgWordGoal()
        imgsFolder = self._getBoosterImgFolder()
        imgsCount = self.imagesChecker.checkImagesDir(imgsFolder)

        if wordGoal and imgsFolder and imgsCount > 0:
            self.settingsReader.setBoosterImagesSettings(isEnabled, int(wordGoal), imgsFolder)

    def _saveWordDisappearingSettings(self) -> None:
        isEnabled = self._getWordDisappearingIsEnabled()
        interval = self._getWordDisappearingInterval()
        self.settingsReader.setWordDisappearingSettings(isEnabled, interval)

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
            wordGoal = self.settingsReader.getBoosterImagesSettings()[BOOSTER_IMAGES_WORDS_GOAL]
            self.BIwordCountInput.setText(str(wordGoal))

        return wordGoal

    def _getBoosterImgFolder(self) -> str:
        """Getter for booster image folder

        Returns
        -------
        str:
            Booster image folder path
        """
        return self.BImageFolderPathLbl.text()

    def _getWordDisappearingIsEnabled(self) -> bool:
        """Getter for word disappearing is enabled

        Returns
        -------
        bool:
            word disappearing feature is enabled or not
        """
        return self.WordDisSettingsGBox.isChecked()

    def _getWordDisappearingInterval(self) -> int:
        """Getter for word disappearing interval

        Returns
        -------
        int:
            word disappearing interval
        """
        interval = self.WDintervalInput.text()

        if not interval:
            interval = self.settingsReader.getWordDisappearingSettings()[WORD_DISAPPEARING_INTERVAL]
            self.WDintervalInput.setText(str(interval))

        return int(interval)