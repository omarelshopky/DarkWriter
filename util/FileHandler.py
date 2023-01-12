from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtCore import QTimer
import os
from util.SettingsReader import SettingsReader
from widget.StatusMessageBox import StatusMessageBox


class FileHandler:
    """A class handle saving and loading processes

    Attributes
    ----------
    writingWindow: QMainWindow
        The writing window that contains the writing ares
    statusMessageBox: StatusMessageBox
        Status message box to show notification to user
    autosaveTimer: QTimer
        Timer to handle saving the file each specific period

    Methods
    -------
    enableAutosave()
        Enable saving the file automatically each specific period.
    setFilePath(path)
        Set the file path to save or load from
    saveToFile(isAuto=True)
        Save the text to file
    loadFromFile()
        Load the text from file
    """
    def __init__(self, writingWindow: QMainWindow):
        self.writingWindow = writingWindow
        self.statusMessageBox = StatusMessageBox(writingWindow)
        self.autosaveTimer = QTimer()

    def enableAutosave(self) -> None:
        """Enable saving the file automatically each specific period."""
        self.autosaveTimer.timeout.connect(lambda: self.saveToFile())
        self.autosaveTimer.start(SettingsReader().getAutosavePeriod())

    def setFilePath(self, path: str) -> None:
        """Set the file path to save or load from

        Parameters
        ----------
        path: str
            The file path
        """
        self._filePath = path.replace('\\', '/')

    def saveToFile(self, isAuto: bool = True):
        """Save the text to file

        Parameters
        ----------
        isAuto: bool
            Is autosave process or user prompted save

        Returns
        -------
        bool
            Is the saving process done successfully or not
        """
        try:
            self.writingWindow.setContent()

            if not isAuto:
                # Open browse to enable user to choose a location
                fname = QFileDialog.getSaveFileName(self.writingWindow, 'Save File', self._filePath, 'Text Files (*.txt)')[0]

                if fname != '':
                    self._filePath = fname
                else:
                    return False

            if os.path.exists(self._filePath):
                os.remove(self._filePath)

            with open(self._filePath, 'w') as file:
                text = ''
                for paragraph in self.writingWindow.contentLines:
                    text += ' '.join(paragraph)
                    text += '\n\n'

                file.write(text)
                del text
                file.close()

            if not isAuto:
                self.statusMessageBox.displaySuccess(self._filePath)

            return True

        except Exception as e:
            self.statusMessageBox.displayFail(self._filePath + '\n' + str(e))
            return False

    def loadFromFile(self) -> None:
        """Load the text from file"""
        contentLines = []

        with open(self._filePath, 'r') as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line: contentLines.append([line])

            del lines
            file.close()

        self.writingWindow.contentLines = contentLines

        paragraphIndex = 0
        for p in contentLines:
            self.writingWindow.countWords(paragraphIndex)
            paragraphIndex += 1

        self.writingWindow.loadedWords = sum(self.writingWindow.wordsCount)
        self.writingWindow.updateContent()
