import json
import util.PathResolver as PathResolver

USER_SETTINGS_KEYS = ["booster-images"]
DEFAULT_SETTINGS_FILE_PATH = "./settings.json"
APP_DIR_NAME = "app-dir-name"
SAVING_STATUS_MESSAGE = "saving-status-message"
WRITING_AREA_SIZE = "writing-area-size"
AUTOSAVE_PERIOD = "autosave-period"
USER_SETTINGS_FILE_NAME = "user-settings-file-name"
BOOSTER_IMAGES = "booster-images"
BOOSTER_IMAGES_IS_ENABLED = "enabled"
BOOSTER_IMAGES_WORDS_GOAL = "words-goal"
BOOSTER_IMAGES_FOLDER_PATH = "images-folder"

class SettingsReader:
    """Singleton Class handle reading app settings from json file

    Attributes
    ----------
    settings : dict
        Dictionary hold all the app settings

    Methods
    -------
    _loadSettings()
        Loads the app settings
    _loadDefaultSettings()
        Loads the default settings registered in the app
    _loadUserSettings()
        Loads the user settings located locally
    _loadSettingsFromJson()
        Loads the settings from json file as dictionary.
    _saveUserSettingsToJson()
        Saves the user settings to json file
    _getSettings()
        Gets the settings dictionary.
    _setSettings(key, value)
        Sets specific setting by key.
    getAppDirName()
        Get app directory name from settings
    getSaveStatusSettings()
        Get settings related to save status.
    getWritingAreaSizeSettings()
        Get settings related to writing area sizes.
    getAutosavePeriod()
        Get auto save period specified in settings
    getBoosterImagesSettings()
        Get auto save period specified in settings
    """
    _instance = None

    def __new__(cls):
        """Override to be a singleton class"""
        if cls._instance is None:
            cls._instance = super(SettingsReader, cls).__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_settings"):
            self._loadSettings()

    def _loadSettings(self) -> None:
        """Loads the app settings"""
        self._loadDefaultSettings()
        self._pathResolver = PathResolver.PathResolver()
        self._loadUserSettings()

    def _loadDefaultSettings(self) -> None:
        """Loads the default settings registered in the app"""
        self._settings = self._loadSettingsFromJson(DEFAULT_SETTINGS_FILE_PATH)

    def _loadUserSettings(self) -> None:
        """Loads the user settings located locally"""
        self._userSettings = self._loadSettingsFromJson(self.getUserSettingsFilePath())

        for settingKey in self._userSettings:
            self._settings[settingKey] = self._userSettings[settingKey]

    def _loadSettingsFromJson(self, settingsFilePath: str) -> dict:
        """Loads the settings from json file as dictionary.

        Parameters
        ----------
        settingsFilePath: str
            the json file name contains the settings
        Returns
        -------
        dict
            Dictionary hold all the app settings
        """
        try:
            with open(settingsFilePath) as settingsFile:
                return json.load(settingsFile)
        except Exception as e:
            return {}

    def _saveUserSettingsToJson(self) -> None:
        """Saves the user settings to json file"""
        with open(self.getUserSettingsFilePath(), "w") as userSettingsFile:
            json.dump(self._userSettings, userSettingsFile)

    def _getSettings(self) -> dict:
        """Gets the settings dictionary.

        Returns
        -------
        dict
            Dictionary hold all the app settings
        """
        return self._settings

    def _setSettings(self, key: str, value) -> None:
        """Sets specific setting by key.

        Parameters
        ----------
        key: str
            the key of the setting
        value: any
            the new value of the setting
        """
        self._settings[key] = value

        if key in USER_SETTINGS_KEYS:
            self._userSettings[key] = value
            self._saveUserSettingsToJson()

    def getAppDirName(self) -> str:
        """Get app directory name from settings

        Returns
        -------
        str
            App directory name
        """
        return self._getSettings()[APP_DIR_NAME]

    def getSaveStatusSettings(self) -> dict:
        """Get settings related to save status.

        Returns
        -------
        dict
            Dictionary hold settings related to save status
        """
        return self._getSettings()[SAVING_STATUS_MESSAGE]

    def getWritingAreaSizeSettings(self) -> dict:
        """Get settings related to writing area sizes.

        Returns
        -------
        dict
            Dictionary hold settings related to writing area sizes
        """
        return self._getSettings()[WRITING_AREA_SIZE]

    def getAutosavePeriod(self) -> int:
        """Get auto save period specified in settings

        Returns
        -------
        int
            autosaving period specified in millisecond
        """
        return self._getSettings()[AUTOSAVE_PERIOD]

    def getUserSettingsFilePath(self) -> str:
        """Get user settings file path

        Returns
        -------
        str
            path to user settings file
        """
        return self._pathResolver.joinPath(self._pathResolver.getAppDirPath(), self._settings[USER_SETTINGS_FILE_NAME])

    def getBoosterImagesSettings(self) -> dict:
        """Get booster images settings

        Returns
        -------
        dict
            Dictionary hold settings related to booster images feature
        """
        return self._getSettings()[BOOSTER_IMAGES]

    def setBoosterImagesSettings(self, isEnabled: bool, wordGoal: int, imgFolder: str) -> None:
        """Sets booster images settings

        Parameters
        ----------
        isEnabled: bool
            Is the booster image feature is enabled or not
        wordGoal: int
            the number of words need to achieve to display a booster
        imgFolder: str
            the folder that contains the images to display
        """
        self._setSettings(
            BOOSTER_IMAGES,
            {
                BOOSTER_IMAGES_IS_ENABLED: isEnabled,
                BOOSTER_IMAGES_WORDS_GOAL: wordGoal,
                BOOSTER_IMAGES_FOLDER_PATH: imgFolder
            }
        )