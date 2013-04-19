import sublime
import sublime_plugin


'''
Extract a range of lines into a new method and call this method from the original location.
This refactoring automatically detects all necessary inputs and outputs from the function and generates the argument list and return statement accordingly.
Sintax of the external command:
    php refactor.phar extract-method <file> <line-range> <new-method>
'''


class ExtractCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # self.view.insert(edit, 0, "ExtractCommand")
        # self.view.insert(edit, 0, "php refactor.phar extract-method <file> <line-range> <new-method>|colordiff")
        # self.view.insert(edit, 0, "php refactor.phar extract-method <file> <line-range> <new-method>|patch -p1")
        # self.view.insert(edit, 0, "php refactor.phar extract-method /tmp/test.php 8-8 add|colordiff")
        self.view.insert(edit, 0, "php refactor.phar extract-method " + self.view.file_name() + " 8-8 add|colordiff")
        return ''


'''
Rename a local variable from one to another name.
Sintax of the external command:
    php refactor.phar rename-local-variable <file> <line> <old-name> <new-name>
'''


class RenameLocalVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "php refactor.phar rename-local-variable " + self.view.file_name() + " 8-8 add|colordiff")


'''
Converts a local variable into an instance variable, creates the property and renames all the occurrences in the selected method to use the instance variable.
Sintax of the external command:
    php refactor.phar convert-local-to-instance-variable <file> <line> <variable>
'''


class OptimizeUseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "php refactor.phar convert-local-to-instance-variable " + self.view.file_name() + " 8-8 add|colordiff")


class ConvertLocalVariableToInstanceVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "ConvertLocalVariableToInstanceVariableCommand")


class ConvertMagicValueToConstantCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "ConvertMagicValueToConstantCommand")


class RenameMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameMethodCommand")


class RenameInstanceVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameInstanceVariableCommand")


class RenameClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameClassCommand")


class RenameNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "RenameNamespaceCommand")
