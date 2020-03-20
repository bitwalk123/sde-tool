import os
import pathlib
import re
import sqlite3

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

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
}
'''


# -----------------------------------------------------------------------------
#  DlgAddOrRevisePart
# -----------------------------------------------------------------------------
class DlgAddOrRevisePart(Gtk.Dialog):

    def __init__(self, parent, id_part_selected):
        Gtk.Dialog.__init__(self, parent=parent, title='Add or Revise?')
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('quest'))
        self.set_default_size(0, 0)
        self.set_resizable(False)

        self.rb1 = Gtk.RadioButton.new_with_label_from_widget(None, 'add New PART of this Project')
        self.rb1.set_active(True)

        box = self.get_content_area()
        box.pack_start(self.rb1, expand=True, fill=True, padding=0)

        if id_part_selected is not None:
            self.rb2 = Gtk.RadioButton.new_with_label_from_widget(self.rb1, 'revise PART ID = ' + str(id_part_selected))
            self.rb2.set_active(True)
            box.pack_start(self.rb2, expand=True, fill=True, padding=0)

        self.show_all()

    def get_result(self):
        if self.rb1.get_active():
            return 'add'
        else:
            return 'revise'


# -----------------------------------------------------------------------------
#  DlgAddOrReviseFile
# -----------------------------------------------------------------------------
class DlgAddOrReviseFile(Gtk.Dialog):

    def __init__(self, parent, id_data_selected, basedir):
        Gtk.Dialog.__init__(self, parent=parent, title='Add New File to the Stage')
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('file'))
        self.set_default_size(400, 0)
        self.set_margin_start(1)
        self.set_margin_end(1)
        self.set_resizable(True)
        self.set_modal(True)

        grid = Gtk.Grid()

        self.rb1 = Gtk.RadioButton.new_with_label_from_widget(None, 'add New Data (File) of this Stage')
        self.rb1.set_active(True)
        grid.attach(self.rb1, 0, 0, 3, 1)
        r = 1

        if id_data_selected is not None:
            self.rb2 = Gtk.RadioButton.new_with_label_from_widget(self.rb1, 'revise Data ID = ' + str(id_data_selected))
            self.rb2.set_active(True)
            grid.attach(self.rb2, 0, 1, 3, 1)
            r = 2

        # Label for File
        lab_file = Gtk.Label(label='File', name="Label")
        lab_file.set_hexpand(False)
        lab_file.set_halign(Gtk.Align.END)

        # Entry for File
        self.file = Gtk.Entry()
        self.file.set_hexpand(True)
        # Button for File
        but_file = Gtk.Button()
        but_file.add(Img().get_image('folder', 16))
        but_file.connect('clicked', self.on_click_choose_file, basedir)
        but_file.set_hexpand(False)

        grid.attach(lab_file, 0, r, 1, 1)
        grid.attach(self.file, 1, r, 1, 1)
        grid.attach(but_file, 2, r, 1, 1)

        container = self.get_content_area()
        container.add(grid)

        self.show_all()

    def get_file(self):
        return self.file.get_text()

    def get_filename(self, basedir):
        dialog = Gtk.FileChooserDialog(title='select file', parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.set_icon_from_file(Img().get_file('file'))
        dialog.set_current_folder(str(basedir))
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
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

    def get_result(self):
        if self.rb1.get_active():
            return 'add'
        else:
            return 'revise'

    def on_click_choose_file(self, widget, basedir):
        filename = self.get_filename(basedir)
        if filename is not None:
            self.file.set_text(filename)

    # -------------------------------------------------------------------------
    # addFileFiltersALL - filter for ALL
    # -------------------------------------------------------------------------
    def addFileFiltersALL(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)


# -----------------------------------------------------------------------------
#  DlgAddNewPart2Project
# -----------------------------------------------------------------------------
class DlgAddNewPart2Project(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, title='Add New Part to the Project')
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('info'))
        self.set_default_size(400, 0)
        self.set_resizable(True)
        self.set_modal(True)

        # Label for PART No.
        lab_num_part = Gtk.Label(label='PART No.', name="Label")
        lab_num_part.set_hexpand(False)
        lab_num_part.set_halign(Gtk.Align.END)
        # Entry for PART No.
        self.num_part = Gtk.Entry()
        self.num_part.set_hexpand(True)

        # Label for Description
        lab_description = Gtk.Label(label='Description', name="Label")
        lab_description.set_hexpand(False)
        lab_description.set_halign(Gtk.Align.END)
        # Entry for Description
        self.description = Gtk.Entry()
        self.description.set_hexpand(True)

        # Label for Product
        lab_product = Gtk.Label(label='Product', name="Label")
        lab_product.set_hexpand(False)
        lab_product.set_halign(Gtk.Align.END)
        # Entry for Product
        self.product = Gtk.Entry()
        self.product.set_hexpand(True)

        # Label for File
        lab_file = Gtk.Label(label='File', name="Label")
        lab_file.set_hexpand(False)
        lab_file.set_halign(Gtk.Align.END)
        # Entry for File
        self.file = Gtk.Entry()
        self.file.set_hexpand(True)
        # Button for File
        but_file = Gtk.Button()
        but_file.add(Img().get_image('folder', 16))
        but_file.connect('clicked', self.on_click_choose_file)
        but_file.set_hexpand(False)

        grid = Gtk.Grid()
        grid.attach(lab_num_part, 0, 0, 1, 1)
        grid.attach(self.num_part, 1, 0, 2, 1)
        grid.attach(lab_description, 0, 1, 1, 1)
        grid.attach(self.description, 1, 1, 2, 1)
        grid.attach(lab_product, 0, 2, 1, 1)
        grid.attach(self.product, 1, 2, 2, 1)
        grid.attach(lab_file, 0, 3, 1, 1)
        grid.attach(self.file, 1, 3, 1, 1)
        grid.attach(but_file, 2, 3, 1, 1)

        container = self.get_content_area()
        container.add(grid)

        self.show_all()

    def get_num_part(self):
        return self.num_part.get_text()

    def get_description(self):
        return self.description.get_text()

    def get_product(self):
        return self.product.get_text()

    def get_file(self):
        return self.file.get_text()

    def get_filename(self):
        dialog = Gtk.FileChooserDialog(title='select file', parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.set_icon_from_file(Img().get_file('file'))
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
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

    def on_click_choose_file(self, widget):
        filename = self.get_filename()
        self.file.set_text(filename)

    # -------------------------------------------------------------------------
    # addFileFiltersALL - filter for ALL
    # -------------------------------------------------------------------------
    def addFileFiltersALL(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)


# -----------------------------------------------------------------------------
#  DlgConfigSupplier
# -----------------------------------------------------------------------------
class DlgConfigSupplier(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, title='Supplier Setting')
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('config'))
        self.set_default_size(400, 0)
        self.set_resizable(True)

        container = self.get_content_area()
        notebook = Gtk.Notebook()
        container.add(notebook)

        # New Project
        grid = self.page_new_project()
        notebook.append_page(grid, Gtk.Label(label="Add New Project"))

        self.show_all()

    # -------------------------------------------------------------------------
    # New Project page
    def page_new_project(self):
        # Label for Project Owner
        lab_name_owner = Gtk.Label(label='Project Owner', name="Label")
        lab_name_owner.set_hexpand(False)
        lab_name_owner.set_halign(Gtk.Align.END)
        # Entry for Project Owner
        self.name_owner = Gtk.Entry()
        self.name_owner.set_hexpand(True)

        # Label for PART No.
        lab_num_part = Gtk.Label(label='PART No.', name="Label")
        lab_num_part.set_hexpand(False)
        lab_num_part.set_halign(Gtk.Align.END)
        # Entry for PART No.
        self.num_part = Gtk.Entry()
        self.num_part.set_hexpand(True)

        # Label for Description
        lab_description = Gtk.Label(label='Description', name="Label")
        lab_description.set_hexpand(False)
        lab_description.set_halign(Gtk.Align.END)
        # Entry for Description
        self.description = Gtk.Entry()
        self.description.set_hexpand(True)

        # Label for File
        lab_file = Gtk.Label(label='File', name="Label")
        lab_file.set_hexpand(False)
        lab_file.set_halign(Gtk.Align.END)
        # Entry for File
        self.file = Gtk.Entry()
        self.file.set_hexpand(True)

        # Label for Product
        lab_product = Gtk.Label(label='Product', name="Label")
        lab_product.set_hexpand(False)
        lab_product.set_halign(Gtk.Align.END)
        # Entry for Product
        self.product = Gtk.Entry()
        self.product.set_hexpand(True)
        # Button for File
        but_file = Gtk.Button()
        but_file.add(Img().get_image('folder', 16))
        but_file.connect('clicked', self.on_click_choose_file)
        but_file.set_hexpand(False)

        grid = Gtk.Grid()
        grid.attach(lab_name_owner, 0, 0, 1, 1)
        grid.attach(self.name_owner, 1, 0, 2, 1)
        grid.attach(lab_num_part, 0, 1, 1, 1)
        grid.attach(self.num_part, 1, 1, 2, 1)
        grid.attach(lab_description, 0, 2, 1, 1)
        grid.attach(self.description, 1, 2, 2, 1)
        grid.attach(lab_product, 0, 3, 1, 1)
        grid.attach(self.product, 1, 3, 2, 1)
        grid.attach(lab_file, 0, 4, 1, 1)
        grid.attach(self.file, 1, 4, 1, 1)
        grid.attach(but_file, 2, 4, 1, 1)

        return grid

    # -------------------------------------------------------------------------
    def get_name_owner(self):
        return self.name_owner.get_text()

    # -------------------------------------------------------------------------
    def get_num_part(self):
        return self.num_part.get_text()

    # -------------------------------------------------------------------------
    def get_description(self):
        return self.description.get_text()

    # -------------------------------------------------------------------------
    def get_product(self):
        return self.product.get_text()

    # -------------------------------------------------------------------------
    def get_file(self):
        return self.file.get_text()

    # -------------------------------------------------------------------------
    def get_filename(self):
        dialog = Gtk.FileChooserDialog(title='select file', parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.set_icon_from_file(Img().get_file('file'))
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
    def on_click_choose_file(self, widget):
        filename = self.get_filename()
        self.file.set_text(filename)

    # -------------------------------------------------------------------------
    # addFileFiltersALL - filter for ALL
    # -------------------------------------------------------------------------
    def addFileFiltersALL(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)


# -----------------------------------------------------------------------------
#  DlgAddNewSupplier
# -----------------------------------------------------------------------------
class DlgAddNewSupplier(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, title='Add New Supplier')
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('info'))
        self.set_default_size(400, 0)
        self.set_resizable(True)

        lab_supplier = Gtk.Label(label='Supplier', name="Label")
        self.name_supplier = Gtk.Entry()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(lab_supplier, expand=False, fill=False, padding=0)
        hbox.pack_start(self.name_supplier, expand=True, fill=True, padding=0)

        container = self.get_content_area()
        container.add(hbox)

        self.show_all()

    def get_supplier_name(self):
        return self.name_supplier.get_text()


# -----------------------------------------------------------------------------
#  DlgAppAbout
# -----------------------------------------------------------------------------
class DlgAppAbout(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, title='About This App')
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('info'))
        self.set_default_size(400, 0)
        self.set_resizable(False)

        lab1 = Gtk.Label(label='SDE Tool', name='Title')
        lab2 = Gtk.Label(label='version ' + parent.app_version, name='Version')
        lab3 = Gtk.Label(label='© 2020 Keiichi Takahashi', name='Author')

        msg = Gtk.TextBuffer()
        text = "This SDE Tool is a helper application for supplier development engineering to organize supplier information."
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
        box.pack_start(desc, expand=False, fill=False, padding=0)

        self.show_all()

    def create_corp_logo(self):
        liststore = Gtk.ListStore(Pixbuf)
        pixbuf = Img().get_pixbuf('logo')
        liststore.append([pixbuf])
        corp_logo = Gtk.IconView()
        corp_logo.set_model(liststore)
        corp_logo.set_pixbuf_column(0)
        corp_logo.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))
        return corp_logo


# -----------------------------------------------------------------------------
#  DlgConfigApp
# -----------------------------------------------------------------------------
class DlgConfigApp(Gtk.Dialog):
    def __init__(self, parent, config):
        Gtk.Dialog.__init__(self, parent=parent, title='App Config', flags=0)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.config = config

        # Config for Database
        config_db = self.config['Database']
        self.dbname = config_db['DBNAME']

        # Config for Application
        config_app = self.config['Application']
        #self.app_pdf = config_app['PDF']
        #self.app_excel = config_app['EXCEL']
        #self.app_word = config_app['WORD']
        #self.app_ppt = config_app['PPT']
        #self.app_filer = config_app['FILER']

        self.set_icon_from_file(Img().get_file('config'))
        self.set_default_size(400, 300)
        self.set_margin_start(1)
        self.set_margin_end(1)

        box = self.get_content_area()

        notebook = Gtk.Notebook()
        box.add(notebook)

        # ---------------------------------------------------------------------
        #  TAB 1
        # ---------------------------------------------------------------------
        tab1 = Gtk.Grid()
        notebook.append_page(tab1, Gtk.Label(label='Database'))

        # database information
        lab_db = Gtk.Label(label='Database', name='Label')
        lab_db.set_hexpand(False)
        lab_db.set_justify(Gtk.Justification.RIGHT)
        lab_db.set_halign(Gtk.Align.END)
        ent_db = Gtk.Entry()
        ent_db.set_text(self.dbname)
        ent_db.set_hexpand(True)
        ent_db.set_editable(False)
        ent_db.set_can_focus(False)
        but_db = Gtk.Button()
        but_db.add(Img().get_image('folder'))
        # TODO
        # implement to choose database
        #but_db.connect('clicked', #####)

        tab1.attach(lab_db, 0, 0, 1, 1)
        tab1.attach(ent_db, 1, 0, 1, 1)
        tab1.attach(but_db, 2, 0, 1, 1)

        # ---------------------------------------------------------------------
        #  TAB 2
        # ---------------------------------------------------------------------
        #tab2 = Gtk.Grid()
        #notebook.append_page(tab2, Gtk.Label(label='Application'))

        # application information
        #list_app_info = [
        #    ['PDF', self.app_pdf, 0],
        #    ['EXCEL', self.app_excel, 1],
        #    ['WORD', self.app_word, 2],
        #    ['PPT', self.app_ppt, 3],
        #    ['FILER', self.app_filer, 4],
        #]
        #for app_info in list_app_info:
        #    lab = Gtk.Label(label=app_info[0], name='Label')
        #    lab.set_hexpand(False)
        #    lab.set_justify(Gtk.Justification.RIGHT)
        #    lab.set_halign(Gtk.Align.END)
        #    ent = Gtk.Entry()
        #    ent.set_text(app_info[1])
        #    ent.set_hexpand(True)
        #    ent.set_editable(False)
        #    ent.set_can_focus(False)
        #    if os.path.isfile(app_info[1]):
        #        icon = Gtk.STOCK_YES
        #    else:
        #        icon = Gtk.STOCK_NO
        #    img = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.MENU)
        #    but = Gtk.Button()
        #    but.add(Img().get_image('folder'))
            # TODO
            # implement to choose database
            #but_db.connect('clicked', #####)

        #    tab2.attach(lab, 0, app_info[2], 1, 1)
        ##    tab2.attach(ent, 1, app_info[2], 1, 1)
        #    tab2.attach(img, 2, app_info[2], 1, 1)
        #    tab2.attach(but, 3, app_info[2], 1, 1)

        self.show_all()


# -----------------------------------------------------------------------------
#  DlgConfigPart
# -----------------------------------------------------------------------------
class DlgConfigPart(Gtk.Dialog):
    id_part_selected = None
    sql_action = None

    num_part = None
    description = None
    name_product = None
    name_file = None
    id_partStr = None

    def __init__(self, parent, id_supplierStr, id_projectStr, id_part_list, obj):
        Gtk.Dialog.__init__(self, parent=parent, title='Config Part')
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('config'))
        self.set_default_size(400, 400)
        self.set_resizable(True)
        self.obj = obj

        self.store = Gtk.ListStore(str, str, str)
        for id_part in id_part_list:
            sql = self.obj.sql("SELECT id_part, num_revision, name_file FROM part_revision WHERE id_part = ? ORDER BY id_part, num_revision", [id_part])
            out = self.obj.get(sql)
            for row in out:
                self.store.append([str(row[0]), str(row[1]), row[2]])

        tree = Gtk.TreeView(model=self.store)

        col = 0
        for label in ('ID', 'Rev', 'File'):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(label, renderer, text=col)
            tree.append_column(column)
            col += 1

        # event handling for selection on the row of the tree
        select = tree.get_selection()
        select.connect('changed', self.on_tree_selection_changed)

        # scrollbar
        scrwin = Gtk.ScrolledWindow()
        scrwin.add(tree)
        scrwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # frame
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        container = Gtk.Box()
        frame.add(container)

        # add button
        but_add = Gtk.Button(name='Button')
        but_add.add(Img().get_image('add'))
        but_add.set_tooltip_text('Add / Revise File')
        but_add.connect('clicked', self.on_click_add_revise, id_supplierStr, id_projectStr)
        container.pack_start(but_add, expand=False, fill=True, padding=0)

        box = self.get_content_area()
        box.pack_start(frame, expand=False, fill=True, padding=0)
        box.pack_start(scrwin, expand=True, fill=True, padding=0)

        self.show_all()

    def get_action(self):
        return self.sql_action

    # -------------------------------------------------------------------------
    #  row selection
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.id_part_selected = model[treeiter][0]
            # self.id_file_selected = model[treeiter][1]

    # -------------------------------------------------------------------------
    def on_click_add_revise(self, widget, id_supplierStr, id_projectStr):
        dialog = DlgAddOrRevisePart(self, self.id_part_selected)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            result = dialog.get_result()
            dialog.destroy()
            if result == 'add':
                self.add_new_part_2_project(id_projectStr, id_supplierStr)
            else:
                self.revise_part()
        else:
            dialog.destroy()
            self.store = None

    # -------------------------------------------------------------------------
    def revise_part(self):
        # revise
        name_file = self.get_filename()
        sql = self.obj.sql("SELECT MAX(num_revision) FROM part_revision WHERE id_part = ?", [self.id_part_selected])
        out = self.obj.get(sql)
        rev = out[0][0]
        if rev is None:
            rev = 1
        else:
            rev += 1
        self.sql_action = self.obj.sql("INSERT INTO part_revision VALUES(NULL, ?, ?, '?')", [self.id_part_selected, rev, name_file])
        self.store.append([str(self.id_part_selected), str(rev), name_file])

    # -------------------------------------------------------------------------
    def add_new_part_2_project(self, id_projectStr, id_supplierStr):
        dialog = DlgAddNewPart2Project(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.num_part = num_part = dialog.get_num_part()
            self.description = description = dialog.get_description()
            name_product = dialog.get_product()
            self.name_file = name_file = dialog.get_file()
            dialog.destroy()

            # determine new id_part
            sql = "SELECT MAX(id_part) FROM part"
            out = self.obj.get(sql)
            id_part = out[0][0] + 1
            self.id_partStr = "id_part = " + str(id_part)
            # obtaine name of project owner
            sql = self.obj.sql("SELECT DISTINCT name_owner FROM project WHERE ? AND ?", [id_projectStr, id_supplierStr])
            out = self.obj.get(sql)
            name_owner = out[0][0]

            id_project = self.get_id(id_projectStr, 'id_project = (.+)')
            id_supplier = self.get_id(id_supplierStr, 'id_supplier = (.+)')

            sql1 = self.obj.sql("INSERT INTO project VALUES(?, ?, ?, '?')", [id_project, id_supplier, id_part, name_owner])
            sql2 = self.obj.sql("INSERT INTO part VALUES(NULL, '?', '?', '?')", [num_part, description, name_product])
            sql3 = self.obj.sql("INSERT INTO part_revision VALUES(NULL, ?, 1, '?')", [id_part, name_file])
            self.sql_action = [sql1, sql2, sql3]
            self.store.append([str(id_part), "1", name_file])
        else:
            dialog.destroy()
            self.store = None

    # -------------------------------------------------------------------------
    def get_filename(self):
        dialog = Gtk.FileChooserDialog(title='select file', parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.set_icon_from_file(Img().get_file('file'))
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
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
    def get_id(self, source, pattern):
        p = re.compile(pattern)
        m = p.match(source)
        id = m.group(1)
        return int(id)

    # -------------------------------------------------------------------------
    # addFileFiltersALL - filter for ALL
    # -------------------------------------------------------------------------
    def addFileFiltersALL(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)


# -----------------------------------------------------------------------------
#  DlgConfigStage
# -----------------------------------------------------------------------------
class DlgConfigStage(Gtk.Dialog):
    id_data_selected = None

    def __init__(self, parent, title, model, iter, obj, basedir):
        Gtk.Dialog.__init__(self, parent=parent, title=title, flags=0)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_icon_from_file(Img().get_file('config'))
        self.set_default_size(800, 400)
        self.set_margin_start(1)
        self.set_margin_end(1)

        self.obj = obj
        self.result = ''
        self.connect('response', self.on_response)
        box = self.get_content_area()

        self.store = Gtk.ListStore(str, str, bool, str, str)

        iter_parent = model.iter_parent(iter)
        iter_grand_parent = model.iter_parent(iter_parent)
        id_stageStr = model[iter][5]
        id_projectStr = model[iter_grand_parent][5]
        sql = self.obj.sql("SELECT id_data FROM data WHERE ? AND ?", [id_projectStr, id_stageStr])
        out = self.obj.get(sql)
        for row in out:
            self.get_revised_data(row)

        tree = Gtk.TreeView(model=self.store)

        # id_data
        self.make_column_text(tree, 0, 'ID')
        # num_revision
        self.make_column_text(tree, 1, 'Rev.')
        # delete flag
        self.make_column_toggle(tree, 2, 'Del')
        # name_file
        self.make_column_text(tree, 3, 'File')
        # name_file
        self.make_column_text(tree, 4, '')

        # scrollbar
        scrwin = Gtk.ScrolledWindow()
        scrwin.add(tree)
        scrwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # frame
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        container = Gtk.Box()
        frame.add(container)

        # add button
        but_add = Gtk.Button(name='Button')
        but_add.add(Img().get_image('add'))
        but_add.set_tooltip_text('Add / Revise File')
        but_add.connect('clicked', self.on_click_add_revise, basedir)
        container.pack_start(but_add, expand=False, fill=True, padding=0)

        # packing
        box.pack_start(frame, expand=False, fill=True, padding=0)
        box.pack_start(scrwin, expand=True, fill=True, padding=0)

        # event handling for selection on the row of the tree
        select = tree.get_selection()
        select.connect('changed', self.on_tree_selection_changed)

        self.show_all()

        # set base counter of id_data
        self.set_initial_id_data()

    def get_revised_data(self, row):
        id_data = row[0]
        sql = self.obj.sql("SELECT num_revision, name_file FROM data_revision WHERE id_data = ?", [id_data])
        out = self.obj.get(sql)
        for row in out:
            num_revision = row[0]
            name_file = row[1]
            self.store.append([str(id_data), str(num_revision), False, name_file, ''])

    def make_column_text(self, tree, xcol, name_label, visible=True):
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(name_label, renderer, text=xcol)
        tree.append_column(column)
        column.set_visible(visible)

    def make_column_toggle(self, tree, xcol, name_label):
        renderer = Gtk.CellRendererToggle()
        renderer.connect('toggled', self.on_cell_toggled)
        column = Gtk.TreeViewColumn(name_label, renderer, active=xcol)
        tree.append_column(column)

    def on_response(self, widget, response_id):
        self.result = self.store

    def get_result(self):
        return self.store

    def on_cell_toggled(self, widget, path):
        self.store[path][2] = not self.store[path][2]

    def on_click_add_revise(self, widget, basedir):
        dialog = DlgAddOrReviseFile(self, self.id_data_selected, basedir)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            result = dialog.get_result()
            if result == 'add':
                self.add_new_file(dialog.file.get_text())
            else:
                self.revise_file(dialog.file.get_text())

        dialog.destroy()

    # -------------------------------------------------------------------------
    #  row selection
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.id_data_selected = model[treeiter][0]

    def set_initial_id_data(self):
        sql = "SELECT MAX(id_data) FROM data"
        out = self.obj.get(sql)
        self.id_data = out[0][0]
        if self.id_data is None:
            self.id_data = 1

    def add_new_file(self, filename):
        self.id_data += 1
        self.store.append([str(self.id_data), '1', False, filename, 'new'])

    def revise_file(self, filename):
        if len(self.store) > 0:
            store_iter = 0
            rev = 0
            while store_iter < len(self.store):
                row = self.store[store_iter][:]
                if row[0] == self.id_data_selected:
                    rev_current = int(row[1])
                    if rev_current > rev:
                        rev = rev_current

                store_iter += 1
            rev += 1
            self.store.append([str(self.id_data_selected), str(rev), False, filename, 'revise'])


# -----------------------------------------------------------------------------
#  DlgOK
# -----------------------------------------------------------------------------
class DlgOK(Gtk.Dialog):

    def __init__(self, parent, title, text):
        Gtk.Dialog.__init__(self, title)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(Img().get_file('info'))
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


# -------------------------------------------------------------------------
#  HandleDB
# -------------------------------------------------------------------------
class HandleDB():
    def __init__(self, parent):
        self.parent = parent
        self.dbname = parent.dbname

    # -------------------------------------------------------------------------
    #  initialize database
    def init(self):
        init_sql = [
            "CREATE TABLE supplier (id_supplier INTEGER PRIMARY KEY, name_supplier TEXT NOT NULL)",
            "CREATE TABLE address (id_address INTEGER PRIMARY KEY, id_supplier INTEGER, name_site TEXT, name_address TEXT, num_telephone TEXT, num_facsimile TEXT, url TEXT)",
            "CREATE TABLE part (id_part INTEGER PRIMARY KEY, num_part TEXT NOT NULL, description TEXT, name_product TEXT)",
            "CREATE TABLE part_revision (id_revision INTEGER PRIMARY KEY, id_part INTEGER, num_revision INTEGER, name_file TEXT)",
            "CREATE TABLE project (id_project INTEGER, id_supplier INTEGER, id_part INTEGER, name_owner TEXT)",
            "CREATE TABLE stage (id_stage INTEGER PRIMARY KEY, name_stage TEXT)",
            "CREATE TABLE data (id_data INTEGER PRIMARY KEY, id_project INTEGER, id_stage INTEGER, placefolder TEXT)",
            "CREATE TABLE data_revision (id_revision INTEGER PRIMARY KEY, id_data INTEGER, num_revision INTEGER, name_file TEXT)",
        ]
        stages = [
            ['CA'],  # 1
            ['Training'],  # 2
            ['PFD'],  # 3
            ['PFMEA'],  # 4
            ['CP'],  # 5
            ['OCAP'],  # 8
            ['MSA'],  # 6
            ['SPC'],  # 7
            ['SCR'],  # 9
            ['FAI'],  # 10
            ['Others'],  # 11
        ]

        con = sqlite3.connect(self.dbname)
        cur = con.cursor()

        for sql in init_sql:
            cur.execute(sql)

        cur.executemany("INSERT INTO stage VALUES(NULL, ?)", stages)
        con.commit()
        con.close()

        # dialog
        text = "No database is found. Then, new database is created."
        dialog = DlgOK(self.parent, "New database", text)
        dialog.run()
        dialog.destroy()

    def add_supplier(self, name_supplier):
        # check duplicate
        sql1 = "SELECT id_supplier FROM supplier WHERE name_supplier = '" + name_supplier + "'"
        out = self.get(sql1)
        if len(out) == 0:
            sql2 = "INSERT INTO supplier VALUES(NULL, '" + name_supplier + "')"
            self.put(sql2)
            return 0;  # no duplication
        else:
            print(name_supplier, "already exists")
            return 1;  # dupplication, error

    def put(self, sql):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def get(self, sql):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        cur.execute(sql)
        out = cur.fetchall()
        con.close()
        return out

    def sql(self, sentense, parameters):
        for param in parameters:
            sentense = sentense.replace('?', str(param), 1)
        return sentense


# -----------------------------------------------------------------------------
#  Img - Image Facility
# -----------------------------------------------------------------------------
class Img(Gtk.Image):
    IMG_ADD = "img/add-128.png"
    IMG_CONFIG = "img/config-128.png"
    IMG_CROSS = "img/cross-128.png"
    IMG_DONE = "img/done-128.png"
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
