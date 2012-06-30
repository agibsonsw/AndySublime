import sublime_plugin
from os import path
from operator import itemgetter
from datetime import datetime

# Lists open files in a quick panel for jumping to, 
# ordered alphabetically or by modified date: index, 0, for alphabetical.
#    { "keys": ["ctrl+alt+x"], "command": "ordered_files", "args": { "index": 0 }  },
#    { "keys": ["ctrl+alt+c"], "command": "ordered_files", "args": { "index": 2 }  },
# Does not work with different groups, windows, or unsaved views (although it could 
# be modified so that it does).

class OrderedFilesCommand(sublime_plugin.WindowCommand):
	def run(self, index):
		OF = OrderedFilesCommand
		OF.file_views = []
		win = self.window
		for vw in win.views():
			if vw.file_name() is not None:
				_, tail = path.split(vw.file_name())
				modified = path.getmtime(vw.file_name())
				OF.file_views.append((tail, vw, modified))
			else:
				pass		# leave new/untitled files (for the moment)
		if index == 0:		# sort by file name (case-insensitive)
			OF.file_views.sort(key = lambda (tail, _, Doh): tail.lower())
			win.show_quick_panel([x for (x, y, z) in OF.file_views], self.on_chosen)
		else:				# sort by modified date (index == 2)
			OF.file_views.sort(key = itemgetter(2))
			win.show_quick_panel([
				(datetime.fromtimestamp(z)).strftime("%d-%m-%y %H:%M ") + x \
				for (x, y, z) in OF.file_views], self.on_chosen)
	def on_chosen(self, index):
		if index != -1:
			self.window.focus_view(OrderedFilesCommand.file_views[index][1])