#!/usr/bin/env python
# coding: utf-8

from PySide2.QtGui import QIcon
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
import configparser
import os.path
import pathlib
import platform
import sys
from database import SqlDB


class SDETool(QMainWindow):
    # Application information
    APP_NAME: str = 'SPC Tool'
    APP_VER: str = '0.3 (alpha)'

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
            reply: QMessageBox.StandardButton = QMessageBox.warning(
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

        # button for application exit
        but_exit = QToolButton()
        but_exit.setIcon(QIcon(self.icons.EXIT))
        but_exit.setStatusTip('Exit application')
        but_exit.clicked.connect(self.closeEvent)
        toolbar.addWidget(but_exit)

        # --------------
        # Tab widget
        tabwidget: QTabWidget = QTabWidget()
        self.setCentralWidget(tabwidget)
        self.createTabs(tabwidget)

        # Status Bar
        statusbar: QStatusBar = QStatusBar()
        self.setStatusBar(statusbar)

        # show window
        self.setWindowTitle(self.getAppTitle())
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
        # tab_database
        tab_database = DBConfig()
        parent.addTab(tab_database, QIcon(self.icons.DB), 'Database')

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


class DBConfig(QScrollArea):
    def __init__(self):
        super().__init__()
        self.icons = Icons()

        self.setWidgetResizable(True)
        base = QWidget(self)
        self.setWidget(base)

        grid = QGridLayout()
        base.setLayout(grid)

        title = QLabel("Database Settings")
        grid.addWidget(title, 0, 0, 1, 3)

        # PART
        part = QLabel("PART")
        grid.addWidget(part, 1, 0, 1, 4)

        lab_num_part = QLabel("PART#")
        ent_num_part = QLineEdit()
        ent_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_num_part = QPushButton()
        but_num_part.setIcon(QIcon(self.icons.CHECK))
        but_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_num_part, 2, 0)
        grid.addWidget(ent_num_part, 2, 1, 1, 2)
        grid.addWidget(but_num_part, 2, 3, 2, 1)

        lab_desc_part = QLabel("Description")
        ent_desc_part = QLineEdit()
        grid.addWidget(lab_desc_part, 3, 0)
        grid.addWidget(ent_desc_part, 3, 1, 1, 2)

        lab_rev_drawing = QLabel("REVISION")
        ent_rev_drawing = QLineEdit()
        ent_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_rev_drawing = QPushButton()
        but_rev_drawing.setIcon(QIcon(self.icons.CHECK))
        but_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_rev_drawing, 4, 0)
        grid.addWidget(ent_rev_drawing, 4, 1, 1, 2)
        grid.addWidget(but_rev_drawing, 4, 3, 2, 1)

        lab_file_drawing = QLabel("PDF File")
        ent_file_drawing = QLineEdit()
        but_file_drawing = QPushButton()
        but_file_drawing.setIcon(QIcon(self.icons.ADD))
        grid.addWidget(lab_file_drawing, 5, 0)
        grid.addWidget(ent_file_drawing, 5, 1)
        grid.addWidget(but_file_drawing, 5, 2)



class Icons():
    # icons
    ADD: str = 'images/iconfinder_insert-object_23421.png'
    CHECK: str = 'images/iconfinder_Tick_Mark_1398911.png'
    DB: str = 'images/iconfinder_database-px-png_63467.png'
    EXIT: str = 'images/Apps-Dialog-Shutdown-icon.png'

def main():
    app = QApplication(sys.argv)
    ex = SDETool()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
