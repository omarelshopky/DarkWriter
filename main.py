from PyQt5.QtWidgets import QApplication
import keyboard
import sys
from window.MainStack import MainStack

def main():
    # Block hot keys
    keyboard.remap_key('windows', 'shift')
    keyboard.remap_key('tab', 'shift')
    keyboard.remap_key('ctrl', 'shift')

    App = QApplication(sys.argv)
    App.setStyle('Breeze') # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']

    mainWidget = MainStack()
    sys.exit(App.exec())

if __name__ == '__main__':
   main()