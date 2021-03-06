import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# module classes of SDE Tool
from sde_module import pcs


class TestSPC(pcs.SPC):
    # CONSTRUCTOR
    def __init__(self):
        pcs.SPC.__init__(self, title="SPC (Test Program)")
        self.set_default_size(600, 400)

        # exit button clicked event
        (self.menubar.get_obj('exit')).connect(
            'clicked',
            self.on_click_app_exit
        )

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
