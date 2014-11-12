#!/usr/bin/env python

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

class TicTacToe(QGraphicsItem):
    def __init__(self):
        super(TicTacToe, self).__init__()
        self.board = [[-1, -1, -1],[-1, -1, -1], [-1, -1, -1]]
        self.O = 0
        self.X = 1
        self.turn = self.O

    def reset(self):
        for y in range(3):
            for x in range(3):
                self.board[y][x] = -1
        self.turn = self.O
        self.update()

    def select(self, x, y):
        if x < 0 or y < 0 or x >= 3 or y >= 3:
            return
        if self.board[y][x] == -1:
            self.board[y][x] = self.turn
            self.turn = 1 - self.turn

    def paint(self, painter, option, widget):
        painter.setPen(Qt.black)
        painter.drawLine(0,100,300,100)
        painter.drawLine(0,200,300,200)
        painter.drawLine(100,0,100,300)
        painter.drawLine(200,0,200,300)

        for y in range(3):
            for x in range(3):
                if self.board[y][x] == self.O:
                    painter.setPen(Qt.red)
                    painter.drawEllipse(QPointF(50+x*100, 50+y*100), 30, 30)
                elif self.board[y][x] == self.X:
                    painter.setPen(Qt.blue)
                    painter.drawLine(20+x*100, 20+y*100, 80+x*100, 80+y*100)
                    painter.drawLine(20+x*100, 80+y*100, 80+x*100, 20+y*100)

    def boundingRect(self):
        return QRectF(0,0,300,300)

    def mousePressEvent(self, event):
        pos = event.pos()
        self.select(int(pos.x()/100), int(pos.y()/100))
        self.update()
        super(TicTacToe, self).mousePressEvent(event)

class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QGraphicsScene(self)
        self.tic_tac_toe = TicTacToe()
        scene.addItem(self.tic_tac_toe)
        scene.setSceneRect(0, 0, 300, 300)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("Tic Tac Toe")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_R:
            self.tic_tac_toe.reset()
        super(MainWindow, self).keyPressEvent(event)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
