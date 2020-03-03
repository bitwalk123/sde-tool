import configparser
import os.path
import pathlib
import random
import re
import subprocess

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from sde_module import utils


class SDETool(Gtk.Window):
    # Application Version
    app_version = "0.1"
    basedir = pathlib.Path('C:/').resolve()

    # CSS
    provider = Gtk.CssProvider()
    provider.load_from_data((utils.SDETOOL_CSS).encode('utf-8'))

    # -------------------------------------------------------------------------
    def __init__(self, confFile):
        # Config
        config = configparser.ConfigParser()
        config.read(confFile, 'UTF-8')

        # Config for Database
        config_db = config['Database']
        self.dbname = config_db['DBNAME']

        # Config for Application
        config_app = config['Application']
        self.app_pdf = config_app['PDF']
        self.app_excel = config_app['EXCEL']
        self.app_word = config_app['WORD']
        self.app_ppt = config_app['PPT']

        self.obj = utils.HandleDB(self)
        if not os.path.exists(self.dbname):
            self.obj.init()

        print(self.basedir)

        # ---------------------------------------------------------------------
        # GUI
        Gtk.Window.__init__(self, title="SDE Tool")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        # self.set_icon_from_file(utils.Img().get_file("logo"))
        self.set_margin_start(2)
        self.set_margin_end(2)
        self.set_default_size(800, 600)

        # ---------------------------------------------------------------------
        # store field
        # 1. str : Name
        # 2. str : Value
        # 3. str : Description
        # 4. int : status (ProgressBar)
        # 5. str : dummy for padding right space
        # 6. str : id (hidden)
        self.store = Gtk.TreeStore(str, str, str, int, str, str)
        self.create_tree()
        tree = Gtk.TreeView(model=self.store)
        # 1. str : Name
        self.make_treeviewcolumn_str(tree, 'Name', 0)
        # 2. str : Value
        self.make_treeviewcolumn_str(tree, 'Value', 1)
        # 3. str : Description
        self.make_treeviewcolumn_str(tree, 'Description', 2)
        # 4. int : status (ProgressBar)
        self.make_treeviewcolumn_progress(tree, 'status', 3)
        # 5. str : dummy for padding right space
        self.make_treeviewcolumn_str(tree, '', 4)
        # 6. str : id for padding right space
        self.make_treeviewcolumn_str(tree, 'id', 5, False)

        # scrollbar
        scrwin = Gtk.ScrolledWindow()
        scrwin.add(tree)
        scrwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # event handling for double-click on the row of the tree
        tree.set_activate_on_single_click(False)
        tree.connect('row-activated', self.on_tree_doubleclicked)

        # event handling for selection on the row of the tree
        select = tree.get_selection()
        select.connect('changed', self.on_tree_selection_changed)

        # frame
        frame = Gtk.Frame()
        container = Gtk.Box()
        frame.add(container)

        # config button
        but_config = Gtk.Button(name='Button')
        but_config.add(utils.Img().get_image('config'))
        but_config.set_tooltip_text('App Config')
        container.pack_start(but_config, expand=False, fill=True, padding=0)

        # add button
        but_add = Gtk.Button(name='Button')
        but_add.add(utils.Img().get_image('add'))
        but_add.set_tooltip_text('Add Supplier')
        but_add.connect('clicked', self.on_click_add_new_supplier)
        container.pack_start(but_add, expand=False, fill=True, padding=0)

        # exit button
        but_exit = Gtk.Button(name='Button')
        but_exit.add(utils.Img().get_image('exit'))
        but_exit.set_tooltip_text('Exit this app')
        but_exit.connect('clicked', self.on_click_app_exit)
        container.pack_end(but_exit, expand=False, fill=True, padding=0)

        # info button
        but_info = Gtk.Button(name='Button')
        but_info.add(utils.Img().get_image('info'))
        but_info.set_tooltip_text('About this app')
        but_info.connect('clicked', self.on_click_app_info)
        container.pack_end(but_info, expand=False, fill=True, padding=0)

        # status bar
        self.status = Gtk.Statusbar(name='Status')
        self.context_id = self.status.get_context_id('sde')

        # widget layout management
        box = Gtk.Box(name='Base', orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(frame, expand=False, fill=True, padding=0)
        box.pack_start(scrwin, expand=True, fill=True, padding=0)
        box.pack_start(self.status, expand=False, fill=True, padding=0)
        self.add(box)

    # -------------------------------------------------------------------------
    def add_new_part(self, id_partStr):
        path = self.DlgFileChooserPDF()
        if path is not None:
            id_part = self.get_id(id_partStr, 'id_part = (.+)')
            # SQL for insert new link of file to table part_revision
            sql = self.obj.make_sql("INSERT INTO part_revision VALUES(NULL, ?, 1, '?')", [id_part, path])
            self.obj.put(sql)

    # -------------------------------------------------------------------------
    def add_new_project(self, id_supplier, iter, tree):
        dialog = utils.DlgAddNewProject(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name_owner = dialog.get_name_owner()
            num_part = dialog.get_num_part()
            description = dialog.get_description()
            product = dialog.get_product()
            name_file = dialog.get_file()
            dialog.destroy()

            # insert new part
            sql = self.obj.make_sql("INSERT INTO part VALUES(NULL, '?', '?', '?')", [num_part, description, product])
            self.obj.put(sql)

            # get maxium id_part
            sql = "SELECT MAX(id_part) FROM part"
            id_part = self.obj.get(sql)[0][0]
            name_file = name_file.replace("'", "''")
            sql = self.obj.make_sql("INSERT INTO part_revision VALUES(NULL, ?, 1, '?')", [id_part, name_file])
            self.obj.put(sql)

            # get maxium id_project
            sql = "SELECT MAX(id_project) FROM project"
            num = self.obj.get(sql)[0][0]
            if num is not None:
                id_project = int(num) + 1
            else:
                id_project = 1

            # insert new object
            sql = self.obj.make_sql("INSERT INTO project VALUES(?, ?, ?, '?')", [id_project, id_supplier, id_part, name_owner])
            self.obj.put(sql)

            # PROJECT
            iter_project = self.store.append(iter, ["Project", str(id_project), None, 0, '', 'id_project = ' + str(id_project)])

            # PART
            iter_part = self.store.append(iter_project, ["PART", None, None, 0, '', 'lbl_part'])
            self.store.append(iter_part, [None, num_part, description, 0, '', 'id_part = ' + str(id_part)])

            # STAGE
            iter_stage = self.store.append(iter_project, ["STAGE", None, None, 0, '', 'lbl_stage'])

            # SQL for getting id_stage and name_stage from stage table order by id_stage ascending
            sql = "SELECT id_stage, name_stage FROM stage ORDER BY id_stage ASC"
            out = self.obj.get(sql)
            for row_stage in out:
                id_stage = str(row_stage[0])
                name_stage = str(row_stage[1])
                id_name = 'id_stage = ' + id_stage;  # id_name for this node
                iter_stage_2 = self.store.append(iter_stage, [name_stage, None, None, 0, '', id_name])

            # expand added rows
            model = tree.get_model()
            path = model.get_path(iter_project)
            tree.expand_to_path(path)
        else:
            dialog.destroy()

    # -------------------------------------------------------------------------
    #  add New Supplier
    def add_new_supplier(self, new_supplier):
        # SQL for getting id_supplier from supplier table where name=supplier is new_supplier
        sql = self.obj.make_sql("SELECT id_supplier FROM supplier WHERE name_supplier = '?'", [new_supplier])
        out = self.obj.get(sql)
        for row_supplier in out:
            id_supplier = str(row_supplier[0])
            id_name = 'id_supplier = ' + id_supplier;  # id_name for this node
            progress = 0
            self.store.append(None, [new_supplier, None, None, progress, '', id_name])

    # -------------------------------------------------------------------------
    # add Part
    def add_part(self, iter_project, id_project):
        # label 'PART' node
        iter_part = self.store.append(iter_project, ['PART', None, None, 0, '', 'lbl_part'])
        # SQL for getting id_part from project table under specific id_project
        sql = self.obj.make_sql("SELECT id_part FROM project WHERE id_project = ?", [id_project])
        out = self.obj.get(sql)

        for row_part in out:
            id_part = str(row_part[0])
            id_name = 'id_part = ' + id_part;  # id_name for this node
            # SQL for num_part and description from part table under specific id_part
            sql2 = self.obj.make_sql("SELECT num_part, description FROM part WHERE ?", [id_name])
            out2 = self.obj.get(sql2)
            for part_info in out2:
                self.store.append(iter_part, [None, part_info[0], part_info[1], 0, '', id_name])

    # -------------------------------------------------------------------------
    # add Project
    def add_project(self, iter_none, id_supplier):
        # SQL for getting unique list of id_project from project table under specific id_supplier
        sql = self.obj.make_sql("SELECT DISTINCT id_project FROM project WHERE id_supplier = ? ORDER BY id_project ASC", [id_supplier])
        out = self.obj.get(sql)
        for row_project in out:
            id_project = str(row_project[0])
            id_name = 'id_project = ' + id_project;  # id_name for this node
            progress = 0
            iter_project = self.store.append(iter_none, ['Project', id_project, None, progress, '', id_name])
            # add Part Node
            self.add_part(iter_project, id_project)
            # add Stage Node
            self.add_stage(iter_project, id_project)

    # -------------------------------------------------------------------------
    # add Stage
    def add_stage(self, iter_project, id_project):
        progress = 0
        iter_stage = self.store.append(iter_project, ['STAGE', None, None, progress, '', 'lbl_stage'])
        sql1 = "SELECT id_stage, name_stage FROM stage ORDER BY id_stage ASC"
        out1 = self.obj.get(sql1)
        # EACH STAGE
        for row_stage in out1:
            id_stage = row_stage[0]
            name_stage = row_stage[1]
            id_name = 'id_stage = ' + str(id_stage)
            iter_stage_each = self.store.append(iter_stage, [name_stage, None, None, 0, '', id_name])
            sql2 = self.obj.make_sql("SELECT id_data FROM data WHERE id_project = ? AND id_stage = ? ORDER BY id_data ASC", [id_project, id_stage])
            out2 = self.obj.get(sql2)
            # DATA for EACH STAGE
            for row_data in out2:
                id_data = row_data[0]
                # PLACEFOLDER CHECK
                sql3 = self.obj.make_sql("SELECT placefolder FROM data WHERE id_data = ?", [id_data])
                out3 = self.obj.get(sql3)
                placefolder = out3[0][0]
                # LATEST REVISION CHECK
                sql4 = self.obj.make_sql("SELECT MAX(num_revision) FROM data_revision WHERE id_data = ?", [id_data])
                out4 = self.obj.get(sql4)
                num_revision = out4[0][0]
                sql5 = self.obj.make_sql("SELECT name_file FROM data_revision WHERE id_data = ? AND num_revision = ?", [id_data, num_revision])
                out5 = self.obj.get(sql5)
                for row_file in out5:
                    name_file = row_file[0]
                    self.add_stage_data(id_data, iter_stage_each, name_file, placefolder)

    # -------------------------------------------------------------------------
    #  add state data
    def add_stage_data(self, id_data, iter, name_file, disp_file=''):
        if len(disp_file) == 0:
            disp_file = pathlib.PurePath(name_file).name

        label_id = 'id_data = ' + str(id_data)
        progress = 0
        self.store.append(iter, [None, disp_file, None, progress, '', label_id])

    # -------------------------------------------------------------------------
    #  ddd Supplier
    def add_supplier(self):
        # SQL for getting id_supplier and name_supplier from supplier table
        sql = "SELECT id_supplier, name_supplier FROM supplier ORDER BY name_supplier ASC"
        out = self.obj.get(sql)
        for row_supplier in out:
            id_supplier = str(row_supplier[0])
            name_supplier = str(row_supplier[1])
            id_name = 'id_supplier = ' + id_supplier;  # id_name for this node
            progress = 0
            iter_none = self.store.append(None, [name_supplier, None, None, progress, '', id_name])
            # add Project Node
            self.add_project(iter_none, id_supplier)

    # -------------------------------------------------------------------------
    #  config Part file
    def config_part_file(self, tree, iter, model):
        iter_parent = model.iter_parent(iter)
        id_projectStr = model[iter_parent][5]

        iter_grand_parent = model.iter_parent(iter_parent)
        id_supplierStr = model[iter_grand_parent][5]

        iter_child = model.iter_children(iter)
        id_part_list = []
        while iter_child is not None:
            id_part = self.get_id_with_model(iter_child, model, "id_part")
            id_part_list.append(id_part)
            iter_child = model.iter_next(iter_child)

        dialog = utils.DlgConfigPart(self, id_supplierStr, id_projectStr, id_part_list, self.obj)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            sql = dialog.get_action()
            if sql is not None:
                if type(sql) == list:
                    for sql0 in sql:
                        self.obj.put(sql0)
                    progress = 0
                    model.append(iter, [None, dialog.num_part, dialog.description, progress, '', dialog.id_partStr])
                    path = model.get_path(iter)
                    tree.expand_to_path(path)
                else:
                    self.obj.put(sql)

        dialog.close()
        del dialog

    # -------------------------------------------------------------------------
    #  model create
    def create_tree(self):
        # add Supplier Model
        self.add_supplier()

    # -------------------------------------------------------------------------
    #  display Data
    def display_data(self, id_dataStr):
        # SQL for getting name_file from part table under specific id_part
        sql1 = self.obj.make_sql("SELECT MAX(num_revision) FROM data_revision WHERE ?", [id_dataStr])
        out1 = self.obj.get(sql1)
        num_revision = out1[0][0]
        sql2 = self.obj.make_sql("SELECT name_file FROM data_revision WHERE ? AND num_revision = ?", [id_dataStr, num_revision])
        out2 = self.obj.get(sql2)
        for info in out2:
            name_file = info[0]
            if name_file is not None:
                self.open_file_with_app(name_file)

    # -------------------------------------------------------------------------
    #  display Part
    def display_part(self, id_partStr):
        sql = self.obj.make_sql("SELECT COUNT(*) FROM part_revision WHERE ?", [id_partStr])
        out = self.obj.get(sql)

        if out[0][0] > 0:
            sql = self.obj.make_sql("SELECT MAX(num_revision) FROM part_revision WHERE ?", [id_partStr])
            out = self.obj.get(sql)
            revision_latest = str(out[0][0])

            # SQL for getting name_file from part table under specific id_part
            sql = self.obj.make_sql("SELECT name_file FROM part_revision WHERE ? AND num_revision = ?", [id_partStr, revision_latest])
            out = self.obj.get(sql)

            # the part drawing is already registered on the db
            for info in out:
                name_file = info[0]
                self.open_file_with_app(name_file)
        else:
            # the part drawing is not registered.
            # show dialog to ask if drawing is to be registered or not.
            response = self.DlgWarnNoLinkFile()
            if response == Gtk.ResponseType.YES:
                self.add_new_part(id_partStr)

    # -------------------------------------------------------------------------
    #  make TreeViewColumn for CellRenderText
    def make_treeviewcolumn_str(self, tree, title, col, visible=True):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn()
        tree.append_column(column)
        column.set_title(title)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', col)
        column.set_resizable(True)
        column.set_visible(visible)

    # -------------------------------------------------------------------------
    #  make TreeViewColumn for CellRenderProgress
    def make_treeviewcolumn_progress(self, tree, title, col):
        cell = Gtk.CellRendererProgress()
        column = Gtk.TreeViewColumn()
        tree.append_column(column)
        column.set_title(title)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'value', col)
        column.set_resizable(False)

    # =========================================================================
    #  Statusbar
    # =========================================================================

    # -------------------------------------------------------------------------
    #  display file name to status bar
    # -------------------------------------------------------------------------
    def display_text_from_db_to_statusbar(self, sql):
        out = self.obj.get(sql)
        if len(out) > 0:
            for info in out:
                name_file = str(pathlib.PurePath(str(info[0])))
                self.status.push(self.context_id, name_file)
        else:
            self.status.push(self.context_id, 'No like to file')

    # =========================================================================
    #  Event Handling
    # =========================================================================

    # -------------------------------------------------------------------------
    #  event for clicking 'Add Supplier' button
    # -------------------------------------------------------------------------
    def on_click_add_new_supplier(self, widget):
        # Dialog for adding new supplier
        dialog = utils.DlgAddNewSupplier(self)
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
                    self.showOKDialog(text, title)
                else:
                    title = "Error"
                    text = "Unknown error occured"
                    self.showOKDialog(text, title)
        else:
            dialog.destroy()

    # -------------------------------------------------------------------------
    #  Exit Application
    # -------------------------------------------------------------------------
    def on_click_app_exit(self, widget):
        Gtk.main_quit()

    # -------------------------------------------------------------------------
    #  Application Information
    # -------------------------------------------------------------------------
    def on_click_app_info(self, widget):
        dialog = utils.DlgAppAbout(self)
        dialog.run()
        dialog.destroy()

    # -------------------------------------------------------------------------
    #  Row Selection on the TreeView
    # -------------------------------------------------------------------------
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            key = model[treeiter][5]
            if key.startswith('id_part'):
                sql = self.obj.make_sql("SELECT name_file FROM part_revision WHERE ?", [key])
                self.display_text_from_db_to_statusbar(sql)
            if key.startswith('id_data'):
                sql = self.obj.make_sql("SELECT name_file FROM data_revision WHERE ?", [key])
                self.display_text_from_db_to_statusbar(sql)

    # -------------------------------------------------------------------------
    #  TreeView row double-clicked
    # -------------------------------------------------------------------------
    def on_tree_doubleclicked(self, tree, path, col, userdata=None):
        model = tree.get_model()
        iter = model.get_iter(path)
        key = model[iter][5]

        if iter is None:
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked row is Supplier related row
        if key.startswith('id_supplier'):
            id_supplier = self.get_id(key, 'id_supplier = (.+)')
            self.add_new_project(id_supplier, iter, tree)
            return
        # ---------------------------------------------------------------------
        #  check if double-clicked row is Part related row
        if key.startswith('id_part'):
            self.display_part(key)
            return
        # ---------------------------------------------------------------------
        #  check if double-clicked row is Data related row
        if key.startswith('id_data'):
            self.display_data(key)
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked row is Stage related row
        if key.startswith('id_stage'):
            sql = self.obj.make_sql("SELECT name_stage from stage WHERE ?", [key])
            out = self.obj.get(sql)
            name = out[0][0]

            self.config_stage_file(iter, model, name)
            tree.expand_to_path(path)
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked on the Part label row
        if key.startswith('lbl_part'):
            if model.iter_has_child(iter):
                self.config_part_file(tree, iter, model)

            return

    # -------------------------------------------------------------------------
    def config_stage_file(self, iter, model, name):
        #  dialog for editing stage file
        dialog = utils.DlgConfigStage(self, title=name, model=model, iter=iter, obj=self.obj, basedir=self.basedir)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            store = dialog.get_result()
            if len(store) > 0:
                # iteration of dialog
                store_iter = 0

                iter_parent = model.iter_parent(iter)
                iter_grand_parent = model.iter_parent(iter_parent)
                # ip_stage
                id_stage = self.get_id_with_model(iter, model, "id_stage")
                # ip_project
                id_project = self.get_id_with_model(iter_grand_parent, model, "id_project")

                while store_iter < len(store):
                    if store[store_iter][4] == 'new':
                        sql = self.obj.make_sql("INSERT INTO data VALUES(NULL, ?, ?, '')", [id_project, id_stage])
                        self.obj.put(sql)
                        sql = "SELECT MAX(id_data) FROM data"
                        out = self.obj.get(sql)
                        id_data = out[0][0]
                        num_revision = store[store_iter][1]
                        name_file = store[store_iter][3]
                        name_file = name_file.replace("'", "''")
                        self.basedir = pathlib.Path(name_file).parent
                        sql = self.obj.make_sql("INSERT INTO data_revision VALUES(NULL, ?, ?, '?')", [id_data, num_revision, name_file])
                        self.obj.put(sql)
                        self.add_stage_data(id_data, iter, name_file)
                    elif store[store_iter][4] == 'revise':
                        id_data = store[store_iter][0]
                        num_revision = store[store_iter][1]
                        name_file = store[store_iter][3]
                        name_file = name_file.replace("'", "''")
                        sql = self.obj.make_sql("INSERT INTO data_revision VALUES(NULL, ?, ?, '?')", [id_data, num_revision, name_file])
                        self.obj.put(sql)

                    store_iter += 1

        dialog.destroy()

    # -------------------------------------------------------------------------
    def get_id_with_model(self, iter, model, label):
        id_string = model[iter][5]
        pattern = label + ' = (.+)'
        return self.get_id(id_string, pattern)

    # -------------------------------------------------------------------------
    def get_id(self, source, pattern):
        p = re.compile(pattern)
        m = p.match(source)
        id = m.group(1)
        return int(id)

    # -------------------------------------------------------------------------
    # openFileWithApp
    #
    # argument
    #   name_file   file to open
    # -------------------------------------------------------------------------
    def open_file_with_app(self, name_file):
        link_file = pathlib.PurePath(name_file)
        extention = (os.path.splitext(link_file)[1][1:]).upper()

        if extention == 'DOC' or extention == 'DOCX':
            app_name = self.app_word
        elif extention == 'XLS' or extention == 'XLSX' or extention == 'XLSM':
            app_name = self.app_excel
        elif extention == 'PPT' or extention == 'PPTX':
            app_name = self.app_ppt
        elif extention == 'PDF':
            app_name = self.app_pdf
        else:
            self.DlgWarnNoAppAssoc(extention)
            return

        subprocess.Popen([app_name, link_file], shell=False)

    # -------------------------------------------------------------------------
    def print_rows(self, store, treeiter, indent):
        while treeiter is not None:
            if store.iter_has_child(treeiter):
                childiter = store.iter_children(treeiter)
                self.print_rows(store, childiter, indent + "\t")
            treeiter = store.iter_next(treeiter)

    # =========================================================================
    #  DIALOGs
    # =========================================================================

    # -------------------------------------------------------------------------
    #  DlgFileChooserPDF
    #  PDF file chooser dialog
    #
    #  return
    #    selected file path with POSIX format
    # -------------------------------------------------------------------------
    def DlgFileChooserPDF(self):
        dialog = Gtk.FileChooserDialog(title='select file',
                                       parent=self,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.set_icon_from_file(utils.Img().get_file('pdf'))
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
        self.addFileFiltersPDF(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            p = pathlib.Path(dialog.get_filename())
            dialog.destroy()
            # change path separator '\' to '/' to avoid unexpected errors
            return str(p.as_posix())
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return None

    # -------------------------------------------------------------------------
    def DlgWarnNoAppAssoc(self, extStr):
        dialog = Gtk.MessageDialog(parent=self,
                                   flags=0,
                                   message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.OK,
                                   text='No application!')
        dialog.set_icon_from_file(utils.Img().get_file("warning"))
        dialog.format_secondary_text('No application found associated with ' + extStr)
        dialog.run()
        dialog.destroy()

    # -------------------------------------------------------------------------
    #  DlgWarnNoLinkFile
    #  Warning dialog when no link file found in database
    #
    #  return
    #    enum:
    #      Gtk.ResponseType.YES
    #      Gtk.ResponseType.NO
    # -------------------------------------------------------------------------
    def DlgWarnNoLinkFile(self):
        dialog = Gtk.MessageDialog(parent=self,
                                   flags=0,
                                   message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.YES_NO,
                                   text='Link is empty!')
        dialog.set_icon_from_file(utils.Img().get_file('warning'))
        dialog.format_secondary_text('Do you want to create link?')

        response = dialog.run()
        dialog.destroy()
        return response

    # -------------------------------------------------------------------------
    # addFileFiltersPDF - filter for PDF
    # -------------------------------------------------------------------------
    def addFileFiltersPDF(self, dialog):
        filter_py = Gtk.FileFilter()
        filter_py.set_name('PDF File')
        filter_py.add_mime_type('application/pdf')
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)

    # -------------------------------------------------------------------------
    # addFileFiltersTEXT - filter for TEXT
    # -------------------------------------------------------------------------
    def addFileFiltersTEXT(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name('Text File')
        filter_text.add_mime_type('text/plain')
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name('All File')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)

    # -------------------------------------------------------------------------
    #  show OKDialog
    # -------------------------------------------------------------------------
    def showOKDialog(self, text, title):
        dialog = utils.DlgOK(self, title, text)
        dialog.run()
        dialog.destroy()


# -----------------------------------------------------------------------------
# MAIN
if __name__ == "__main__":
    # read Config File
    if os.name == 'nt':
        CONF_FILEPATH = 'sde.conf'
    else:
        CONF_FILEPATH = 'sde_posix.conf'

    win = SDETool(CONF_FILEPATH)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
