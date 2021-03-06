import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import numpy as np
import math
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas
)
from matplotlib.figure import Figure

# module classes of SDE Tool
from sde_module import excel, dlg, mbar, utils


# =============================================================================
#  SPC class
#  spc GUI of SDE Tool
# =============================================================================
class SPC(Gtk.Window):
    mainpanel = None
    grid_master = None

    # CSS
    provider = Gtk.CssProvider()
    provider.load_from_data((utils.SDETOOL_CSS).encode('utf-8'))

    # CONSTRUCTOR
    def __init__(self, title='SPC'):
        Gtk.Window.__init__(self, title=title)
        self.set_icon_from_file(utils.img().get_file("logo"))
        self.set_margin_start(1)
        self.set_margin_end(1)

        # CSS
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        ### menubar
        self.menubar = mbar.spc()
        box.pack_start(self.menubar, expand=False, fill=True, padding=0)

        # folder button clicked event
        (self.menubar.get_obj('folder')).connect(
            'clicked',
            self.on_file_clicked
        )

        # main pabel
        # self.mainpanel = SPCMain(self)
        mainpanel = Gtk.Notebook()
        mainpanel.set_tab_pos(Gtk.PositionType.BOTTOM)
        page_master = self.create_page_master()
        mainpanel.append_page(page_master, Gtk.Label(label="Master"))
        box.pack_start(mainpanel, expand=True, fill=True, padding=0)

        self.mainpanel = mainpanel

    # -------------------------------------------------------------------------
    #  calc
    #  Aggregation from Excel for SPC
    #
    #  argument
    #    filename : Excel file to read
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def calc(self, filename):
        sheets = excel.ExcelSPC(filename)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # check if read format is appropriate ot not
        if sheets.valid is not True:
            title = 'Error'
            text = 'Not appropriate format!'
            # OK dialog
            utils.show_ok_dialog(self, title, text, 'error')
            # delete instance
            del sheets
            return

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # create tabs for tables & charts
        # sheets.create_tabs(self.mainpanel)
        self.create_tabs(sheets)

        # update GUI
        self.show_all()

    # -------------------------------------------------------------------------
    #  create_panel_master
    #  creating 'Master' page
    #
    #  argument
    #    (none)
    #
    #  return
    #    instance of container
    # -------------------------------------------------------------------------
    def create_page_master(self):
        grid = Gtk.Grid()

        # scrollbar window
        scrwin = Gtk.ScrolledWindow()
        scrwin.add(grid)
        scrwin.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC
        )
        self.grid_master = grid

        return scrwin

    # -------------------------------------------------------------------------
    #  create_panel_part
    #  creating 'Master' page
    #
    #  argument
    #    (none)
    #
    #  return
    #    instance of container
    # -------------------------------------------------------------------------
    def create_page_part(self, tabname):
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        self.mainpanel.append_page(notebook, Gtk.Label(label=tabname))

        # DATA tab
        grid_data = Gtk.Grid()
        scrwin_data = Gtk.ScrolledWindow()
        scrwin_data.add(grid_data)
        scrwin_data.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC
        )
        notebook.append_page(scrwin_data, Gtk.Label(label='DATA'))

        # PLOT tab (tentative)
        box_plot = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_plot.set_homogeneous(True)
        scrwin_plot = Gtk.ScrolledWindow()
        scrwin_plot.add(box_plot)
        scrwin_plot.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC
        )
        notebook.append_page(scrwin_plot, Gtk.Label(label='PLOT'))

        return grid_data, box_plot

    # -------------------------------------------------------------------------
    #  create_tabs
    #  create tab instances
    #
    #  argument
    #    sheet :
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def create_tabs(self, sheet):
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        #  'Master' tab

        # get 'Master' grid container
        grid_master = self.get_grid_master()

        # get 'Master' datafrane
        df_master = sheet.get_master()

        # create 'Master' tab
        self.create_tab_master(grid_master, df_master)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        #  PART tab

        # obtain unique part list
        list_part = sheet.get_unique_part_list()

        # create tab for etch part
        for name_part in list_part:
            # create initial tab for part
            grid_part_data, box_part_plot = self.create_page_part(name_part)

            # get dataframe of part data
            df_part = sheet.get_part(name_part)

            # create tab to show part data
            self.create_tab_part_data(grid_part_data, df_part)

            # get parameter list
            list_param = sheet.get_param_list(name_part)

            self.create_tab_part_plot(box_part_plot, df_part, name_part, list_param, sheet)

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
    #    sheet      : instance of Excel sheet
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def create_tab_part_plot(self, box, df, name_part, list_param, sheet):
        for param in list_param:
            # print(param)
            metrics = sheet.get_metrics(name_part, param)
            # print(metrics.items())

            x = df['Sample']
            y = df[param]

            fig = Figure(dpi=100)
            splot = fig.add_subplot(111, title=param, ylabel='Value')
            splot.grid(True)

            if metrics['Spec Type'] == 'Two-Sided':
                if not np.isnan(metrics['USL']):
                    splot.axhline(y=metrics['USL'], linewidth=1, color='blue', label='USL')
                if not np.isnan(metrics['UCL']):
                    splot.axhline(y=metrics['UCL'], linewidth=1, color='red', label='UCL')
                if not np.isnan(metrics['Target']):
                    splot.axhline(y=metrics['Target'], linewidth=1, color='purple', label='Target')
                if not np.isnan(metrics['LCL']):
                    splot.axhline(y=metrics['LCL'], linewidth=1, color='red', label='LCL')
                if not np.isnan(metrics['LSL']):
                    splot.axhline(y=metrics['LSL'], linewidth=1, color='blue', label='LSL')
            elif metrics['Spec Type'] == 'One-Sided':
                if not np.isnan(metrics['USL']):
                    splot.axhline(y=metrics['USL'], linewidth=1, color='blue', label='USL')
                if not np.isnan(metrics['UCL']):
                    splot.axhline(y=metrics['UCL'], linewidth=1, color='red', label='UCL')
            # Avg
            splot.axhline(y=metrics['Avg'], linewidth=1, color='green', label='Avg')

            # Line
            splot.plot(x, y, linewidth=1, color="gray")

            size_oos = 60
            size_ooc = 100
            if metrics['Spec Type'] == 'Two-Sided':
                # OOC check
                x_ooc = x[(df[param] < metrics['LCL']) | (df[param] > metrics['UCL'])]
                y_ooc = y[(df[param] < metrics['LCL']) | (df[param] > metrics['UCL'])]
                splot.scatter(x_ooc, y_ooc, s=size_ooc, c='orange', marker='o', label="Recent")
                # OOS check
                x_oos = x[(df[param] < metrics['LSL']) | (df[param] > metrics['USL'])]
                y_oos = y[(df[param] < metrics['LSL']) | (df[param] > metrics['USL'])]
                splot.scatter(x_oos, y_oos, s=size_oos, c='red', marker='o', label="Recent")
            elif metrics['Spec Type'] == 'One-Sided':
                # OOC check
                x_ooc = x[(df[param] > metrics['UCL'])]
                y_ooc = y[(df[param] > metrics['UCL'])]
                splot.scatter(x_ooc, y_ooc, s=size_ooc, c='orange', marker='o', label="Recent")
                # OOS check
                x_oos = x[(df[param] > metrics['USL'])]
                y_oos = y[(df[param] > metrics['USL'])]
                splot.scatter(x_oos, y_oos, s=size_oos, c='red', marker='o', label="Recent")

            splot.scatter(x, y, s=20, c='black', marker='o', label="Recent")

            x_label = splot.get_xlim()[1]

            if metrics['Spec Type'] == 'Two-Sided':
                if not np.isnan(metrics['USL']):
                    splot.text(x_label, y=metrics['USL'], s=' USL', color='blue')
                if not np.isnan(metrics['UCL']):
                    splot.text(x_label, y=metrics['UCL'], s=' UCL', color='red')
                if not np.isnan(metrics['Target']):
                    splot.text(x_label, y=metrics['Target'], s=' Target', color='purple')
                if not np.isnan(metrics['LCL']):
                    splot.text(x_label, y=metrics['LCL'], s=' LCL', color='red')
                if not np.isnan(metrics['LSL']):
                    splot.text(x_label, y=metrics['LSL'], s=' LSL', color='blue')
            elif metrics['Spec Type'] == 'One-Sided':
                if not np.isnan(metrics['USL']):
                    splot.text(x_label, y=metrics['USL'], s=' USL', color='blue')
                if not np.isnan(metrics['UCL']):
                    splot.text(x_label, y=metrics['UCL'], s=' UCL', color='red')
            # Avg
            splot.text(x_label, y=metrics['Avg'], s=' Avg', color='green')

            canvas = FigureCanvas(fig)
            canvas.set_size_request(800, 600)
            box.pack_start(canvas, expand=False, fill=True, padding=0)

    # -------------------------------------------------------------------------
    #  get_grid_master
    #  get grid instance for 'Master' page
    #
    #  argument
    #    (none)
    #
    #  return
    #    instance of grid for 'Master' page
    # -------------------------------------------------------------------------
    def get_grid_master(self):
        return self.grid_master

    # -------------------------------------------------------------------------
    #  on_file_clicked
    #  Open Folder
    #
    #  argument
    #    widget : clicked widget, automatically added from caller
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def on_file_clicked(self, widget):
        filename = dlg.file_chooser.get(parent=self, flag='excel')
        if filename is not None:
            self.calc(filename)

# ---
# PROGRAM END
