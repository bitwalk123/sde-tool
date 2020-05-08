# -----------------------------------------------------------------------------
#  dlg.py --- dialog class for SDE Tool
# -----------------------------------------------------------------------------
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf

import pathlib
import platform

from . import rc


# =============================================================================
#  NBDialog --- dialog with notebook class (template)
# =============================================================================
class NBDialog(Gtk.Dialog):
    def __init__(self, parent, title):
        Gtk.Dialog.__init__(self, parent=parent, title=title)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(rc.Img().get_file('config'))
        self.set_default_size(600, 0)
        self.set_resizable(True)

        container = self.get_content_area()
        self.notebook = Gtk.Notebook()
        container.add(self.notebook)

    # -------------------------------------------------------------------------
    #  get_notebook
    #  get container instance for layouting widgets on it
    #
    #  argument:
    #    (none)
    #
    #  return
    #    Gtk.Notebook() layout instance
    # -------------------------------------------------------------------------
    def get_notebook(self):
        return self.notebook


# =============================================================================
#  GridPane --- dialog pane with grid layout (template)
# =============================================================================
class GridPane(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent

    # -------------------------------------------------------------------------
    def get_filename(self):
        dialog = Gtk.FileChooserDialog(title='select file', parent=self.parent, action=Gtk.FileChooserAction.OPEN)
        dialog.set_icon_from_file(rc.Img().get_file('file'))
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        self.addFileFiltersALL(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            p = pathlib.Path(dialog.get_filename())
            dialog.destroy()
            # change path separator '\' to '/' to avoid unexpected errors
            name_file = str(p.as_posix())
            return name_file
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return None

    # -------------------------------------------------------------------------
    # addFileFiltersALL - filter for ALL
    # -------------------------------------------------------------------------
    def addFileFiltersALL(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)


# -----------------------------------------------------------------------------
#  app_about
# -----------------------------------------------------------------------------
class app_about(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, title='About This App')
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(rc.Img().get_file('info'))
        self.set_default_size(400, 0)
        self.set_resizable(False)

        lab1 = Gtk.Label(label='SDE Tool', name='Title')
        lab2 = Gtk.Label(label='version ' + parent.app_version, name='Version')
        lab3 = Gtk.Label(label='© 2020 Keiichi Takahashi', name='Author')
        lab4 = Gtk.Label(label='running on python ' + platform.python_version(), name='PyVer')

        msg = Gtk.TextBuffer()
        text = "This SDE Tool is a support application for Supplier Development Engineering to organize supplier information."
        msg.set_text(text)
        desc = Gtk.TextView(name='Desc')
        desc.set_buffer(msg)
        desc.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)
        desc.set_editable(False)
        desc.set_can_focus(False)
        desc.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))

        box = self.get_content_area()
        box.pack_start(lab1, expand=False, fill=False, padding=0)
        box.pack_start(lab2, expand=False, fill=False, padding=0)
        box.pack_start(lab3, expand=False, fill=False, padding=0)
        box.pack_start(lab4, expand=False, fill=False, padding=0)
        box.pack_start(desc, expand=False, fill=False, padding=0)

        self.show_all()

    def create_app_logo(self):
        liststore = Gtk.ListStore(Pixbuf)
        pixbuf = rc.Img().get_pixbuf('logo')
        liststore.append([pixbuf])
        app_logo = Gtk.IconView()
        app_logo.set_model(liststore)
        app_logo.set_pixbuf_column(0)
        app_logo.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))
        return app_logo


# -----------------------------------------------------------------------------
#  ok dialog
# -----------------------------------------------------------------------------
class ok(Gtk.Dialog):

    def __init__(self, parent, title, text):
        Gtk.Dialog.__init__(self, title)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(rc.Img().get_file('info'))
        self.set_default_size(200, 0)
        self.set_resizable(False)

        msg = Gtk.TextBuffer()
        msg.set_text(text)
        tview = Gtk.TextView()
        tview.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)
        tview.set_buffer(msg)
        tview.set_editable(False)
        tview.set_can_focus(False)
        tview.set_top_margin(10)
        tview.set_bottom_margin(10)
        tview.set_left_margin(10)
        tview.set_right_margin(10)
        tview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))

        content = self.get_content_area()
        content.add(tview)

        self.show_all()


# -----------------------------------------------------------------------------
#  setting_supplier
# -----------------------------------------------------------------------------
class setting_supplier(NBDialog):

    def __init__(self, parent):
        NBDialog.__init__(self, parent=parent, title='Supplier Setting')
        notebook = self.get_notebook()

        # New Project
        self.pane_new_proj = setting_supplier_new_proj(parent)
        notebook.append_page(self.pane_new_proj, Gtk.Label(label="Add New Project"))

        self.show_all()

    # -------------------------------------------------------------------------
    def get_name_owner(self):
        return self.pane_new_proj.name_owner.get_text()

    # -------------------------------------------------------------------------
    def get_num_part(self):
        return self.pane_new_proj.num_part.get_text()

    # -------------------------------------------------------------------------
    def get_description(self):
        return self.pane_new_proj.description.get_text()

    # -------------------------------------------------------------------------
    def get_product(self):
        return self.pane_new_proj.product.get_text()

    # -------------------------------------------------------------------------
    def get_file(self):
        return self.pane_new_proj.file.get_text()


# -----------------------------------------------------------------------------
#  setting_supplier_new_proj
# -----------------------------------------------------------------------------
class setting_supplier_new_proj(GridPane):
    def __init__(self, parent):
        GridPane.__init__(self, parent=parent)

        # ---------------------------------------------------------------------
        # Label for Project Owner
        lab_name_owner = Gtk.Label(label='Project Owner', name="Label")
        lab_name_owner.set_hexpand(False)
        lab_name_owner.set_halign(Gtk.Align.END)
        # Entry for Project Owner
        self.name_owner = Gtk.Entry()
        self.name_owner.set_hexpand(True)
        # ---------------------------------------------------------------------
        # Label for PART No.
        lab_num_part = Gtk.Label(label='PART No.', name="Label")
        lab_num_part.set_hexpand(False)
        lab_num_part.set_halign(Gtk.Align.END)
        # Entry for PART No.
        self.num_part = Gtk.Entry()
        self.num_part.set_hexpand(True)
        # ---------------------------------------------------------------------
        # Label for Description
        lab_description = Gtk.Label(label='Description', name="Label")
        lab_description.set_hexpand(False)
        lab_description.set_halign(Gtk.Align.END)
        # Entry for Description
        self.description = Gtk.Entry()
        self.description.set_hexpand(True)
        # ---------------------------------------------------------------------
        # Label for File
        lab_file = Gtk.Label(label='File', name="Label")
        lab_file.set_hexpand(False)
        lab_file.set_halign(Gtk.Align.END)
        # Entry for File
        self.file = Gtk.Entry()
        self.file.set_hexpand(True)
        # ---------------------------------------------------------------------
        # Label for Product
        lab_product = Gtk.Label(label='Product', name="Label")
        lab_product.set_hexpand(False)
        lab_product.set_halign(Gtk.Align.END)
        # Entry for Product
        self.product = Gtk.Entry()
        self.product.set_hexpand(True)
        # Button for File
        but_file = Gtk.Button()
        but_file.add(rc.Img().get_image('folder', 16))
        but_file.connect('clicked', self.on_click_choose_file)
        but_file.set_hexpand(False)
        # ---------------------------------------------------------------------
        #  grid layout
        self.attach(lab_name_owner, 0, 0, 1, 1)
        self.attach(self.name_owner, 1, 0, 2, 1)
        self.attach(lab_num_part, 0, 1, 1, 1)
        self.attach(self.num_part, 1, 1, 2, 1)
        self.attach(lab_description, 0, 2, 1, 1)
        self.attach(self.description, 1, 2, 2, 1)
        self.attach(lab_product, 0, 3, 1, 1)
        self.attach(self.product, 1, 3, 2, 1)
        self.attach(lab_file, 0, 4, 1, 1)
        self.attach(self.file, 1, 4, 1, 1)
        self.attach(but_file, 2, 4, 1, 1)

    # =========================================================================
    #  EVENT HANDLING
    # =========================================================================

    # -------------------------------------------------------------------------
    #  on_click_choose_file
    # -------------------------------------------------------------------------
    def on_click_choose_file(self, widget):
        filename = self.get_filename()
        if filename is not None:
            self.file.set_text(filename)
