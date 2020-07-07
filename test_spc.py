import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# module classes of SDE Tool
from sde_module import panel


class TestSPC(panel.SPC):
    # CONSTRUCTOR
    def __init__(self):
        panel.SPC.__init__(self, title="SPC (Test Program)")


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
