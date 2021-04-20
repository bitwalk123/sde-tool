#!/usr/bin/env python
# coding: utf-8

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QTabWidget,
)
from database import SqlDB
from win_db_basic import WinDBData
from win_db_pcs import WinDBPCS
from win_db_misc import WinDBMisc
from win_db_spc import WinDBSPC
from resource import Icons


# =============================================================================
#  DBTab - Tab related to Database
# =============================================================================
class TabDB(QTabWidget):
    def __init__(self, db: SqlDB):
        super().__init__()
        self.db = db
        self.icons = Icons()

        tab_data = WinDBData(self.db)
        self.addTab(tab_data, QIcon(self.icons.PEN), 'Basic')

        tab_pcs = WinDBPCS(self.db)
        self.addTab(tab_pcs, QIcon(self.icons.CLIP), 'PCS')

        tab_spc = WinDBSPC(self.db)
        self.addTab(tab_spc, QIcon(self.icons.PLOT), 'SPC')

        tab_misc = WinDBMisc(self.db)
        self.addTab(tab_misc, QIcon(self.icons.CONF), 'Misc.')
