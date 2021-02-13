#!/usr/bin/env python
# coding: utf-8

import sys
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget,
)


class SDETool(QMainWindow):
    # Application information
    app_name: str = 'SPC Tool'
    app_ver: str = '0.3 (alpha)'

    # icons
    icon_exit: str = 'images/Apps-Dialog-Shutdown-icon.png'

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle(self.getAppTitle())
        self.show()

    # -------------------------------------------------------------------------
    #  initUI
    # -------------------------------------------------------------------------
    def initUI(self):
        # Create pyqt toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # spacer
        spacer: QWidget = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        # button for application exit
        but_exit = QToolButton()
        but_exit.setIcon(QIcon(self.icon_exit))
        but_exit.setStatusTip('Exit application')
        but_exit.clicked.connect(self.closeEvent)
        toolbar.addWidget(but_exit)

    # -------------------------------------------------------------------------
    #  getAppTitle
    #  get application title string
    #
    #  argument
    #    (none)
    #
    #  return
    #    application title string
    # -------------------------------------------------------------------------
    def getAppTitle(self):
        title: str = self.app_name + ' - ' + self.app_ver
        return(title)

    # -------------------------------------------------------------------------
    #  closeEvent
    #  Dialog for close confirmation
    #
    #  argument
    #    event
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def closeEvent(self, event):
        sender = self.sender()

        reply: QMessageBox.StandardButton = QMessageBox.warning(
            self,
            'Quit App',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if sender is not None:
            # Exit button is clicked
            if reply == QMessageBox.Yes:
                QApplication.quit()
            return
        else:
            # 'X' on the window is clicked
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


def main():
    app = QApplication(sys.argv)
    ex = SDETool()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
