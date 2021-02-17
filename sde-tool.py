#!/usr/bin/env python
# coding: utf-8

from PySide2.QtGui import QIcon
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
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


# =============================================================================
#  DBTab - Tab related to Database
# =============================================================================
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
        # SUPPLIER Label
        supplier = QLabel('<font size=14>SUPPLIER</font>')
        supplier.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(supplier, row, 0, 1, 6)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME SHORT
        lab_name_supplier_short = QLabel('<font size=4>SHORT NAME</font>')
        lab_name_supplier_short.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_name_supplier_short = QLineEdit()
        ent_name_supplier_short.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_name_supplier_short = QPushButton()
        but_name_supplier_short.setIcon(QIcon(self.icons.CHECK))
        but_name_supplier_short.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_name_supplier_short, row, 0)
        grid.addWidget(ent_name_supplier_short, row, 1)
        grid.addWidget(but_name_supplier_short, row, 5, 3, 1)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME FULL
        lab_name_supplier = QLabel('<font size=4>FULL NAME</font>')
        lab_name_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_name_supplier = QLineEdit()
        ent_name_supplier.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(lab_name_supplier, row, 0)
        grid.addWidget(ent_name_supplier, row, 1, 1, 4)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME in local language
        lab_name_supplier_local = QLabel('<font size=4>Local NAME</font>')
        lab_name_supplier_local.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_name_supplier_local = QLineEdit()
        ent_name_supplier_local.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(lab_name_supplier_local, row, 0)
        grid.addWidget(ent_name_supplier_local, row, 1, 1, 4)
        row += 1

        # click on but_name_supplier_short
        but_name_supplier_short.clicked.connect(
            lambda: self.on_click_set_supplier(
                ent_name_supplier_short,
                ent_name_supplier,
                ent_name_supplier_local
            )
        )

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # PART Label
        part = QLabel('<font size=14>PART</font>')
        part.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(part, row, 0, 1, 6)
        row += 1

        # ---------------------------------------------------------------------
        # PART NUMBER
        lab_num_part = QLabel('<font size=4>PART#</font>')
        lab_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_num_part = QLineEdit()
        ent_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_num_part = QPushButton()
        but_num_part.setIcon(QIcon(self.icons.CHECK))
        but_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_num_part, row, 0)
        grid.addWidget(ent_num_part, row, 1)
        grid.addWidget(but_num_part, row, 5, 4, 1)
        row += 1

        # ---------------------------------------------------------------------
        # Original PART NUMBER
        lab_num_part_orig = QLabel('<font size=4>Orig. PART#</font>')
        lab_num_part_orig.setStyleSheet("QLabel {color: gray;}")
        lab_num_part_orig.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo_num_part_orig = QComboBox()
        combo_num_part_orig.setEnabled(False)
        combo_num_part_orig.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        check_num_part_orig = QCheckBox('use original drawing')
        check_num_part_orig.stateChanged.connect(
            lambda: self.getPartsOptionCombo(
                combo_num_part_orig,
                check_num_part_orig
            )
        )
        grid.addWidget(lab_num_part_orig, row, 0)
        grid.addWidget(combo_num_part_orig, row, 1)
        grid.addWidget(check_num_part_orig, row, 2, 1, 3)
        row += 1

        # ---------------------------------------------------------------------
        # PART Description
        lab_desc_part = QLabel('<font size=4>Description</font>')
        lab_desc_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_desc_part = QLineEdit()
        ent_desc_part.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(lab_desc_part, row, 0)
        grid.addWidget(ent_desc_part, row, 1, 1, 4)
        row += 1

        # ---------------------------------------------------------------------
        # PART Supplier
        lab_part_supplier = QLabel('<font size=4>Part Supplier</font>')
        lab_part_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo_part_supplier = QComboBox()
        self.add_supplier_list_to_combo(combo_part_supplier)
        combo_part_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab_part_supplier, row, 0)
        grid.addWidget(combo_part_supplier, row, 1)
        row += 1

        # click on but_num_part
        but_num_part.clicked.connect(
            lambda: self.on_click_set_part(
                ent_num_part,
                combo_num_part_orig,
                check_num_part_orig,
                ent_desc_part,
                combo_part_supplier
            )
        )

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Drawing Label
        part = QLabel('<font size=14>Drawing</font>')
        part.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(part, row, 0, 1, 6)
        row += 1

        # ---------------------------------------------------------------------
        # Horizontal Line 1
        # hline1 = QFrame(self)
        # hline1.setFrameShape(QFrame.HLine)
        # hline1.setFrameShadow(QFrame.Sunken)
        # hline1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # grid.addWidget(hline1, row, 0, 1, 6)
        # row += 1

        # ---------------------------------------------------------------------
        # Drawing (small label)
        # lab_title_drawing = QLabel('<font size=4>Drawing</font>')
        # grid.addWidget(lab_title_drawing, row, 0, 1, 6)
        # row += 1

        # ---------------------------------------------------------------------
        # PART Number
        lab_num_part_drawing = QLabel('<font size=4>Part#</font>')
        lab_num_part_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo_num_part_drawing = QComboBox()
        combo_num_part_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.getParts4Combo(combo_num_part_drawing)
        but_num_part_drawing = QPushButton()
        but_num_part_drawing.setIcon(QIcon(self.icons.CHECK))
        but_num_part_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_num_part_drawing, row, 0)
        grid.addWidget(combo_num_part_drawing, row, 1)
        grid.addWidget(but_num_part_drawing, row, 5, 3, 1)
        row += 1

        # ---------------------------------------------------------------------
        # PART Drawing Revision
        lab_rev_drawing = QLabel('<font size=4>Revision</font>')
        lab_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_rev_drawing = QLineEdit()
        ent_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab_rev_drawing, row, 0)
        grid.addWidget(ent_rev_drawing, row, 1)
        row += 1

        # ---------------------------------------------------------------------
        # PART Drawing file
        lab_file_drawing = QLabel('<font size=4>PDF file</font>')
        lab_file_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_file_drawing = QLineEdit()
        ent_file_drawing.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        but_file_drawing = QPushButton()
        but_file_drawing.setIcon(QIcon(self.icons.ADD))
        but_file_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab_file_drawing, row, 0)
        grid.addWidget(ent_file_drawing, row, 1, 1, 3)
        grid.addWidget(but_file_drawing, row, 4)
        row += 1

    # -------------------------------------------------------------------------
    #  getParts4Combo
    #  get parts list for combobox
    #
    #  argument
    #    combo: QComboBox
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def getParts4Combo(self, combo: QComboBox):
        combo.clear()
        combo.clearEditText()
        sql = "SELECT num_part FROM part;"
        out = self.db.get(sql)
        for supplier in out:
            combo.addItem(supplier[0])
        combo.setEnabled(True)

    # -------------------------------------------------------------------------
    #  getPartsOptionCombo
    #  get parts list for combobox activated by checkbox
    #
    #  argument
    #    combo: QComboBox
    #    check: QCheckBox
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def getPartsOptionCombo(self, combo: QComboBox, check: QCheckBox):
        combo.clear()
        combo.clearEditText()
        if check.checkState() == Qt.Checked:
            sql = "SELECT num_part FROM part;"
            out = self.db.get(sql)
            for supplier in out:
                combo.addItem(supplier[0])
            combo.setEnabled(True)
        else:
            combo.setEnabled(False)

    # -------------------------------------------------------------------------
    #  add_supplier_list_to_combo
    #  add supplier list to specified combobox
    #
    #  argument
    #    obj_combo: QComboBox  instance of QComboBox
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def add_supplier_list_to_combo(self, obj_combo: QComboBox):
        obj_combo.clear()
        obj_combo.clearEditText()
        sql = "SELECT name_supplier_short FROM supplier;"
        out = self.db.get(sql)
        for supplier in out:
            obj_combo.addItem(supplier[0])

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

        sql = self.db.sql(
            "INSERT INTO supplier VALUES(NULL, '?', '?', '?');",
            [name_supplier_short, name_supplier, name_supplier_local]
        )
        self.db.put(sql)

    # -------------------------------------------------------------------------
    #  on_click_part
    #  add part to database
    #
    #  argument
    #    obj_short: QLineEdit  Common name of supplier
    #    obj_full: QLineEdit   Full name of supplier in English
    #    obj_local: QLineEdit  Full name of supplier in Local Language
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def on_click_set_part(self, obj_part: QLineEdit, obj_combo_1: QComboBox, obj_check: QCheckBox, obj_desc: QLineEdit, obj_combo_2: QComboBox):
        # obtain part number
        num_part = obj_part.text()
        obj_part.setText(None)

        # obtain original part number if selected
        id_part_orig = 'NULL'
        if obj_combo_1.isEnabled():
            num_part_org = obj_combo_1.currentText()
            sql1 = self.db.sql(
                "SELECT id_part FROM part WHERE num_part = '?';", [num_part_org])
            print(sql1)
            out = self.db.get(sql1)
            for id in out:
                id_part_orig = id[0]
            obj_combo_1.clear()
            obj_combo_1.clearEditText()
            obj_combo_1.setEnabled(False)

        # clear QCheckBox
        if obj_check.isChecked():
            obj_check.setEnabled(False)

        # obtain part description
        description = obj_desc.text()
        obj_desc.setText(None)

        # obtain id_supplier from selected supplier on the QComboBox
        supplier = obj_combo_2.currentText()
        sql2 = self.db.sql(
            "SELECT id_supplier FROM supplier WHERE name_supplier_short = '?';", [supplier])
        print(sql2)
        out = self.db.get(sql2)
        for id in out:
            id_supplier = id[0]

        print(num_part)
        print(description)
        print(supplier)
        print(id_supplier)

        # insert new part to part table
        sql3 = self.db.sql(
            "INSERT INTO part VALUES(NULL, ?, ?, '?', '?', NULL);",
            [id_part_orig, id_supplier, num_part, description]
        )
        print(sql3)
        self.db.put(sql3)

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

        # ---------------------------------------------------------------------
        # PART dump
        lab_dump_part = QLabel('<font size=4>DUMP table part</font>')
        but_dump_part = QPushButton()
        but_dump_part.setIcon(QIcon(self.icons.CHECK))
        but_dump_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        but_dump_part.clicked.connect(self.on_click_dump_part)
        grid.addWidget(lab_dump_part, row, 0)
        grid.addWidget(but_dump_part, row, 1)
        row += 1

    def on_click_dump_supplier(self):
        sql = "SELECT * FROM supplier;"
        out = self.db.get(sql)
        print(len(out))
        for line in out:
            print(line)

    def on_click_dump_part(self):
        sql = "SELECT * FROM part;"
        out = self.db.get(sql)
        print(len(out))
        for line in out:
            print(line)

def main():
    app = QApplication(sys.argv)
    ex = SDETool()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
