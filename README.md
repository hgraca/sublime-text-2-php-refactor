# Sublime Text 2 PHP Refactor

    A wrapper for the refactoring tool  "QafooLabs / php-refactoring-browser"

    Note: This software is under development and in alpha state. Refactorings
    do not contain all necessary pre-conditions and might mess up your code.
    Check the diffs carefully before applying the patches.

## Dependences

    This plugin depends on the php tool php-refactoring-browser, which can be downloaded here:
        http://qafoolabs.github.com/php-refactoring-browser/assets/refactor.phar

## Usefull command lines

    ln -s ${PWD} ~/.config/sublime-text-2/Packages/PhpRefactor

## Usefull sublime console lines

    view.run_command('extract', {'execute': False})
    view.run_command('extract', {'execute': True})