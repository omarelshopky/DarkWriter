from UI.writingWindowUI import Ui_WritingWindow
from components.FileHandler import FileHandler
from components.writingSize import getSize
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
import keyboard




class WritingWindow(QMainWindow, Ui_WritingWindow):

    def __init__(self, widget):
        super().__init__()
        self.fileHandler = FileHandler(self)
        self.loadedWords = 0
        self.contentLines = []
        self.wordsCount = [0]
        self.isDisappearable = True
        self.saving = False
        self.reachMax = False
        self.mainWidget = widget
        self.setupUi(self)
        self.UiComponentsEvent()
        self.hideNavigation()
        # self.previousBtn.setIcon(self.iconFromBase64(leftArrow))
        # self.nextBtn.setIcon(self.iconFromBase64(rightArrow))


    # def iconFromBase64(self, base64):
    #     pixmap = QPixmap()
    #     pixmap.loadFromData(QByteArray.fromBase64(base64))
    #     icon = QIcon(pixmap)
    #     return icon

    def calculateLineHeight(self):
        try:
            writingAreaSize = getSize()
            self.textEdit.setMinimumWidth(writingAreaSize[0])
            self.textEdit.setMaximumWidth(writingAreaSize[0])
            self.textEdit.document().setDocumentMargin(writingAreaSize[1])
        except:
            self.textEdit.document().setDocumentMargin(90)

        self.textEdit.setPlainText('o')
        firstLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.textEdit.setPlainText('o\no')
        secnondLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.maxLinesHeight = firstLine + 5 * (secnondLine - firstLine)
        self.textEdit.setMaximumHeight(self.maxLinesHeight)
        self.textEdit.setMinimumHeight(self.maxLinesHeight)



    def hideNavigation(self):
        self.nextBtn.hide()
        self.previousBtn.hide()

    def UiComponentsEvent(self):
        # Saves the file and Closes the app 
        self.saveAndQuitBtn.clicked.connect(lambda:self.closeApp())
    
        # Block additional 10min
        self.snoozeBtn.clicked.connect(lambda:self.addSnooze())

        self.textEdit.document().contentsChanged.connect(lambda:self.setIsDisappearable())
        
        # self.nextBtn.clicked.connect(lambda:self.nextParagraph())
        # self.previousBtn.clicked.connect(lambda:self.previousParagraph())

        # Catch pressing on keyboard
        self.textEdit.installEventFilter(self)


    # Sets Blocking Attributes from the calling Windows
    def setBlocking(self, amount, isTime):
        self.blockingAmount = amount
        self.blockingInTime = isTime


    # Set the file path to read and write
    def setFilePath(self, path):
        self.filePath = path
        self.fileHandler.setFilePath(path)
        self.startTimers()


    # Start All needed timers
    def startTimers(self):
        self.progressTimer = QTimer()
        self.progressTimer.timeout.connect(lambda: self.stopProgressTimer())

        self.updateProgressTimer = QTimer()
        self.updateProgressTimer.timeout.connect(lambda: self.updateProgressbar())
        
        self.activateProgressBar()

        self.wordDisappearTimer = QTimer()
        self.wordDisappearTimer.timeout.connect(lambda: self.disapearWord())
        self.wordDisappearTimer.start(3000)

        self.checkLinesTimer = QTimer()
        self.checkLinesTimer.timeout.connect(lambda: self.checkLines())
        self.checkLinesTimer.start(10)

        self.fileHandler.enableAutosave()


    def activateProgressBar(self):
        self.hideEndSessionBtns()

        if self.blockingInTime:
            self.startProgressTimer(self.blockingAmount)
        
        if self.blockingAmount != 0:
            self.updateProgressTimer.start(1000)

        else:
            self.showEndSessionBtns()

        

    # Update the progress color and value and restart the timer if not 100%
    def updateProgressbar(self):
        amount = self.updateProgressValue()
        # self.updateProgressColor(amount)

        if int(amount) == 100:
            self.showEndSessionBtns()
            self.saving = True
            self.updateProgressTimer.stop()


    def updateProgressValue(self):

        if self.blockingInTime:
            remain = self.progressTimer.remainingTime() / 60000
        else:
            remain = int(self.blockingAmount) - self.getWordsTyped()

        amount = 100 - ((remain / int(self.blockingAmount)) * 100)

        self.progressBar.setValue(amount)    

        return amount


    # # Updates the progress bar's color according to its amount
    # def updateProgressColor(self, amount):
        
    #     if amount <= 25:
    #         color = 'ED2938'
    #     elif amount <= 50:
    #         color = 'FF8C01'
    #     elif amount <= 75:
    #         color = 'FFE733'
    #     else:
    #         color = '37DD5C'

    #     self.progressBar.setStyleSheet("QProgressBar"
    #         "{"
    #         "border: solid grey;"
    #         "color: black;"
    #         "height: 5px"
    #         "}"
    #         "QProgressBar::chunk"
    #         "{"
    #         f"background-color: #{color};"
    #         "} ")


    def startProgressTimer(self, timeInMin):
        self.progressTimer.start(int(timeInMin) * 60000)


    def stopProgressTimer(self):
        self.progressTimer.stop()


    # Show snooze and Quit buttons with hiding progress bar
    def showEndSessionBtns(self):
        self.progressBar.hide()
        self.snoozeBtn.show()
        self.saveAndQuitBtn.show()


    # Hide snooze and Quit buttons with showing progress bar
    def hideEndSessionBtns(self):
        self.progressBar.show()
        self.snoozeBtn.hide()
        self.saveAndQuitBtn.hide()
        self.progressBar.setValue(0)


    # Close the app
    def closeApp(self):
        self.setIsDisappearable()
        state = self.fileHandler.saveToFile(True)

        if state == True: # Successfully save the file
            self.close()
            self.mainWidget.close()


    # Block additional 10 minutes
    def addSnooze(self):
        self.saving = False
        self.setBlocking(10, True)
        self.activateProgressBar()
        

    def setContent(self):
        index = int(self.currentParLbl.text())
        if len(self.contentLines) < index + 1:
            self.contentLines.append(self.textEdit.toPlainText().split('\n'))
            self.wordsCount.append(0)
        else:
            self.contentLines[index] = self.textEdit.toPlainText().split('\n')

        self.countWords(index)


    def updateContent(self):
        self.textEdit.clear()
        self.textEdit.setPlainText('\n'.join(self.contentLines[int(self.currentParLbl.text())]))


    # Count number of words in the current paragraph
    def countWords(self, index):

        currentParagraphWords = 0
        for line in self.contentLines[index]:
            for word in line.split(' '):
                if word != '' and word != ' ':
                    currentParagraphWords += 1
        
        if len(self.wordsCount) < index+1:
            self.wordsCount.append(0)

        self.wordsCount[index] = currentParagraphWords


    # Returns number of words in the whole file
    def getWordsTyped(self):
        self.setContent()
        currentWords = sum(self.wordsCount)
        
        if currentWords < self.loadedWords:
            self.loadedWords = currentWords
            return 0
        else:
            return currentWords - self.loadedWords


    # Remove the last word from the content
    def disapearWord(self):
        if self.isDisappearable and not self.saving:
            self.setContent()
            index = int(self.currentParLbl.text())

            if self.contentLines[index][-1] == '':
                if len(self.contentLines[index]) > 1:
                    self.contentLines[index].pop()

                else:
                    if index != 0:
                        self.contentLines.pop(int(self.currentParLbl.text()))
                        self.previousParagraph(False)
                        index = int(self.currentParLbl.text())

            if len(self.contentLines[index]) != 0:
                line = self.contentLines[index][-1]
                self.contentLines[index][-1] = ' '.join(line.split(' ')[:-1])

            self.updateContent()

            # Set cursor at the end of text
            self.setCursor(self.textEdit.document().characterCount() - 1)

        self.isDisappearable = True
  

    # Set the cursor in specific position
    def setCursor(self, position):
        cursor = self.textEdit.textCursor()
        cursor.setPosition(cursor.position() + position)
        self.textEdit.setTextCursor(cursor)


    # Detect pressing Enter
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.textEdit:
            index = int(self.currentParLbl.text())

            if event.key() == Qt.Key_Return and self.textEdit.hasFocus():
                self.createNewParagraph()
            
            if (event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete) and self.textEdit.hasFocus():
                self.setContent()
                
                if self.contentLines[index][-1] == '' and len(self.contentLines[index]) <= 1 and index != 0 and self.reachMax == False:
                    self.contentLines.pop(index)
                    self.contentLines[index-1][-1] += ' '
                    self.previousParagraph(False)
                    # Set cursor at the end of text
                    self.setCursor(self.textEdit.document().characterCount() - 1)

            # if event.key() == Qt.Key_Escape and self.textEdit.hasFocus():
            #     self.close()
            #     self.mainWidget.close()

        return super().eventFilter(obj, event)


    def checkLines(self):
        
        if self.textEdit.document().size().height() > self.maxLinesHeight:
            index = int(self.currentParLbl.text())
            # Remove the last character
            self.reachMax = True
            self.setContent()
            lastChar = self.contentLines[index][-1][-1]
            keyboard.press_and_release('backspace')
            self.createNewParagraph()
            self.contentLines[index][-1] = self.contentLines[index][-1][:-1]
            self.contentLines[index+1][0] = lastChar
            self.updateContent()
            keyboard.press_and_release('right')
        else:
            self.reachMax = False


    def createNewParagraph(self):
        self.setContent()

        if int(self.currentParLbl.text()) < len(self.contentLines)-1:
            self.nextParagraph()
        else:
            self.contentLines.append([])
            self.wordsCount.append(0)
            self.currentParLbl.setText(str(int(self.currentParLbl.text())+1))
            self.updateContent()

        # Remove the additional new line
        keyboard.press_and_release('backspace')

        # Save the file
        self.fileHandler.saveToFile()


    def setIsDisappearable(self):
        self.isDisappearable = False
                

    # Go to the next paragraph
    def nextParagraph(self):
        if int(self.currentParLbl.text()) < len(self.contentLines)-1:
            self.setContent()
            self.currentParLbl.setText(str(int(self.currentParLbl.text())+1))
            self.updateContent()


    # Go back to the previous paragraph
    def previousParagraph(self, isSet = True):
        if int(self.currentParLbl.text()) > 0:
            if isSet:
                self.setContent()
            self.currentParLbl.setText(str(int(self.currentParLbl.text())-1))
            self.updateContent()

