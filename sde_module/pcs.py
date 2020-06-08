# -----------------------------------------------------------------------------
#  sde.py --- SDE related data
# -----------------------------------------------------------------------------
import gi
import pathlib

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# -----------------------------------------------------------------------------
#  store for SDE Tool
#
#  store field
#  1. str  : Name
#  2. str  : Value
#  3. str  : Description
#  4. int  : Status (ProgressBar)
#  5. bool : Check (ToggleButton)
#  6. str  : Dummy for padding right space
#  7. str  : id (hidden)
# -----------------------------------------------------------------------------
class store(Gtk.TreeStore):
    row = {
        'name': 0,
        'value': 1,
        'desc': 2,
        'progress': 3,
        'check': 4,
        'dummy': 5,
        'id': 6
    }

    def __init__(self, db_instance):
        Gtk.TreeStore.__init__(self, str, str, str, int, bool, str, str)
        self.obj = db_instance
        self.node_1_supplier()

    # =========================================================================
    #   STRUCTURED STORE DATA
    # =========================================================================

    # -------------------------------------------------------------------------
    #  node_add
    #
    #  arguments
    #    parent : parent node
    #    name   : Name
    #    value  : Value
    #    desc   : Description
    #    id     : id
    #
    #  return
    #    iteration (node)
    # -------------------------------------------------------------------------
    def node_add(self, parent, name, value, desc, id):
        progress = 0
        check = False
        return self.append(
            parent,
            [name, value, desc, progress, check, '', id]
        )

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
            # _/_/_/_/_/_/_/_/_/
            #  ADD NODE (ROW)
            iter_none = self.node_add(
                parent=None,
                name=name_supplier,
                value=None,
                desc=None,
                id=id_name
            )
            # add Project Node
            self.node_2_project(iter_none, id_supplier)

    # -------------------------------------------------------------------------
    #  node_2_project
    # -------------------------------------------------------------------------
    def node_2_project(self, iter_none, id_supplier):
        # SQL for getting unique list of id_project from project table under specific id_supplier
        sql = self.obj.sql(
            "SELECT DISTINCT id_project FROM project WHERE id_supplier = ? ORDER BY id_project ASC",
            [id_supplier]
        )
        out = self.obj.get(sql)

        # EACH PROJECT
        for row_project in out:
            id_project = str(row_project[0])
            id_name = 'id_project = ' + id_project;  # id_name for this node
            # _/_/_/_/_/_/_/_/_/
            #  ADD NODE (ROW)
            iter_project = self.node_add(
                parent=iter_none,
                name='Project',
                value=id_project,
                desc=None,
                id=id_name
            )
            # add Part Node
            self.node_3_part(iter_project, id_project)
            # add Stage Node
            self.node_3_stage(iter_project, id_project)

    # -------------------------------------------------------------------------
    #  node_3_part
    # -------------------------------------------------------------------------
    def node_3_part(self, iter_project, id_project):
        # label 'PART' node
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        iter_part = self.node_add(
            parent=iter_project,
            name='PART',
            value=None,
            desc=None,
            id='lbl_part'
        )
        # SQL for getting id_part from project table under specific id_project
        sql = self.obj.sql(
            "SELECT id_part FROM project WHERE id_project = ?",
            [id_project]
        )
        out = self.obj.get(sql)

        # EACH PART
        for row_part in out:
            id_part = str(row_part[0])
            id_name = 'id_part = ' + id_part;  # id_name for this node
            # SQL for num_part and description from part table under specific id_part
            sql2 = self.obj.sql(
                "SELECT num_part, description FROM part WHERE ?",
                [id_name]
            )
            out2 = self.obj.get(sql2)
            for part_info in out2:
                # _/_/_/_/_/_/_/_/_/
                #  ADD NODE (ROW)
                self.node_add(
                    parent=iter_part,
                    name=None,
                    value=part_info[0],
                    desc=part_info[1],
                    id=id_name
                )

    # -------------------------------------------------------------------------
    #  node_3_stage
    # -------------------------------------------------------------------------
    def node_3_stage(self, iter_project, id_project):
        # label 'STAGE' node
        # _/_/_/_/_/_/_/_/_/
        #  ADD NODE (ROW)
        iter_stage = self.node_add(iter_project, 'STAGE', None, None, 'lbl_stage')
        sql = "SELECT id_stage, name_stage FROM stage ORDER BY id_stage ASC"
        out = self.obj.get(sql)
        # EACH STAGE
        for row_stage in out:
            id_stage = row_stage[0]
            name_stage = row_stage[1]
            id_name = 'id_stage = ' + str(id_stage)
            # _/_/_/_/_/_/_/_/_/
            #  ADD NODE (ROW)
            iter_stage_each = self.node_add(
                parent=iter_stage,
                name=name_stage,
                value=None,
                desc=None,
                id=id_name
            )
            sql = self.obj.sql(
                "SELECT id_data FROM data WHERE id_project = ? AND id_stage = ? ORDER BY id_data ASC",
                [id_project, id_stage]
            )
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
            sql1 = self.obj.sql(
                "SELECT placefolder FROM data WHERE id_data = ?",
                [id_data]
            )
            out1 = self.obj.get(sql1)
            placefolder = out1[0][0]

            # LATEST REVISION CHECK
            sql2 = self.obj.sql(
                "SELECT MAX(num_revision) FROM data_revision WHERE id_data = ?",
                [id_data]
            )
            out2 = self.obj.get(sql2)
            num_revision = out2[0][0]

            # GET LATEST FILE LINK
            sql3 = self.obj.sql(
                "SELECT name_file FROM data_revision WHERE id_data = ? AND num_revision = ?",
                [id_data, num_revision]
            )
            out3 = self.obj.get(sql3)
            for row_file in out3:
                name_file = row_file[0]
                if len(placefolder) == 0:
                    placefolder = pathlib.PurePath(name_file).name

                label_id = 'id_data = ' + str(id_data)
                # _/_/_/_/_/_/_/_/_/
                #  ADD NODE (ROW)
                self.node_add(
                    parent=iter,
                    name=None,
                    value=placefolder,
                    desc=None,
                    id=label_id
                )

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
        # 5. bool : Check (ToggleButton)
        self.treeviewcolumn_toggle(tree, 'check', 4)
        # 6. str : Dummy for padding right space
        self.treeviewcolumn_str(tree, '', 5)
        # 7. str : id for padding right space
        self.treeviewcolumn_str(tree, 'id', 6, False)

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

    # -------------------------------------------------------------------------
    #  TreeViewColumn for CellRenderToggle
    # -------------------------------------------------------------------------
    def treeviewcolumn_toggle(self, tree, title, col):
        cell = Gtk.CellRendererToggle()
        column = Gtk.TreeViewColumn()
        tree.append_column(column)
        column.set_title(title)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'active', col)
        column.set_resizable(False)
        # TEST
        cell.connect('toggled', self.on_chk_renderer_toggled)

    def on_chk_renderer_toggled(self, cell, path):
        print(cell.get_active())
        print(path)
        self[path][4] = not self[path][self.row['check']]

# ---
#  END OF PROGRAM
