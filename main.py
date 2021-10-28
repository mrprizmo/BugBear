import sys
from PyQt5 import uic
from typing import Any
from random import randint
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QPixmap, QTransform, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow
from clickableLabel import ClickableLabel


class BugBear(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.unitUI()

        self.switching_sound = QSound("music\\switching.wav")

        self.rotate_transform = QTransform()
        self.rotate_transform.rotate(90)
        self.wheel_map = [[0 for __ in range(4)] for _ in range(4)]

        for i in range(self.wheel_layout.count()):
            self.wheel_layout.itemAt(i).widget().clicked.connect(self.rotate_wheel)
        self.btn_restart.clicked.connect(self.restart)

        self.restart()

    def unitUI(self) -> None:
        uic.loadUi("UI\\mainwindow.ui", self)
        self.setFixedSize(self.size())
        self.setCursor(QCursor(QPixmap("image\\mouse.png"), 0, 0))
        for i in range(4):
            for j in range(4):
                cl = ClickableLabel(self)
                cl.setPixmap(QPixmap("image\\wheel.png"))
                cl.setScaledContents(True)
                self.wheel_layout.addWidget(cl, i, j)

    def rotate_wheel(self) -> None:
        self.statusbar.showMessage('')
        self.switching_sound.play()
        cur_i, cur_j = 0, 0

        for i in range(self.wheel_layout.rowCount()):
            for j in range(self.wheel_layout.columnCount()):
                if self.wheel_layout.itemAt(i * self.wheel_layout.columnCount() + j).widget() == self.sender():
                    cur_i, cur_j = i, j
                    break

        for i in range(self.wheel_layout.rowCount()):
            temp = self.wheel_layout.itemAt(i * self.wheel_layout.columnCount() + cur_j).widget()
            temp.setPixmap(temp.pixmap().transformed(self.rotate_transform))
            self.wheel_map[i][cur_j] ^= 1

        for j in range(self.wheel_layout.columnCount()):
            temp = self.wheel_layout.itemAt(cur_i * self.wheel_layout.columnCount() + j).widget()
            temp.setPixmap(temp.pixmap().transformed(self.rotate_transform))
            self.wheel_map[cur_i][j] ^= 1

        self.sender().setPixmap(self.sender().pixmap().transformed(self.rotate_transform))
        self.wheel_map[cur_i][cur_j] ^= 1

        if sum(map(sum, self.wheel_map)) == 0:
            self.statusbar.showMessage("Да вы медвежатник, шеф!")

    def restart(self) -> None:
        self.statusbar.showMessage('')
        for i in range(self.wheel_layout.rowCount()):
            for j in range(self.wheel_layout.columnCount()):
                if self.wheel_map[i][j]:
                    temp = self.wheel_layout.itemAt(i * self.wheel_layout.columnCount() + j).widget()
                    temp.setPixmap(temp.pixmap().transformed(self.rotate_transform))
                    self.wheel_map[i][j] ^= 1

        for _ in range(randint(20, 50)):
            cur_i, cur_j = randint(0, self.wheel_layout.rowCount() - 1), randint(0, self.wheel_layout.columnCount() - 1)
            for i in range(self.wheel_layout.rowCount()):
                self.wheel_map[i][cur_j] ^= 1
            for j in range(self.wheel_layout.columnCount()):
                self.wheel_map[cur_i][j] ^= 1
            self.wheel_map[cur_i][cur_j] ^= 1

        for i in range(self.wheel_layout.rowCount()):
            for j in range(self.wheel_layout.columnCount()):
                if self.wheel_map[i][j]:
                    temp = self.wheel_layout.itemAt(i * self.wheel_layout.columnCount() + j).widget()
                    temp.setPixmap(temp.pixmap().transformed(self.rotate_transform))


def except_hook(cls: Any, exception: Any, traceback: Any) -> None:
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BugBear()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
