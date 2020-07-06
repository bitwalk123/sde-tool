import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import pandas as pd
import math


class SPC():
    filename = None
    sheets = None
    valid = False

    # CONSTRUCTOR
    def __init__(self, filename):
        self.filename = filename
        self.sheets = self.read(filename)
        self.valid = self.check_valid_sheet(self.sheets)

    # -------------------------------------------------------------------------
    #  check_valid_sheet
    #  check if read file (sheets) has 'Master' tab
    #
    #  argument
    #    sheets : dataframe containing Excel contents
    #
    #  return
    #    True if dataframe is valid for SPC, otherwise False
    # -------------------------------------------------------------------------
    def check_valid_sheet(self, sheets):
        # check if 'Master' tab exists
        if 'Master' in sheets.keys():
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    #  get_master
    #  get dataframe of 'Master' tab
    #
    #  return
    #    dataframe of 'Master' tab
    # -------------------------------------------------------------------------
    def get_master(self):
        df_master = self.sheets['Master']
        # drop row if column 'Part Number' is NaN
        df_master = df_master.dropna(subset=['Part Number'])

        return df_master

    # -------------------------------------------------------------------------
    #  get_sheets
    #  get dataframe containing Excel contents
    #
    #  argument
    #    (none)
    #
    #  return
    #    dataframe containing Excel contents
    # -------------------------------------------------------------------------
    def get_sheets(self):
        return self.sheets

    # -------------------------------------------------------------------------
    #  read
    #  read specified Excel file
    #
    #  argument
    #    filename : Excel file
    #
    #  return
    #    array of dataframe including all Excel sheets
    # -------------------------------------------------------------------------
    def read(self, filename):
        # read specified filename as Excel file including all tabs
        return pd.read_excel(filename, sheet_name=None)

    # -------------------------------------------------------------------------
    #  create_tabs
    #  create tab instances
    #
    #  argument
    #    panel : panel instance to greate tabs
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def create_tabs(self, panel):
        grid_master = panel.get_grid_master()
        self.create_tab_master(grid_master)

    # -------------------------------------------------------------------------
    #  create_tab_master
    #  creating 'Master' tab
    #
    #  argument
    #    grid : grid container where creating table
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def create_tab_master(self, grid):
        # get 'Master' datafrane
        df = self.get_master()
        n_rows = len(df)
        x = 0; # column
        y = 0; # row

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        #  table header

        # first column
        lab = Gtk.Label(name='LabelHead', label='#')
        lab.set_hexpand(True)
        lab.set_alignment(xalign=0.5, yalign=0.5)
        grid.attach(lab, x, y, 1, 1)
        x += 1

        # rest of columns
        for item in df.columns.values:
            lab = Gtk.Label(name='LabelHead', label=item)
            lab.set_hexpand(True)
            lab.set_alignment(xalign=0.5, yalign=0.5)
            grid.attach(lab, x, y, 1, 1)
            x += 1

        y += 1

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        #  table contents
        for row in df.itertuples(name=None):
            x = 0
            for item in list(row):
                if (type(item) is float) or (type(item) is int):
                    # the first column '#' starts from 0,
                    # change to start from 1
                    if x == 0:
                        item += 1

                    # right align on the widget
                    xpos = 1.0
                    if math.isnan(item):
                        item = ''
                else:
                    # left align on the widget
                    xpos = 0.0

                item = str(item)

                lab = Gtk.Label(name='Label', label=item)
                lab.set_hexpand(True)
                lab.set_alignment(xalign=xpos, yalign=0.5)
                grid.attach(lab, x, y, 1, 1)
                x += 1

            y += 1

# ---
# PROGRAM END