#!/usr/bin/env python

import random

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

class CelllarAutomaton(QGraphicsItem):
    def __init__(self, width=500, height=500, size=5):
        super(CelllarAutomaton, self).__init__()
        self.width = width
        self.height = height
        self.size = size
        self.NH = self.height//size
        self.NW = self.width//size
        self.board = []
        for y in range(self.NH):
            self.board.append([0] * self.NW)
        self.board[0][self.NW//2] = 1
        self.pos = 0

    def reset(self):
        for y in range(self.NH):
            for x in range(self.NW):
                self.board[y][x] = 0
        self.board[0][self.NW//2] = 1
        self.pos = 0
        self.update()

    def randomInit(self):
        for y in range(self.NH):
            for x in range(self.NW):
                self.board[y][x] = 0
        for x in range(self.NW):
            self.board[0][x] = int(random.random() < 0.2)
        self.pos = 0
        self.update()

    def paint(self, painter, option, widget):
        painter.setPen(QColor(220,220,220))
        for y in range(self.NH):
            painter.drawLine(0, y*self.size, self.width, y*self.size)
        for x in range(self.NW):
            painter.drawLine(x*self.size, 0, x*self.size, self.height)

        painter.setBrush(Qt.black)
        for y in range(self.NH):
            for x in range(self.NW):
                if self.board[y][x] == 1:
                    painter.drawRect(self.size*x, self.size*y, self.size, self.size)

    def do_prev(self):
        if self.pos == 0:
            return
        for x in range(self.NW):
            self.board[self.pos][x] = 0
        self.pos -= 1
        self.update()

    def do_next(self, n):
        if self.pos+1 >= self.NH:
            return False
        p = []
        for i in range(8):
            p.append(n & 0b1) 
            n >>= 1

        self.board[self.pos+1][0] = p[(self.board[self.pos][0]<<1) + self.board[self.pos][1]]
        self.board[self.pos+1][self.NW-1] = p[(self.board[self.pos][self.NW-2]<<1) + self.board[self.pos][self.NW-1]]
        for x in range(1,self.NW-1):
            self.board[self.pos+1][x] = p[(self.board[self.pos][x-1]<<2)
                                            + (self.board[self.pos][x]<<1)
                                            + (self.board[self.pos][x+1])]
        self.pos += 1
        self.update()
        return True

    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 400, 400)
        self.graphicsView.setScene(scene)
        self.celluarAutomaton = CelllarAutomaton(400,400)
        scene.addItem(self.celluarAutomaton)

        validator = QIntValidator(0,1)
        ruleLayout = QGridLayout()
        ruleLayout.setAlignment(Qt.AlignTop)
        self.ruleEdits = []
        for i in range(7,-1,-1):
            ruleEdit = QLineEdit()
            ruleEdit.setValidator(validator)
            ruleEdit.setText("0")
            ruleEdit.setFixedWidth(30)
            ruleEdit.textEdited.connect(self.update_rule)
            ruleLayout.addWidget(QLabel("{0:03b}".format(i)), 0, 7-i)
            ruleLayout.addWidget(ruleEdit, 1,7-i)
            self.ruleEdits.append(ruleEdit)

        validator2 = QIntValidator(0,255)
        self.rule10Edit = QLineEdit()
        self.rule10Edit.setValidator(validator2)
        self.rule10Edit.textEdited.connect(self.update_rule10)
        rule10Layout = QHBoxLayout()
        rule10Layout.addWidget(QLabel("Rule"))
        rule10Layout.addWidget(self.rule10Edit)

        self.resetButton = QPushButton("&Reset")
        self.resetButton.clicked.connect(self.reset)
        self.randomInitButton = QPushButton("&Random init")
        self.randomInitButton.clicked.connect(self.randomInit)
        self.nextButton = QPushButton("&Next")
        self.nextButton.clicked.connect(self.do_next)
        self.prevButton = QPushButton("&Prev")
        self.prevButton.clicked.connect(self.do_prev)
        self.autoButton = QPushButton("&Auto")
        self.autoButton.clicked.connect(self.auto)
        self.stopButton = QPushButton("&Stop")
        self.stopButton.clicked.connect(self.stop)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.resetButton)
        buttonLayout.addWidget(self.randomInitButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.prevButton)
        buttonLayout.addWidget(self.autoButton)
        buttonLayout.addWidget(self.stopButton)

        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(ruleLayout)
        propertyLayout.addLayout(rule10Layout)
        propertyLayout.addLayout(buttonLayout)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Cellular Automaton")
        self.updating_rule = False
        self.rule10Edit.setText("90")
        self.update_rule10()
        self.timer = None

    def update_rule(self):
        if self.updating_rule: return
        rule = 0
        for i in range(8):
            n = self.ruleEdits[i].text()
            if n == "": return
            rule = (rule << 1) + int(n)
        self.updating_rule = True
        self.rule10Edit.setText(str(rule))
        self.updating_rule = False

    def update_rule10(self):
        n = self.rule10Edit.text()
        if n == "": return
        rule = int(n)
        self.updating_rule = True
        for i in range(7,-1,-1):
            self.ruleEdits[i].setText(str(rule & 0b1))
            rule >>= 1
        self.updating_rule = False

    def do_next(self):
        n = self.rule10Edit.text()
        return self.celluarAutomaton.do_next(int(n))

    def do_prev(self):
        self.celluarAutomaton.do_prev()

    def reset(self):
        self.celluarAutomaton.reset()

    def randomInit(self):
        self.celluarAutomaton.randomInit()

    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def timeout(self):
        r = self.do_next()
        if not r:
            self.stop()

    def stop(self):
        if self.timer:
            self.timer.stop()
            self.timer = None

    #def keyPressEvent(self, event):
    #    key = event.key()
    #    super(MainWindow, self).keyPressEvent(event)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
