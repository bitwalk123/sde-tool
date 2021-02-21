#!/usr/bin/env python
# coding: utf-8

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QToolButton,
    QWidget,
)
import configparser
import os.path
import sys
from about_dialog import AboutDlg
from database import SqlDB
from tab_db import TabDB
from tab_pcs import TabPCS
from tab_spc import TabSPC
from resource import Icons


# =============================================================================
#  SDETool - main class of SDE Tool
# =============================================================================
class SDETool(QMainWindow):
    # Application information
    APP_NAME: str = 'SPC Tool'
    APP_VER: str = '0.3 (alpha)'

    # initial windows position and size
    x_init: int = 100
    y_init: int = 100
    w_init: int = 800
    h_init: int = 600

    # configuraion file
    confFile: str = 'sde.ini'
    config: configparser.ConfigParser = None

    def __init__(self):
        super().__init__()

        # CONFIGURATION FILE READ
        self.config = configparser.ConfigParser()
        self.config.read(self.confFile, 'UTF-8')

        # INITIALIZE
        self.initDB()
        self.initUI()

    # -------------------------------------------------------------------------
    #  initDB
    # -------------------------------------------------------------------------
    def initDB(self):
        self.icons = Icons()
        # ---------------------------------------------------------------------
        #  DATABASE CONNECTION
        # ---------------------------------------------------------------------
        # Config for Database
        config_db = self.config['Database']
        dbname = config_db['DBNAME']

        # get database instance
        self.db = SqlDB(dbname)
        if not os.path.exists(dbname):
            # If database does not exist, create new database.
            self.db.init()

            # 'New DB is created.' dialog
            QMessageBox.warning(
                self,
                'New DB',
                'New DB is created.',
                QMessageBox.Ok,
                QMessageBox.Ok
            )

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

        # button for application information
        but_info = QToolButton()
        but_info.setIcon(QIcon(self.icons.INFO))
        but_info.setStatusTip('About this application')
        but_info.clicked.connect(self.aboutApp)
        toolbar.addWidget(but_info)

        # button for application exit
        but_exit = QToolButton()
        but_exit.setIcon(QIcon(self.icons.EXIT))
        but_exit.setStatusTip('Exit application')
        but_exit.clicked.connect(self.closeEvent)
        toolbar.addWidget(but_exit)

        # --------------
        # Tab widget
        tabwidget: QTabWidget = QTabWidget()
        tabwidget.setTabPosition(QTabWidget.South)
        self.setCentralWidget(tabwidget)
        self.createTabs(tabwidget)

        # Status Bar
        statusbar: QStatusBar = QStatusBar()
        self.setStatusBar(statusbar)

        # show window
        self.setWindowTitle(self.getAppTitle())
        self.setGeometry(self.x_init, self.y_init, self.w_init, self.h_init)
        self.show()

    # -------------------------------------------------------------------------
    #  createTabs
    #  create tabs on the QTabWidget
    #
    #  argument
    #    parent: QTabWidget
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def createTabs(self, parent: QTabWidget):
        # tab_pcs
        tab_pcs = TabPCS(self.db)
        parent.addTab(tab_pcs, QIcon(self.icons.CLIP), 'PCS')

        # tab_spc
        tab_spc = TabSPC(self.db)
        parent.addTab(tab_spc, QIcon(self.icons.PLOT), 'SPC')

        # tab_db
        tab_db = TabDB(self.db)
        parent.addTab(tab_db, QIcon(self.icons.DB), 'Database')

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
        title: str = self.APP_NAME + ' - ' + self.APP_VER
        return (title)

    # -------------------------------------------------------------------------
    #  aboutApp
    #  Application Information
    #
    #  argument
    #    event
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def aboutApp(self, event):
        sender = self.sender()
        dlg = AboutDlg(self)
        dlg.show()

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
