#!/usr/bin/env python
# coding: utf-8
import sqlite3


# =============================================================================
#  SqlDB - handle Database
# =============================================================================
class SqlDB():
    dbname: str = None

    def __init__(self, dbname):
        self.dbname = dbname

    # -------------------------------------------------------------------------
    #  initialize database
    # -------------------------------------------------------------------------
    def init(self):
        init_sql = [
            'CREATE TABLE part (id_part INTEGER PRIMARY KEY, id_part_orig INTEGER, id_supplier INTEGER, num_part TEXT NOT NULL UNIQUE, description TEXT, name_product TEXT)',
            'CREATE TABLE drawing (id_drawing INTEGER PRIMARY KEY, id_part INTEGER, id_rev INTEGER, drawing NONE)',
            'CREATE TABLE supplier (id_supplier INTEGER PRIMARY KEY, name_supplier_short TEXT NOT NULL UNIQUE, name_supplier TEXT, name_supplier_local TEXT)',
        ]
        stages = [
            ['CA'],  # 1
            ['Training'],  # 2
            ['PFD'],  # 3
            ['PFMEA'],  # 4
            ['Control Plan'],  # 5
            ['OCAP'],  # 8
            ['MSA'],  # 6
            ['SPC'],  # 7
            ['SCAR'],  # 9
            ['FAI'],  # 10
            ['Others'],  # 11
        ]

        con = sqlite3.connect(self.dbname)
        cur = con.cursor()

        for sql in init_sql:
            cur.execute(sql)

        # cur.executemany("INSERT INTO stage VALUES(NULL, ?)", stages)
        con.commit()
        con.close()

    # -------------------------------------------------------------------------
    #  put
    #  execute SQL
    #
    #  argument:
    #    sql : SQL statement
    # -------------------------------------------------------------------------
    def put(self, sql):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    # -------------------------------------------------------------------------
    #  get
    #  query with SQL
    #
    #  argument:
    #    sql : SQL statement
    #
    #  return
    #    out : matrix of output
    # -------------------------------------------------------------------------
    def get(self, sql):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        cur.execute(sql)
        out = cur.fetchall()
        con.close()
        return out

    # -------------------------------------------------------------------------
    #  sql
    #  create sql replacing ?s by parameters
    #
    #  argument:
    #    sentense   : SQL statement with ?s
    #    parameters : parameters to replace
    #
    #  return
    #    sentense : full SQL replaced with parameters
    # -------------------------------------------------------------------------
    def sql(self, sentense, parameters):
        for param in parameters:
            sentense = sentense.replace('?', str(param), 1)
        return sentense
