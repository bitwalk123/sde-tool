# -----------------------------------------------------------------------------
#  dlg.py --- dialog class for SDE Tool
# -----------------------------------------------------------------------------
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf

import platform
from . import rc


# -----------------------------------------------------------------------------
#  dialog_app_about
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
#  dialog_ok
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
