#!/usr/bin/env python3

# This module is the Terminal User Interface for Title Keys
# [STATE]   : POC ( Development )
# [AUTHOR]  : bignos@gmail.com
#

# coding=utf-8
import curses
import npyscreen
import sys

from modules import transform2JSON  # Local module import to load data from JSON file


class TUI(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name='Title Keys TUI')

class MainForm(npyscreen.FormBaseNew):
    # Constructor
    def create(self):
        y, x = self.useable_space()
        left_panel_max_width = (3*x)//4

        self.add(npyscreen.TitleFixedText,\
                name = "[Games list]")

        self.grid = self.add(npyscreen.GridColTitles,\
                col_titles=['Name','Region','Type','Ticket'],\
                select_whole_line=True,\
                max_width=left_panel_max_width,\
                max_height=((3*y) // 5))

        self.add(npyscreen.TitleFixedText,\
                name = "[Install]",\
                rely = -(y - ((3*y) // 5) - 4) )

        self.console = self.add(npyscreen.GridColTitles,\
                col_titles=['Name', 'Region', 'Type'],\
                max_width=left_panel_max_width)
        
        self.add(npyscreen.TitleFixedText,\
                name = "[Search]",\
                relx = -((x - left_panel_max_width) - 2),\
                rely = -(y - 2))

        self.console.values = []

        self.add_handlers({
            "^Q" : self.when_exit,
            })
        self.grid.add_handlers({
            ' '  : self.when_selected
            })

        self.title_list = transform2JSON.WiiUTitlekeyList.loadFromJSON(transform2JSON.wiiu_title_key_json)
        self.grid.values = []
        self.sorted_title_keys = []
        self.selected_values = []
        for title_key in sorted(self.title_list.wii_u_title_key_list, key=lambda tk: tk.name):
            if title_key.key != ''\
            and title_key.name != ''\
            and title_key.name.find('(Event Preview)')\
            and title_key.ttype != 'Demo'\
            and title_key.region != 'JPN':
                self.grid.values.append([title_key.name, title_key.region, title_key.ttype, title_key.ticket])
                self.sorted_title_keys.append(title_key)

        self.selected = []

    def when_selected(self, inpt):
        selected_line = self.grid.edit_cell[0]
        if self.sorted_title_keys[selected_line] not in self.selected_values:
            self.selected_values.append(self.sorted_title_keys[selected_line])
            self.console.values.append([self.sorted_title_keys[selected_line].name,\
                    self.sorted_title_keys[selected_line].region,\
                    self.sorted_title_keys[selected_line].ttype])
            self.console.display()

    def when_exit(self, inpt):
        # self.parentApp.setNextForm(None)
        sys.exit(0)

if __name__ == '__main__':
    app = TUI()
    app.run()
