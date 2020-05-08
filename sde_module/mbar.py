# -----------------------------------------------------------------------------
#  mbar.py --- widget class for SDE Tool
# -----------------------------------------------------------------------------
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from . import rc


# =============================================================================
#  MenuBar --- menubar class (template)
# =============================================================================
class MenuBar(Gtk.Frame):
    def __init__(self):
        Gtk.Frame.__init__(self)
        self.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.box = Gtk.Box()
        self.add(self.box)

    # -------------------------------------------------------------------------
    #  get_box
    #  get container instance for layouting widgets on it
    #
    #  argument:
    #    (none)
    #
    #  return
    #    Gtk.Box() layout instance
    # -------------------------------------------------------------------------
    def get_box(self):
        return self.box

# -----------------------------------------------------------------------------
#  menubar_button --- button class for menubar class
# -----------------------------------------------------------------------------
class menubar_button(Gtk.Button):
    def __init__(self, name, image, tooltip):
        Gtk.Button.__init__(self, name=name)
        self.add(rc.img().get_image(image))
        self.set_tooltip_text(tooltip)


# =============================================================================
#  implementation
# =============================================================================

# -----------------------------------------------------------------------------
#  menubar_main --- menubar class for main panel of SDE Tool
# -----------------------------------------------------------------------------
class main(MenuBar):
    def __init__(self):
        MenuBar.__init__(self)
        box = self.get_box()

        # config button
        self.but_config = menubar_button(name='Button', image='config', tooltip='App Config')
        box.pack_start(self.but_config, expand=False, fill=True, padding=0)

        # add supplier button
        self.but_supplier = menubar_button(name='Button', image='add', tooltip='Add Supplier')
        box.pack_start(self.but_supplier, expand=False, fill=True, padding=0)

        # exit button
        self.but_exit = menubar_button(name='Button', image='exit', tooltip='Exit this app')
        box.pack_end(self.but_exit, expand=False, fill=True, padding=0)

        # info button
        self.but_info = menubar_button(name='Button', image='info', tooltip='About this app')
        box.pack_end(self.but_info, expand=False, fill=True, padding=0)

    # -------------------------------------------------------------------------
    #  get_obj - get object instance of button
    #
    #  argument:
    #    image : image name of button
    # -------------------------------------------------------------------------
    def get_obj(self, name_image):
        if name_image == 'config':
            return self.but_config
        if name_image == 'add':
            return self.but_supplier
        if name_image == 'exit':
            return self.but_exit
        if name_image == 'info':
            return self.but_info

