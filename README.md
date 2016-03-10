SublimeFiglet
=============

A [Sublime Text][3] plugin for 2 and 3 to add in Big ASCII Lettering via
[pyfiglet][2], a Python implementation of the original [Figlet][1] project. It
looks like this (although you can select your font):

        _                        _             _
       / \   _ __ ___   __ _ ___(_)_ __   __ _| |
      / _ \ | '_ ` _ \ / _` |_  / | '_ \ / _` | |
     / ___ \| | | | | | (_| |/ /| | | | | (_| |_|
    /_/   \_\_| |_| |_|\__,_/___|_|_| |_|\__, (_)
                                         |___/


How to Use
==========

This Package adds three commands to the command palette:

* `Figlet: Add Text` lets you type text (or uses your selection) and figletizes
  it.

* `Figlet: Select Font` lets you choose a font out of the installed list that
  come with pyfiglet. See a list of the font styles at the [figlet font
  page](http://www.figlet.org/examples.html).


Installation
============

Please use [Package Control](https://sublime.wbond.net/installation) to install this plugin. This will ensure that it will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

2. When the plugin list appears, type `figlet`. Among the entries you should see `Figlet Big ASCII Text`. If that entry is not highlighted, use the keyboard or mouse to select it.


License
=======

SublimeFiglet is released under the MIT license.

Copyright (c) 2016 Adam Johnson <me@adamj.eu>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




[1]: http://www.figlet.org/
[2]: https://github.com/pwaller/pyfiglet
[3]: http://www.sublimetext.com/2
