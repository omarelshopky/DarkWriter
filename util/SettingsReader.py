import json

class SettingsReader:
    """Singleton Class handle reading app settings from json file

    Attributes
    ----------
    settings : dict
        Dictionary hold all the app settings

    Methods
    -------
    _loadSettingsFromJson()
        Loads the settings from json file as dictionary.
    _getSettings()
        Gets the settings dictionary.
    getAppDirName()
        Get app directory name from settings
    getSaveStatusSettings()
        Get settings related to save status.
    getWritingAreaSizeSettings()
        Get settings related to writing area sizes.
    getAutosavePeriod()
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
            self._settings = self._loadSettingsFromJson()

    def _loadSettingsFromJson(self) -> dict:
        """Loads the settings from json file as dictionary.

        Returns
        -------
        dict
            Dictionary hold all the app settings
        """
        with open("./settings.json") as settingsFile:
            return json.load(settingsFile)

    def _getSettings(self) -> dict:
        """Gets the settings dictionary.

        Returns
        -------
        dict
            Dictionary hold all the app settings
        """
        return self._settings

    def getAppDirName(self) -> str:
        """Get app directory name from settings

        Returns
        -------
        str
            App directory name
        """
        return self._getSettings()["app-dir-name"]

    def getSaveStatusSettings(self) -> dict:
        """Get settings related to save status.

        Returns
        -------
        dict
            Dictionary hold settings related to save status
        """
        return self._getSettings()["saving-status-message"]

    def getWritingAreaSizeSettings(self) -> dict:
        """Get settings related to writing area sizes.

        Returns
        -------
        dict
            Dictionary hold settings related to writing area sizes
        """
        return self._getSettings()["writing-area-size"]

    def getAutosavePeriod(self) -> dict:
        """Get auto save period specified in settings

        Returns
        -------
        int
            autosaving period specified in millisecond
        """
        return self._getSettings()["autosave-period"]