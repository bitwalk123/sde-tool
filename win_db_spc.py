#!/usr/bin/env python
# coding: utf-8

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QWidget,
)
from database import SqlDB
from resource import Icons


class WinDBSPC(QScrollArea):
    def __init__(self, db: SqlDB):
        super().__init__()
        self.setWidgetResizable(True)
        self.db = db
        self.icons = Icons()

        base = QWidget(self)
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)
        grid = QGridLayout()
        base.setLayout(grid)
        row = 0

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # SPC Label
        test = QLabel('SPC data')
        test.setStyleSheet("QLabel {font-size:14pt; padding: 0 2px; background: #ddf;}")
        test.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        grid.addWidget(test, row, 0, 1, 2)
        row += 1

        # ---------------------------------------------------------------------
        # Excel file read
        lab_dump_supplier = QLabel('Excel data uploader')
        lab_dump_supplier.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        but_dump_supplier = QPushButton()
        but_dump_supplier.setIcon(QIcon(self.icons.EXCEL))
        but_dump_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        but_dump_supplier.setStatusTip('read SPC Excel file')
        #but_dump_supplier.clicked.connect(self.on_click_dump_supplier)
        grid.addWidget(lab_dump_supplier, row, 0)
        grid.addWidget(but_dump_supplier, row, 1)
        row += 1
