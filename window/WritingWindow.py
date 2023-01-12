from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget
from PyQt5.QtCore import QTimer, Qt, QEvent
import keyboard
from cenum.AppWindow import AppWindow
from designPy.writingWindowUI import Ui_WritingWindow
from util.FileHandler import FileHandler
from util.SettingsReader import SettingsReader, BOOSTER_IMAGES_WORDS_GOAL, BOOSTER_IMAGES_IS_ENABLED
from util.WindowSizer import WindowSizer
from widget.BoosterImageWidget import BoosterImageWidget

class WritingWindow(QMainWindow, Ui_WritingWindow):
    """Writing window widget

    Attributes
    ----------
    mainStack : QStackedWidget
        Main stacked widget that contains all the app windows
    fileHandler: FileHandler
        The file handler object that handle saving and loading files
    loadedWords: int
        The Number of words has been loaded
    contentLines: list
        List contains the lines of each paragraph
    wordsCount: list
        List contains the words count of each paragraph
    isDisappearble: bool
        Is the disappearing feature are enable or not
    duringSavingProcess: bool
        Is the app is currently in saving process
    reachMax: bool
        If the user reach the maximum number of lines for a paragraph
    """
    def __init__(self, mainStack: QStackedWidget) -> None:
        super().__init__()
        self.mainStack = mainStack
        self.fileHandler = FileHandler(self)
        self.loadedWords = 0
        self.contentLines = []
        self.wordsCount = [0]
        self.isDisappearable = True
        self.duringSavingProcess = False
        self.reachMax = False
        self.setupUi(self)
        self._setupEvents()
        self._hideNavigation()
        self._setWritingAreaSize()

    def _setupEvents(self) -> None:
        """Setup all events in the UI components"""
        self.saveAndQuitBtn.clicked.connect(lambda: self._saveAndClose())
        self.saveAndContinueBtn.clicked.connect(lambda: self._saveAndContinue())
        self.snoozeBtn.clicked.connect(lambda: self.__addSnooze())
        self.textEdit.document().contentsChanged.connect(lambda: self._setIsDisappearable())
        self.textEdit.installEventFilter(self) # Catch pressing on keyboard

    def _hideNavigation(self) -> None:
        """Hide paragraph navigation arrows"""
        self.nextBtn.hide()
        self.previousBtn.hide()

    def _setWritingAreaSize(self) -> None:
        """Set writing area size according to display resolution"""
        try:
            writingAreaSize = WindowSizer().getWritingAreaSize()
            self.textEdit.setMinimumWidth(writingAreaSize[0])
            self.textEdit.setMaximumWidth(writingAreaSize[0])
            self.textEdit.document().setDocumentMargin(writingAreaSize[1])
        except:
            self.textEdit.document().setDocumentMargin(90)

    def startBlockingSessions(self, filePath: str, isNewDraft: bool, blockingAttributes: dict) -> None:
        """start blocking session

        Parameters
        ----------
        filePath: str
            The file path
        isNewDraft: bool
            if the session is new draft or open existing one
        blockingAttributes: dict
            the blocking attributes like amount and is time or words count
        """
        self._boosterImageWidget = BoosterImageWidget(self)
        self._boosterImgSettings = SettingsReader().getBoosterImagesSettings()
        self._currentBoosterGoal = self._boosterImgSettings[BOOSTER_IMAGES_WORDS_GOAL]
        self._setFilePath(filePath)
        self._setBlocking(blockingAttributes["blockingAmount"], blockingAttributes["isTimeBlocking"])
        self._setNumOfSessions(blockingAttributes["numOfSessions"])
        self.mainStack.setCurrentIndex(AppWindow.WRITING_WINDOW.value)
        self._calculateMaximumHeight()
        self._startTimers()

        if isNewDraft == False:
            self.fileHandler.loadFromFile()
            self.currentParLbl.setText(str(len(writingWindow.contentLines) - 1))
            self.updateContent()
            self._setCursor(writingWindow.textEdit.document().characterCount() - 1)
            self.duringSavingProcess = True

    def _setFilePath(self, path: str) -> None:
        """Set the file path to read and write

        Parameters
        ----------
        path: str
            The file path
        """
        self.filePath = path
        self.fileHandler.setFilePath(path)

    def _setBlocking(self, amount: int, isTime: bool) -> None:
        """Sets Blocking Attributes from the option window

        Parameters
        ----------
        amount: int
            The blocking amount (minutes, words) according to the type
        isTime: bool
            Is the blocking type is time period or words
        """
        self.blockingAmount = amount
        self.blockingInTime = isTime

    def _setNumOfSessions(self, numOfSessions: int) -> None:
        """Sets number of blocking sessions

        Parameters
        ----------
        numOfSessions: int
            the num of blocking sessions
        """
        self.numOfSessions = int(numOfSessions)
        self.currentSession = 1
        self._setSessionLabel()

    def _calculateMaximumHeight(self) -> None:
        """Calculate writing area's line height"""
        self.textEdit.setPlainText('o')
        firstLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.textEdit.setPlainText('o\no')
        secondLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.maxLinesHeight = firstLine + 5 * (secondLine - firstLine)
        self.textEdit.setMaximumHeight(self.maxLinesHeight)
        self.textEdit.setMinimumHeight(self.maxLinesHeight)

    def _startTimers(self) -> None:
        """Start All needed timers"""
        self.progressTimer = QTimer()
        self.progressTimer.timeout.connect(lambda: self._stopProgressTimer())

        self.updateProgressTimer = QTimer()
        self.updateProgressTimer.timeout.connect(lambda: self._updateProgressbar())

        self._activateProgressBar()

        self.wordDisappearTimer = QTimer()
        self.wordDisappearTimer.timeout.connect(lambda: self._disappearWord())
        self.wordDisappearTimer.start(3000)

        self.checkLinesTimer = QTimer()
        self.checkLinesTimer.timeout.connect(lambda: self._checkLines())
        self.checkLinesTimer.start(10)

        self.fileHandler.enableAutosave()

    def _restartWordDisappearTimer(self):
        """Restart the word disappear timer"""
        self.wordDisappearTimer.start(3000)

    def _activateProgressBar(self) -> None:
        """Active progress bar timer"""
        self._hideEndSessionBtns()

        if self.blockingInTime:
            self._startProgressTimer(self.blockingAmount)

        if self.blockingAmount != 0:
            self.updateProgressTimer.start(1000)
        else:
            self._showEndSessionBtns()

    def _updateProgressbar(self) -> None:
        """Update the progress value and restart the timer if not 100%"""
        if int(self._updateProgressValue()) == 100:
            self._showEndSessionBtns()
            self.duringSavingProcess = True
            self.updateProgressTimer.stop()

    def _updateProgressValue(self) -> float:
        """Update the progress bar value

        Returns
        -------
        int
            progress value in percent
        """
        wordsTyped = self._getWordsTyped()

        if self.blockingInTime:
            remain = self.progressTimer.remainingTime() / 60000
        else:
            remain = int(self.blockingAmount) - wordsTyped

        amount = 100 - ((remain / int(self.blockingAmount)) * 100)

        self.progressBar.setValue(amount)
        self._checkBoosterGoal(wordsTyped)

        return amount

    def _startProgressTimer(self, timeInMin: str) -> None:
        """Start the progress timer for time blocking sessions

        Parameters
        ----------
        timeInMin: int
            The time period of blocking in minutes
        """
        self.progressTimer.start(int(timeInMin) * 60000)

    def _stopProgressTimer(self) -> None:
        """Stop the progress timer for time blocking sessions"""
        self.progressTimer.stop()

    def _showEndSessionBtns(self) -> None:
        """Show snooze and Quit buttons with hiding progress bar"""
        self.progressBar.hide()
        self.sessionLbl.hide()

        if self.currentSession == self.numOfSessions:
            self.snoozeBtn.show()
            self.saveAndQuitBtn.show()
        else:
            self.saveAndContinueBtn.show()

    def _hideEndSessionBtns(self) -> None:
        """Hide snooze and Quit buttons with showing progress bar"""
        self.progressBar.show()
        self.sessionLbl.show()
        self.snoozeBtn.hide()
        self.saveAndQuitBtn.hide()
        self.saveAndContinueBtn.hide()
        self.progressBar.setValue(0)

    def _saveAndClose(self):
        """Saves the file and close the app if success"""
        if self._saveSession():
            self._closeApp()

    def _saveAndContinue(self):
        """Saves the file and continue the next session"""
        if self._saveSession():
            self.currentSession += 1
            self._setSessionLabel()
            self.loadedWords += self._getWordsTyped()
            self._currentBoosterGoal = self._boosterImgSettings[BOOSTER_IMAGES_WORDS_GOAL]
            self.duringSavingProcess = False
            self._activateProgressBar()

    def _saveSession(self):
        """Saves the current content to file"""
        self.duringSavingProcess = True
        savingStatus = self.fileHandler.saveToFile(False)
        self.duringSavingProcess = not savingStatus
        self._restartWordDisappearTimer()

        return savingStatus

    def _closeApp(self) -> None:
        """Closes the app"""
        self.mainStack.close()

    def _addSnooze(self):
        """Block for additional 10 minutes"""
        self.duringSavingProcess = False
        self._setBlocking(10, True)
        self._activateProgressBar()

    def setContent(self) -> None:
        """Set writing area content according to current paragraph index"""
        paragraphIndex = int(self.currentParLbl.text())

        if len(self.contentLines) < paragraphIndex + 1:
            self.contentLines.append(self.textEdit.toPlainText().split('\n'))
            self.wordsCount.append(0)
        else:
            self.contentLines[paragraphIndex] = self.textEdit.toPlainText().split('\n')

        self.countWords(paragraphIndex)

    def updateContent(self) -> None:
        """Update writing area content"""
        self.textEdit.clear()
        self.textEdit.setPlainText('\n'.join(self.contentLines[int(self.currentParLbl.text())]))

    def countWords(self, paragraphIndex: int) -> None:
        """Count number of words in the current paragraph

        Parameters
        ----------
        paragraphIndex: int
            The paragraph index to count its words
        """
        currentParagraphWords = 0
        for line in self.contentLines[paragraphIndex]:
            for word in line.split(' '):
                if word != '' and word != ' ':
                    currentParagraphWords += 1

        if len(self.wordsCount) < paragraphIndex + 1:
            self.wordsCount.append(0)

        self.wordsCount[paragraphIndex] = currentParagraphWords

    def _getWordsTyped(self) -> int:
        """Gets number of words in the whole file

        Returns
        -------
        int
            Number of words in the whole file
        """
        self.setContent()
        currentWords = sum(self.wordsCount)

        if currentWords < self.loadedWords:
            self.loadedWords = currentWords
            return 0
        else:
            return currentWords - self.loadedWords

    def _disappearWord(self) -> None:
        """Remove the last word from the content"""
        if self.isDisappearable and not self.duringSavingProcess:
            self.setContent()
            index = int(self.currentParLbl.text())

            if self.contentLines[index][-1] == '':
                if len(self.contentLines[index]) > 1:
                    self.contentLines[index].pop()

                else:
                    if index != 0:
                        self.contentLines.pop(int(self.currentParLbl.text()))
                        self._previousParagraph(False)
                        index = int(self.currentParLbl.text())

            if len(self.contentLines[index]) != 0:
                line = self.contentLines[index][-1]
                self.contentLines[index][-1] = ' '.join(line.split(' ')[:-1])

            self.updateContent()
            self._setCursor(self.textEdit.document().characterCount() - 1) # Set cursor at the end of text

        self.isDisappearable = True

    def _setCursor(self, position: int) -> None:
        """Set the cursor in specific position

        Parameters
        ----------
        position: int
            The position to set cursor to
        """
        cursor = self.textEdit.textCursor()
        cursor.setPosition(cursor.position() + position)
        self.textEdit.setTextCursor(cursor)

    def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
        """Detect pressing Enter

        Parameters
        ----------
        obj:
            The object that fetch the event
        event:
            The pressing event

        Returns
        -------
        bool
            Is the saving process done successfully or not
        """
        if event.type() == QEvent.KeyPress and obj is self.textEdit:
            index = int(self.currentParLbl.text())

            if event.key() == Qt.Key_Return and self.textEdit.hasFocus():
                self._createNewParagraph()

            if (event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete) and self.textEdit.hasFocus():
                self.setContent()

                if self.contentLines[index][-1] == '' and len(self.contentLines[index]) <= 1 and index != 0 and self.reachMax == False:
                    self.contentLines.pop(index)
                    self.contentLines[index-1][-1] += ' '
                    self._previousParagraph(False)
                    self._setCursor(self.textEdit.document().characterCount() - 1) # Set cursor at the end of text

            # if event.key() == Qt.Key_Escape and self.textEdit.hasFocus():
            #     self.close()
            #     self.mainStack.close()

        return super().eventFilter(obj, event)

    def _checkLines(self) -> None:
        """Check that lines reach maximum"""
        if self.textEdit.document().size().height() > self.maxLinesHeight:
            index = int(self.currentParLbl.text())
            # Remove the last character
            self.reachMax = True
            self.setContent()
            lastChar = self.contentLines[index][-1][-1]
            keyboard.press_and_release('backspace')
            self._createNewParagraph()
            self.contentLines[index][-1] = self.contentLines[index][-1][:-1]
            self.contentLines[index+1][0] = lastChar
            self.updateContent()
            keyboard.press_and_release('right')
        else:
            self.reachMax = False

    def _createNewParagraph(self) -> None:
        """Create new paragraph"""
        self.setContent()

        if int(self.currentParLbl.text()) < len(self.contentLines)-1:
            self._nextParagraph()
        else:
            self.contentLines.append([])
            self.wordsCount.append(0)
            self.currentParLbl.setText(str(int(self.currentParLbl.text())+1))
            self.updateContent()

        keyboard.press_and_release('backspace') # Remove the additional new line
        self.fileHandler.saveToFile() # Save the file

    def _setIsDisappearable(self, isDisappearable: bool = False) -> None:
        """Set is disapperable attribute

        Parameters
        ----------
        isDisappearable: bool
            The attribute value
        """
        self.isDisappearable = isDisappearable
        if isDisappearable: self._restartWordDisappearTimer()

    def _nextParagraph(self):
        """Go to the next paragraph"""
        if int(self.currentParLbl.text()) < len(self.contentLines) - 1:
            self.setContent()
            self.currentParLbl.setText(str(int(self.currentParLbl.text()) + 1))
            self.updateContent()

    def _previousParagraph(self, isSet = True):
        """Go back to the previous paragraph

        Parameters
        ----------
        isSet: bool
            whether to set content or not
        """
        if int(self.currentParLbl.text()) > 0:
            if isSet: self.setContent()
            self.currentParLbl.setText(str(int(self.currentParLbl.text()) - 1))
            self.updateContent()

    def _setSessionLabel(self):
        """Sets session label with current progress"""
        self.sessionLbl.setText(f"Session {self.currentSession} of {self.numOfSessions}")

    def _checkBoosterGoal(self, wordsTyped):
        if self._boosterImgSettings[BOOSTER_IMAGES_IS_ENABLED] and wordsTyped >= self._currentBoosterGoal:
            self._boosterImageWidget.display()
            self._currentBoosterGoal += self._boosterImgSettings[BOOSTER_IMAGES_WORDS_GOAL]