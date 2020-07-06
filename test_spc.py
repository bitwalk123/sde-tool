import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# module classes of SDE Tool
from sde_module import dlg, excel, mbar, panel, utils


class TestSPC(Gtk.Window):
    mainpanel = None

    # CSS
    provider = Gtk.CssProvider()
    provider.load_from_data((utils.SDETOOL_CSS).encode('utf-8'))

    # CONSTRUCTOR
    def __init__(self):
        Gtk.Window.__init__(self, title="SPC (Test Program)")
        self.set_icon_from_file(utils.img().get_file("logo"))
        self.set_margin_start(1)
        self.set_margin_end(1)
        self.set_default_size(800, 400)

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

        # main pabel
        self.mainpanel = panel.spc(self)
        box.pack_start(self.mainpanel, expand=True, fill=True, padding=0)

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
        sheets = excel.SPC(filename)

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
        sheets.create_tabs(self.mainpanel)
        # update GUI
        self.show_all()

    # -------------------------------------------------------------------------
    #  on_click_app_exit
    #  Exit Application, emitting 'destroy' signal
    #
    #  argument
    #    widget : clicked widget, automatically added from caller
    #
    #  return
    #    (none)
    # -------------------------------------------------------------------------
    def on_click_app_exit(self, widget):
        self.emit('destroy')

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


# -----------------------------------------------------------------------------
#  app_exit
#  Application Exit, executing Gtk.main_quit()
#
#  argument
#    obj : object, automatically added from caller
#
#  return
#    (none)
# -----------------------------------------------------------------------------
def app_exit(obj):
    Gtk.main_quit()


# -----------------------------------------------------------------------------
#  MAIN
# -----------------------------------------------------------------------------
win = TestSPC()
win.connect("destroy", app_exit)
win.show_all()
Gtk.main()

# ---
# PROGRAM END
