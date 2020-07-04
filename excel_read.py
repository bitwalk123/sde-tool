import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pandas as pd


class ExcelSPC():
    def __init__(self, filename):
        self.filename = filename
        self.df = self.read()
        self.valid = self.check_valid_sheet()

    def read(self):
        return (pd.read_excel(self.filename, sheet_name=None))

    def check_valid_sheet(self):
        if 'Master' in self.df.keys():
            return(True)
        else:
            return(False)


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ファイル選択用ダイアログ")
        self.set_default_size(400, 0)

        box = Gtk.Box()
        self.add(box)

        but = Gtk.Button(label="ファイル選択")
        but.connect("clicked", self.on_file_clicked)
        box.pack_end(but, False, True, 0)

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title="ファイルの選択",
                                       parent=self,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL,
                           Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN,
                           Gtk.ResponseType.OK)
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("「開く」がクリックされました。")
            file_name = dialog.get_filename()
            print("ファイル「" + file_name + "」が選択されました。")

            sheets = ExcelSPC(file_name)
            #df = sheets.read()
            #print(df)
        elif response == Gtk.ResponseType.CANCEL:
            print("「キャンセル」がクリックされました。")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_xlsx = Gtk.FileFilter()
        filter_xlsx.set_name("Excel ファイル")
        filter_xlsx.add_pattern("*.xlsx")
        filter_xlsx.add_pattern("*.xlsm")
        dialog.add_filter(filter_xlsx)

        filter_sheet = Gtk.FileFilter()
        filter_sheet.set_name("スプレッドシート")
        filter_sheet.add_mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        dialog.add_filter(filter_sheet)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("全てのファイル")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
