from aiohttp import content_disposition_filename
from components.SaveStatusMessage import SaveStatusMessage
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
import os

class FileHandler:
    def __init__(self, parent):
        self.parent = parent
        self.saveStatusMessage = SaveStatusMessage(parent)

        # Timer to Save the file each 10s
        self.autosaveTimer = QTimer()
        

    # Enable saving the file automaticlly
    def enableAutosave(self):
        self.autosaveTimer.timeout.connect(lambda: self.saveToFile())
        self.autosaveTimer.start(5000)
    

    def setFilePath(self, path):
        self.filePath = path.replace('\\', '/')


    def saveToFile(self, close = False):
        try:
            self.parent.setContent()

            if close:
                # Open browse to enable user to choose a location
                fname = QFileDialog.getSaveFileName(self.parent, 'Save File', self.filePath, 'Text Files (*.txt)')[0]
                
                if fname != '':
                    self.filePath = fname
                else:
                    return False

            if os.path.exists(self.filePath):
                os.remove(self.filePath) 

            with open(self.filePath, 'w') as file:
                text = ''
                for paragraph in self.parent.contentLines:
                    text += ' '.join(paragraph)
                    text += '\n'

                file.write(text)
                del text
                file.close()

            if close:
                self.saveStatusMessage.displaySuccess(self.filePath)

            return True

        except Exception as e:
            self.saveStatusMessage.displayFail(self.filePath + '\n' + str(e))
            return False

            

    def loadFromFile(self):
        contentLines = []

        with open(self.filePath, 'r') as file:
            lines = file.readlines()
        
            for line in lines:
                contentLines.append([line.strip()])
                
            del lines
            file.close()
            
        self.parent.contentLines = contentLines

        i = 0
        for p in contentLines:
            self.parent.countWords(i)
            i += 1

        self.parent.loadedWords = sum(self.parent.wordsCount)
        self.parent.updateContent()

