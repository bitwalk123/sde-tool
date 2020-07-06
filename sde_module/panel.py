# -----------------------------------------------------------------------------
#  panel.py --- panel widgets for SDE Tool
# -----------------------------------------------------------------------------
import gi
import os
import pathlib
import re
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from . import dlg, pcs, utils


# -----------------------------------------------------------------------------
#  main
#  main GUI of SDE Tool
# -----------------------------------------------------------------------------
class main(Gtk.Notebook):
    # column position of id
    col_id = 6

    def __init__(self, parent, obj):
        Gtk.Notebook.__init__(self)
        self.parent = parent
        self.obj = obj

        panel_main = self.create_panel_main()
        self.append_page(panel_main, Gtk.Label(label="Main"))

    # -------------------------------------------------------------------------
    #  create_panel_main
    # -------------------------------------------------------------------------
    def create_panel_main(self):
        # tree
        self.store = pcs.store(self.obj)
        tree = Gtk.TreeView(model=self.store)
        self.store.create_tree_header(tree)

        # scrollbar window
        scrwin = Gtk.ScrolledWindow()
        scrwin.add(tree)
        scrwin.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC
        )

        # event handling for double-click on the row of the tree
        tree.set_activate_on_single_click(False)
        tree.connect(
            'row-activated',
            self.on_tree_doubleclicked
        )

        # event handling for selection on the row of the tree
        select = tree.get_selection()
        select.connect(
            'changed',
            self.on_tree_selection_changed
        )

        return scrwin

    # =========================================================================
    #  STATUSBAR related
    # =========================================================================

    # -------------------------------------------------------------------------
    #  set_statusbar_info
    #
    #  arguments
    #    instance :
    #    id       :
    # -------------------------------------------------------------------------
    def set_statusbar_info(self, instance, id):
        self.statusbar = instance
        self.context_id = id

    # -------------------------------------------------------------------------
    #  display file name to status bar
    #
    #  argument
    #    sql :
    # -------------------------------------------------------------------------
    def statusbar_from_db(self, sql):
        out = self.obj.get(sql)
        if len(out) > 0:
            for info in out:
                name_file = str(pathlib.PurePath(str(info[0])))
                self.statusbar.push(self.context_id, name_file)
        else:
            self.statusbar.push(self.context_id, 'No like to file')

    # =========================================================================
    #  EVENT HANDLING
    # =========================================================================

    # -------------------------------------------------------------------------
    #  on_click_add_new_supplier
    #  Add New Supplier
    #
    #  argument
    #    widget :
    # -------------------------------------------------------------------------
    def on_click_add_new_supplier(self, widget):
        # Dialog for adding new supplier
        dialog = dlg.add_new_supplier(self.parent)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            new_supplier = dialog.get_supplier_name()
            dialog.destroy()

            if new_supplier is not None:
                response = self.obj.add_supplier(new_supplier)
                if response == 0:
                    self.supplier_add_new(new_supplier)
                elif response == 1:
                    title = "Duplication"
                    text = utils.concat(
                        "Supplier, '",
                        new_supplier,
                        "' already exists on the database."
                    )
                    utils.show_ok_dialog(self.parent, title, text, 'error')
                else:
                    title = "Error"
                    text = "Unknown error occured!"
                    utils.show_ok_dialog(self.parent, title, text, 'error')
        else:
            dialog.destroy()

    # -------------------------------------------------------------------------
    #  on_tree_doubleclicked
    #  TreeView row Double clicked
    #
    #  arguments
    #    tree     :
    #    path     :
    #    col      :
    #    userdata :
    # -------------------------------------------------------------------------
    def on_tree_doubleclicked(self, tree, path, col, userdata=None):
        model = tree.get_model()
        iter = model.get_iter(path)
        key = model[iter][self.col_id]

        if iter is None:
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked row is Supplier related row
        if key.startswith('id_supplier'):
            id_supplier = utils.get_id(key, 'id_supplier = (.+)')
            self.supplier_setting(id_supplier, iter, tree)
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked row is Part related row
        if key.startswith('id_part'):
            self.part_display(key)
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked row is Data related row
        if key.startswith('id_data'):
            self.data_display(key)
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked row is Stage related row
        if key.startswith('id_stage'):
            sql = self.obj.sql(
                "SELECT name_stage from stage WHERE ?",
                [key]
            )
            out = self.obj.get(sql)
            name = out[0][0]

            self.stage_setting(iter, model, name)
            tree.expand_to_path(path)
            return

        # ---------------------------------------------------------------------
        #  check if double-clicked on the Part label row
        if key.startswith('lbl_part'):
            if model.iter_has_child(iter):
                self.config_part_file(tree, iter, model)

            return

    # -------------------------------------------------------------------------
    #  on_tree_selection_changed
    #  Row Selection on the TreeView
    #
    #  argument
    #    selection :
    # -------------------------------------------------------------------------
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            key = model[treeiter][self.col_id]

            if key.startswith('id_part'):
                sql = self.obj.sql(
                    "SELECT name_file FROM part_revision WHERE ?",
                    [key]
                )
                self.statusbar_from_db(sql)

            if key.startswith('id_data'):
                sql = self.obj.sql(
                    "SELECT name_file FROM data_revision WHERE ?",
                    [key]
                )
                self.statusbar_from_db(sql)

    # =========================================================================
    #  GENERAL METHODS
    # =========================================================================

    # -------------------------------------------------------------------------
    #  config_part_file
    #  config Part file
    #
    #  arguments
    #    tree  :
    #    iter  :
    #    model :
    # -------------------------------------------------------------------------
    def config_part_file(self, tree, iter, model):
        iter_parent = model.iter_parent(iter)
        id_projectStr = model[iter_parent][self.col_id]

        iter_grand_parent = model.iter_parent(iter_parent)
        id_supplierStr = model[iter_grand_parent][self.col_id]

        iter_child = model.iter_children(iter)
        id_part_list = []
        while iter_child is not None:
            id_part = utils.get_id_with_model(iter_child, model, "id_part", self.col_id)
            id_part_list.append(id_part)
            iter_child = model.iter_next(iter_child)

        dialog = dlg.part_setting(self.parent, id_supplierStr, id_projectStr, id_part_list, self.obj)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            ########################################################
            # POTENTIAL BUG!!!
            # NEED TO OVERHAUL DATA HANDLING WITH DIALOG ALGORITHM
            ########################################################
            sql = dialog.get_action()
            if sql is not None:
                if type(sql) == list:
                    for sql0 in sql:
                        print(sql)
                        self.obj.put(sql0)
                    model.node_add(
                        parent=iter,
                        name=None,
                        value=dialog.num_part,
                        desc=dialog.description,
                        id=dialog.id_partStr
                    )
                    path = model.get_path(iter)
                    tree.expand_to_path(path)
                else:
                    self.obj.put(sql)

        dialog.close()
        del dialog

    # -------------------------------------------------------------------------
    #  data_display
    #  display Data
    #
    #  argument
    #    id_dataStr : id_data in string format
    # -------------------------------------------------------------------------
    def data_display(self, id_dataStr):
        # SQL for getting name_file from part table under specific id_part
        sql1 = self.obj.sql(
            "SELECT MAX(num_revision) FROM data_revision WHERE ?",
            [id_dataStr]
        )
        out1 = self.obj.get(sql1)
        revision_latest = out1[0][0]

        sql2 = self.obj.sql(
            "SELECT name_file FROM data_revision WHERE ? AND num_revision = ?",
            [id_dataStr, revision_latest]
        )
        out2 = self.obj.get(sql2)

        for info in out2:
            name_file = info[0].strip()
            if name_file is not None:
                utils.open_file_with_app(name_file)

    # -------------------------------------------------------------------------
    #  add new Part
    #
    #  argument
    #    id_partStr : id_part in string format
    # -------------------------------------------------------------------------
    def part_add_new(self, id_partStr):
        filename = dlg.file_chooser.get(parent=self)

        if filename is not None:
            id_part = utils.get_id(id_partStr, 'id_part = (.+)')
            # SQL for insert new link of file to table part_revision
            sql = self.obj.sql(
                "INSERT INTO part_revision VALUES(NULL, ?, 1, '?')",
                [id_part, filename]
            )
            self.obj.put(sql)

    # -------------------------------------------------------------------------
    #  part_display
    #  display Part
    #
    #  argument
    #    id_partStr : id_part in string format
    # -------------------------------------------------------------------------
    def part_display(self, id_partStr):
        sql1 = self.obj.sql(
            "SELECT COUNT(*) FROM part_revision WHERE ?",
            [id_partStr]
        )
        out1 = self.obj.get(sql1)

        if out1[0][0] > 0:
            sql1 = self.obj.sql(
                "SELECT MAX(num_revision) FROM part_revision WHERE ?",
                [id_partStr]
            )
            out1 = self.obj.get(sql1)
            revision_latest = str(out1[0][0])

            # SQL for getting name_file from part table under specific id_part
            sql2 = self.obj.sql(
                "SELECT name_file FROM part_revision WHERE ? AND num_revision = ?",
                [id_partStr, revision_latest]
            )
            out2 = self.obj.get(sql2)

            # the part drawing is already registered on the db
            for info in out2:
                name_file = info[0].strip()
                utils.open_file_with_app(name_file)
        else:
            # the part drawing is not registered.
            # show dialog to ask if drawing is to be registered or not.
            response = self.part_display_no_file()
            if response == Gtk.ResponseType.YES:
                self.part_add_new(id_partStr)

    # -------------------------------------------------------------------------
    #  part_display_no_file
    #  Warning dialog when no link file found in database
    #
    #  return
    #    enum :
    #      Gtk.ResponseType.YES
    #      Gtk.ResponseType.NO
    # -------------------------------------------------------------------------
    def part_display_no_file(self):
        dialog = Gtk.MessageDialog(
            parent=self.parent,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text='Filename is empty!'
        )
        dialog.set_icon_from_file(utils.img().get_file('warning'))
        dialog.format_secondary_text('Do you want to create link?')

        response = dialog.run()
        dialog.destroy()
        return response

    # -------------------------------------------------------------------------
    #  project_add_new
    #
    #  argument
    #    dialog      :
    #    id_supplier :
    #    iter        :
    #    num_part    :
    #    tree        :
    # -------------------------------------------------------------------------
    def project_add_new(self, dialog, id_supplier, iter, num_part, tree):
        name_owner = dialog.get_name_owner()
        description = dialog.get_description()
        product = dialog.get_product()
        name_file = dialog.get_file()
        dialog.destroy()

        # insert new part
        sql = self.obj.sql(
            "INSERT INTO part VALUES(NULL, '?', '?', '?')",
            [num_part, description, product]
        )
        self.obj.put(sql)

        # get maxium id_part, since newest part has largest id_part
        sql = "SELECT MAX(id_part) FROM part"
        id_part = self.obj.get(sql)[0][0]

        # add file link to part_revision table
        if (len(name_file) > 0) and os.path.exists(name_file):
            name_file = name_file.replace("'", "''")
            sql = self.obj.sql(
                "INSERT INTO part_revision VALUES(NULL, ?, 1, '?')",
                [id_part, name_file]
            )
            self.obj.put(sql)

        # get maxium id_project
        # note: id_project is not PRIMARY KEY
        sql = "SELECT MAX(id_project) FROM project"
        num = self.obj.get(sql)[0][0]
        if num is not None:
            id_project = int(num) + 1
        else:
            id_project = 1

        # insert new object to database
        sql = self.obj.sql(
            "INSERT INTO project VALUES(?, ?, ?, '?')",
            [id_project, id_supplier, id_part, name_owner]
        )
        self.obj.put(sql)

        # insert new project to tree
        # PROJECT
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        iter_project = self.store.node_add(
            parent=iter,
            name="Project",
            value=str(id_project),
            desc=None,
            id='id_project = ' + str(id_project)
        )
        # PART
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        iter_part = self.store.node_add(
            parent=iter_project,
            name="PART",
            value=None,
            desc=None,
            id='lbl_part'
        )
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        self.store.node_add(
            parent=iter_part,
            name=None,
            value=num_part,
            desc=description,
            id='id_part = ' + str(id_part)
        )
        # STAGE
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        iter_stage = self.store.node_add(
            parent=iter_project,
            name="STAGE",
            value=None,
            desc=None,
            id='lbl_stage'
        )
        # SQL for getting id_stage and name_stage from stage table order by id_stage ascending
        sql = "SELECT id_stage, name_stage FROM stage ORDER BY id_stage ASC"
        out = self.obj.get(sql)
        for row_stage in out:
            id_stage = str(row_stage[0])
            name_stage = str(row_stage[1])
            id_name = 'id_stage = ' + id_stage;  # id_name for this node
            # _/_/_/_/_/_/_/_/_/
            #  ADD NODE (ROW)
            self.store.node_add(
                parent=iter_stage,
                name=name_stage,
                value=None,
                desc=None,
                id=id_name
            )

        # ---------------------------------------------------------------------
        # expand added rows
        utils.tree_node_expand(tree, iter_project)

    # -------------------------------------------------------------------------
    #  stage_setting
    #
    #  arguments
    #    iter  :
    #    model :
    #    name  :
    # -------------------------------------------------------------------------
    def stage_setting(self, iter, model, name):
        #  dialog for editing stage file
        dialog = dlg.stage_setting(
            parent=self.parent,
            title=name,
            model=model,
            iter=iter,
            col_id=self.col_id,
            obj=self.obj,
            basedir=self.parent.basedir
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            store = dialog.get_result()
            if len(store) > 0:
                # iteration of dialog
                store_iter = 0

                iter_parent = model.iter_parent(iter)
                iter_grand_parent = model.iter_parent(iter_parent)
                # id_stage
                id_stage = utils.get_id_with_model(iter, model, "id_stage", self.col_id)
                # id_project
                id_project = utils.get_id_with_model(iter_grand_parent, model, "id_project", self.col_id)

                while store_iter < len(store):
                    if store[store_iter][4] == 'new':
                        sql = self.obj.sql("INSERT INTO data VALUES(NULL, ?, ?, '')", [id_project, id_stage])
                        self.obj.put(sql)
                        sql = "SELECT MAX(id_data) FROM data"
                        out = self.obj.get(sql)
                        id_data = out[0][0]
                        num_revision = store[store_iter][1]
                        name_file = store[store_iter][3]
                        name_file = name_file.replace("'", "''")
                        self.basedir = pathlib.Path(name_file).parent
                        sql = self.obj.sql("INSERT INTO data_revision VALUES(NULL, ?, ?, '?')", [id_data, num_revision, name_file])
                        self.obj.put(sql)
                        self.stage_setting_add_file_2_node(id_data, iter, name_file)
                    elif store[store_iter][4] == 'revise':
                        id_data = store[store_iter][0]
                        num_revision = store[store_iter][1]
                        name_file = store[store_iter][3]
                        name_file = name_file.replace("'", "''")
                        sql = self.obj.sql("INSERT INTO data_revision VALUES(NULL, ?, ?, '?')", [id_data, num_revision, name_file])
                        self.obj.put(sql)

                    store_iter += 1

        dialog.destroy()

    # -------------------------------------------------------------------------
    #  stage_setting_add_file_2_node
    #
    #  arguments
    #    id_data   :
    #    iter      :
    #    name_file :
    #    disp_file :
    # -------------------------------------------------------------------------
    def stage_setting_add_file_2_node(self, id_data, iter, name_file, disp_file=''):
        if len(disp_file) == 0:
            disp_file = pathlib.PurePath(name_file).name

        label_id = 'id_data = ' + str(id_data)
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        self.store.node_add(
            parent=iter,
            name=None,
            value=disp_file,
            desc=None,
            id=label_id
        )

    # -------------------------------------------------------------------------
    #  supplier_add_new
    #  add New Supplier
    #
    #  argument
    #    new_supplier : name of new supplier
    # -------------------------------------------------------------------------
    def supplier_add_new(self, new_supplier):
        # SQL for getting id_supplier from supplier table where name=supplier is new_supplier
        sql = self.obj.sql(
            "SELECT id_supplier FROM supplier WHERE name_supplier = '?'",
            [new_supplier]
        )
        out = self.obj.get(sql)
        for row_supplier in out:
            id_supplier = str(row_supplier[0])
            id_name = 'id_supplier = ' + id_supplier;  # id_name for this node
            # _/_/_/_/_/_/_/_/_/
            #  ADD NODE (ROW)
            self.store.node_add(
                parent=None,
                name=new_supplier,
                value=None,
                desc=None,
                id=id_name
            )

    # -------------------------------------------------------------------------
    #  supplier_setting
    #  Supplier setting
    #
    #  arguments
    #    id_supplier :  supplier id
    #    iter        :  iteration
    #    tree        :  instance of this tree widget
    # -------------------------------------------------------------------------
    def supplier_setting(self, id_supplier, iter, tree):
        dialog = dlg.supplier_setting(self.parent)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # check if new part is added ot not
            num_part = dialog.get_num_part()
            if len(num_part) > 0:
                self.project_add_new(dialog, id_supplier, iter, num_part, tree)

        dialog.destroy()


# -----------------------------------------------------------------------------
#  spc
#  spc GUI of SDE Tool
# -----------------------------------------------------------------------------
class spc(Gtk.Notebook):
    parent = None
    grid_master = None

    def __init__(self, parent):
        Gtk.Notebook.__init__(self)
        self.parent = parent

        page_master = self.create_panel_master()
        self.append_page(page_master, Gtk.Label(label="Master"))

    # -------------------------------------------------------------------------
    #  create_panel_master
    # -------------------------------------------------------------------------
    def create_panel_master(self):
        self.grid_master = Gtk.Grid()

        # scrollbar window
        scrwin = Gtk.ScrolledWindow()
        scrwin.add(self.grid_master)
        scrwin.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC
        )

        return scrwin

    def get_grid_master(self):
        return self.grid_master

    def test(self):
        but = Gtk.Button(label="TEST")
        self.grid_master.attach(but, 0, 0, 1, 1)

# ---
#  END OF PROGRAM
