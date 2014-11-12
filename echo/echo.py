#!/usr/bin/env python

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
import echo_ui

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = echo_ui.Ui_Echo()
        self.ui.setupUi(self)
        self.ui.submitButton.clicked.connect(self.submit)

    def submit(self):
        text = self.ui.inputEdit.text()
        self.ui.textBrowser.append(text)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
