from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Any, List

class Overlay(QtWidgets.QWidget):
    trigger = QtCore.pyqtSignal(list)
    def __init__(self) -> None:
        super().__init__()

        self.__to_paint__: List[Any] = []
        self.__should_draw__: bool = False
        self.__state__: int = -1
        self.__paint_loading__: int = 0
        self.__paint_info__: int = 1
        self.__img__ = QtGui.QPixmap("img/pl_search.png")
                                 
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.trigger.connect(self.show_overlay)

    def paintEvent(self, event) -> None:
        if not self.__should_draw__:
            return
        if self.__state__ == self.__paint_loading__:
            self.paint_loading()
        if self.__state__ == self.__paint_info__:
            QtCore.QTimer.singleShot(10000, self.hide_overlay)
            self.paint_info()
    
    def show_overlay(self, show: List[Any]) -> None:
        self.__to_paint__ = show[0]
        self.__state__ = show[1]
        self.__should_draw__ = True
        self.update()   # force repaint
        self.show()

    def hide_overlay(self) -> None:
        self.__should_draw__ = False
        self.update()
        self.hide()
    
    def paint_loading(self) -> None:
        painter = QtGui.QPainter(self)
        x = (self.width() - self.__img__.width()) // 2
        y = (self.height() - self.__img__.height()) // 2
        painter.drawPixmap(x, y, self.__img__)
        painter.end()

    def paint_info(self) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2)
        painter.setPen(pen)

        font = QtGui.QFont()
        font.setPointSize(12)
        painter.setFont(font)

        for x, y, w, h, z, item_name, item_price in self.__to_paint__:
            painter.drawRect(x, y, w, h) # detected text

            # background
            rect1 = QtCore.QRect(x, z, w, 20)
            painter.fillRect(rect1, QtGui.QColor(0, 0, 0, 180))
            rect2 = QtCore.QRect(x, z+20, w, 20)
            painter.fillRect(rect2, QtGui.QColor(0, 0, 0, 180))

            # info
            painter.drawText(rect1, QtCore.Qt.AlignCenter, item_name)
            painter.drawText(rect2, QtCore.Qt.AlignCenter, f'{item_price} pl')
