import sqlite3


# -------------------------------------------------------------------------
#  handle Database
# -------------------------------------------------------------------------
class SqlDB():
    dbname: str = None

    def __init__(self, dbname):
        self.dbname = dbname

    # -------------------------------------------------------------------------
    #  initialize database
    # -------------------------------------------------------------------------
    def init(self):
        init_sql = [
            'CREATE TABLE part (id_part INTEGER PRIMARY KEY, num_part TEXT NOT NULL, description TEXT, name_product TEXT)',
            'CREATE TABLE drawing (id_drawing INTEGER PRIMARY KEY, id_part INTEGER, id_rev INTEGER, drawing NONE)',
            'CREATE TABLE supplier (id_supplier INTEGER PRIMARY KEY, name_supplier_short TEXT NOT NULL, name_supplier TEXT, name_supplier_jp TEXT)',
            'CREATE TABLE part_supplier (id_part_supplier INTEGER PRIMARY KEY, id_part INTEGER, id_supplier INTEGER)',
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

        #cur.executemany("INSERT INTO stage VALUES(NULL, ?)", stages)
        con.commit()
        con.close()
