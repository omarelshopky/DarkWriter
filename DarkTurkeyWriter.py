from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.uic import loadUi
import sys
from ctypes import windll
from optionWindowUI import Ui_optionWindow


class StackWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Hide the titlebar
        # self.setWindowFlag(Qt.FramelessWindowHint) 
            
        # Make the window always the top
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Setting Window full screen according to the screen size
        user32 = windll.user32
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)
        self.setGeometry(0, 0, self.width, self.height)

        # Add the startup window and show
        self.addWidget(OptionWindow(self))
        self.show()



class OptionWindow(QMainWindow, Ui_optionWindow):
    def __init__(self, widget):
        super().__init__()
        self.mainWidget = widget
        self.setupUi(self)
        self.showMaximized()
        #loadUi('file', self)
        # self.UiComponents()
        self.show()
  
  

    # Build the widgets
    def UiComponents(self):
        
        self.setLayout()
        button = QPushButton("Close", self)
        button.setGeometry(100, 100, 100, 50)
        button.setStyleSheet("border : 2px solid black") # adding border to label
        button.clicked.connect(lambda:self._close())




    # Close the Window
    def _close(self):
        self.close()
        self.mainWidget.close()



  
def main():
    App = QApplication(sys.argv)

    mainWidget = StackWidget()
    
    sys.exit(App.exec())

	
if __name__ == '__main__':
   main()


# fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files', 'Images (*.png, *.xmp *.jpg)')
# self.filename.setText(fname[0])