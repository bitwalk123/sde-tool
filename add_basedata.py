# add basic data to db
import configparser
import os
import sqlite3

suppliers = [
    ['Techno Quartz Inc.', 'Harmony Tower, 32-2, Honcho 1-chome, Nakano-ku, Tokyo 164-0012, Japan'],
    ['Fujikin Incorporated', '2-3-2 Itachibori Nishi-ku, Osaka 550-0012, Japan'],
    ['Advantec Co.,Ltd.', '293-1 Minato, Saijo, Ehime 793-0046, Japan'],
    ['AGC Inc.', '1-5-1 Marunouchi, Chiyoda-ku, Tokyo 100-8405 Japan'],
    ['NHK Spring Co., Ltd.', '3-10 Fukuura, Kanazawa-ku, Yokohama, Japan'],
    ['NGK Insulators, Ltd.', '1 Maegata-cho, Handa, Aichi 475-0825'],
    ['HORIBA STEC, Co., Ltd.', '11-5 Hokodate-cho Kamitoba, Minami-ku, Kyoto 601-8116, Japan'],
    ['ISHIHARA CHEMICAL CO., LTD.', '5-26 Nishiyanagiwara-cho, Hyogo-ku, Kobe-shi, Hyogo 652-0806, Japan'],
    ['Greene, Tweed & Co. Japan', '12F PMO Tamachi 5-31-17 Shiba, Minato-ku Tokyo, 108-0014, Japan'],
    ['WATAKEN Co., Ltd.', '204 Onuma Nishikatsura, Minamitsuru-gun, Yamanashi 403-0022, Japan'],
    ['Kogadenki Co., Ltd.', '1-chōme-5-3 Higashiōi Shinagawa City, Tōkyō-to 140-0011, Japan'],
    ['OHKAWA CORPORATION', '2-11-20 Sakura-shinmachi, Setagaya, Tokyo, Japan 154-0015, Japan'],
    ['TODOROKI SANGYO CO., LTD.', '3 Chome-2-4 Keya, Fukui, 918-8550, Japan'],
]

parts = [
    ['1173-600-01', 'CHAMBER-PROC RV SPLIT FLOW INTREPID'],
    ['1114-201-01', 'VALVE-PNEU,2P,NC,PA,W-SEAL 1.125,DURABLE'],
    ['1132-521-01', 'VALVE-PNEU,3P,NC,PA,W-SEAL 1.125,DURABLE'],
    ['1198-171-01', 'VALVE-PNEU,2P,NC,PA,W-SEAL 1.125,DURABLE'],
    ['1198-176-01', 'VALVE-PNEU,3P,NC,PA,W-SEAL 1.125,DURABLE'],
]

projects = [
    ['1', '1', '1'],
    ['2', '2', '2'],
    ['2', '2', '3'],
    ['2', '2', '4'],
    ['2', '2', '5'],
]

CONF_FILEPATH = 'sde.conf'
config = configparser.ConfigParser()
config.read(CONF_FILEPATH, 'UTF-8')

config_db = config['Database']
dbname = config_db['DBNAME']

if not os.path.exists(dbname):
    print("no database exists!")
    exit(0)

con = sqlite3.connect(dbname)

cur = con.cursor()
cur.executemany("INSERT INTO supplier VALUES(NULL, ?, ?)", suppliers)
cur.executemany("INSERT INTO part VALUES(NULL, ?, ?)", parts)
cur.executemany("INSERT INTO project VALUES(?, ?, ?)", projects)
con.commit()
