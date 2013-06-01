# Sublime Text 2 PHP Refactor

    A wrapper for the refactoring tool  "QafooLabs / php-refactoring-browser"

    Note: The external tool this plugin uses is under development and in alpha state.
          Refactorings do not contain all necessary pre-conditions and might mess up your code.
          Check the diffs carefully before applying the patches.

    ATTENTION:
    At the moment this is not installing through Package Control, I'm looking into it.
        In the mean while, you can install it manualy, just downloading the zip package and unpacking it to the sublime packages folder (in Linux ~/.config/sublime-text-2/Packages), or making a git clone to that location.

        In Linux, type this in the command line:
        wget https://github.com/hgraca/sublime-text-2-php-refactor/archive/master.zip
        unzip ./master.zip -d ~/.config/sublime-text-2/Packages
        mv ~/.config/sublime-text-2/Packages/sublime-text-2-php-refactor-master/ ~/.config/sublime-text-2/Packages/sublime-text-2-php-refactor/
        rm -f ./master.zip

        Or this:
        git clone https://github.com/hgraca/sublime-text-2-php-refactor.git ~/.config/sublime-text-2/Packages/sublime-text-2-php-refactor

## How to use

    - Extract method: select a piece of code, click with the right button:
        PHP Refactor > Extract
            Diff will show what will change
            Patch will apply the changes

## Future developments

       Developed by PHP Refactoring Browser
       ▼   Wraped by this plugin
       ▼   ▼
    - [x] [x] Extract Method
    - [x] [x] Rename Local Variable
    - [ ] [ ] Optimize use statements
    - [x] [x] Convert Local Variable to Instance Variable
    - [ ] [ ] Convert Magic Value to Constant
    - [ ] [ ] Rename Method
    - [ ] [ ] Rename Instance Variable
    - [ ] [ ] Rename Class (PSR-0 aware)
    - [ ] [ ] Rename Namespace (PSR-0 aware)
    - [ ] [ ] Extract Interface

## Dependencies

    This plugin depends on the php tool php-refactoring-browser. The plugin ships with the latest version,
    but if you want to update it, you can download it here:
        http://qafoolabs.github.com/php-refactoring-browser/assets/refactor.phar

## Usefull command lines

    ln -s ${PWD} ~/.config/sublime-text-2/Packages/PhpRefactor

## Usefull sublime console lines

    view.run_command('extract', {'execute': False})
    view.run_command('extract', {'execute': True})
    view.run_command('renamelocalvariable', {'execute': False})
    view.run_command('renamelocalvariable', {'execute': true})
    view.run_command('convertlocalvariabletoinstancevariable', {'execute': False})
    view.run_command('convertlocalvariabletoinstancevariable', {'execute': true})
