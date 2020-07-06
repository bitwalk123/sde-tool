import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pandas as pd

# SDE Tool Classes
from sde_module import excel, mbar, utils


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SPC (Test Program)")
        self.set_icon_from_file(utils.img().get_file("logo"))
        self.set_default_size(600, 0)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        ### menubar
        menubar = mbar.spc()
        box.pack_start(menubar, expand=False, fill=True, padding=0)

        # folder button clicked event
        (menubar.get_obj('folder')).connect(
            'clicked',
            self.on_file_clicked
        )
        # exit button clicked event
        (menubar.get_obj('exit')).connect(
            'clicked',
            self.on_click_app_exit
        )

    # -------------------------------------------------------------------------
    #  File Open Filter
    # -------------------------------------------------------------------------
    def add_filters(self, dialog):
        filter_xls = Gtk.FileFilter()
        filter_xls.set_name('Excel')
        filter_xls.add_pattern('*.xls')
        filter_xls.add_pattern('*.xlsx')
        filter_xls.add_pattern('*.xlsm')
        dialog.add_filter(filter_xls)

        filter_any = Gtk.FileFilter()
        filter_any.set_name('All types')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)

    # -------------------------------------------------------------------------
    #  Aggregation from Excel for SPC
    # -------------------------------------------------------------------------
    def calc(self, filename):
        sheets = excel.SPC(filename)
        # check if read format is appropriate ot not
        if sheets.valid is not True:
            title = 'Error'
            text = 'Not appropriate format!'
            utils.show_ok_dialog(self, title, text, 'error')
            del sheets
            return


    # -------------------------------------------------------------------------
    #  Exit Application
    # -------------------------------------------------------------------------
    def on_click_app_exit(self, widget):
        self.emit('destroy')

    # -------------------------------------------------------------------------
    #  Open Folder
    # -------------------------------------------------------------------------
    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title="Select Excel file",
                                       parent=self,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL,
                           Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN,
                           Gtk.ResponseType.OK)
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.calc(dialog.get_filename())

        dialog.destroy()


# -----------------------------------------------------------------------------
#  Application Exit
# -----------------------------------------------------------------------------
def app_exit(obj):
    Gtk.main_quit()


# -----------------------------------------------------------------------------
#  MAIN
# -----------------------------------------------------------------------------
win = MyWindow()
win.connect("destroy", app_exit)
win.show_all()
Gtk.main()
