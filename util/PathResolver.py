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
        try:
            try:
                defaultPath = os.path.expanduser(f'~/My Documents/{self.appDirName}/')

                if not os.path.exists(defaultPath):
                    os.makedirs(defaultPath)

                filePath = os.path.join(defaultPath, self._getCurrentDateTime() + '.txt')
            except Exception as e:
                # print(str(e))

                CSIDL_PERSONAL = 5       # My Documents
                SHGFP_TYPE_CURRENT = 0   # Get current, not default value

                docDirBuffer = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, docDirBuffer)

                defaultPath = f'{docDirBuffer.value}\\{self.appDirName}'

                if not os.path.exists(defaultPath):
                    os.mkdir(defaultPath, 0o777)

                filePath = os.path.join(defaultPath, self._getCurrentDateTime() + '.txt')
        except Exception as e:
            # print(str(e))
            pass

        return filePath

    def _getCurrentDateTime(self) -> str:
        """Gets current date time in specific formate

        Returns
        -------
        str
            Current datetime
        """
        return datetime.now().strftime("%Y-%m-%d_%H-%M") # dd-mm-YY_H-M

