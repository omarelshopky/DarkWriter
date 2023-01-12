import imghdr
import os
from util.SettingsReader import SettingsReader, BOOSTER_IMAGES_FOLDER_PATH
from util.PathResolver import PathResolver

class ImagesChecker:
    """Singleton Class handle reading app settings from json file

    Attributes
    ----------
    settings : dict
        Dictionary hold all the app settings

    Methods
    -------
    _checkIsImage(filePath)
        Check if the file is image or not
    checkImagesDir(dirPath)
        Check the directory content
    getBoosterImages()
        Get the available images to the booster feature
    """
    _instance = None

    def __new__(cls):
        """Override to be a singleton class"""
        if cls._instance is None:
            cls._instance = super(ImagesChecker, cls).__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_pathResolver"):
            self._boosterImages = []
            self._pathResolver = PathResolver()

    def _checkIsImage(self, filePath: str) -> bool:
        """Check if the file is image or not

        Parameters
        ----------
        filePath: str
            The path of the file need to be checked

        Returns
        -------
        bool
            true: is image, false: text file
        """
        if not os.path.isdir(filePath) and imghdr.what(filePath) is not None:
            return True
        else:
            return False

    def checkImagesDir(self, dirPath: str) -> int:
        """Check the directory content

        Parameters
        ----------
        dirPath: str
            The path of the dir need to be checked

        Returns
        -------
        int
            the number of images found in the directory
        """
        try:
            self._boosterImages = []

            for file in os.listdir(dirPath):
                filePath = self._pathResolver.joinPath(dirPath, file)

                if self._checkIsImage(filePath):
                    self._boosterImages.append(filePath)

            return len(self._boosterImages)
        except Exception as e:
            return 0

    def getBoosterImages(self) -> list:
        """Get the available images to the booster feature

        Returns
        -------
        list
            Contains paths to the booster images
        """
        self.checkImagesDir(SettingsReader().getBoosterImagesSettings()[BOOSTER_IMAGES_FOLDER_PATH])
        return self._boosterImages