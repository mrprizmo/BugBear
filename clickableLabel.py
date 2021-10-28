from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QEvent


class ClickableLabel(QLabel):
    clicked: pyqtSignal = pyqtSignal()

    def mousePressEvent(self, event: QEvent) -> None:
        self.clicked.emit()