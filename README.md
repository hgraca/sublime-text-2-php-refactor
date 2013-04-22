# Sublime Text 2 PHP Refactor

    A wrapper for the refactoring tool  "QafooLabs / php-refactoring-browser"

    Note: The external tool this plugin uses is under development and in alpha state. Refactorings
    do not contain all necessary pre-conditions and might mess up your code.
    Check the diffs carefully before applying the patches.

## Dependences

    This plugin depends on the php tool php-refactoring-browser. The latest version can be downloaded here:
        http://qafoolabs.github.com/php-refactoring-browser/assets/refactor.phar

## Future developments

       Developed by PHP Refactoring Browser
       ▼   Implemented in this plugin
       ▼   ▼
    - [x] [x] Extract Method
    - [x] [ ] Rename Local Variable
    - [ ] [ ] Optimize use statements
    - [x] [ ] Convert Local Variable to Instance Variable
    - [ ] [ ] Convert Magic Value to Constant
    - [ ] [ ] Rename Method
    - [ ] [ ] Rename Instance Variable
    - [ ] [ ] Rename Class (PSR-0 aware)
    - [ ] [ ] Rename Namespace (PSR-0 aware)
    - [ ] [ ] Extract Interface

## Usefull command lines

    ln -s ${PWD} ~/.config/sublime-text-2/Packages/PhpRefactor

## Usefull sublime console lines

    view.run_command('extract', {'execute': False})
    view.run_command('extract', {'execute': True})