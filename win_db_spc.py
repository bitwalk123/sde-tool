#!/usr/bin/env python
# coding: utf-8

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
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
