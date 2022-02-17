from pydoc import doc
from UI.writingWindowUI import Ui_WritingWindow
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
import keyboard

class WritingWindow(QMainWindow, Ui_WritingWindow):

    def __init__(self, widget):
        super().__init__()
        self.fileHandler = FileHandler(self)
        self.wordsTyped = 0
        self.contentLines = []
        self.isDisappearable = True
        self.mainWidget = widget
        self.setupUi(self)
        self.textEdit.document().setDocumentMargin(90)
        self.UiComponentsEvent()
        # self.test = QTextEdit()
        # self.test.
        
  

    def UiComponentsEvent(self):
        # Saves the file and Closes the app 
        self.saveAndQuitBtn.clicked.connect(lambda:self.closeApp())
    
        # Block additional 10min
        self.snoozeBtn.clicked.connect(lambda:self.addSnooze())

        self.textEdit.document().contentsChanged.connect(lambda:self.setIsDisappearable())
        
        self.nextBtn.clicked.connect(lambda:self.nextParagraph())
        self.previousBtn.clicked.connect(lambda:self.previousParagraph())

        # Catch pressing Enter
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
        self.updateProgressTimer.timeout.connect(lambda: self.stopUpdateProgressTimer())

        self.wordDisappearTimer = QTimer()
        self.wordDisappearTimer.timeout.connect(lambda: self.stopWordDisappearTimer())
        self.startWordDisappearTimer()

        self.activateProgressBar()


    def activateProgressBar(self):
        self.hideEndSessionBtns()

        if self.blockingInTime:
            self.startProgressTimer(self.blockingAmount)
        
        if self.blockingAmount != 0:
            self.startUpdateProgressTimer()
        else:
            self.showEndSessionBtns()


    def startUpdateProgressTimer(self):
        self.updateProgressTimer.start(500)
        

    # Update the progress color and value and restart the timer if not 100%
    def stopUpdateProgressTimer(self):
        self.updateProgressTimer.stop()

        amount = self.updateProgressValue()
        self.updateProgressColor(amount)

        if amount != 100:
            self.startUpdateProgressTimer()
        else:
            self.showEndSessionBtns()

        

    def updateProgressValue(self):
        if self.blockingInTime:
            remain = self.progressTimer.remainingTime() / 60000
        else:
            remain = int(self.blockingAmount) - self.getWordsTyped()

        amount = 100 - ((remain / int(self.blockingAmount)) * 100)

        self.progressBar.setValue(amount)    

        return amount


    # Updates the progress bar's color according to its amount
    def updateProgressColor(self, amount):
        
        if amount <= 25:
            color = 'ED2938'
        elif amount <= 50:
            color = 'FF8C01'
        elif amount <= 75:
            color = 'FFE733'
        else:
            color = '37DD5C'

        self.progressBar.setStyleSheet("QProgressBar"
            "{"
            "border: solid grey;"
            "color: black;"
            "height: 5px"
            "}"
            "QProgressBar::chunk"
            "{"
            f"background-color: #{color};"
            "} ")


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
        self.setContent()
        state = self.fileHandler.saveToFile(self.contentLines, True)

        if state == True: # Successfully save the file
            self.close()
            self.mainWidget.close()


    # Block additional 10 minutes
    def addSnooze(self):
        self.setBlocking(10, True)
        self.activateProgressBar()
        

    def setContent(self):
        index = int(self.currentParLbl.text())
        if len(self.contentLines) < index + 1:
            self.contentLines.append(self.textEdit.toPlainText().split('\n'))
        else:
            self.contentLines[index] = self.textEdit.toPlainText().split('\n')


    def updateContent(self):
        self.textEdit.clear()
        self.textEdit.setPlainText('\n'.join(self.contentLines[int(self.currentParLbl.text())]))


    def getWordsTyped(self):
        self.setContent()

        currentParagraphLines = 0
        for line in self.contentLines[int(self.currentParLbl.text())]:
            for word in line.split(' '):
                if word != '' and word != ' ':
                    currentParagraphLines += 1

        return self.wordsTyped + currentParagraphLines


    def startWordDisappearTimer(self):
        self.wordDisappearTimer.start(3000)


    def stopWordDisappearTimer(self):
        self.updateProgressTimer.stop()
        if self.isDisappearable:
            self.disapearWord()
        self.startWordDisappearTimer()
        self.isDisappearable = True


    def disapearWord(self):
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

  
    # Set the cursor in specific position
    def setCursor(self, position):
        cursor = self.textEdit.textCursor()
        cursor.setPosition(cursor.position() + position)
        self.textEdit.setTextCursor(cursor)


    # Goes to next paragraph when pressing enter detected
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.textEdit:
            if event.key() == Qt.Key_Return and self.textEdit.hasFocus():
                self.setContent()

                if int(self.currentParLbl.text()) < len(self.contentLines)-1:
                    self.nextParagraph()
                else:
                    self.contentLines.append([])
                    self.currentParLbl.setText(str(int(self.currentParLbl.text())+1))
                    self.updateContent()

                # Remove the additional new line
                keyboard.press_and_release('backspace')

                # Save the file
                self.fileHandler.saveToFile(self.contentLines)
                
        return super().eventFilter(obj, event)


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



class FileHandler:
    def __init__(self, parent):
        self.parent = parent
        self.saveStatusMessage = SaveStatusMessage(parent)


    def setFilePath(self, path):
        self.filePath = path


    def saveToFile(self, contentLines, close = False):
        try:
            if close:
                # Open browse to enable user to choose a location
                fname = QFileDialog.getSaveFileName(self.parent, 'Save File', self.filePath, 'Text Files (*.txt)')[0]
                
                if fname != '':
                    self.filePath = fname
                else:
                    return False
        
            with open(self.filePath, 'w') as file:
                text = ''
                for paragraph in contentLines:
                    text += '\n'.join(paragraph)
                    text += '\n\n'

                file.write(text)
                del text

            if close:
                self.saveStatusMessage.displaySuccess(self.filePath)

            return True

        except:
            self.saveStatusMessage.displayFail(self.filePath)
            return False

            

    def loadFromFile(self):
        contentLine = []

        # with open(self.filePath, 'w') as file:



class SaveStatusMessage:
    def __init__(self, parent):
        self.parent = parent


    def _display(self, title, text):
        dlg = QMessageBox(self.parent)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        button = dlg.exec()
        return button == QMessageBox.Ok


    def displaySuccess(self, filePath):
        return self._display("Well Done!", f"Your draft was successfully saved here\n\n{filePath}")


    def displayFail(self, filePath):
        return self._display("Sorry!", f"There is an error saving your draft here\n\n{filePath}")
