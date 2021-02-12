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
    # icons
    icon_exit: str = 'images/Apps-Dialog-Shutdown-icon.png'

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('SDE Tool')
        self.show()

    def initUI(self):
        # Create pyqt toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # spacer
        spacer: QWidget = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        but_exit = QToolButton()
        but_exit.setIcon(QIcon(self.icon_exit))
        but_exit.setStatusTip('Exit application')
        but_exit.clicked.connect(self.closeEvent)
        toolbar.addWidget(but_exit)

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
