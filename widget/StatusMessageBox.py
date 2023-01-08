from PyQt5.QtWidgets import QMessageBox, QMainWindow
from util.SettingsReader import SettingsReader


class StatusMessageBox(QMessageBox):
    """A widget displays status in a message box

    Methods
    -------
    _display(title, content)
        Popup message box with specific title and content.
    displaySuccess(filePath)
        Display that saving done successfully at specific path.
    displayFail(filePath)
        Display that saving failed at specific path.
    """
    def __init__(self, parentWindow: QMainWindow) -> None:
        """SaveStatus Constructor

        Parameters
        ----------
        parentWindow: QMainWindow
            the parent window that call the message box.
        """
        super().__init__(parentWindow)
        self.settings = SettingsReader().getSaveStatusSettings()

    def _display(self, status: str, filePath: str) -> bool:
        """Popup message box with specific title and content.

        Parameters
        ----------
        status: str
            The status of saving process
        filePath: str
            Path tried to save in.

        Returns
        -------
        bool
            Is the user click ok button or not
        """
        self.setWindowTitle(self.settings[status]["title"])
        self.setText(self._prepareContent(self.settings[status]["content"], filePath))

        return self.exec() == QMessageBox.Ok

    def displaySuccess(self, filePath: str) -> bool:
        """Display that saving done successfully at specific path.

        Parameters
        ----------
        filePath: str
            path tried to save in.

        Returns
        -------
        bool
            Is the user click ok button or not
        """
        return self._display("success", filePath)

    def displayFail(self, filePath: str) -> bool:
        """Display that saving failed at specific path.

        Parameters
        ----------
        filePath: str
            path tried to save in.

        Returns
        -------
        bool
            Is the user click ok button or not
        """
        return self._display("fail", filePath)

    def _prepareContent(self, content: str, filePath: str) -> str:
        return content.replace('FILE_PATH', filePath)
