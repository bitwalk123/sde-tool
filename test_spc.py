import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# SDE Tool Classes
from sde_module import dlg, excel, mbar, panel, utils


class MyWindow(Gtk.Window):
    mainpanel = None

    # CSS
    provider = Gtk.CssProvider()
    provider.load_from_data((utils.SDETOOL_CSS).encode('utf-8'))

    def __init__(self):
        Gtk.Window.__init__(self, title="SPC (Test Program)")
        self.set_icon_from_file(utils.img().get_file("logo"))
        self.set_margin_start(1)
        self.set_margin_end(1)
        self.set_default_size(800, 600)


        # CSS
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

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

        ### main pabel
        self.mainpanel = panel.spc(self)
        box.pack_start(self.mainpanel, expand=True, fill=True, padding=0)

    # -------------------------------------------------------------------------
    #  Aggregation from Excel for SPC
    # -------------------------------------------------------------------------
    def calc(self, filename):
        sheets = excel.SPC(filename)
        # check if read format is appropriate ot not
        if sheets.valid is not True:
            title = 'Error'
            text = 'Not appropriate format!'
            # OK dialog
            utils.show_ok_dialog(self, title, text, 'error')
            # delete instance
            del sheets
            return

        # ---------------------------------------------------------------------
        # 'Master' tab of the sheets
        sheets.create_table_master(self.mainpanel.get_grid_master())
        self.show_all()

    # -------------------------------------------------------------------------
    #  Exit Application
    # -------------------------------------------------------------------------
    def on_click_app_exit(self, widget):
        self.emit('destroy')

    # -------------------------------------------------------------------------
    #  Open Folder
    # -------------------------------------------------------------------------
    def on_file_clicked(self, widget):
        filename = dlg.file_chooser.get(parent=self, flag='excel')
        if filename is not None:
            self.calc(filename)


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
