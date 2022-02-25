from UI.writingWindowUI import Ui_WritingWindow
from components.FileHandler import FileHandler
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
import keyboard

# rightArrow = b'iVBORw0KGgoAAAANSUhEUgAAANwAAADcCAYAAAAbWs+BAAAACXBIWXMAAC4jAAAuIwF4pT92AAAGdWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDMgNzkuMTY0NTI3LCAyMDIwLzEwLzE1LTE3OjQ4OjMyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjIuMSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIyLTAyLTE1VDAxOjU4OjUwKzAyOjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDIyLTAyLTE1VDAxOjU4OjUwKzAyOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMi0wMi0xNVQwMTo1ODo1MCswMjowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpmZGExNDJiOC1iNDFkLTJiNGEtOWJhMS1kMWZmMmNkNWQ3ZGIiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDozODgxMDVhYy1iNjNhLTJmNDMtOTQ5OC1iMTMxYzNkMDU4ZmUiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo4MGJkYjFiNS0xMWE4LWMyNDQtYjBlNy03NzQ3OTljZDA2MTQiIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjgwYmRiMWI1LTExYTgtYzI0NC1iMGU3LTc3NDc5OWNkMDYxNCIgc3RFdnQ6d2hlbj0iMjAyMi0wMi0xNVQwMTo1ODo1MCswMjowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIyLjEgKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpmZGExNDJiOC1iNDFkLTJiNGEtOWJhMS1kMWZmMmNkNWQ3ZGIiIHN0RXZ0OndoZW49IjIwMjItMDItMTVUMDE6NTg6NTArMDI6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMi4xIChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8L3JkZjpTZXE+IDwveG1wTU06SGlzdG9yeT4gPHBob3Rvc2hvcDpEb2N1bWVudEFuY2VzdG9ycz4gPHJkZjpCYWc+IDxyZGY6bGk+RkIxODUzODJFODA5RjU3QjU4RjhEMEQ1Q0E0RkY4RUM8L3JkZjpsaT4gPC9yZGY6QmFnPiA8L3Bob3Rvc2hvcDpEb2N1bWVudEFuY2VzdG9ycz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5iyl2MAAAoFUlEQVR4nO19a5RUxdX2PlWnu2fGES8DqKCsQ8vFT2EkXlDIpwJyMe9LjBLEYLhEv0RdLq8R0YCGJCZxGeWNhGhwKbgUMNwigsGICsJo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'

# leftArrow = b'iVBORw0KGgoAAAANSUhEUgAAANwAAADcCAYAAAAbWs+BAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAALiMAAC4jAXilP3YAAAZ1aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA2LjAtYzAwMyA3OS4xNjQ1MjcsIDIwMjAvMTAvMTUtMTc6NDg6MzIgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi4xIChXaW5kb3dzKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjItMDItMTVUMDE6NTg6NTArMDI6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjItMDItMTVUMDE6NTg6NTArMDI6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDIyLTAyLTE1VDAxOjU4OjUwKzAyOjAwIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOmZkYTE0MmI4LWI0MWQtMmI0YS05YmExLWQxZmYyY2Q1ZDdkYiIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjM4ODEwNWFjLWI2M2EtMmY0My05NDk4LWIxMzFjM2QwNThmZSIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjgwYmRiMWI1LTExYTgtYzI0NC1iMGU3LTc3NDc5OWNkMDYxNCIgcGhvdG9zaG9wOkNvbG9yTW9kZT0iMyIgcGhvdG9zaG9wOklDQ1Byb2ZpbGU9InNSR0IgSUVDNjE5NjYtMi4xIiBkYzpmb3JtYXQ9ImltYWdlL3BuZyI+IDx4bXBNTTpIaXN0b3J5PiA8cmRmOlNlcT4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNyZWF0ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ODBiZGIxYjUtMTFhOC1jMjQ0LWIwZTctNzc0Nzk5Y2QwNjE0IiBzdEV2dDp3aGVuPSIyMDIyLTAyLTE1VDAxOjU4OjUwKzAyOjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjIuMSAoV2luZG93cykiLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmZkYTE0MmI4LWI0MWQtMmI0YS05YmExLWQxZmYyY2Q1ZDdkYiIgc3RFdnQ6d2hlbj0iMjAyMi0wMi0xNVQwMTo1ODo1MCswMjowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIyLjEgKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDwvcmRmOlNlcT4gPC94bXBNTTpIaXN0b3J5PiA8cGhvdG9zaG9wOkRvY3VtZW50QW5jZXN0b3JzPiA8cmRmOkJhZz4gPHJkZjpsaT5GQjE4NTM4MkU4MDlGNTdCNThGOEQwRDVDQTRGRjhFQzwvcmRmOmxpPiA8L3JkZjpCYWc+IDwvcGhvdG9zaG9wOkRvY3VtZW50QW5jZXN0b3JzPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PmLKXYwAAAAhdEVYdENyZWF0aW9uIFRpbWUAMjAyMjowMjoxNSAwMTo0NTozMOpAoKwAABfLSURB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'


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
        self.textEdit.document().setDocumentMargin(90)
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
        self.textEdit.setPlainText('o')
        firstLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.textEdit.setPlainText('o\no')
        secnondLine = self.textEdit.document().size().height()
        self.textEdit.clear()
        self.maxLinesHeight = firstLine + 5 * (secnondLine - firstLine)

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

            if event.key() == Qt.Key_Escape and self.textEdit.hasFocus():
                self.close()
                self.mainWidget.close()

        return super().eventFilter(obj, event)


    def checkLines(self):
        
        if self.textEdit.document().size().height() > self.maxLinesHeight:
            index = int(self.currentParLbl.text())
            # Remove the last character
            self.reachMax = True
            keyboard.press_and_release('backspace')
            self.createNewParagraph()
            self.contentLines[index][-1] = self.contentLines[index][-1][:-1]
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

