# coding=utf8
import sublime
import sublime_plugin
import os
import subprocess
from os.path import basename

installed_dir = os.path.basename(os.getcwd())

'''
    Global function to send system messages
'''


def msg(msg):
    print "[PHP Refactor] %s" % msg


def shellquote(s):
    return "\"" + s.replace("\"", "\\\"") + "\""

'''
    Plugin preferences
'''


class Prefs:

    @staticmethod
    def load():
        settings = sublime.load_settings('sublime-text-2-php-refactor.sublime-settings')
        Prefs.backup = settings.get('backup')
        msg("Backup file before applying changes? %s" % Prefs.backup)
        Prefs.confirm = settings.get('confirm')
        msg("Confirm action before applying changes? %s" % Prefs.confirm)
        Prefs.path_to_php = settings.get('path_to_php') if settings.get('path_to_php') else 'php'


Prefs.load()


'''
    Top level class for the plugin commands
'''


class Refactor():
    REFACTOR = shellquote(os.path.normpath(sublime.packages_path() + os.sep + installed_dir + os.sep + "lib" + os.sep + "refactor.phar"))

    def execute(self, name, command, execute=False):

        msg('Executing: ' + name + ' (' + command + ')')

        p = subprocess.Popen(command, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        if p.stdout is not None:
            text = p.stdout.readlines()
            text = '\n'.join(text)
            if (False == execute):
                fileName = basename(self.view.file_name())
                title = name + '_' + fileName + '.diff'
                self.view_in_tab(title, text)
            else:
                msg(text)
                self.view.run_command('revert')

    def view_in_tab(self, title, text, syntax='Diff'):
        # Helper function to display information in a tab.
        tab = self.view.window().new_file()
        _id = tab.buffer_id()
        tab.set_name(title)
        tab.set_scratch(_id)
        tab.settings().set('gutter', True)
        tab.settings().set('line_numbers', False)
        tab.set_syntax_file('Packages/' + syntax + '/' + syntax + '.tmLanguage')
        ed = tab.begin_edit()
        tab.insert(ed, 0, text)
        tab.end_edit(ed)
        return tab, _id

    def confirm(self, on_confirm):
        window = sublime.active_window()
        backup = 'Off'
        if (True == Prefs.backup):
            backup = 'On'

        yes = []
        yes.append('Yes, apply patch.')
        yes.append('Backups are: ' + backup)

        no = []
        no.append("No, don't apply patch")
        no.append('Cancel the operation.')

        if sublime.platform() == 'osx':
            sublime.set_timeout(lambda: window.show_quick_panel([yes, no], on_confirm), 200)
        else:
            window.show_quick_panel([yes, no], on_confirm)

    def patch(self, execute, filePath):
        patch = ''
        if (True == execute):
            backup = ' --no-backup-if-mismatch'
            if (True == Prefs.backup):
                backup = ' -b'
            patch = '|patch' + backup + ' ' + filePath
        return patch


'''
    Extract a range of lines into a new method and call this method from the original location.
    This refactoring automatically detects all necessary inputs and outputs from the function and generates the argument list and return statement accordingly.
    Sintax of the external command:
        php refactor.phar extract-method <file> <line-range> <new-method>|colordiff
        php refactor.phar extract-method <file> <line-range> <new-method>|patch -b <file>
'''


class ExtractCommand(sublime_plugin.TextCommand, Refactor):

    def run(self, edit, execute=False):
        msg("ExtractCommand")
        window = sublime.active_window()
        sels = self.view.sel()
        for sel in sels:
            firstLine = str(self.view.rowcol(sel.begin())[0] + 1)
            lastLine = str(self.view.rowcol(sel.end())[0] + 1)
            window.show_input_panel("What is the new function name?", '', lambda newFcName: self.runCommandLine(self.view.file_name(), firstLine, lastLine, newFcName, execute), None, None)
        return ''

    def runCommandLine(self, filePath, fromLine, toLine, newFcName, execute=False):
        filePath = shellquote(filePath)
        patch = self.patch(execute, filePath)

        command = Prefs.path_to_php + " " + self.REFACTOR + " extract-method " + filePath + " " + fromLine + "-" + toLine + " " + newFcName + patch

        if ((True == execute) and (True == Prefs.confirm)):
            self.confirm(lambda x: self.execute('extract_' + newFcName, command, execute))
        else:
            self.execute('extract_' + newFcName, command, execute)


'''
    Rename a local variable from one to another name.
    Sintax of the external command:
        php refactor.phar rename-local-variable <file> <line> <old-name> <new-name>
'''


class RenamelocalvariableCommand(sublime_plugin.TextCommand, Refactor):

    def run(self, edit, execute=False):
        msg("RenameLocalVariableCommand")
        window = sublime.active_window()
        sels = self.view.sel()
        for sel in sels:
            line = str(self.view.rowcol(sel.begin())[0] + 1)
            selection = self.view.substr(sel).strip("$")
            window.show_input_panel("What is the variable new name?", '', lambda newVarName: self.runCommandLine(self.view.file_name(), line, selection, newVarName.strip("$"), execute), None, None)
        return ''

    def runCommandLine(self, filePath, line, oldVarName, newVarName, execute=False):
        filePath = shellquote(filePath)
        patch = self.patch(execute, filePath)

        command = Prefs.path_to_php + " " + self.REFACTOR + " rename-local-variable " + filePath + " " + line + " " + oldVarName + " " + newVarName + patch

        if ((True == execute) and (True == Prefs.confirm)):
            self.confirm(lambda x: self.execute('rename-local-var_' + oldVarName + newVarName, command, execute))
        else:
            self.execute('rename-local-var_' + oldVarName + '_' + newVarName, command, execute)


'''

'''


class OptimizeuseCommand(sublime_plugin.TextCommand, Refactor):
    def run(self, edit):
        msg("OptimizeUseCommand")


'''
    Converts a local variable into an instance variable, creates the property and renames all the occurrences in the selected method to use the instance variable.
    Sintax of the external command:
        php refactor.phar convert-local-to-instance-variable <file> <line> <variable>
'''


class ConvertlocalvariabletoinstancevariableCommand(sublime_plugin.TextCommand, Refactor):

    def run(self, edit, execute=False):
        sels = self.view.sel()
        for sel in sels:
            line = str(self.view.rowcol(sel.begin())[0] + 1)
            selection = self.view.substr(sel).strip("$")
            self.runCommandLine(self.view.file_name(), line, selection, execute)

    def runCommandLine(self, filePath, line, varName, execute=False):
        filePath = shellquote(filePath)
        patch = self.patch(execute, filePath)

        command = Prefs.path_to_php + " " + self.REFACTOR + " convert-local-to-instance-variable " + filePath + " " + line + " " + varName + patch

        if ((True == execute) and (True == Prefs.confirm)):
            self.confirm(lambda x: self.execute('local-var-to-instance_' + varName, command, execute))
        else:
            self.execute('local-var-to-instance_' + varName, command, execute)


'''

'''


class ConvertmagicvaluetoconstantCommand(sublime_plugin.TextCommand, Refactor):
    def run(self, edit):
        msg("ConvertMagicValueToConstantCommand")


'''

'''


class RenamemethodCommand(sublime_plugin.TextCommand, Refactor):
    def run(self, edit):
        msg("RenameMethodCommand")


'''

'''


class RenameinstancevariableCommand(sublime_plugin.TextCommand, Refactor):
    def run(self, edit):
        msg("RenameInstanceVariableCommand")


'''

'''


class RenameclassCommand(sublime_plugin.TextCommand, Refactor):
    def run(self, edit):
        msg("RenameClassCommand")


'''

'''


class RenamenamespaceCommand(sublime_plugin.TextCommand, Refactor):
    def run(self, edit):
        msg("RenameNamespaceCommand")
