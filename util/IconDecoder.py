from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QByteArray
import json
from config.icons import icons

class IconDecoder:
    """Singleton Class handle decoding icons from base64

    Attributes
    ----------
    _icons : dict
        Dictionary hold all the icons encode

    Methods
    -------
    _getEncodedIcon(iconKey)
        Get specific icon from encode dict
    getDecodedIcon(iconKey)
        Get specific icon as QIcon object
    """
    _instance = None

    def __new__(cls):
        """Override to be a singleton class"""
        if cls._instance is None:
            cls._instance = super(IconDecoder, cls).__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_icons"):
            self._icons = icons

    def _getEncodedIcon(self, iconKey: str) -> str:
        """Get specific icon from encode dict

        Parameters
        ----------
        iconKey: str
            The key of the icon required

        Returns
        -------
        str
            Dictionary hold all the icons encode
        """
        return bytes(self._icons[iconKey], 'ascii')

    def getDecodedIcon(self, iconKey: str) -> QIcon:
        """Get specific icon as QIcon object

        Parameters
        ----------
        iconKey: str
            The key of the icon required

        Returns
        -------
        QIcon
            the required icon as an object
        """
        try:
            iconBase64 = self._getEncodedIcon(iconKey)
            iconPixmap = QPixmap()
            iconPixmap.loadFromData(QByteArray.fromBase64(iconBase64))
            return QIcon(iconPixmap)
        except Exception as e:
            return None