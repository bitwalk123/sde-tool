import pandas as pd


class SPC():
    filename = None
    sheets = None
    valid = False

    def __init__(self, filename):
        self.filename = filename
        self.sheets = self.read(filename)
        self.valid = self.check_valid_sheet(self.sheets)

        # aggregation
        #df = self.sheets['Master']
        #self.aggregate(df)

    def aggregate(self, df_master):
        # drop row if column 'Part Number' is NaN
        df_master = df_master.dropna(subset=['Part Number'])
        print(df_master)
        for row in df_master.values:
            print(row[0])

    def check_valid_sheet(self, sheets):
        # check if 'Master' tab exists
        if 'Master' in sheets.keys():
            return True
        else:
            return False

    def get_sheets(self):
        return self.sheets

    def read(self, filename):
        # read specified filename as Excel file including all tabs
        return pd.read_excel(filename, sheet_name=None)
