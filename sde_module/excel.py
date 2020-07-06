import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import pandas as pd
import math


class SPC():
    filename = None
    sheets = None
    valid = False

    def __init__(self, filename):
        self.filename = filename
        self.sheets = self.read(filename)
        self.valid = self.check_valid_sheet(self.sheets)

    def check_valid_sheet(self, sheets):
        # check if 'Master' tab exists
        if 'Master' in sheets.keys():
            return True
        else:
            return False

    def get_master(self):
        df_master = self.sheets['Master']
        # drop row if column 'Part Number' is NaN
        df_master = df_master.dropna(subset=['Part Number'])
        # fill ather NaN to 0
        #df_master = df_master.fillna(0)
        return df_master

    def get_sheets(self):
        return self.sheets

    def read(self, filename):
        # read specified filename as Excel file including all tabs
        return pd.read_excel(filename, sheet_name=None)

    def create_table_master(self, grid):
        df = self.get_master()
        n_rows = len(df)
        x = 0
        y = 0

        # table header
        lab = Gtk.Label(name='LabelHead', label='#')
        lab.set_hexpand(True)
        lab.set_alignment(xalign=0.5, yalign=0.5)
        grid.attach(lab, x, y, 1, 1)
        x += 1

        for item in df.columns.values:
            lab = Gtk.Label(name='LabelHead', label=item)
            lab.set_hexpand(True)
            lab.set_alignment(xalign=0.5, yalign=0.5)
            grid.attach(lab, x, y, 1, 1)
            x += 1
        y += 1

        for row in df.itertuples(name=None):
            x = 0
            for item in list(row):
                if (type(item) is float) or (type(item) is int):
                    xpos = 1.0
                    if math.isnan(item):
                        #print(item, type(item))
                        item = ''
                else:
                    xpos = 0.0

                item = str(item)

                lab = Gtk.Label(name='Label', label=item)
                lab.set_hexpand(True)
                lab.set_alignment(xalign=xpos, yalign=0.5)
                grid.attach(lab, x, y, 1, 1)
                x += 1

            y += 1
