#!/usr/bin/env python3

# This module is the Terminal User Interface for Title Keys
# [STATE]   : POC ( Development )
# [AUTHOR]  : bignos@gmail.com
#

# coding=utf-8
import npyscreen

from modules import transform2JSON  # Local module import to load data from JSON file

class TUI(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name='Title Keys TUI')

class MainForm(npyscreen.ActionForm):
    # Constructor
    def create(self):
        # self.add(npyscreen.SimpleGrid, )
        # self.add(npyscreen.GridColTitles, relx = 42, rely=15, width=20, col_titles = ['1','2','3','4'])
        grid = self.add(npyscreen.GridColTitles, col_titles = ['Name','Region','Type','Ticket'], column_width=20)
        self.title_list = transform2JSON.WiiUTitlekeyList.loadFromJSON(transform2JSON.wiiu_title_key_json)
        grid.values = []
        for title_key in self.title_list.wii_u_title_key_list:
            grid.values.append([title_key.name, title_key.region, title_key.ttype, title_key.ticket])

    def on_ok(self):
        self.parentApp.switchForm(None)

if __name__ == '__main__':
    app = TUI()
    app.run()
