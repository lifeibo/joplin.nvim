#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim

token = vim.vars.get('joplin_token', b'')
url = vim.vars.get('joplin_url', b'http://127.0.0.1:41184')
window_width = vim.vars.get('joplin_window_width', 30)
icon_open = vim.vars.get('joplin_icon_open', b'-').decode()
icon_close = vim.vars.get('joplin_icon_close', b'+').decode()
icon_todo = vim.vars.get('joplin_icon_todo', b'[ ]').decode()
icon_completed = vim.vars.get('joplin_icon_completed', b'[x]').decode()
icon_note = vim.vars.get('joplin_icon_note', b'').decode()
pin_todo = vim.vars.get('joplin_pin_todo', 1)
hide_completed = vim.vars.get('joplin_hide_completed', 0)
folder_order_by = vim.vars.get('joplin_notebook_order_by', b'title').decode()
folder_order_desc = vim.vars.get('joplin_notebook_order_desc', 0)
note_order_by = vim.vars.get('joplin_note_order_by', b'updated_time').decode()
note_order_desc = vim.vars.get('joplin_note_order_desc', 0)
number = vim.vars.get('joplin_number', 0)
relativenumber = vim.vars.get('joplin_relativenumber', 0)
map_note_info = vim.vars.get('joplin_map_note_info', b'').decode()
map_note_type_switch = vim.vars.get('joplin_map_note_type_switch',
                                    b'').decode()
map_todo_completed_switch = vim.vars.get('joplin_map_todo_completed_switch',
                                         b'').decode()
map_tag_add = vim.vars.get('joplin_map_tag_add', b'').decode()
map_tag_del = vim.vars.get('joplin_map_tag_del', b'').decode()
map_resrouce_attach = vim.vars.get('joplin_map_resource_attach', b'').decode()
map_link_resource = vim.vars.get('joplin_map_link_resource', b'').decode()
map_link_node = vim.vars.get('joplin_map_link_node', b'').decode()
