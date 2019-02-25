#!/usr/bin/env python3

# This module is the Terminal User Interface for Title Keys
#   IT drive FunKiiU for easy game install
# [STATE]   : POC ( Functionnal )
# [AUTHOR]  : bignos@gmail.com
#

# coding=utf-8

__VERSION__ = 0.1

import npyscreen
import os

from modules import transform2JSON  # Local module import to load data from JSON file


# -[ Consts ]-
funkiiu_exec = './FunKiiU.py'

# -[ Variables ]-
cl_install_with_ticket = ''
cl_install_without_ticket = ''

# -[ Class ]-
class TUI(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name='Title Keys TUI')

class MainForm(npyscreen.FormBaseNew):
    # Constructor
    def create(self):
        y, x = self.useable_space()
        left_panel_max_width = (3*x)//4

        self.add(npyscreen.TitleFixedText,\
                name = "[Games]",\
                width = 20)

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

        right_panel_y_base = -(y -2)
        right_panel_x = -((x - left_panel_max_width) - 2)
        
        self.add(npyscreen.TitleFixedText,\
                name = "[Search]",\
                relx = right_panel_x,\
                rely = right_panel_y_base)

        self.search_name = self.add(npyscreen.TitleText,\
                name = "Name:",\
                value = "",\
                begin_entry_at=10,\
                relx = right_panel_x,\
                rely = right_panel_y_base + 2)
        self.search_name.when_value_edited = self._update_grid

        self.search_region = self.add(npyscreen.TitleSelectOne,\
                name = "Region:",\
                values = ['No Filter','EUR', 'USA'],\
                value = [0],\
                height = 4,\
                begin_entry_at=10,\
                relx = right_panel_x,\
                rely = right_panel_y_base + 4)
        self.search_region.when_value_edited = self._update_grid

        self.search_type = self.add(npyscreen.TitleSelectOne,\
                name = "Type:",\
                values = ['No Filter', 'eShop/Application', 'DLC', 'Patch', 'System Application', 'Unknown'],\
                value = [0],\
                height = 6,\
                begin_entry_at=10,\
                relx = right_panel_x,\
                rely = right_panel_y_base + 8)
        self.search_type.when_value_edited = self._update_grid

        self.btn_install = self.add(npyscreen.ButtonPress,\
                name = '<Install>',\
                when_pressed_function = self._do_install,\
                relx = -30,\
                rely = -3)

        self.btn_quit = self.add(npyscreen.ButtonPress,\
                name = '<Quit>',\
                when_pressed_function = self._do_exit,\
                relx = -16,\
                rely = -3)

        self.console.values = []

        self.add_handlers({
            "^Q" : self.when_exit,
            "i"  : self.when_install
            })
        self.grid.add_handlers({
            ' '  : self.when_selected
            })

        self.title_list = transform2JSON.WiiUTitlekeyList.loadFromJSON(transform2JSON.wiiu_title_key_json)
        self.selected_values = []
        self._update_grid()

    def when_selected(self, inpt):
        selected_line = self.grid.edit_cell[0]
        if self.sorted_title_keys[selected_line] not in self.selected_values:
            self.selected_values.append(self.sorted_title_keys[selected_line])
            self.console.values.append([self.sorted_title_keys[selected_line].name,\
                    self.sorted_title_keys[selected_line].region,\
                    self.sorted_title_keys[selected_line].ttype])
            self.console.update()

    def when_install(self, inpt):
        self._do_install()

    def when_exit(self, inpt):
        self._do_exit()

    # -[ Private ]-

    def _update_grid(self):
        self.grid.values = []
        self.sorted_title_keys = []
        for title_key in sorted(self.title_list.wii_u_title_key_list, key=lambda tk: tk.name):
            if title_key.key != ''\
            and title_key.name != ''\
            and title_key.name.find('(Event Preview)')\
            and title_key.ttype != 'Demo'\
            and title_key.region != 'JPN':
                if self._add_if_ok(title_key):
                    self._add_value_to_grid(title_key)
        self.grid.update()
        if self.grid.edit_cell:
            self.grid.edit_cell[0] = 0
            self.grid.ensure_cursor_on_display_up()

    def _add_value_to_grid(self, title_key):
        self.grid.values.append([title_key.name, title_key.region, title_key.ttype, title_key.ticket])
        self.sorted_title_keys.append(title_key)

    def _add_if_ok(self, title_key):
        if self.search_name.value != '' and title_key.name.lower().find(self.search_name.value.lower()) == -1:
            return False
        if self.search_region.value[0] != 0 and title_key.region != self.search_region.values[self.search_region.value[0]]:
            return False
        if self.search_type.value[0] != 0 and title_key.ttype != self.search_type.values[self.search_type.value[0]]:
            return False

        return True

    def _do_install(self):
        global cl_install_without_ticket, cl_install_with_ticket
        if len(self.selected_values) == 0:
            npyscreen.notify_confirm('The install list is empty', title= 'WARNING')
            return
        key_list = []
        key_with_ticket = []
        key_without_ticket = []
        for title_key in self.selected_values:
            if title_key.ticket:
                key_with_ticket.append(title_key.tid)
            else:
                key_without_ticket.append(title_key.tid)
        if len(key_with_ticket) > 0:
            cl_install_with_ticket = '{} -title {} -onlinetickets'.format(funkiiu_exec, ' '.join(key_with_ticket))
        if len(key_without_ticket) > 0:
            cl_install_without_ticket = '{} -title {} -onlinekeys'.format(funkiiu_exec, ' '.join(key_without_ticket))
        self._do_exit()

    def _do_exit(self):
        self.parentApp.switchForm(None)

if __name__ == '__main__':
    app = TUI()
    app.run()
    if cl_install_with_ticket != '':
        os.system(cl_install_with_ticket)
    if cl_install_without_ticket != '':
        os.system(cl_install_without_ticket)
