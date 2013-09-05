SublimeFiglet
=============

A [Sublime Text][3] package to add in Big ASCII Lettering via [pyfiglet][2], a Python implementation of the original [Figlet][1] project. It looks like this (although you can select your font):


           d8888                             d8b                888
          d88888                             Y8P                888
         d88P888                                                888
        d88P 88888888b.d88b.  8888b. 8888888888888888b.  .d88b. 888
       d88P  888888 "888 "88b    "88b   d88P 888888 "88bd88P"88b888
      d88P   888888  888  888.d888888  d88P  888888  888888  888Y8P
     d8888888888888  888  888888  888 d88P   888888  888Y88b 888 "
    d88P     888888  888  888"Y88888888888888888888  888 "Y88888888
                                                             888
                                                        Y8b d88P
                                                         "Y88P"


How to Use
==========

This Package adds three commands to the command palette:

* `Figlet: Add Text` lets you type text (or uses your selection) and figletizes it.

* `Figlet: Add Comment` lets you type text (or uses your selection) and figletizes it as a comment.

* `Figlet: Select Font` lets you choose a font out of the installed list that come with pyfiglet. See a list of the font styles at the [figlet font page](http://www.figlet.org/examples.html).


        888'Y88 Y88b Y88     888   e88 88e   Y88b Y8P 888
        888 ,'Y  Y88b Y8     888  d888 888b   Y88b Y  888
        888C8   b Y88b Y     888 C8888 8888D   Y88b   "8"
        888 ",d 8b Y88b   e  88P  Y888 888P     888    e
        888,d88 88b Y88b "8",P'    "88 88"      888   "8"


How to Install
==============

If you don't have PackageControl, [go install it](https://sublime.wbond.net/installation) (and don't forget to restart Sublime.)

Afterwards, go to Preferences->Package Control, pick "Install Package" from the menu, wait a second and type in "figlet" to find this package in the list. Press Enter to confirm installation. That's it!


License
=======

SublimeFiglet is released under the MIT license.

Copyright (c) 2012 Adam Johnson <me@adamj.eu>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




[1]: http://www.figlet.org/
[2]: https://github.com/pwaller/pyfiglet
[3]: http://www.sublimetext.com/2
