# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
from ctypes import windll
import time
  
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.user32 = windll.user32

        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        # setting title
        self.setWindowTitle("Python ")
  
        # setting geometry
        self.setGeometry(0, 0, self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1))
  
        # calling method
        self.UiComponents()
  
        # showing all the widgets
        self.show()
  
    # method for widgets
    def UiComponents(self):
  
        # creating label
        label = QLabel("Dark", self)
  
        # setting geometry to label
        label.setGeometry(100, 100, 120, 40)
  
        # adding border to label
        label.setStyleSheet("border : 2px solid black")
  
        # opening window in maximized size
        # self.showMaximized()
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# get the handle to the taskbar
h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)

# hide the taskbar
windll.user32.ShowWindow(h, 9)
# start the app
sys.exit(App.exec())




# get the handle to the taskbar
h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)

# hide the taskbar
windll.user32.ShowWindow(h, 0)

# time.sleep(10)
# show the taskbar again
windll.user32.ShowWindow(h, 9)