#!/usr/bin/env python
# coding: utf-8

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QGridLayout,
    QWidget,
)
from database import SqlDB
from win_db_basic import WinDBData
from win_db_pcs import WinDBPCS
from win_db_misc import WinDBMisc
from resource import Icons


# =============================================================================
#  DBTab - Tab related to Database
# =============================================================================
class TabPCS(QWidget):
    def __init__(self, db: SqlDB):
        super().__init__()
        self.db = db
        self.icons = Icons()

        #self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid = QGridLayout()
        self.setLayout(grid)
        row = 0

        # ---------------------------------------------------------------------
        # SUPPLIER dump
        lab_supplier = QLabel('Supplier')
        lab_supplier.setStyleSheet("QLabel {font-size:10pt; padding: 0 2px;}")
        #lab_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab_supplier, row, 0)
        row += 1
