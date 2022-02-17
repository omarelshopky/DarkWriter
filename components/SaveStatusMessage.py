from PyQt5.QtWidgets import * 


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
