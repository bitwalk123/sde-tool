# -----------------------------------------------------------------------------
#  panel.py --- panel widgets for SDE Tool
# -----------------------------------------------------------------------------
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os.path
import pathlib
import subprocess

from . import pcs


# -----------------------------------------------------------------------------
#  PanelMain - main GUI of SDE Tool
# -----------------------------------------------------------------------------
class PanelMain(Gtk.Notebook):
    def __init__(self, obj):
        Gtk.Notebook.__init__(self)
        self.obj = obj

        panel_main = self.create_panel_main()
        self.append_page(panel_main, Gtk.Label(label="Main"))

    # -------------------------------------------------------------------------
    #  create_panel_main
    # -------------------------------------------------------------------------
    def create_panel_main(self):
        # tree
        store = pcs.store(self.obj)
        tree = Gtk.TreeView(model=store)
        store.create_tree_header(tree)

        # scrollbar window
        scrwin = Gtk.ScrolledWindow()
        scrwin.add(tree)
        scrwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # event handling for double-click on the row of the tree
        tree.set_activate_on_single_click(False)
        tree.connect('row-activated', self.on_tree_doubleclicked)

        # event handling for selection on the row of the tree
        select = tree.get_selection()
        select.connect('changed', self.on_tree_selection_changed)

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
    #  TreeView row Double clicked
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
            self.config_supplier(id_supplier, iter, tree)

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
            sql = self.obj.sql("SELECT name_stage from stage WHERE ?", [key])
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
    #  Row Selection on the TreeView
    # -------------------------------------------------------------------------
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            key = model[treeiter][5]

            if key.startswith('id_part'):
                sql = self.obj.sql("SELECT name_file FROM part_revision WHERE ?", [key])
                self.statusbar_from_db(sql)

            if key.startswith('id_data'):
                sql = self.obj.sql("SELECT name_file FROM data_revision WHERE ?", [key])
                self.statusbar_from_db(sql)

    # =========================================================================
    #  FUNCTIONS
    # =========================================================================

    # -------------------------------------------------------------------------
    #  display_data - display Data
    #
    #  argument
    #    id_dataStr: id_data in string format
    # -------------------------------------------------------------------------
    def display_data(self, id_dataStr):
        # SQL for getting name_file from part table under specific id_part
        sql1 = self.obj.sql("SELECT MAX(num_revision) FROM data_revision WHERE ?", [id_dataStr])
        out1 = self.obj.get(sql1)
        revision_latest = out1[0][0]
        sql2 = self.obj.sql("SELECT name_file FROM data_revision WHERE ? AND num_revision = ?", [id_dataStr, revision_latest])
        out2 = self.obj.get(sql2)

        for info in out2:
            name_file = info[0]
            if name_file is not None:
                self.open_file_with_app(name_file)

    # -------------------------------------------------------------------------
    #  display_part - display Part
    #
    #  argument
    #    id_partStr: id_part in string format
    # -------------------------------------------------------------------------
    def display_part(self, id_partStr):
        sql = self.obj.sql("SELECT COUNT(*) FROM part_revision WHERE ?", [id_partStr])
        out = self.obj.get(sql)

        if out[0][0] > 0:
            sql = self.obj.sql("SELECT MAX(num_revision) FROM part_revision WHERE ?", [id_partStr])
            out = self.obj.get(sql)
            revision_latest = str(out[0][0])

            # SQL for getting name_file from part table under specific id_part
            sql = self.obj.sql("SELECT name_file FROM part_revision WHERE ? AND num_revision = ?", [id_partStr, revision_latest])
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
    # open_file_with_app
    #
    # argument
    #   name_file   file to open
    # -------------------------------------------------------------------------
    def open_file_with_app(self, name_file):
        link_file = pathlib.PurePath(name_file)
        # Explorer can cover all cases on Windows NT
        subprocess.Popen(['explorer', link_file])

