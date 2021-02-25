#!/usr/bin/env python
# coding: utf-8

from PySide2.QtGui import QIcon
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QWidget,
)
from database import SqlDB
from resource import Icons


class WinDBData(QScrollArea):
    def __init__(self, db: SqlDB):
        super().__init__()
        self.setWidgetResizable(True)
        self.db = db
        self.icons = Icons()

        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)
        grid = QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 2)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(4, 1)
        grid.setColumnStretch(5, 1)
        base.setLayout(grid)
        row = 0

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # SUPPLIER Label
        supplier = QLabel('SUPPLIER')
        supplier.setStyleSheet("QLabel {font-size:14pt; padding: 0 2px; background: #ddf;}")
        supplier.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(supplier, row, 0, 1, 6)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME SHORT
        lab_name_supplier_short = QLabel('SHORT NAME')
        lab_name_supplier_short.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
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
        lab_name_supplier = QLabel('FULL NAME')
        lab_name_supplier.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_name_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_name_supplier = QLineEdit()
        ent_name_supplier.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(lab_name_supplier, row, 0)
        grid.addWidget(ent_name_supplier, row, 1, 1, 4)
        row += 1

        # ---------------------------------------------------------------------
        # SUPPLIER NAME in local language
        lab_name_supplier_local = QLabel('Local NAME')
        lab_name_supplier_local.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
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
        part = QLabel('PART')
        part.setStyleSheet("QLabel {font-size:14pt; padding: 0 2px; background: #ddf;}")
        part.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(part, row, 0, 1, 6)
        row += 1

        # ---------------------------------------------------------------------
        # PART NUMBER
        lab_num_part = QLabel('PART#')
        lab_num_part.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_num_part = QLineEdit()
        ent_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_num_part = QPushButton()
        but_num_part.setIcon(QIcon(self.icons.CHECK))
        but_num_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_num_part, row, 0)
        grid.addWidget(ent_num_part, row, 1)
        grid.addWidget(but_num_part, row, 5, 5, 1)
        row += 1

        # ---------------------------------------------------------------------
        # Original PART NUMBER
        lab_num_part_orig = QLabel('Orig. PART#')
        lab_num_part_orig.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;color: gray;}")
        lab_num_part_orig.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo_num_part_orig = QComboBox()
        combo_num_part_orig.setEnabled(False)
        combo_num_part_orig.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        check_num_part_orig = QCheckBox('use original drawing')
        check_num_part_orig.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        check_num_part_orig.stateChanged.connect(
            lambda: self.getPartsOptionCombo(
                lab_num_part_orig,
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
        lab_desc_part = QLabel('Description')
        lab_desc_part.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_desc_part.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_desc_part = QLineEdit()
        ent_desc_part.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(lab_desc_part, row, 0)
        grid.addWidget(ent_desc_part, row, 1, 1, 4)
        row += 1

        # ---------------------------------------------------------------------
        # PART Supplier
        lab_part_supplier = QLabel('Part Supplier')
        lab_part_supplier.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_part_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo_part_supplier = QComboBox()
        self.add_supplier_list_to_combo(combo_part_supplier)
        combo_part_supplier.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(lab_part_supplier, row, 0)
        grid.addWidget(combo_part_supplier, row, 1)
        row += 1

        # ---------------------------------------------------------------------
        # Assy PART NUMBER
        lab_num_part_assy = QLabel('Assy PART#')
        lab_num_part_assy.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;color: gray;}")
        lab_num_part_assy.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo_num_part_assy = QComboBox()
        combo_num_part_assy.setEnabled(False)
        combo_num_part_assy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        check_num_part_assy = QCheckBox('link to Assy')
        check_num_part_assy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        #check_num_part_assy.stateChanged.connect(
        #    lambda: self.getPartsOptionCombo(
        #        lab_num_part_assy,
        #        combo_num_part_assy,
        #        check_num_part_assy
        #    )
        #)
        grid.addWidget(lab_num_part_assy, row, 0)
        grid.addWidget(combo_num_part_assy, row, 1)
        grid.addWidget(check_num_part_assy, row, 2, 1, 3)
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
        drawing = QLabel('Drawing')
        drawing.setStyleSheet("QLabel {font-size:14pt; padding: 0 2px; background: #ddf;}")
        drawing.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(drawing, row, 0, 1, 6)
        row += 1

        # ---------------------------------------------------------------------
        # PART Number
        lab_num_part_drawing = QLabel('Part#')
        lab_num_part_drawing.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_num_part_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo_num_part_drawing = QComboBox()
        combo_num_part_drawing.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        combo_num_part_drawing.setEnabled(False)
        self.getParts4Combo(combo_num_part_drawing)
        lab_num_supplier_drawing = QLabel()
        lab_num_supplier_drawing.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px; color:gray;}")
        lab_num_supplier_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but_num_part_drawing = QPushButton()
        but_num_part_drawing.setIcon(QIcon(self.icons.CHECK))
        but_num_part_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab_num_part_drawing, row, 0)
        grid.addWidget(combo_num_part_drawing, row, 1)
        grid.addWidget(lab_num_supplier_drawing, row, 2, 1, 3)
        grid.addWidget(but_num_part_drawing, row, 5, 4, 1)
        row += 1

        # ---------------------------------------------------------------------
        # PART Drawing Description
        lab_num_desc_drawing = QLabel()
        lab_num_desc_drawing.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px; color:gray;}")
        lab_num_desc_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab_num_desc_drawing, row, 1, 1, 4)
        row += 1

        self.part_selection_change(combo_num_part_drawing, lab_num_supplier_drawing, lab_num_desc_drawing)
        combo_num_part_drawing.currentIndexChanged.connect(
            lambda: self.part_selection_change(
                combo_num_part_drawing,
                lab_num_supplier_drawing,
                lab_num_desc_drawing
            )
        )
        # ---------------------------------------------------------------------
        # PART Drawing Revision
        lab_rev_drawing = QLabel('Revision')
        lab_rev_drawing.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_rev_drawing = QLineEdit()
        ent_rev_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab_rev_drawing, row, 0)
        grid.addWidget(ent_rev_drawing, row, 1)
        row += 1

        # ---------------------------------------------------------------------
        # PART Drawing file
        lab_file_drawing = QLabel('PDF file')
        lab_file_drawing.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        lab_file_drawing.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ent_file_drawing = QLineEdit()
        ent_file_drawing.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        but_file_drawing = QPushButton()
        but_file_drawing.setIcon(QIcon(self.icons.PDF))
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
    def getPartsOptionCombo(self, label: QLabel, combo: QComboBox, check: QCheckBox):
        combo.clear()
        combo.clearEditText()
        if check.checkState() == Qt.Checked:
            sql = "SELECT num_part FROM part;"
            out = self.db.get(sql)
            for supplier in out:
                combo.addItem(supplier[0])
            label.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;color: black;}")
            combo.setEnabled(True)
        else:
            label.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;color: gray;}")
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
            "INSERT INTO part VALUES(NULL, ?, ?, '?', '?', NULL, NULL);",
            [id_part_orig, id_supplier, num_part, description]
        )
        print(sql3)
        self.db.put(sql3)

    # -------------------------------------------------------------------------
    #  part_selection_change
    #  PART selection change in Drwaing part
    #
    #  argument
    #    obj_combo: QComboBox
    #    obj_lab_supplier: QLabel
    #    obj_lab_desc: QLabel
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def part_selection_change(self, obj_combo: QComboBox, obj_lab_supplier: QLabel, obj_lab_desc: QLabel):
        num_part = obj_combo.currentText()
        if len(num_part) == 0:
            return
        print(num_part)

        sql1 = self.db.sql("SELECT id_part, id_supplier FROM part WHERE num_part = '?';", [num_part])
        out = self.db.get(sql1)
        for id in out:
            id_part = id[0]
            id_supplier = id[1]
        print(id_part)
        print(id_supplier)

        sql3 = self.db.sql("SELECT name_supplier_short FROM supplier WHERE id_supplier = ?;", [id_supplier])
        out = self.db.get(sql3)
        for id in out:
            name_supplier_short = id[0]
        print(name_supplier_short)

        sql4 = self.db.sql("SELECT description FROM part WHERE id_part = ?;", [id_part])
        out = self.db.get(sql4)
        for id in out:
            description = id[0]
        print(description)

        obj_lab_supplier.setText(name_supplier_short)
        obj_lab_desc.setText(description)

