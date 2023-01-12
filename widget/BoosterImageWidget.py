from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QPixmap, QPen, QPainter
from PyQt5.QtWidgets import QDialog, QMainWindow, QLabel, QGridLayout
import random
from util.ImagesChecker import ImagesChecker

IMAGE_SIZE = 800
ANIMATION_DURATION = 400
DISPLAY_DURATION = 500

class BoosterImageWidget(QDialog):
    def __init__(self, parentWindow: QMainWindow):
        super().__init__(parentWindow)
        self._setupUi()
        self._boosterImages = ImagesChecker().getBoosterImages()

    def _setupUi(self):
        """Setup the ui component"""
        # Make window transparent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.boosterImageLbl = QLabel()
        self.boosterImageLbl.setScaledContents(True)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.boosterImageLbl, 1, 1)
        self.setLayout(self.gridLayout)
        self.setGeometry(self.parent().width() / 2, self.parent().height() / 2, 100, 100)

    def paintEvent(self, event=None):
        """Override paint event to make the widget transparent"""
        painter = QPainter(self)
        painter.setOpacity(0)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())

    def _getRandomImagePath(self) -> str:
        """Gets random image path from the available images list"""
        return random.choice(self._boosterImages)

    def _setImage(self, imagePath: str):
        """Set the booster image"""
        self.boosterImagePixmap = QPixmap(imagePath)
        self.boosterImageLbl.setPixmap(self.boosterImagePixmap)

    def _sizeUpAnimation(self):
        """Perform size up animation process"""
        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(ANIMATION_DURATION)
        self.animation.setStartValue(QRect((self.parent().width() / 2), (self.parent().height() / 2), 0, 0))
        self.animation.setEndValue(QRect((self.parent().width() / 2) - (IMAGE_SIZE / 2), (self.parent().height() / 2) - (IMAGE_SIZE / 2), IMAGE_SIZE, IMAGE_SIZE))
        self.animation.start()

    def _sizeDownAnimation(self) -> None:
        """Perform size down animation process"""
        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(ANIMATION_DURATION)
        self.animation.setStartValue(QRect((self.parent().width() / 2) - (IMAGE_SIZE / 2), (self.parent().height() / 2) - (IMAGE_SIZE / 2), IMAGE_SIZE, IMAGE_SIZE))
        self.animation.setEndValue(QRect(self.parent().width() / 2, self.parent().height() / 2, 0, 0))
        self.animation.start()
        QTimer.singleShot(ANIMATION_DURATION, self.close)

    def display(self) -> None:
        """Display booster image"""
        imagePath = self._getRandomImagePath()
        self._setImage(imagePath)
        self._sizeUpAnimation()
        self.show()
        QTimer.singleShot(DISPLAY_DURATION, self._sizeDownAnimation)
