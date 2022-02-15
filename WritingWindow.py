from UI.writingWindowUI import Ui_WritingWindow
from PyQt5.QtWidgets import * 


class WritingWindow(QMainWindow, Ui_WritingWindow):
    def __init__(self, widget):
        super().__init__()
        self.mainWidget = widget
        self.setupUi(self)
        self.UiComponentsLogic()
        self.show()
        #loadUi('file', self)
  
  
    def UiComponentsLogic(self):
        # Closes the app when quit button pressed
        self.saveAndQuitBtn.clicked.connect(lambda:self.closeApp())
        self.progressBar.hide()
        


    # Close the app
    def closeApp(self):
        self.close()
        self.mainWidget.close()


    # Open browse files dialog
    def browseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.', 'Text Files (*.txt)')
        self.odFilePathTxt.setText(fname[0])

