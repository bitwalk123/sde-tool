#!/usr/bin/env python
# coding: utf-8

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
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
        grid.addWidget(lab_app_name, row, 0, 1, 2)
        row += 1

        lab_app_ver1 = QLabel('VERSION')
        lab_app_ver1.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_app_ver2 = QLabel(parent.APP_VER)
        lab_app_ver2.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        grid.addWidget(lab_app_ver1, row, 0)
        grid.addWidget(lab_app_ver2, row, 1)
        row += 1

        lab_app_copyright1 = QLabel('COPYRIGHT')
        lab_app_copyright1.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_app_copyright2 = QLabel(parent.APP_COPYRIGHT)
        lab_app_copyright2.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        grid.addWidget(lab_app_copyright1, row, 0)
        grid.addWidget(lab_app_copyright2, row, 1)
        row += 1

        lab_app_license1 = QLabel('LICENSE')
        lab_app_license1.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_app_license2 = QLabel(parent.APP_LICENSE)
        lab_app_license2.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_app_license2.setOpenExternalLinks(True)
        grid.addWidget(lab_app_license1, row, 0)
        grid.addWidget(lab_app_license2, row, 1)
        row += 1

        self.setWindowIcon(QIcon(self.icons.INFO))
        self.show()


    # Greets the user
    def closeEvent(self, event):
        self.close()
