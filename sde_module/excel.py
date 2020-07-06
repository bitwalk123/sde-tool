import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import pandas as pd


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
        return df_master

    def get_model_master(self):
        store = Gtk.TreeStore(
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
        )
        return store

    def get_sheets(self):
        return self.sheets

    def read(self, filename):
        # read specified filename as Excel file including all tabs
        return pd.read_excel(filename, sheet_name=None)

    def set_colhead_master(self, tree):
        df_master = self.get_master()
        for colname in df_master.columns.values:
            column = Gtk.TreeViewColumn(title=colname)
            tree.append_column(column)

