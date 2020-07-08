import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import pandas as pd
import numpy as np
import math
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas
)
from matplotlib.figure import Figure


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
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        #  'Master' tab

        # get 'Master' grid container
        grid_master = panel.get_grid_master()

        # get 'Master' datafrane
        df_master = self.get_master()

        # create 'Master' tab
        self.create_tab_master(grid_master, df_master)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        #  PART tab

        # obtain unique part list
        list_part = self.get_unique_part_list()

        # create tab for etch part
        for name_part in list_part:
            # create initial tab for part
            grid_part_data, container_plot = panel.create_page_part(name_part)

            # get dataframe of part data
            df_part = self.get_part(name_part)

            # create tab to show part data
            self.create_tab_part_data(grid_part_data, df_part)

            # get parameter list
            list_param = self.get_param_list(name_part)

            self.create_tab_part_plot(container_plot, df_part, list_param)

    # -------------------------------------------------------------------------
    #  create_tab_master
    #  creating 'Master' tab
    #
    #  argument
    #    grid : grid container where creating table
    #    df   : dataframe for 'Master'
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def create_tab_master(self, grid, df):
        x = 0;  # column
        y = 0;  # row

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

    # -------------------------------------------------------------------------
    #  create_tab_part_data
    #  creating DATA tab in (Part Number) tab
    #
    #  argument
    #    grid : grid container where creating table
    #    df   : dataframe for specified (Part Number)
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def create_tab_part_data(self, grid, df):
        x = 0;  # column
        y = 0;  # row

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

    # -------------------------------------------------------------------------
    #  create_tab_part_plot
    #  creating PLOT tab in (Part Number) tab
    #
    #  argument
    #    container  : container where creating plot
    #    df         : dataframe for specified (Part Number)
    #    list_param : parameter list to plot
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def create_tab_part_plot(self, container, df, list_param):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.add(box)

        param = list_param[3]
        x = df['Sample']
        y = df[param]

        # f = Figure(figsize=(5, 4), dpi=100)
        f = Figure(dpi=100)
        a = f.add_subplot(111, title=param, ylabel='Value')
        a.grid(True)
        a.axhline(y=757.43, linewidth=1, color='blue', label='LSL')
        a.axhline(y=759.97, linewidth=1, color='blue', label='USL')
        a.axhline(y=758.7, linewidth=1, color='purple', label='Target')
        a.plot(x, y, linewidth=1, color="gray")
        a.scatter(x, y, s=20, c='black', marker='o', label="Recent")
        canvas = FigureCanvas(f)
        # container.add(canvas)
        box.pack_start(canvas, True, True, 0)

    # -------------------------------------------------------------------------
    #  get_master
    #  get dataframe of 'Master' tab
    #
    #  argument
    #    (none)
    #
    #  return
    #    pandas dataframe of 'Master' tab
    # -------------------------------------------------------------------------
    def get_master(self):
        df = self.sheets['Master']
        # drop row if column 'Part Number' is NaN
        df = df.dropna(subset=['Part Number'])

        return df

    # -------------------------------------------------------------------------
    #  get_param_list
    #  get list of 'Parameter Name' of specified 'Part Number'
    #
    #  argument
    #    name_part : part name
    #
    #  return
    #    list of 'Parameter Name' of specified 'Part Number'
    # -------------------------------------------------------------------------
    def get_param_list(self, name_part):
        df = self.get_master()
        return list(df[df['Part Number'] == name_part]['Parameter Name'])

    # -------------------------------------------------------------------------
    #  get_part
    #  get dataframe of specified name_part tab
    #
    #  argument
    #    (none)
    #
    #  return
    #    pandas dataframe of specified name_part tab
    # -------------------------------------------------------------------------
    def get_part(self, name_part):
        # dataframe of specified name_part tab
        df = self.sheets[name_part]

        # delete row including NaN
        df = df.dropna(how='all')

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        #  the first row od data sheet is used for 'Create Charts' button for
        #  the Excel macro
        #
        #  So, new dataframe is created for this application
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

        # obtain number of rows on this dataframe
        row_size = len(df)

        # extract data rows
        df1 = df[1:row_size]

        # extract column name used for this dataframe
        list_colname = list(df.loc[0])
        df1.columns = list_colname

        return df1

    # -------------------------------------------------------------------------
    #  get_sheets
    #  get dataframe containing Excel contents
    #
    #  argument
    #    (none)
    #
    #  return
    #    array of pandas dataframe containing Excel tab/data
    # -------------------------------------------------------------------------
    def get_sheets(self):
        return self.sheets

    # -------------------------------------------------------------------------
    #  get_unique_part_list
    #  get unique part list found in 'Part Number' column in 'Master' tab
    #
    #  argument
    #    (none)
    #
    #  return
    #    list of unique 'Part Number'
    # -------------------------------------------------------------------------
    def get_unique_part_list(self):
        df = self.get_master()
        list_part = list(np.unique(df['Part Number']))
        return list_part

    # -------------------------------------------------------------------------
    #  read
    #  read specified Excel file
    #
    #  argument
    #    filename : Excel file
    #
    #  return
    #    array of pandas dataframe including all Excel sheets
    # -------------------------------------------------------------------------
    def read(self, filename):
        # read specified filename as Excel file including all tabs
        return pd.read_excel(filename, sheet_name=None)

# ---
# PROGRAM END
