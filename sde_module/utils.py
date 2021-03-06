# -----------------------------------------------------------------------------
#  utils.py --- resource class for SDE Tool
# -----------------------------------------------------------------------------
import gi
import pathlib
import re
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from . import dlg

# CSS for GUI
SDETOOL_CSS = '''
#About {
    background-color: white;
}
#Author {
    font-size: 10pt;
    font-family: sans-serif;
    margin-left: 10px;
    margin-right: 10px;
}
#Base {
    font-size: 10pt;
    font-family: sans-serif;
}
#Button {
    padding: 2px;
}
#Corp {
    font-size: 11pt;
    font-family: sans-serif;
    margin-right: 10px;
}
#Desc {
    font-size: 9pt;
    font-style: italic;
    font-family: serif;
    padding: 20px;
}
#Label {
    font-size: 10pt;
    padding-left: 5px;
    padding-right: 10px;
}
#LabelHead {
    font-size: 10pt;
    font-weight: bold;
    color: white;
    background-color: darkblue;
    padding-left: 5px;
    padding-right: 10px;
}
#PyVer {
    font-size: 10pt;
    font-style: italic;
    font-family: serif;
    margin-left: 10px;
    margin-right: 10px;
}
#Status {
    font-size: 9pt;
    font-family: sans-serif;
    background-color: #ffe;
    color: #040;
}
#Title {
    font-size: 24pt;
    font-family: sans-serif;
    margin-top: 10px;
}
#Version {
    font-size: 10pt;
    font-style: italic;
    font-family: serif;
    margin-bottom: 5px;
}
'''


# -----------------------------------------------------------------------------
#  image
#  Image Facility
# -----------------------------------------------------------------------------
class image(Gtk.Image):
    def __init__(self, image, size=Gtk.IconSize.DND):
        Gtk.Image.__init__(self)
        icon_name = self.get_icon_name(image)
        self.set_from_icon_name(icon_name, size)

    def get_icon_name(self, image_name):
        if image_name == "add":
            return "list-add"
        elif image_name == "config":
            return "emblem-system"
        elif image_name == "exit":
            return "application-exit"
        elif image_name == "folder":
            return "folder"
        elif image_name == "info":
            return "dialog-information"

        return

# -----------------------------------------------------------------------------
#  img
#  Image Facility
# -----------------------------------------------------------------------------
class img(Gtk.Image):
    IMG_ADD = "img/add-128.png"
    IMG_CONFIG = "img/config-128.png"
    IMG_CROSS = "img/cross-128.png"
    IMG_DONE = "img/done-128.png"
    IMG_ERROR = "img/error-128.png"
    IMG_EXIT = "img/exit-128.png"
    IMG_FILE = "img/file-128.png"
    IMG_FOLDER = "img/folder-128.png"
    IMG_INFO = "img/info-128.png"
    IMG_LOGO = "img/logo-128.png"
    IMG_PDF = "img/pdf.png"
    IMG_QUEST = "img/question-128.png"
    IMG_WARNING = "img/warning-128.png"

    def __init__(self):
        Gtk.Image.__init__(self)

    def get_image(self, image_name, size=24):
        pixbuf = self.get_pixbuf(image_name, size)
        return Gtk.Image.new_from_pixbuf(pixbuf)

    def get_pixbuf(self, image_name, size=24):
        name_file = self.get_file(image_name)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(name_file)
        pixbuf = pixbuf.scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)
        return pixbuf

    def get_file(self, image_name):
        if image_name == "add":
            name_file = self.IMG_ADD
        elif image_name == "config":
            name_file = self.IMG_CONFIG
        elif image_name == "cross":
            name_file = self.IMG_CROSS
        elif image_name == "done":
            name_file = self.IMG_DONE
        elif image_name == "error":
            name_file = self.IMG_ERROR
        elif image_name == "exit":
            name_file = self.IMG_EXIT
        elif image_name == "file":
            name_file = self.IMG_FILE
        elif image_name == "folder":
            name_file = self.IMG_FOLDER
        elif image_name == "info":
            name_file = self.IMG_INFO
        elif image_name == "logo":
            name_file = self.IMG_LOGO
        elif image_name == "pdf":
            name_file = self.IMG_PDF
        elif image_name == "quest":
            name_file = self.IMG_QUEST
        elif image_name == "warning":
            name_file = self.IMG_WARNING
        return name_file


# =============================================================================
#  METHODS for GENERAL PURPOSE
# =============================================================================

# -----------------------------------------------------------------------------
#  concat
#  concatenate strings
#
#  argument
#    *args : variable number of string arguments to be concatenated
# -----------------------------------------------------------------------------
def concat(*args):
    result = ''
    for str in args:
        result = result + str

    return result


# -------------------------------------------------------------------------
#  get_id
#  get Id
#
#  arguments
#    source  : string
#    pattern : regular expression
# -------------------------------------------------------------------------
def get_id(source, pattern):
    p = re.compile(pattern)
    m = p.match(source)
    id = m.group(1)

    return int(id)


# -------------------------------------------------------------------------
#  get_id_with_model
#  get Id  with Model iter
#
#  arguments
#    iter
#    model
#    label
#    col
#
#  return
#    integer id
# -------------------------------------------------------------------------
def get_id_with_model(iter, model, label, col):
    id_string = model[iter][col]
    pattern = label + ' = (.+)'
    return get_id(id_string, pattern)


# -------------------------------------------------------------------------
#  open_file_with_app
#
#  argument
#    name_file :  file to open
# -------------------------------------------------------------------------
def open_file_with_app(name_file):
    link_file = pathlib.PurePath(name_file)
    # Explorer can cover all cases on Windows NT
    subprocess.Popen(['explorer', link_file])


# -------------------------------------------------------------------------
#  show_ok_dialog
#  show OK Dialog
#
#  arguments
#    parent : instance of top level window
#    title  : title of the dialog
#    text   : message string of the dialog
#    image  : icon image of dialog
# -------------------------------------------------------------------------
def show_ok_dialog(parent, title, text, image='info'):
    dialog = dlg.ok(parent, title, text, image)
    dialog.run()
    dialog.destroy()


# -------------------------------------------------------------------------
#  tree_node_expand
#
#  arguments
#    tree : instance of the tree widget
#    iter : the iteration (node) to expand
# -------------------------------------------------------------------------
def tree_node_expand(tree, iter):
    model = tree.get_model()
    path = model.get_path(iter)
    tree.expand_to_path(path)

# ---
#  END OF PROGRAM
