# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
from ctypes import windll


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hide the titlebar
        self.setWindowFlag(Qt.FramelessWindowHint) 
        
        # Make the window always the top
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # setting title
        self.setWindowTitle("Python ")
  
        # Setting Window full screen according to the screen size
        self.user32 = windll.user32
        self.setGeometry(0, 0, self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1))
  
        # calling method
        self.UiComponents()
  
        # Showing all the widgets
        self.show()
  

    # Build the widgets
    def UiComponents(self):
  
        button = QPushButton("Close", self)
        button.setGeometry(500, 500, 100, 50)
        button.setStyleSheet("border : 2px solid black") # adding border to label
        button.clicked.connect(lambda:self._close())

    def _close(self):
        self.close()

  
  
def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

	
if __name__ == '__main__':
   main()


# get the handle to the taskbar
# h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)

# hide the taskbar
# windll.user32.ShowWindow(h, 0)

# # show the taskbar again
# windll.user32.ShowWindow(h, 9)