#!/usr/bin/env python
# coding: utf-8

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QTabWidget,
)
from database import SqlDB
from win_db_basic import WinDBData
from win_db_pcs import WinDBPCS
from win_db_misc import WinDBMisc
from resource import Icons


# =============================================================================
#  DBTab - Tab related to Database
# =============================================================================
class TabSPC(QTabWidget):
    def __init__(self, db: SqlDB):
        super().__init__()
        self.db = db
        self.icons = Icons()

