from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import Qt
from ctypes import windll
from window.OptionWindow import OptionWindow
from window.WritingWindow import WritingWindow


class MainStack(QStackedWidget):
    """Main app window stack contains all the app main windows
    """
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

    def close(self) -> None:
        self.currentWidget().close()
        super().close()