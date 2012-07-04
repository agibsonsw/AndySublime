import sublime, sublime_plugin
# Works for standard functions and methods.
# Assign a key-binding such as Shift-F1.
# Click into a function or method and press Shift-F1.
# Help will be displayed in an output panel.
# Un-commment the timeout if you wish the panel to disappear after an interval.
class PyHelpCommand(sublime_plugin.TextCommand):
    py_types = (None, 'complex', 'dict', 'file', 'float', 'frozenset',
        'int', 'list', 'long', 'set', 'str', 'tuple', 'unicode', 'xrange',
        'bytearray', 'buffer', 'memoryview', '__builtins__', 'object')
    def run(self, edit):
        curr_view = self.view
        if not curr_view.match_selector(0, 'source.python'): return
        word_end = curr_view.sel()[0].end()
        if curr_view.sel()[0].empty():
            word = curr_view.substr(curr_view.word(word_end)).lower()
        else:
            word = curr_view.substr(curr_view.sel()[0]).lower()
        if word is None or len(word) <= 1:
            sublime.status_message('No word selected')
            return

        libs = curr_view.find_all('^((?:from|import).*$)')
        for lib in libs:
            try:
                exec(curr_view.substr(lib))
            except Exception:
                pass
                
        for obj in PyHelpCommand.py_types:
            try:
                if obj is None:
                    help_text = eval(word + '.__doc__')
                else:
                    help_text = eval(obj + '.' + word + '.__doc__')
                if help_text is not None:
                    self.display_help(help_text)
                    return
            except:
                pass
        line_region = curr_view.line(word_end)
        line_begin = line_region.begin()
        context = curr_view.find('[a-z_0-9\.\(\)]*' + word, line_begin, sublime.IGNORECASE)
        found_txt = curr_view.substr(context)
        try:
            help_text = eval(found_txt + '.__doc__')
        except Exception:
            help_text = None
        if help_text is not None:
            self.display_help(help_text)
        else:
            sublime.status_message('No help available')

    def display_help(self, help_text):
        win = sublime.active_window()
        the_output = win.get_output_panel('help_panel')
        the_output.set_read_only(False)
        edit = the_output.begin_edit()
        the_output.insert(edit, the_output.size(), help_text)
        the_output.end_edit(edit)
        the_output.set_read_only(True)
        win.run_command("show_panel", {"panel": "output." + "help_panel"})
        # sublime.set_timeout(self.hide_help, 5000)

    def hide_help(self):
        sublime.active_window().run_command("hide_panel", {"panel": "output." + "help_panel"})