from PyQt5 import QtWidgets, QtCore, QtGui

class Overlay(QtWidgets.QWidget):
    trigger = QtCore.pyqtSignal(list)
    def __init__(self):
        super().__init__()

        self.__to_paint__ = []
        self.__should_draw__ = False
        self.__state__ = -1
        self.__paint_loading__ = 0
        self.__paint_pl__ = 1
        self.__img__ = QtGui.QPixmap("imgs/pl_search.png")
                                 
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

    def paintEvent(self, event):
        if not self.__should_draw__:
            return
        if self.__state__ == self.__paint_loading__:
            self.paint_loading()
        if self.__state__ == self.__paint_pl__:
            QtCore.QTimer.singleShot(10000, self.hide_overlay)
            self.paint_pl()
    
    def show_overlay(self, show):
        self.__to_paint__ = show[0]
        self.__state__ = show[1]
        self.__should_draw__ = True
        self.update()   # force repaint
        self.show()

    def hide_overlay(self):
        self.__should_draw__ = False
        self.update()
        self.hide()
    
    def paint_loading(self):
        painter = QtGui.QPainter(self)
        x = (self.width() - self.__img__.width()) // 2
        y = (self.height() - self.__img__.height()) // 2
        painter.drawPixmap(x, y, self.__img__)
        painter.end()

    def paint_pl(self):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2)
        painter.setPen(pen)

        font = QtGui.QFont()
        font.setPointSize(12)
        painter.setFont(font)

        for x, y, w, h, z, text, pl in self.__to_paint__:
            painter.drawRect(x, y, w, h) # detected text

            # background of text
            rect1 = QtCore.QRect(x, z, w, 20)
            painter.fillRect(rect1, QtGui.QColor(0, 0, 0, 180))
            rect2 = QtCore.QRect(x, z+20, w, 20)
            painter.fillRect(rect2, QtGui.QColor(0, 0, 0, 180))

            # text
            painter.drawText(rect1, QtCore.Qt.AlignCenter, text)
            painter.drawText(rect2, QtCore.Qt.AlignCenter, f'{pl} pl')
