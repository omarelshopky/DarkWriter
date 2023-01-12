import ctypes.wintypes
from datetime import datetime
import os
from util.SettingsReader import SettingsReader

class PathResolver():
    """A class handle creating new files in app document directory

    Attributes
    ----------
    appDirName : str
        The app directory name

    Methods
    -------
    getNewFilePath()
        Gets the path of the new created file in default dir
    getAppDirPath()
        Gets the path of the app directory
    _getCurrentDateTime()
        Gets current date time in specific formate
    """
    def __init__(self):
        self.appDirName = SettingsReader().getAppDirName()

    def getNewFilePath(self) -> str:
        """Gets the path of the new created file in default dir

        Returns
        -------
        str
            The path to newly created file
        """
        return self.joinPath(self.getAppDirPath(), self._getCurrentDateTime() + '.txt')

    def joinPath(self, dir: str, file: str) -> str:
        """Joins file with directory to get the full path

        Parameters
        ----------
        dir: str
            The directory path
        file: str
            The file name

        Returns
        -------
        str:
            The full path to the file
        """
        return os.path.join(dir, file)

    def getAppDirPath(self) -> str:
        """Gets the path of the app directory

        Returns
        -------
        str
            The path to the app directory
        """
        try:
            try:
                appDirPath = os.path.expanduser(f'~/My Documents/{self.appDirName}/')

                if not os.path.exists(appDirPath):
                    os.makedirs(appDirPath)

                return appDirPath
            except Exception as e:
                CSIDL_PERSONAL = 5       # My Documents
                SHGFP_TYPE_CURRENT = 0   # Get current, not default value

                docDirBuffer = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, docDirBuffer)

                appDirPath = f'{docDirBuffer.value}\\{self.appDirName}'

                if not os.path.exists(appDirPath):
                    os.mkdir(appDirPath, 0o777)

                return appDirPath
        except Exception as e:
            # print(str(e))
            return ""

    def _getCurrentDateTime(self) -> str:
        """Gets current date time in specific formate

        Returns
        -------
        str
            Current datetime
        """
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # dd-mm-YY_Hour-Min-Sec

