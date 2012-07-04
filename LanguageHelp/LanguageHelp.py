import sublime, sublime_plugin
import subprocess

# Will open a .chm help file for the function under the cursor (Windows only). The same 
# key-binding can be used (currently for PHP, JavaScript and jQuery) because the command 
# will determine the current syntax.
# Only for standard functions (currently) - not classes/methods, etc.
# You will need to obtain/download a .chm for each language and modify the path in the 
# code that follows.
# 
#     { "keys": ["ctrl+f1"], "command": "language_help" },
# The file hh.exe (or a more recent alternative) needs to be available on your Windows 
# environment-path(s).

# Requires the file 'PyHelp.py' for Python help - which doesn't use a .chm and displays 
# in an output panel. (Edit this file as indicated if this file is not available or required).
PHP_HELP = \
"""hh.exe mk:@MSITStore:C:\\Windows\\Help\\php_enhanced_en.chm::/res/function.%(func)s.html"""
JS_HELP = \
"""hh.exe mk:@MSITStore:C:\\Windows\\Help\\javascript.chm::/jsref_%(func)s.htm"""
jQuery_HELP = \
"""hh.exe mk:@MSITStore:C:\Windows\Help\jQuery-UI-Reference-1.7.chm::/api/%(func)s.htm"""

class LanguageHelpCommand(sublime_plugin.TextCommand):
    proc1 = None
    def run(self, edit):
        curr_view = self.view
        curr_sel = curr_view.sel()[0]
        if curr_view.match_selector(curr_sel.begin(), 'source.php'):
            source = 'PHP'
        elif curr_view.match_selector(curr_sel.begin(), 'source.js.jquery'):
            source = 'JQUERY'
        elif curr_view.match_selector(curr_sel.begin(), 'source.js'):
            source = 'JS'
        # Delete the following 3 lines if the file 'PyHelp.py' is not available:
        elif curr_view.match_selector(curr_sel.begin(), 'source.python'):
            self.view.run_command("py_help")
            return
        else:
            return

        word_end = curr_sel.end()
        if curr_sel.empty():
            word = curr_view.substr(curr_view.word(word_end)).lower()
        else:
            word = curr_view.substr(curr_sel).lower()
        if word is None or len(word) <= 1:
            sublime.status_message('No function selected')
            return
        if source == 'PHP':
            word = word.replace('_', '-')
            HELP = PHP_HELP % { "func": word }
        elif source == 'JQUERY':
            HELP = jQuery_HELP % { "func": word }
        elif source == 'JS':
            HELP = JS_HELP % { "func": word }
        try:
            if self.proc1 is not None:
                self.proc1.kill()
        except Exception:
            pass
        self.proc1 = subprocess.Popen(HELP, shell=False)