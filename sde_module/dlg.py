# -----------------------------------------------------------------------------
#  dlg.py
#  dialog class for SDE Tool
# -----------------------------------------------------------------------------
import gi
import os
import pathlib
import platform

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from . import mbar, utils


# =============================================================================
#  CancelOKDialog
#  dialog with Cancel & OK buttons class (templete)
# =============================================================================
class CancelOKDialog(Gtk.Dialog):
    def __init__(self, parent, title, flags=0):
        Gtk.Dialog.__init__(self, parent=parent, title=title, flags=flags)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.parent = parent


# =============================================================================
#  NBDialog
#  dialog with notebook class (template)
# =============================================================================
class NBDialog(CancelOKDialog):
    def __init__(self, parent, title):
        CancelOKDialog.__init__(self, parent=parent, title=title)
        self.parent = parent

        self.set_icon_from_file(utils.img().get_file('config'))
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
#  GridPane
#  dialog pane with grid layout (template)
# =============================================================================
class GridPane(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent

    # -------------------------------------------------------------------------
    def get_filename(self):
        f = file_chooser(self.parent)
        return f.get()


# =============================================================================
#  implementation
# =============================================================================

# -----------------------------------------------------------------------------
#  add_new_supplier
# -----------------------------------------------------------------------------
class add_new_supplier(CancelOKDialog):

    def __init__(self, parent):
        CancelOKDialog.__init__(self, parent=parent, title='Add New Supplier')
        self.set_icon_from_file(utils.img().get_file('add'))
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
#  app_about
# -----------------------------------------------------------------------------
class app_about(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, title='About This App')
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(utils.img().get_file('info'))
        self.set_default_size(400, 0)
        self.set_resizable(False)

        lab1 = Gtk.Label(
            label='SDE Tool',
            name='Title'
        )
        lab2 = Gtk.Label(
            label='version ' + parent.app_version,
            name='Version'
        )
        lab3 = Gtk.Label(
            label='© 2020 Keiichi Takahashi',
            name='Author'
        )
        lab4 = Gtk.Label(
            label='running on python ' + platform.python_version() + ' / ' + parent.app_platform,
            name='PyVer'
        )

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
        pixbuf = utils.img().get_pixbuf('logo')
        liststore.append([pixbuf])
        app_logo = Gtk.IconView()
        app_logo.set_model(liststore)
        app_logo.set_pixbuf_column(0)
        app_logo.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))
        return app_logo


# -----------------------------------------------------------------------------
#  file chooser
# -----------------------------------------------------------------------------
class file_chooser():
    basedir = ''
    parent = None

    def __init__(self, parent):
        self.parent = parent

    # -------------------------------------------------------------------------
    #  get
    #  get filename with dialog (class method)
    #
    #  argument
    #    cls : this class object for this class method
    # -------------------------------------------------------------------------
    @classmethod
    def get(cls):
        dialog = Gtk.FileChooserDialog(title='select file', parent=cls.parent, action=Gtk.FileChooserAction.OPEN)
        dialog.set_icon_from_file(utils.img().get_file('file'))
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        if os.path.exists(cls.basedir):
            dialog.set_current_folder(str(cls.basedir))

        cls.filename_filter_all(dialog)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            p = pathlib.Path(dialog.get_filename())
            cls.basedir = os.path.dirname(p)
            dialog.destroy()
            # change path separator '\' to '/' to avoid unexpected errors
            name_file = str(p.as_posix())
            return name_file
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return None

    # -------------------------------------------------------------------------
    #  filename_filter_all
    #  filter for ALL
    #
    #  argument
    #    dialog : instance of Gtk.FileChooserDialog to attach this file filter
    # -------------------------------------------------------------------------
    def filename_filter_all(dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)


# -----------------------------------------------------------------------------
#  ok dialog
# -----------------------------------------------------------------------------
class ok(Gtk.Dialog):

    def __init__(self, parent, title, text, image):
        Gtk.Dialog.__init__(self, parent=parent, title=title)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_icon_from_file(utils.img().get_file(image))
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
#  part_setting
# -----------------------------------------------------------------------------
class part_setting(CancelOKDialog):
    id_part_selected = None
    sql_action = None

    num_part = None
    description = None
    name_product = None
    name_file = None
    id_partStr = None

    def __init__(self, parent, id_supplierStr, id_projectStr, id_part_list, obj):
        CancelOKDialog.__init__(self, parent=parent, title='Part Setting')
        self.set_icon_from_file(utils.img().get_file('config'))
        self.set_default_size(400, 400)
        self.set_resizable(True)
        self.obj = obj

        # ---------------------------------------------------------------------
        #  menubar
        # ---------------------------------------------------------------------
        menubar = mbar.sub_add()
        but_add = menubar.get_obj('add')
        but_add.set_tooltip_text('Add or Revise PART')
        but_add.connect(
            'clicked',
            self.on_click_add_or_revise,
            id_supplierStr,
            id_projectStr
        )

        # ---------------------------------------------------------------------
        #  main part with treeview with list store
        # ---------------------------------------------------------------------
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

        # ---------------------------------------------------------------------
        #  layout and packing
        # ---------------------------------------------------------------------
        box = self.get_content_area()
        box.pack_start(menubar, expand=False, fill=True, padding=0)
        box.pack_start(scrwin, expand=True, fill=True, padding=0)

        self.show_all()

    # -------------------------------------------------------------------------
    #  get_action
    # -------------------------------------------------------------------------
    def get_action(self):
        return self.sql_action

    # -------------------------------------------------------------------------
    #  row selection
    # -------------------------------------------------------------------------
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.id_part_selected = model[treeiter][0]
            # self.id_file_selected = model[treeiter][1]

    # -------------------------------------------------------------------------
    #  on_click_add_or_revise
    #
    #  arguments
    #    widget
    #    id_supplierStr
    #    id_projectStr
    # -------------------------------------------------------------------------
    def on_click_add_or_revise(self, widget, id_supplierStr, id_projectStr):
        dialog = part_setting_add_or_revise(self, self.id_part_selected)
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
    #  revise_part
    # -------------------------------------------------------------------------
    def revise_part(self):
        f = file_chooser(self.parent)
        name_file = f.get()
        if name_file is not None:
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
    #  add_new_part_2_project
    # -------------------------------------------------------------------------
    def add_new_part_2_project(self, id_projectStr, id_supplierStr):
        dialog = part_setting_add_new_2_project(self)
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

            id_project = utils.get_id(id_projectStr, 'id_project = (.+)')
            id_supplier = utils.get_id(id_supplierStr, 'id_supplier = (.+)')

            sql1 = self.obj.sql("INSERT INTO project VALUES(?, ?, ?, '?')", [id_project, id_supplier, id_part, name_owner])
            sql2 = self.obj.sql("INSERT INTO part VALUES(NULL, '?', '?', '?')", [num_part, description, name_product])

            if len(name_file.strip()) > 0:
                print("DEBUG", name_file)
                sql3 = self.obj.sql("INSERT INTO part_revision VALUES(NULL, ?, 1, '?')", [id_part, name_file])
                self.sql_action = [sql1, sql2, sql3]
            else:
                self.sql_action = [sql1, sql2]

            self.store.append([str(id_part), "1", name_file])
        else:
            dialog.destroy()
            self.store = None


# -----------------------------------------------------------------------------
#  part_setting_add_or_revise
# -----------------------------------------------------------------------------
class part_setting_add_or_revise(CancelOKDialog):

    def __init__(self, parent, id_part_selected):
        CancelOKDialog.__init__(self, parent=parent, title='Add or Revise?')
        self.set_icon_from_file(utils.img().get_file('quest'))
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
#  part_setting_add_new_2_project
# -----------------------------------------------------------------------------
class part_setting_add_new_2_project(CancelOKDialog):
    def __init__(self, parent):
        CancelOKDialog.__init__(self, parent=parent, title='Add New Part to the Project')
        self.set_icon_from_file(utils.img().get_file('info'))
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
        but_file.add(utils.img().get_image('folder', 16))
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

    def on_click_choose_file(self, widget):
        f = file_chooser(self.parent)
        name_file = f.get()
        self.file.set_text(name_file)


# -----------------------------------------------------------------------------
#  supplier_setting
# -----------------------------------------------------------------------------
class supplier_setting(NBDialog):

    def __init__(self, parent):
        NBDialog.__init__(self, parent=parent, title='Supplier Setting')
        notebook = self.get_notebook()

        # New Project
        self.pane_new_proj = supplier_setting_new_proj(parent)
        notebook.append_page(self.pane_new_proj, Gtk.Label(label="Add New Project"))

        self.show_all()

    # -------------------------------------------------------------------------
    def get_name_owner(self):
        return self.pane_new_proj.name_owner.get_text().strip()

    # -------------------------------------------------------------------------
    def get_num_part(self):
        return self.pane_new_proj.num_part.get_text().strip()

    # -------------------------------------------------------------------------
    def get_description(self):
        return self.pane_new_proj.description.get_text().strip()

    # -------------------------------------------------------------------------
    def get_product(self):
        return self.pane_new_proj.product.get_text().strip()

    # -------------------------------------------------------------------------
    def get_file(self):
        return self.pane_new_proj.file.get_text().strip()


# -----------------------------------------------------------------------------
#  supplier_setting_new_proj
# -----------------------------------------------------------------------------
class supplier_setting_new_proj(GridPane):
    def __init__(self, parent):
        GridPane.__init__(self, parent=parent)
        self.parent = parent

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
        but_file.add(utils.img().get_image('folder', 16))
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
        f = file_chooser(self.parent)
        filename = f.get()
        if filename is not None:
            self.file.set_text(filename)


# ---
#  END OF PROGRAM


# -----------------------------------------------------------------------------
#  stage_setting
# -----------------------------------------------------------------------------
class stage_setting(CancelOKDialog):
    id_data_selected = None

    def __init__(self, parent, title, model, iter, col_id, obj, basedir):
        CancelOKDialog.__init__(self, parent=parent, title=title)

        self.set_icon_from_file(utils.img().get_file('config'))
        self.set_default_size(800, 400)
        self.set_margin_start(1)
        self.set_margin_end(1)

        self.col_id = col_id
        self.obj = obj
        self.result = ''
        self.connect('response', self.on_response)

        # ---------------------------------------------------------------------
        #  menubar
        # ---------------------------------------------------------------------
        frame = mbar.sub_add()
        but_add = frame.get_obj('add')
        but_add.set_tooltip_text('Add or Revise File')
        but_add.connect(
            'clicked',
            self.on_click_add_revise,
            basedir
        )

        # ---------------------------------------------------------------------
        #  main part with treeview with list store
        # ---------------------------------------------------------------------
        self.store = Gtk.ListStore(str, str, bool, str, str)
        iter_parent = model.iter_parent(iter)
        iter_grand_parent = model.iter_parent(iter_parent)
        id_stageStr = model[iter][self.col_id]
        id_projectStr = model[iter_grand_parent][self.col_id]
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

        # ---------------------------------------------------------------------
        #  layout and packing
        # ---------------------------------------------------------------------
        box = self.get_content_area()
        box.pack_start(frame, expand=False, fill=True, padding=0)
        box.pack_start(scrwin, expand=True, fill=True, padding=0)

        # event handling for selection on the row of the tree
        select = tree.get_selection()
        select.connect('changed', self.on_tree_selection_changed)

        self.show_all()

        # set base counter of id_data
        self.set_initial_id_data()

    # -------------------------------------------------------------------------
    #  get_revised_data
    #
    #  argument
    #    row :
    # -------------------------------------------------------------------------
    def get_revised_data(self, row):
        id_data = row[0]
        sql = self.obj.sql("SELECT num_revision, name_file FROM data_revision WHERE id_data = ?", [id_data])
        out = self.obj.get(sql)
        for row in out:
            num_revision = row[0]
            name_file = row[1]
            self.store.append([str(id_data), str(num_revision), False, name_file, ''])

    # -------------------------------------------------------------------------
    #  make_column_text
    #
    #  arguments
    #    tree       :
    #    xcol       :
    #    name_label :
    #    visible    :
    # -------------------------------------------------------------------------
    def make_column_text(self, tree, xcol, name_label, visible=True):
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(name_label, renderer, text=xcol)
        tree.append_column(column)
        column.set_visible(visible)

    # -------------------------------------------------------------------------
    #  make_column_toggle
    #
    #  arguments
    #    tree       :
    #    xcol       :
    #    name_label :
    # -------------------------------------------------------------------------
    def make_column_toggle(self, tree, xcol, name_label):
        renderer = Gtk.CellRendererToggle()
        renderer.connect('toggled', self.on_cell_toggled)
        column = Gtk.TreeViewColumn(name_label, renderer, active=xcol)
        tree.append_column(column)

    # -------------------------------------------------------------------------
    #  on_response
    #
    #  arguments
    #    widget      :
    #    response_id :
    # -------------------------------------------------------------------------
    def on_response(self, widget, response_id):
        self.result = self.store

    # -------------------------------------------------------------------------
    #  get_result
    # -------------------------------------------------------------------------
    def get_result(self):
        return self.store

    # -------------------------------------------------------------------------
    #  on_cell_toggled
    #
    #  arguments
    #    widget :
    #    path   :
    # -------------------------------------------------------------------------
    def on_cell_toggled(self, widget, path):
        self.store[path][2] = not self.store[path][2]

    # -------------------------------------------------------------------------
    #  on_click_add_revise
    #
    #  arguments
    #    widget  :
    #    basedir :
    # -------------------------------------------------------------------------
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
    #  on_tree_selection_changed
    #  row selection
    #
    #  argument
    #    selection :
    # -------------------------------------------------------------------------
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.id_data_selected = model[treeiter][0]

    # -------------------------------------------------------------------------
    #  set_initial_id_data
    # -------------------------------------------------------------------------
    def set_initial_id_data(self):
        sql = "SELECT MAX(id_data) FROM data"
        out = self.obj.get(sql)
        self.id_data = out[0][0]
        if self.id_data is None:
            self.id_data = 1

    # -------------------------------------------------------------------------
    #  add_new_file
    #
    #  arguments
    #    filename :
    # -------------------------------------------------------------------------
    def add_new_file(self, filename):
        self.id_data += 1
        self.store.append([str(self.id_data), '1', False, filename, 'new'])

    # -------------------------------------------------------------------------
    #  revise_file
    #
    #  arguments
    #    filename :
    # -------------------------------------------------------------------------
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
#  DlgAddOrReviseFile
# -----------------------------------------------------------------------------
class DlgAddOrReviseFile(Gtk.Dialog):

    def __init__(self, parent, id_data_selected, basedir):
        Gtk.Dialog.__init__(self, parent=parent, title='Add New File to the Stage')
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_icon_from_file(utils.img().get_file('file'))
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
        but_file.add(utils.img().get_image('folder', 16))
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
        dialog.set_icon_from_file(utils.img().get_file('file'))
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
