import configparser
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import os.path
from sde_module import dlg, db, mbar, panel, rc


# -----------------------------------------------------------------------------
#  SDETool
#  Supplier Development Engineering Tool to organize supplier information
#
#  COPYRIGHT 2020 Keiichi Takahashi
# -----------------------------------------------------------------------------
class SDETool(Gtk.Window):
    # Application Version
    app_version = "0.2"

    # configuraion file
    confFile = 'sde.conf'

    # CSS
    provider = Gtk.CssProvider()
    provider.load_from_data((rc.SDETOOL_CSS).encode('utf-8'))

    def __init__(self):
        Gtk.Window.__init__(self, title="SDE Tool")

        # ---------------------------------------------------------------------
        #  CONFIGURATION FILE READ
        # ---------------------------------------------------------------------
        self.config = configparser.ConfigParser()
        self.config.read(self.confFile, 'UTF-8')

        # ---------------------------------------------------------------------
        #  DATABASE
        # ---------------------------------------------------------------------
        # Config for Database
        config_db = self.config['Database']
        self.dbname = config_db['DBNAME']
        # get database instance
        self.obj = db.HandleDB(self)
        if not os.path.exists(self.dbname):
            self.obj.init()

        # ---------------------------------------------------------------------
        #  GUI
        # ---------------------------------------------------------------------
        # CSS
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                                 self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        # decoration for top level window
        self.set_icon_from_file(rc.Img().get_file("logo"))
        self.set_margin_start(1)
        self.set_margin_end(1)
        self.set_default_size(800, 600)

        # top level widget layout management
        box = Gtk.Box(name='Base', orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        ### menubar
        menubar = mbar.menuBar_main()
        box.pack_start(menubar, expand=False, fill=True, padding=0)

        # add button clicked event
        (menubar.get_obj('add')).connect('clicked', self.on_click_add_new_supplier)
        # info button clicked event
        (menubar.get_obj('info')).connect('clicked', self.on_click_app_info)
        # exit button clicked event
        (menubar.get_obj('exit')).connect('clicked', self.on_click_app_exit)

        ### main pabel
        mainpanel = panel.PanelMain(self, self.obj)
        box.pack_start(mainpanel, expand=True, fill=True, padding=0)

        ### status bar
        self.statusbar = Gtk.Statusbar(name='Status')
        self.context_id = self.statusbar.get_context_id('sde')
        box.pack_start(self.statusbar, expand=False, fill=True, padding=0)
        mainpanel.set_statusbar_info(self.statusbar, self.context_id)

    # -------------------------------------------------------------------------
    #  show OKDialog
    # -------------------------------------------------------------------------
    def showOKDialog(self, title, text):
        dialog = dlg.ok(self, title, text)
        dialog.run()
        dialog.destroy()

    # =========================================================================
    #  EVENT HANDLING
    # =========================================================================

    # -------------------------------------------------------------------------
    #  on_click_add_new_supplier
    #
    #  Add Supplier
    # -------------------------------------------------------------------------
    def on_click_add_new_supplier(self, widget):
        # Dialog for adding new supplier
        dialog = dlg.DlgAddNewSupplier(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            new_supplier = dialog.get_supplier_name()
            dialog.destroy()

            if new_supplier is not None:
                response = self.obj.add_supplier(new_supplier)
                if response == 0:
                    self.add_new_supplier(new_supplier)
                elif response == 1:
                    title = "Duplication"
                    text = "'" + new_supplier + "' already exists in the database."
                    self.showOKDialog(title, text)
                else:
                    title = "Error"
                    text = "Unknown error occured"
                    self.showOKDialog(title, text)
        else:
            dialog.destroy()

    # -------------------------------------------------------------------------
    #  Exit Application
    # -------------------------------------------------------------------------
    def on_click_app_exit(self, widget):
        self.emit('destroy')

    # -------------------------------------------------------------------------
    #  Application Information
    # -------------------------------------------------------------------------
    def on_click_app_info(self, widget):
        dialog = dlg.app_about(self)
        dialog.run()
        dialog.destroy()


# -----------------------------------------------------------------------------
#  Application Exit
# -----------------------------------------------------------------------------
def app_exit(obj):
    Gtk.main_quit()


# -----------------------------------------------------------------------------
#  MAIN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    win = SDETool()
    win.connect('destroy', app_exit)
    win.show_all()
    Gtk.main()
