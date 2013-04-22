# coding=utf8
import sublime
import sublime_plugin
import os
import subprocess
from os.path import basename


'''
    Global function to send system messages
'''


def msg(msg):
    print "[PHP Refactor] %s" % msg


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


Prefs.load()


'''
    Top level class for the plugin commands
'''


class Refactor():
    REFACTOR = sublime.packages_path() + "/sublime-text-2-php-refactor/lib/refactor.phar"

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


'''
    Extract a range of lines into a new method and call this method from the original location.
    This refactoring automatically detects all necessary inputs and outputs from the function and generates the argument list and return statement accordingly.
    Sintax of the external command:
        php refactor.phar extract-method <file> <line-range> <new-method>|colordiff
        php refactor.phar extract-method <file> <line-range> <new-method>|patch -b <file>
'''


class ExtractCommand(sublime_plugin.TextCommand, Refactor):

    def run(self, edit, execute=False):
        window = sublime.active_window()
        sels = self.view.sel()
        for sel in sels:
            firstLine = str(self.view.rowcol(sel.begin())[0] + 1)
            lastLine = str(self.view.rowcol(sel.end())[0] + 1)
            window.show_input_panel("What is the new function name?", '', lambda newFcName: self.runCommandLine(self.view.file_name(), firstLine, lastLine, newFcName, execute), None, None)
        return ''

    def runCommandLine(self, filePath, fromLine, toLine, newFcName, execute=False):
        patch = ''
        if (True == execute):
            backup = ' --no-backup-if-mismatch'
            if (True == Prefs.backup):
                backup = ' -b'
            patch = '|patch' + backup + ' ' + filePath

        command = "php " + self.REFACTOR + " extract-method " + self.view.file_name() + " " + fromLine + "-" + toLine + " " + newFcName + patch

        if ((True == execute) and (True == Prefs.confirm)):
            self.confirm(lambda x: self.execute('extract_' + newFcName, command, execute))
        else:
            self.execute('extract_' + newFcName, command, execute)


'''
    Rename a local variable from one to another name.
    Sintax of the external command:
        php refactor.phar rename-local-variable <file> <line> <old-name> <new-name>
'''


class RenameLocalVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("php refactor.phar rename-local-variable " + self.view.file_name() + " 8 $oldName $newName|colordiff")


'''
    Converts a local variable into an instance variable, creates the property and renames all the occurrences in the selected method to use the instance variable.
    Sintax of the external command:
        php refactor.phar convert-local-to-instance-variable <file> <line> <variable>
'''


class OptimizeUseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("php refactor.phar convert-local-to-instance-variable " + self.view.file_name() + " 8 $variable|colordiff")


'''

'''


class ConvertLocalVariableToInstanceVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("ConvertLocalVariableToInstanceVariableCommand")


'''

'''


class ConvertMagicValueToConstantCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("ConvertMagicValueToConstantCommand")


'''

'''


class RenameMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("RenameMethodCommand")


'''

'''


class RenameInstanceVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("RenameInstanceVariableCommand")


'''

'''


class RenameClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("RenameClassCommand")


'''

'''


class RenameNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        msg("RenameNamespaceCommand")
