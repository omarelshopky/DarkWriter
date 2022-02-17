from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from ctypes import windll
import sys
import keyboard
from OptionWindow import OptionWindow
from WritingWindow import WritingWindow


class StackWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Hide the titlebar
        self.setWindowFlag(Qt.FramelessWindowHint) 
            
        # Make the window always the top
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Setting Window full screen according to the screen size
        user32 = windll.user32
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)
        self.setGeometry(0, 0, self.width, self.height)

        # Add the startup window and show
        self.addWidget(OptionWindow(self))
        self.addWidget(WritingWindow(self))
        self.show()



def main():
    # Block hot keys
    keyboard.remap_key('windows', 'shift')
    keyboard.remap_key('tab', 'shift')
    keyboard.remap_key('ctrl', 'shift')

    App = QApplication(sys.argv)

    mainWidget = StackWidget()
    
    sys.exit(App.exec())

	

if __name__ == '__main__':
   main()
