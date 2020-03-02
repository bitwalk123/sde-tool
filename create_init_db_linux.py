# create initial db
import configparser
import os
import sqlite3

suppliers = [
    ['Techno Quartz Inc.', 'Harmony Tower, 32-2, Honcho 1-chome, Nakano-ku, Tokyo 164-0012, Japan'],        # 1
    ['Fujikin Incorporated', '2-3-2 Itachibori Nishi-ku, Osaka 550-0012, Japan'],                           # 2
    ['Advantec Co.,Ltd.', '293-1 Minato, Saijo, Ehime 793-0046, Japan'],                                    # 3
    ['AGC Inc.', '1-5-1 Marunouchi, Chiyoda-ku, Tokyo 100-8405 Japan'],                                     # 4
    ['NHK Spring Co., Ltd.', '3-10 Fukuura, Kanazawa-ku, Yokohama, Japan'],                                 # 5
    ['NGK Insulators, Ltd.', '1 Maegata-cho, Handa, Aichi 475-0825'],                                       # 6
    ['Horiba Stec, Co., Ltd.', '11-5 Hokodate-cho Kamitoba, Minami-ku, Kyoto 601-8116, Japan'],             # 7
    ['Ishihara Chemical Co., Ltd.', '5-26 Nishiyanagiwara-cho, Hyogo-ku, Kobe-shi, Hyogo 652-0806, Japan'], # 8
    ['Greene, Tweed & Co. Japan', '12F PMO Tamachi 5-31-17 Shiba, Minato-ku Tokyo, 108-0014, Japan'],       # 9
    ['Wataken Co., Ltd.', '204 Onuma Nishikatsura, Minamitsuru-gun, Yamanashi 403-0022, Japan'],            # 10
    ['Kogadenki Co., Ltd.', '1-chōme-5-3 Higashiōi Shinagawa City, Tōkyō-to 140-0011, Japan'],              # 11
    ['Ohkawa Corporation', '2-11-20 Sakura-shinmachi, Setagaya, Tokyo, Japan 154-0015, Japan'],             # 12
    ['Todoroki Sangyo Co., Ltd.', '3 Chome-2-4 Keya, Fukui, 918-8550, Japan'],                              # 13
    ['Toyo Tanso Co., Ltd.', '5-7-12 Takeshima, Nishiyodogawa-ku, Osaka 555-0011, Japan'],                  # 14
    ['Nikkoshi Co., Ltd.', 'Masonic 39MT building 10F, 2-4-5 Azabudai, Minato-ku, Tokyo 106-0041 Japan'],   # 15
    ['Alpha Tech Limited', '929-1 Sekiguchi, Atsugi, Kanagawa 243-0804'],                                   # 16
]

parts = [
    ['1173-600-01', 'CHAMBER-PROC RV SPLIT FLOW INTREPID', 'EPI Intrepid', '/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/Drawing/1173-600-01-c.pdf'],   # 1
    ['1114-201-01', 'VALVE-PNEU,2P,NC,PA,W-SEAL 1.125,DURABLE', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Fujikin/Drawing/1114-201-01-b.pdf'],    # 2
    ['1132-521-01', 'VALVE-PNEU,3P,NC,PA,W-SEAL 1.125,DURABLE', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Fujikin/Drawing/1132-521-01-b.pdf'],    # 3
    ['1198-171-01', 'VALVE-PNEU,2P,NC,PA,W-SEAL 1.125,DURABLE', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Fujikin/Drawing/Z01-D055-3622-000-00_1.pdf'],   # 4
    ['1198-176-01', 'VALVE-PNEU,3P,NC,PA,W-SEAL 1.125,DURABLE', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Fujikin/Drawing/Z01-D055-3624-000-00_1.pdf'],   # 5
    ['1028-706-01', 'LINE-GAS CV TO IGS-2', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Advantec/Drawing/1028-706-01-c.pdf'],   # 6
    ['2529696-01', 'SiC CARRIER 200mm-165 ATM-HT', 'A400', '/home/bitwalk/ドキュメント/Suppliers/AGC/Drawing/2529696-c1.pdf'],    # 7
    ['2608618-01', 'SiC CARRIER 200mm-165', 'A400', '/home/bitwalk/ドキュメント/Suppliers/AGC/Drawing/2608618-01-c.pdf'],         # 8
    ['2413353-01', 'SiC CARRIER 300mm-170', 'A400', '/home/bitwalk/ドキュメント/Suppliers/AGC/Drawing/2413353-a1.pdf'],           # 9
    ['1108-541-01', 'SiC PEDESTAL LPC POLY', 'A400', '/home/bitwalk/ドキュメント/Suppliers/AGC/Drawing/1108-541-01-b.pdf'],       # 10
    ['1159-986-01', '325 SUSCEPTOR HEATER 4NGM', 'PECVD XP8 300MM End product', '/home/bitwalk/ドキュメント/Suppliers/NHK Spring/Drawing/1159-986-01-A.pdf'],    # 11
    ['1189-059-01', 'SUSCEPTOR-LOW MASS TYPE IB ESA', 'EPI Intrepid', '/home/bitwalk/ドキュメント/Suppliers/Toyo Tanso/Drawing/1189-059-01-c.pdf'],   # 12
    ['1195-918-01', 'SUSCEPTOR-LOW MASS TYPE 2 A', 'EPI Intrepid', '/home/bitwalk/ドキュメント/Suppliers/Toyo Tanso/Drawing/1194-316-01-b.pdf'],      # 13
    ['1194-316-01', 'SUSCEPTOR-LOW MASS TYPE V B ESA', 'EPI Intrepid', '/home/bitwalk/ドキュメント/Suppliers/Toyo Tanso/Drawing/1195-918-01-b.pdf'],  # 14
    ['1039-622-01', 'TANK-VAPORIZER', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Horiba Stec/1039-622-01-b.pdf'],           # 15
    ['1126-248-01', 'TC SOCKET', 'PECVD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Ishihara Chemical/Drawing/1126-248-01-a.pdf'],  # 16
    ['1118-642-01', 'SEAL PLATE-VALVE, SLIT (40X310,BONDED)', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Green Tweed/Drawing/1118-642-01-b.pdf'], # 17
    ['1104-757-01', 'RIB-BODY B', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Wataken/Drawing/1104-757_JSC.pdf'],                    # 18
    ['1104-759-01', 'BLOCK-LOCATE PIN', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Wataken/Drawing/1104-759-01-a.pdf'],             # 19
    ['1121-870-01', 'ASE PLATE-SHD', 'Quarter Chamber Process Modules', '/home/bitwalk/ドキュメント/Suppliers/Wataken/Drawing/1121-870-01-a.pdf'],    # 20
    ['1135-490-01', 'RIB-SHD BASE PLATE E', 'Quarter Chamber Process Modules', '/home/bitwalk/ドキュメント/Suppliers/Wataken/Drawing/1135-490_JSC.pdf'],  # 21
    ['1099-308-01', 'SUPPORT-RF SHAFT', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Kogadenki/Drawing/1099-308-01-a.pdf'],   # 22
    ['1099-310-01', 'RF BAR-MAIN/RC', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Ohkawa/Drawing/1099-310-01-a.pdf'],    #23
    ['1180-535-01', 'SCREW M6', 'Quarter Chamber Process Modules', '/home/bitwalk/ドキュメント/Suppliers/Todoroki Sangyo/Drawing/pdr-d039-9969-000_JSC.pdf'], #24
    ['1071-550-01', 'ANODIZE-HEATER 1PHB', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/1071-550-01-a.pdf'],   #25
    ['1041-545-01', 'ANODIZE-HEATER 1PHB', 'PEALD XP8 300MM End product', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/1041-545-01-d.pdf'],   #26
    ['1065-389-01', 'SHOWER PLATE', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/1065-389-01-d.pdf'],   #27
    ['1072-669-01', 'SHOWER-PLATE', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/1072-669-01-c.pdf'],   #28
    ['1012-013-01', 'SHOWER PLATE', 'Eagle 12 Process Chamber', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/1012-013-01-b.pdf'],   #29
    ['1170-511-01', 'ASSY-SUSCEPTOR HEATER', 'CP Common', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d037-7106-000_JSC.pdf'],   #30
    ['1159-984-01', 'ASSY-SUSCEPTOR HEATER', 'PECVD XP8 300MM End product', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/1159-984-01-a.pdf'],   #31
    ['1192-930-01', 'ASSY-SUSCEPTOR HEATER', 'PECVD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d053-3868-000_JSC.pdf'],   #32
    ['1181-529-01', 'ASSY-SUSCEPTOR HEATER', 'PECVD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d050-0744-000_JSC.pdf'],   #33
    ['1183-950-01', 'SHOWER PLATE', 'PECVD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d050-8623-000_JSC.pdf'],   #34
    ['1194-379-01', 'SHOWER PLATE', 'PECVD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d054-3859-000_JSC.pdf'],   #35
    ['1198-167-01', 'SHOWER PLATE', 'PECVD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d055-3612-000_JSC.pdf'],   #36
    ['1198-168-01', 'SHOWER PLATE', 'PECVD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d055-3729-000_JSC.pdf'],   #37
    ['1115-388-01', 'SHOWER PLATE', 'PEALD XP8 300MM DCM', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/1115-388-01-c.pdf'],   #38
    ['1179-948-01', 'SHOWER-PLATE', 'Quarter Chamber Process Modules', '/home/bitwalk/ドキュメント/Suppliers/Nikkoshi/Drawing/pdr-d039-9030-000_JSC.pdf'],   #39
    ['D063-7425', 'CHAMBER-PROC RV SPLIT FLOW INTREPID', 'EPI Intrepid', '/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/Drawing/D063-7425.pdf'], # 40
]

# project
#   id_project
#   id_supplier
#   id_part
projects = [
    [1, 1, 1],
    [1, 1, 40],
    [2, 2, 2],
    [3, 2, 3],
    [4, 2, 4],
    [5, 2, 5],
    [6, 3, 6],
    [7, 4, 7],
    [8, 4, 8],
    [9, 4, 9],
    [10, 4, 10],
    [11, 5, 11],
    [12, 14, 12],
    [13, 14, 13],
    [14, 14, 14],
    [15, 7, 15],
    [16, 8, 16],
    [17, 9, 17],
    [18, 10, 18],
    [19, 10, 19],
    [20, 10, 20],
    [21, 10, 21],
    [22, 11, 22],
    [23, 12, 23],
    [24, 13, 24],
    [25, 15, 25],
    [26, 15, 26],
    [27, 15, 27],
    [28, 15, 28],
    [29, 15, 29],
    [30, 15, 30],
    [31, 15, 31],
    [32, 15, 32],
    [33, 15, 33],
    [34, 15, 34],
    [35, 15, 35],
    [36, 15, 36],
    [37, 15, 37],
    [38, 15, 38],
    [39, 15, 39],
]

stages = [
    ['CA / Audit'],     # 1
    ['Training'],       # 2
    ['PFD'],            # 3
    ['PFMEA'],          # 4
    ['Control Plan'],   # 5
    ['MSA'],            # 6
    ['SPC'],            # 7
    ['OCAP'],           # 8
    ['SCR'],            # 9
    ['FAI'],            # 10
    ['Others'],         # 11
]

# data
#   name_file
#   id_project
#   id_stage
data = [
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/1460 Form 1 Supplier Audit Report_Techno Quartz.doc', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/QA-A-A01-044 ASM Audit Evidence_Techno Quartz_08112019.pdf', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/QA-A-A01-046-01 ASM ATM Chamber Process Flow 12112019.pdf', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/QA-A-A01-046-02 ASM ATM Chamber Process Flow 02042020.pdf', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/QA-A-A01-047 ASM Audit Evidence_Flame polish & welding_Techno Quartz_13112019.pdf', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/1460 Form 2 Supplier Audit Finding and Corrective Action Report_TQ.xlsx', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/1460 Form 2 Supplier Audit Finding and Corrective Action Report_TQ reply at Jan\'20.xlsx', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/1460 Form 2 Supplier Audit Finding and Corrective Action Report_TQ reply at Feb\'20.xlsx', 1, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/ASM CE_for_Suppliers_Sep 2019.pdf', 1, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/ASM MSA_Rev.3.7.pdf', 1, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/ASM SPC_Rev.2.1(J)_PSQA-CS18-030.pdf', 1, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/ASM SPC Macro Manual.pdf', 1, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/ASM Control Plan and OCAP(J) Rev.B.pdf', 1, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/Process_flow_20200129.pdf', 1, 3],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/TQ_MSA.xlsx', 1, 6],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/TQ_MSA_result + additional 600mm.xlsx', 1, 6],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/TQ_MSA_result_S006_X.pdf', 1, 6],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/TQ_MSA_result_S006_Y.pdf', 1, 6],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/TQ_MSA_result_S006_Z.pdf', 1, 6],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/TQ_MSA_result.xlsx', 1, 6],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/127 Form 1 Supplier Change Request TQ 1202-997-01_02062020.doc', 1, 9],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/TQ FAI Timeline.xlsx', 1, 10],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/Breakage Report 01152020.pptx', 1, 11],
    ['/home/bitwalk/ドキュメント/Suppliers/Techno Quartz/Breakage Report 01152020.pdf', 1, 11],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/130 Form 4a Supplier Capability Assessment (Fujikin Japan).xlsx', 2, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/FujikinCapability Assessment.pptx', 2, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/168 Form 3 Supplier Audit Finding and CA Report - Fujikin Tsukuba.xlsx', 2, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/168 Form 3 Supplier Audit Finding and CA Report (open) Fujikin Tsukuba.xlsx', 2, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/168 Form 3 Supplier Audit Finding and CA Report ((open) 4 Feb 20) Fujikin Tsukuba.xlsx', 2, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/168 Form 3 Supplier Audit Finding and CA Report (open 5 Feb 20) Fujikin Tsukuba.xlsx', 2, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/190531 GP 407 Supplier Quality Requirements Policy.pdf', 2, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/Z01-D051-3766-000-02_1.pdf', 2, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/Z01-D052-2333-000-00_1.pdf', 2, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/140624 FCST1000MPD_QCFlow_Rev1.pdf', 2, 3],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/TQ31-2001311_1(QCFlow_ASM_NHSD_English).pdf', 2, 3],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/TQ31-2001312_1_P-FMEA_FPR-NHSD-20-6.35UGC-PA-AMN.pdf', 2, 4],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/Agneda_Fujikin_20200117.pdf', 2, 11],
    ['/home/bitwalk/ドキュメント/Suppliers/Fujikin/TBKT200117-1_1_minutes.pdf', 2, 11],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/130 Form 4A (Supplier Capability Assessment (Advantec)_ audit.xlsx', 6, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/168 Form 3 Supplier Audit Finding and CAR Open.xlsx', 6, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/ASM PCS Training attendance (Advantec).pdf', 6, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/ASM PFMEA_Rev.3.3a.pptx', 6, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/GP_377_Supply_Chain_Process_Control_System_Engagement.pdf', 6, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/GP_407_Supplier_Quality_Requirements_Policy.pdf', 6, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/Process Flow Diagram.pdf', 6, 3],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/Advantec  PFMEA.xlsx', 6, 4],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/Advantec  PFMEA revew.xlsx', 6, 4],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/Gas Line PFMEA RevA.pdf', 6, 4],
    ['/home/bitwalk/ドキュメント/Suppliers/Advantec/Advantec gas piping evaluation results(20131129).pptx', 6, 11],
    ['/home/bitwalk/ドキュメント/Suppliers/AGC/AGC evidence/General_4.0_QCflow.pdf', 7, 3],
    ['/home/bitwalk/ドキュメント/Suppliers/AGC/First Article Submission by Suppliers to ASM 190606.pptx', 7, 10],
    ['/home/bitwalk/ドキュメント/Suppliers/NHK Spring/130 Form 4A (Supplier Capability Assessment_Heater)_NHKSpring_6.2.18.xlsx', 8, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/NHK Spring/130 Form 4a Supplier Capability Assessment_NHK Spring 20200130.xlsx', 8, 1],
    ['/home/bitwalk/ドキュメント/Suppliers/NHK Spring/03 ASM Control Plan and OCAP Training Rev B.pdf', 8, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/NHK Spring/04 ASM MSA_Rev.3.7.pptx', 8, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/NHK Spring/ASMSPCMacroRev2.0.xlsm', 8, 2],
    ['/home/bitwalk/ドキュメント/Suppliers/NHK Spring/NHKSpringSPC20200204Rev2.0.xlsm', 8, 7],
]
# read config file
CONF_FILEPATH = 'sde.conf'
config = configparser.ConfigParser()
config.read(CONF_FILEPATH, 'UTF-8')

config_db = config['Database']
dbname = config_db['DBNAME']

# delete database if exists
if os.path.exists(dbname):
    os.remove(dbname)

# create database
con = sqlite3.connect(dbname)

cur = con.cursor()
# create tables
cur.execute("CREATE TABLE supplier (id_supplier INTEGER PRIMARY KEY, name_supplier TEXT NOT NULL, address TEXT)")
cur.execute("CREATE TABLE part (id_part INTEGER PRIMARY KEY, num_part TEXT NOT NULL, description TEXT, name_product TEXT, name_file TEXT)")
cur.execute("CREATE TABLE project (id_project INTEGER, id_supplier INTEGER, id_part INTEGER)")
cur.execute("CREATE TABLE stage (id_stage INTEGER PRIMARY KEY, name_stage TEXT)")
cur.execute("CREATE TABLE data (id_data INTEGER PRIMARY KEY, name_file TEXT, id_project INTEGER, id_stage INTEGER)")
# insert initial data
cur.executemany("INSERT INTO supplier VALUES(NULL, ?, ?)", suppliers)
cur.executemany("INSERT INTO part VALUES(NULL, ?, ?, ?, ?)", parts)
cur.executemany("INSERT INTO project VALUES(?, ?, ?)", projects)
cur.executemany("INSERT INTO stage VALUES(NULL, ?)", stages)
cur.executemany("INSERT INTO data VALUES(NULL, ?, ?, ?)", data)
con.commit()
con.close()
