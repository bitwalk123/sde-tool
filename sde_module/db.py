# -----------------------------------------------------------------------------
#  db.py --- database class for SDE Tool
# -----------------------------------------------------------------------------
import sqlite3

from . import dlg

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
            'CREATE TABLE supplier (id_supplier INTEGER PRIMARY KEY, name_supplier TEXT NOT NULL)',
            'CREATE TABLE address (id_address INTEGER PRIMARY KEY, id_supplier INTEGER, name_site TEXT, name_address TEXT, num_telephone TEXT, num_facsimile TEXT, url TEXT)',
            'CREATE TABLE part (id_part INTEGER PRIMARY KEY, num_part TEXT NOT NULL, description TEXT, name_product TEXT)',
            'CREATE TABLE part_revision (id_revision INTEGER PRIMARY KEY, id_part INTEGER, num_revision INTEGER, name_file TEXT)',
            'CREATE TABLE project (id_project INTEGER, id_supplier INTEGER, id_part INTEGER, name_owner TEXT)',
            'CREATE TABLE stage (id_stage INTEGER PRIMARY KEY, name_stage TEXT)',
            'CREATE TABLE data (id_data INTEGER PRIMARY KEY, id_project INTEGER, id_stage INTEGER, placefolder TEXT)',
            'CREATE TABLE data_revision (id_revision INTEGER PRIMARY KEY, id_data INTEGER, num_revision INTEGER, name_file TEXT)',
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
        dialog = dlg.ok(self.parent, "New database", text)
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
