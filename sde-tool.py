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
from resource import Icons


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
        # tab_database
        tab_database = DBTab(self.db)
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


class DBTab(QTabWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.icons = Icons()

        tab_add = QScrollArea()
        tab_add.setWidgetResizable(True)
        self.create_tab_add(tab_add)
        self.addTab(tab_add, QIcon(self.icons.PEN), 'Data Input')

        tab_misc = QScrollArea()
        tab_misc.setWidgetResizable(True)
        self.create_tab_misc(tab_misc)
        self.addTab(tab_misc, QIcon(self.icons.CONF), 'Misc.')

    # =========================================================================
    #  create_tab_add
    #  create tab 'tab_add"
    #
    #  argument
    #    parentparent: QScrollArea
    #
    #  return
    #    (none)
    # =========================================================================
    def create_tab_add(self, parent: QScrollArea):
        base = QWidget(self)
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        parent.setWidget(base)
        grid = QGridLayout()
        base.setLayout(grid)
        row = 0

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # PART Label
        part = QLabel('<font size=14>PART</font>')
        part.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(part, row, 0, 1, 4)
        row += 1

        # ---------------------------------------------------------------------
        # PART NUMBER
        lab_num_part = QLabel('<font size=4>PART#</font>')
        ent_num_part = QLineEdit()
        ent_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_num_part = QPushButton()
        but_num_part.setIcon(QIcon(self.icons.CHECK))
        but_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_num_part, row, 0)
        grid.addWidget(ent_num_part, row, 1, 1, 2)
        grid.addWidget(but_num_part, row, 3, 2, 1)
        row += 1

        # ---------------------------------------------------------------------
        # PART Description
        lab_desc_part = QLabel('<font size=4>Description</font>')
        ent_desc_part = QLineEdit()
        grid.addWidget(lab_desc_part, row, 0)
        grid.addWidget(ent_desc_part, row, 1, 1, 2)
        row += 1

        # ---------------------------------------------------------------------
        # Horizontal Line 1
        hline1 = QFrame(self)
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        hline1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(hline1, row, 0, 1, 4)
        row += 1

        # ---------------------------------------------------------------------
        # Drawing (small label)
        title = QLabel('<font size=4>Drawing</font>')
        grid.addWidget(title, row, 0, 1, 4)
        row += 1

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # PART Drawing Revision
        lab_rev_drawing = QLabel('<font size=4>Revision</font>')
        ent_rev_drawing = QLineEdit()
        ent_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_rev_drawing = QPushButton()
        but_rev_drawing.setIcon(QIcon(self.icons.CHECK))
        but_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_rev_drawing, row, 0)
        grid.addWidget(ent_rev_drawing, row, 1)
        grid.addWidget(but_rev_drawing, row, 3, 2, 1)
        row += 1

        # ---------------------------------------------------------------------
        # PART Drawing file
        lab_file_drawing = QLabel('<font size=4>PDF file</font>')
        ent_file_drawing = QLineEdit()
        but_file_drawing = QPushButton()
        but_file_drawing.setIcon(QIcon(self.icons.ADD))
        grid.addWidget(lab_file_drawing, row, 0)
        grid.addWidget(ent_file_drawing, row, 1)
        grid.addWidget(but_file_drawing, row, 2)
        row += 1

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # SUPPLIER Label
        supplier = QLabel('<font size=14>SUPPLIER</font>')
        supplier.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(supplier, row, 0, 1, 4)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME SHORT
        lab_name_supplier_short = QLabel('<font size=4>SHORT NAME</font>')
        ent_name_supplier_short = QLineEdit()
        ent_name_supplier_short.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_name_supplier_short = QPushButton()
        but_name_supplier_short.setIcon(QIcon(self.icons.CHECK))
        but_name_supplier_short.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_name_supplier_short, row, 0)
        grid.addWidget(ent_name_supplier_short, row, 1)
        grid.addWidget(but_name_supplier_short, row, 3, 3, 1)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME FULL
        lab_name_supplier = QLabel('<font size=4>FULL NAME</font>')
        ent_name_supplier = QLineEdit()
        grid.addWidget(lab_name_supplier, row, 0)
        grid.addWidget(ent_name_supplier, row, 1, 1, 2)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME in local language
        lab_name_supplier_local = QLabel('<font size=4>Local NAME</font>')
        ent_name_supplier_local = QLineEdit()
        grid.addWidget(lab_name_supplier_local, row, 0)
        grid.addWidget(ent_name_supplier_local, row, 1, 1, 2)
        row += 1

        # button click
        but_name_supplier_short.clicked.connect(
            lambda: self.on_click_set_supplier(
                ent_name_supplier_short,
                ent_name_supplier,
                ent_name_supplier_local
            )
        )

    # -------------------------------------------------------------------------
    #  on_click_supplier
    #  add supplier to database
    #
    #  argument
    #    obj_short: QLineEdit  Common name of supplier
    #    obj_full: QLineEdit   Full name of supplier in English
    #    obj_local: QLineEdit  Full name of supplier in Local Language
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def on_click_set_supplier(self, obj_short: QLineEdit, obj_full: QLineEdit, obj_local: QLineEdit):
        name_supplier_short = obj_short.text()
        name_supplier = obj_full.text()
        name_supplier_local = obj_local.text()
        obj_short.setText(None)
        obj_full.setText(None)
        obj_local.setText(None)

        sql = self.db.sql("INSERT INTO supplier VALUES(NULL, '?', '?', '?')", [name_supplier_short, name_supplier, name_supplier_local])
        #print(sql)
        self.db.put(sql)

    # =========================================================================
    #  create_tab_misc
    #  create tab 'tab_misc"
    #
    #  argument
    #    parentparent: QScrollArea
    #
    #  return
    #    (none)
    # =========================================================================
    def create_tab_misc(self, parent: QScrollArea):
        base = QWidget(self)
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        parent.setWidget(base)
        grid = QGridLayout()
        base.setLayout(grid)
        row = 0

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # TEST Label
        test = QLabel('<font size=14>TEST</font>')
        test.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(test, row, 0, 1, 2)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER dump
        lab_dump_supplier = QLabel('<font size=4>DUMP table supplier</font>')
        but_dump_supplier = QPushButton()
        but_dump_supplier.setIcon(QIcon(self.icons.CHECK))
        but_dump_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        but_dump_supplier.clicked.connect(self.on_click_dump_supplier)
        grid.addWidget(lab_dump_supplier, row, 0)
        grid.addWidget(but_dump_supplier, row, 1)
        row += 1

    def on_click_dump_supplier(self):
        sql = "SELECT * FROM supplier;"
        out = self.db.get(sql)
        for line in out:
            print(line)

def main():
    app = QApplication(sys.argv)
    ex = SDETool()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
