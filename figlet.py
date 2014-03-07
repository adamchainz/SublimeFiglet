# coding=utf-8
import os
import sublime
import sublime_plugin
import sys

# Import from packages or locally.
try:
    import pyfiglet
except ImportError:
    sys.path.append(os.path.abspath(__file__))
    import pyfiglet


def figlet_text(text):
    settings = sublime.load_settings("Preferences.sublime-settings")
    font = settings.get('figlet_font', 'standard')

    width = get_width()

    result = pyfiglet.Figlet(font=font, width=width).renderText(text=text)

    # Strip trailing whitespace, because why not?
    if settings.get('figlet_no_trailing_spaces', True):
        result = '\n'.join((line.rstrip() for line in result.split('\n')))

    return result


def get_width():
    # Return width to wrap at (or large number if wrapping not enabled)
    width = 1000000

    view_settings = sublime.active_window().active_view().settings()
    if view_settings.get('word_wrap'):
        output_width = view_settings.get('wrap_width')
        if output_width not in (None, 0):
            width = output_width

    return width


class FigletSelectFontCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.fonts = pyfiglet.FigletFont.getFonts()
        self.window.show_quick_panel(self.fonts, self.on_done)

    def on_done(self, index):
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("figlet_font", self.fonts[index])
        sublime.save_settings("Preferences.sublime-settings")


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
