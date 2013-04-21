# coding=utf8
import sublime
import sublime_plugin
import functools
import os
import subprocess
from os.path import dirname, realpath, basename


'''
Extract a range of lines into a new method and call this method from the original location.
This refactoring automatically detects all necessary inputs and outputs from the function and generates the argument list and return statement accordingly.
Sintax of the external command:
    php refactor.phar extract-method <file> <line-range> <new-method>|colordiff
    php refactor.phar extract-method <file> <line-range> <new-method>|patch -b <file>

package setting: -b (backup original file)
key bindings: ctrl +r +e +d (diff)
key bindings: ctrl +r +e +a (apply)
'''


class ExtractCommand(sublime_plugin.TextCommand):
    # @TODO: create the commands ExtractDiffCommand and ExtractExecCommand

    # name = 'extract diff'
    # outputWindow = None

    def run(self, edit):
        window = sublime.active_window()
        sels = self.view.sel()
        for sel in sels:
            firstLine = str(self.view.rowcol(sel.begin())[0] + 1)
            lastLine = str(self.view.rowcol(sel.end())[0] + 1)
            window.show_input_panel("What is the new function name?", '', lambda newFcName: self.runCommandLine(self.view.file_name(), firstLine, lastLine, newFcName), None, None)
        return ''

    def runCommandLine(self, filePath, fromLine, toLine, newFcName, execute=False):
        command = "php refactor.phar extract-method " + self.view.file_name() + " " + fromLine + "-" + toLine + " " + newFcName
        print command
        self.performAction('extract_' + newFcName, command)

    # @TODO: create class Action(name, command)) with method execute(execute=False)
    def performAction(self, name, command):
        fileName = basename(self.view.file_name())

        if not command:
            print 'Action ' + name + ': No command supplied'
            return

        originalWd = os.getcwd()
        print 'originalWd: ' + originalWd
        wd = sublime.packages_path() + "/sublime-text-2-php-refactor/lib"
        if wd:
            os.chdir(wd)

        print 'Performing action: ' + name + ' (' + command + ') in ' + os.getcwd()

        p = subprocess.Popen(command, cwd=wd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        os.chdir(originalWd)
        if p.stdout is not None:
            msg = p.stdout.readlines()
            msg = '\n'.join(msg)
            outputWindow = self.getOutputWindow(name + '_' + fileName + '.diff')
            edit = outputWindow.begin_edit()
            outputWindow.insert(edit, 0, msg)
            outputWindow.end_edit(edit)
            outputWindow.set_read_only(True)

    def getOutputWindow(self, windowName, sintax='Diff'):
        outputWindow = sublime.active_window().new_file()
        outputWindow.set_name(windowName)
        outputWindow.set_syntax_file('Packages/' + sintax + '/' + sintax + '.tmLanguage')
        outputWindow.set_read_only(False)

        return outputWindow

'''
    def confirm(self):
        window = sublime.active_window()
        window.show_input_panel("BUG!", '', '', None, None)
        window.run_command('hide_panel')

        yes = []
        yes.append('Yes, delete the selected items.')

        no = []
        no.append('No')
        no.append('Cancel the operation.')
        if sublime.platform() == 'osx':
            sublime.set_timeout(lambda: window.show_quick_panel([yes, no], functools.partial(self.on_confirm)), 200)
        else:
            window.show_quick_panel([yes, no], functools.partial(self.on_confirm))

    def on_confirm(self):
        print "confirmed"
'''

'''
Rename a local variable from one to another name.
Sintax of the external command:
    php refactor.phar rename-local-variable <file> <line> <old-name> <new-name>
'''


class RenameLocalVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "php refactor.phar rename-local-variable " + self.view.file_name() + " 8 $oldName $newName|colordiff")


'''
Converts a local variable into an instance variable, creates the property and renames all the occurrences in the selected method to use the instance variable.
Sintax of the external command:
    php refactor.phar convert-local-to-instance-variable <file> <line> <variable>
'''


class OptimizeUseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "php refactor.phar convert-local-to-instance-variable " + self.view.file_name() + " 8 $variable|colordiff")


'''

'''


class ConvertLocalVariableToInstanceVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "ConvertLocalVariableToInstanceVariableCommand")


'''

'''


class ConvertMagicValueToConstantCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "ConvertMagicValueToConstantCommand")


'''

'''


class RenameMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameMethodCommand")


'''

'''


class RenameInstanceVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameInstanceVariableCommand")


'''

'''


class RenameClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameClassCommand")


'''

'''


class RenameNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameNamespaceCommand")
