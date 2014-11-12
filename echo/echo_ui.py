# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'echo.ui'
#
# Created: Wed Nov 12 18:33:05 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Echo(object):
    def setupUi(self, Echo):
        Echo.setObjectName("Echo")
        Echo.resize(250, 200)
        self.textBrowser = QtWidgets.QTextBrowser(Echo)
        self.textBrowser.setGeometry(QtCore.QRect(40, 90, 180, 79))
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Echo)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 30, 180, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.inputEdit.setObjectName("inputEdit")
        self.horizontalLayout.addWidget(self.inputEdit)
        self.submitButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.submitButton.setObjectName("submitButton")
        self.horizontalLayout.addWidget(self.submitButton)

        self.retranslateUi(Echo)
        QtCore.QMetaObject.connectSlotsByName(Echo)

    def retranslateUi(self, Echo):
        _translate = QtCore.QCoreApplication.translate
        Echo.setWindowTitle(_translate("Echo", "Echo"))
        self.submitButton.setText(_translate("Echo", "Submit"))

