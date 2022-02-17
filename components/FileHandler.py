from components.SaveStatusMessage import SaveStatusMessage
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 


class FileHandler:
    def __init__(self, parent):
        self.parent = parent
        self.saveStatusMessage = SaveStatusMessage(parent)

        # Timer to Save the file each 10s
        self.autosaveTimer = QTimer()
        self.autosaveTimer.timeout.connect(lambda: self.autosave())
        self.autosaveTime.start(10000)

    
    # Save the file each 
    def autosave(self):
        self.autosaveTimer.stop()
        self.saveToFile()
        self.autosaveTime.start(10000)
        

    def setFilePath(self, path):
        self.filePath = path


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
        
            with open(self.filePath, 'w') as file:
                text = ''
                for paragraph in self.parent.contentLines:
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

