# -----------------------------------------------------------------------------
#  rc.py --- resource class for SDE Tool
# -----------------------------------------------------------------------------
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

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
    margin-left: 5px;
    margin-right: 10px;
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
#  img - Image Facility
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


# -----------------------------------------------------------------------------
#  concat - concatenate strings
# -----------------------------------------------------------------------------
def concat(*args):
    result = ''
    for str in args:
        result = result + str

    return result
