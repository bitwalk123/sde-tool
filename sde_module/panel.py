# -----------------------------------------------------------------------------
#  panel.py --- panel widgets for SDE Tool
# -----------------------------------------------------------------------------
import gi
import os
import pathlib
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import dlg, pcs, utils


# -----------------------------------------------------------------------------
#  main - main GUI of SDE Tool
# -----------------------------------------------------------------------------
class main(Gtk.Notebook):
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
    # -------------------------------------------------------------------------
    def set_statusbar_info(self, instance, id):
        self.statusbar = instance
        self.context_id = id

    # -------------------------------------------------------------------------
    #  display file name to status bar
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
    #
    #  Add New Supplier
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
    #  on_tree_doubleclicked - TreeView row Double clicked
    # -------------------------------------------------------------------------
    def on_tree_doubleclicked(self, tree, path, col, userdata=None):
        model = tree.get_model()
        iter = model.get_iter(path)
        key = model[iter][6]

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
    #  on_tree_selection_changed - Row Selection on the TreeView
    # -------------------------------------------------------------------------
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            key = model[treeiter][5]

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
    #  data_display - display Data
    #
    #  argument
    #    id_dataStr: id_data in string format
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
            name_file = info[0]
            if name_file is not None:
                self.open_file_with_app(name_file)

    # -------------------------------------------------------------------------
    #  open_file_with_app
    #
    #  argument
    #    name_file:  file to open
    # -------------------------------------------------------------------------
    def open_file_with_app(self, name_file):
        link_file = pathlib.PurePath(name_file)
        # Explorer can cover all cases on Windows NT
        subprocess.Popen(['explorer', link_file])

    # -------------------------------------------------------------------------
    #  add new Part
    # -------------------------------------------------------------------------
    def part_add_new(self, id_partStr):
        f = dlg.file_chooser(self.parent)
        filename = f.get()

        if filename is not None:
            id_part = utils.get_id(id_partStr, 'id_part = (.+)')
            # SQL for insert new link of file to table part_revision
            sql = self.obj.sql(
                "INSERT INTO part_revision VALUES(NULL, ?, 1, '?')",
                [id_part, filename]
            )
            self.obj.put(sql)


    # -------------------------------------------------------------------------
    #  part_display - display Part
    #
    #  argument
    #    id_partStr:  id_part in string format
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
                name_file = info[0]
                self.open_file_with_app(name_file)
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
    #    enum:
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
        iter_project = self.store.append(
            iter,
            ["Project", str(id_project), None, 0, False, '', 'id_project = ' + str(id_project)]
        )
        # PART
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        iter_part = self.store.append(
            iter_project,
            ["PART", None, None, 0, False, '', 'lbl_part']
        )
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        self.store.append(
            iter_part,
            [None, num_part, description, 0, False, '', 'id_part = ' + str(id_part)]
        )
        # STAGE
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        iter_stage = self.store.append(
            iter_project,
            ["STAGE", None, None, 0, False, '', 'lbl_stage']
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
            self.store.append(
                iter_stage, [name_stage, None, None, 0, False, '', id_name]
            )

        # ---------------------------------------------------------------------
        # expand added rows
        utils.tree_node_expand(tree, iter_project)

    # -------------------------------------------------------------------------
    #  supplier_add_new - add New Supplier
    #
    #  argument:
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
            progress = 0
            # _/_/_/_/_/_/_/_/_/
            #  ADD NODE (ROW)
            self.store.append(
                None,
                [new_supplier, None, None, progress, False, '', id_name]
            )

    # -------------------------------------------------------------------------
    #  supplier_setting - Supplier setting
    #
    #  argument
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
#  END OF PROGRAM
