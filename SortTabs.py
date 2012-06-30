import sublime_plugin
from os import path
from operator import itemgetter

# A simple command to sort current tabs alphabetically (returning focus to the 
# original tab).
# Does not work with different groups or windows. Not catered for unsaved views 
# (although it seems to work okay if there are any). It could be modified to 
# work in these circumstances.
#   { "keys": ["ctrl+alt+b"], "command": "sort_tabs" },
class SortTabsCommand(sublime_plugin.WindowCommand):
	def run(self):
		file_views = []
		win = self.window
		curr_view = win.active_view()
		for vw in win.views():
			_, tail = path.split(vw.file_name() or path.sep)
			group, _ = win.get_view_index(vw)
			file_views.append((tail.lower(), vw, group))
		file_views.sort(key = itemgetter(2, 0))
		moving_index = 0
		for index, (_, vw, group) in enumerate(file_views):
			if index == 0 or group > prev_group:
				moving_index = 0
				prev_group = group
			else:
				moving_index += 1
			win.set_view_index(vw, group, moving_index)
		win.focus_view(curr_view)