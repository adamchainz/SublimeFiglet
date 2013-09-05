# coding=utf-8
import os
import sys
import sublime
import sublime_plugin

try:
    # Do we have the module?
    import pyfiglet
except ImportError:
    # No? Ok, let's use our local one:
    sys.path.append(os.path.abspath(__file__))
    import pyfiglet


def figlet_text(text):
    # Get Font Setting
    settings = sublime.load_settings("Preferences.sublime-settings")
    font = settings.get('figlet_font', 'standard')

    # Support Word Wrap settings in ST
    view_settings = sublime.active_window().active_view().settings()
    if view_settings.get('word_wrap') != True:
        width = 10000
    else:
        output_width = view_settings.get('wrap_width')
        if not output_width in (None, 0):
            width = output_width

    # Get text
    fig = pyfiglet.Figlet(font=font, width=width)
    result = fig.renderText(text=text)

    # Strip trailing whitespace, because why not?
    if settings.get('figlet_no_trailing_spaces', True):
        result = '\n'.join((line.rstrip() for line in result.split('\n')))

    return result


class FigletSelectFontCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.fonts = pyfiglet.FigletFont.getFonts()
        self.window.show_quick_panel(self.fonts, self.on_done)

    def on_done(self, index):
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("figlet_font", self.fonts[index])


class FigletTextCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if len(view.sel()) == 1 and view.sel()[0].size() > 0:
            s = view.sel()[0]
            text = view.substr(s)

            edit = view.begin_edit()
            view.erase(edit, s)
            self.on_done(text, edit)
        else:
            self.window.show_input_panel("Text to Figletize:", "",
                                         self.on_done, None, None)
        pass

    def on_done(self, text, edit=None):
        if text == "":
            return

        text = figlet_text(text)

        # Put into view.
        view = self.window.active_view()

        if edit is None:
            edit = view.begin_edit()

        self.window.run_command('single_selection')

        cursor = view.sel()[0].a
        text = text[:len(text) - 1]
        view.insert(edit, cursor, text)

        # Select
        view.sel().add(sublime.Region(cursor, cursor + len(text)))

        view.end_edit(edit)


class FigletCommentCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if len(view.sel()) == 1 and view.sel()[0].size() > 0:
            s = view.sel()[0]
            text = view.substr(s)

            edit = view.begin_edit()
            view.erase(edit, s)
            self.on_done(text, edit)
        else:
            self.window.show_input_panel("Text to Figletize:", "",
                                         self.on_done, None, None)
        pass

    def on_done(self, text, edit=None):
        if text == "":
            return

        text = figlet_text(text)

        # Put into view, with correct tabbing + one more, and commentize
        view = self.window.active_view()

        if edit is None:
            edit = view.begin_edit()

        self.window.run_command('single_selection')

        cursor = view.sel()[0].a
        current_line = view.line(cursor)
        prefix = view.substr(sublime.Region(current_line.a, cursor))

        text = text[:len(text) - 1]
        text = text.replace("\n", "\n" + prefix)

        view.insert(edit, cursor, text)

        view.sel().add(sublime.Region(cursor, cursor + len(text)))

        # self.window.run_command('split_selection_into_lines')
        self.window.run_command('toggle_comment', {'block': True})

        view.end_edit(edit)
