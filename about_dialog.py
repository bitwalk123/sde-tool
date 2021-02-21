#!/usr/bin/env python
# coding: utf-8

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from resource import Icons

class AboutDlg(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.icons = Icons()

        grid = QGridLayout()
        base = QWidget()
        base.setLayout(grid)
        but = QPushButton('OK')

        layout = QVBoxLayout()
        layout.addWidget(base)
        layout.addWidget(but)
        self.setLayout(layout)

        # click
        but.clicked.connect(self.closeEvent)
        row = 0

        lab_app_name = QLabel(parent.APP_NAME)
        lab_app_name.setStyleSheet("QLabel {font-size:14pt; padding: 0 2px;}")
        lab_app_name.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(lab_app_name, row, 0, 1, 2)
        row += 1

        lab_app_ver1 = QLabel('version')
        lab_app_ver1.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_app_ver1.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        lab_app_ver2 = QLabel(parent.APP_VER)
        lab_app_ver2.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_app_ver2.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(lab_app_ver1, row, 0)
        grid.addWidget(lab_app_ver2, row, 1)
        row += 1

    # Greets the user
    def closeEvent(self, event):
        self.close()
