from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget
from PyQt5.QtCore import QTimer, Qt, QEvent
import keyboard
from designPy.writingWindowUI import Ui_WritingWindow
from util.FileHandler import FileHandler
from util.WindowSizer import WindowSizer

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
    saving: bool
        Is the app is currently in saving process
    reachMax: bool
        If the user reach the maximum number of lines for a paragraph

    Methods
    -------
    _setupEvents()
        Setup all events in the UI components
    _setWritingAreaSize()
        Set writing area size according to display resolution
    _hideNavigation()
        Hide paragraph navigation arrows
    calculateLineHeight()
        Calculate writing area's line height
    setBlocking(amount, isTime)
        Sets Blocking Attributes from the option window
    setFilePath(path)
        Set the file path to read and write
    _startTimers()
        Start All needed timers
    _activateProgressBar()
        Active progress bar timer
    _updateProgressbar()
        Update the progress value and restart the timer if not 100%
    _updateProgressValue()
        Update the progress bar value
    _startProgressTimer(timeInMin)
        Start the progress timer for time blocking sessions
    _stopProgressTimer()
        Stop the progress timer for time blocking sessions
    _showEndSessionBtns()
        Show snooze and Quit buttons with hiding progress bar
    _hideEndSessionBtns()
        Hide snooze and Quit buttons with showing progress bar
    _closeApp()
        Saves the file and Closes the app
    _addSnooze()
        Block for additional 10 minutes
    setContent()
        Set writing area content according to current paragraph index
    updateContent()
        Update writing area content
    countWords(paragraphIndex)
        Count number of words in the current paragraph
    _getWordsTyped()
        Gets number of words in the whole file
    _disapearWord()
        Remove the last word from the content
    setCursor(position)
        Set the cursor in specific position
    eventFilter(obj, event)
        Detect pressing Enter
    _checkLines()
        Check that lines reach maximum
    _createNewParagraph()
        Create new paragraph
    _setIsDisappearable(isDisappearable=False)
        Set is disapperable attribute
    _nextParagraph()
        Go to the next paragraph
    _previousParagraph(isSet=True)
        Go back to the previous paragraph
    """
    def __init__(self, mainStack: QStackedWidget) -> None:
        super().__init__()
        self.mainStack = mainStack
        self.fileHandler = FileHandler(self)
        self.loadedWords = 0
        self.contentLines = []
        self.wordsCount = [0]
        self.isDisappearable = True
        self.saving = False
        self.reachMax = False
        self.setupUi(self)
        self._setupEvents()
        self._hideNavigation()

    def _setupEvents(self) -> None:
        """Setup all events in the UI components"""
        self.saveAndQuitBtn.clicked.connect(lambda: self._closeApp())
        self.snoozeBtn.clicked.connect(lambda: self.__addSnooze())
        self.textEdit.document().contentsChanged.connect(lambda: self._setIsDisappearable())
        self.textEdit.installEventFilter(self) # Catch pressing on keyboard

    def _setWritingAreaSize(self) -> None:
        """Set writing area size according to display resolution"""
        try:
            writingAreaSize = WindowSizer().getWritingAreaSize()
            self.textEdit.setMinimumWidth(writingAreaSize[0])
            self.textEdit.setMaximumWidth(writingAreaSize[0])
            self.textEdit.document().setDocumentMargin(writingAreaSize[1])
        except:
            self.textEdit.document().setDocumentMargin(90)

    def _hideNavigation(self) -> None:
        """Hide paragraph navigation arrows"""
        self.nextBtn.hide()
        self.previousBtn.hide()

    def calculateLineHeight(self) -> None:
        """Calculate writing area's line height"""
        self._setWritingAreaSize()
        self.textEdit.setPlainText('o')
        firstLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.textEdit.setPlainText('o\no')
        secondLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.maxLinesHeight = firstLine + 5 * (secondLine - firstLine)
        self.textEdit.setMaximumHeight(self.maxLinesHeight)
        self.textEdit.setMinimumHeight(self.maxLinesHeight)

    def setBlocking(self, amount: int, isTime: bool) -> None:
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

    def setFilePath(self, path: str) -> None:
        """Set the file path to read and write

        Parameters
        ----------
        path: str
            The file path
        """
        self.filePath = path
        self.fileHandler.setFilePath(path)
        self._startTimers()

    def _startTimers(self) -> None:
        """Start All needed timers"""
        self.progressTimer = QTimer()
        self.progressTimer.timeout.connect(lambda: self._stopProgressTimer())

        self.updateProgressTimer = QTimer()
        self.updateProgressTimer.timeout.connect(lambda: self._updateProgressbar())

        self._activateProgressBar()

        self.wordDisappearTimer = QTimer()
        self.wordDisappearTimer.timeout.connect(lambda: self._disapearWord())
        self.wordDisappearTimer.start(3000)

        self.checkLinesTimer = QTimer()
        self.checkLinesTimer.timeout.connect(lambda: self._checkLines())
        self.checkLinesTimer.start(10)

        self.fileHandler.enableAutosave()

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
            self.saving = True
            self.updateProgressTimer.stop()

    def _updateProgressValue(self) -> float:
        """Update the progress bar value

        Returns
        -------
        int
            progress value in percent
        """
        if self.blockingInTime:
            remain = self.progressTimer.remainingTime() / 60000
        else:
            remain = int(self.blockingAmount) - self._getWordsTyped()

        amount = 100 - ((remain / int(self.blockingAmount)) * 100)

        self.progressBar.setValue(amount)

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
        self.snoozeBtn.show()
        self.saveAndQuitBtn.show()

    def _hideEndSessionBtns(self) -> None:
        """Hide snooze and Quit buttons with showing progress bar"""
        self.progressBar.show()
        self.snoozeBtn.hide()
        self.saveAndQuitBtn.hide()
        self.progressBar.setValue(0)

    def _closeApp(self) -> None:
        """Saves the file and Closes the app"""
        self._setIsDisappearable()

        if self.fileHandler.saveToFile(False) == True: # Successfully save the file
            self.close()
            self.mainStack.close()

    def _addSnooze(self):
        """Block for additional 10 minutes"""
        self.saving = False
        self.setBlocking(10, True)
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

    def _disapearWord(self) -> None:
        """Remove the last word from the content"""
        if self.isDisappearable and not self.saving:
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
            self.setCursor(self.textEdit.document().characterCount() - 1) # Set cursor at the end of text

        self.isDisappearable = True

    def setCursor(self, position: int) -> None:
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
                    self.setCursor(self.textEdit.document().characterCount() - 1) # Set cursor at the end of text

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
