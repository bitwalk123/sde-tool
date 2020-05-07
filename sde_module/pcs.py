# -----------------------------------------------------------------------------
#  sde.py --- SDE related data
# -----------------------------------------------------------------------------
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pathlib


# -----------------------------------------------------------------------------
#  store for SDE Tool
#
#  store field
#  1. str : Name
#  2. str : Value
#  3. str : Description
#  4. int : Status (ProgressBar)
#  5. str : Dummy for padding right space
#  6. str : id (hidden)
# -----------------------------------------------------------------------------
class store(Gtk.TreeStore):
    def __init__(self, db_instance):
        Gtk.TreeStore.__init__(self, str, str, str, int, str, str)
        self.obj = db_instance
        self.node_1_supplier()

    # =========================================================================
    #   STRUCTURED STORE DATA
    # =========================================================================

    # -------------------------------------------------------------------------
    #  node_1_supplier
    # -------------------------------------------------------------------------
    def node_1_supplier(self):
        # SQL for getting id_supplier and name_supplier from supplier table
        sql = "SELECT id_supplier, name_supplier FROM supplier ORDER BY name_supplier ASC"
        out = self.obj.get(sql)

        # EACH SUPPLIER
        for row_supplier in out:
            id_supplier = str(row_supplier[0])
            name_supplier = str(row_supplier[1])
            id_name = 'id_supplier = ' + id_supplier;  # id_name for this node
            progress = 0
            iter_none = self.append(None, [name_supplier, None, None, progress, '', id_name])

            # add Project Node
            self.node_2_project(iter_none, id_supplier)

    # -------------------------------------------------------------------------
    #  node_2_project
    # -------------------------------------------------------------------------
    def node_2_project(self, iter_none, id_supplier):
        # SQL for getting unique list of id_project from project table under specific id_supplier
        sql = self.obj.sql("SELECT DISTINCT id_project FROM project WHERE id_supplier = ? ORDER BY id_project ASC", [id_supplier])
        out = self.obj.get(sql)

        # EACH PROJECT
        for row_project in out:
            id_project = str(row_project[0])
            id_name = 'id_project = ' + id_project;  # id_name for this node
            progress = 0
            iter_project = self.append(iter_none, ['Project', id_project, None, progress, '', id_name])

            # add Part Node
            self.node_3_part(iter_project, id_project)
            # add Stage Node
            self.node_3_stage(iter_project, id_project)

    # -------------------------------------------------------------------------
    #  node_3_part
    # -------------------------------------------------------------------------
    def node_3_part(self, iter_project, id_project):
        # label 'PART' node
        iter_part = self.append(iter_project, ['PART', None, None, 0, '', 'lbl_part'])

        # SQL for getting id_part from project table under specific id_project
        sql = self.obj.sql("SELECT id_part FROM project WHERE id_project = ?", [id_project])
        out = self.obj.get(sql)

        # EACH PART
        for row_part in out:
            id_part = str(row_part[0])
            id_name = 'id_part = ' + id_part;  # id_name for this node
            # SQL for num_part and description from part table under specific id_part
            sql2 = self.obj.sql("SELECT num_part, description FROM part WHERE ?", [id_name])
            out2 = self.obj.get(sql2)
            for part_info in out2:
                self.append(iter_part, [None, part_info[0], part_info[1], 0, '', id_name])

    # -------------------------------------------------------------------------
    #  node_3_stage
    # -------------------------------------------------------------------------
    def node_3_stage(self, iter_project, id_project):
        progress = 0
        # label 'STAGE' node
        iter_stage = self.append(iter_project, ['STAGE', None, None, progress, '', 'lbl_stage'])

        sql = "SELECT id_stage, name_stage FROM stage ORDER BY id_stage ASC"
        out = self.obj.get(sql)
        # EACH STAGE
        for row_stage in out:
            id_stage = row_stage[0]
            name_stage = row_stage[1]
            id_name = 'id_stage = ' + str(id_stage)
            iter_stage_each = self.append(iter_stage, [name_stage, None, None, 0, '', id_name])
            sql = self.obj.sql("SELECT id_data FROM data WHERE id_project = ? AND id_stage = ? ORDER BY id_data ASC", [id_project, id_stage])
            out = self.obj.get(sql)
            self.node_4_stage_data(iter_stage_each, out)

    # -------------------------------------------------------------------------
    #  node_4_stage_data - stage data
    # -------------------------------------------------------------------------
    def node_4_stage_data(self, iter, out):
        # DATA for EACH STAGE
        for row_data in out:
            id_data = row_data[0]

            # PLACEFOLDER CHECK
            sql1 = self.obj.sql("SELECT placefolder FROM data WHERE id_data = ?", [id_data])
            out1 = self.obj.get(sql1)
            placefolder = out1[0][0]

            # LATEST REVISION CHECK
            sql2 = self.obj.sql("SELECT MAX(num_revision) FROM data_revision WHERE id_data = ?", [id_data])
            out2 = self.obj.get(sql2)
            num_revision = out2[0][0]

            # GET LATEST FILE LINK
            sql3 = self.obj.sql("SELECT name_file FROM data_revision WHERE id_data = ? AND num_revision = ?", [id_data, num_revision])
            out3 = self.obj.get(sql3)
            for row_file in out3:
                name_file = row_file[0]
                if len(placefolder) == 0:
                    placefolder = pathlib.PurePath(name_file).name

                label_id = 'id_data = ' + str(id_data)
                progress = 0
                self.append(iter, [None, placefolder, None, progress, '', label_id])

    # =========================================================================
    #  HEADER CREATION ON THE TREE WIDGET
    # =========================================================================

    # -------------------------------------------------------------------------
    #  create_tree_header
    # -------------------------------------------------------------------------
    def create_tree_header(self, tree):
        # 1. str : Name
        self.treeviewcolumn_str(tree, 'Name', 0)
        # 2. str : Value
        self.treeviewcolumn_str(tree, 'Value', 1)
        # 3. str : Description
        self.treeviewcolumn_str(tree, 'Description', 2)
        # 4. int : Status (ProgressBar)
        self.treeviewcolumn_progress(tree, 'status', 3)
        # 5. str : Dummy for padding right space
        self.treeviewcolumn_str(tree, '', 4)
        # 6. str : id for padding right space
        self.treeviewcolumn_str(tree, 'id', 5, False)

    # -------------------------------------------------------------------------
    #  TreeViewColumn for CellRenderProgress
    # -------------------------------------------------------------------------
    def treeviewcolumn_progress(self, tree, title, col):
        cell = Gtk.CellRendererProgress()
        column = Gtk.TreeViewColumn()
        tree.append_column(column)
        column.set_title(title)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'value', col)
        column.set_resizable(False)

    # -------------------------------------------------------------------------
    #  TreeViewColumn for CellRenderText
    # -------------------------------------------------------------------------
    def treeviewcolumn_str(self, tree, title, col, visible=True):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn()
        tree.append_column(column)
        column.set_title(title)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', col)
        column.set_resizable(True)
        column.set_visible(visible)
