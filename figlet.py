# coding=utf-8
import os
import subprocess
import sublime
import sublime_plugin


def figlet_text(text):
    # Get Font Setting
    settings = sublime.load_settings("Preferences.sublime-settings")
    font = settings.get("figlet_font", None)

    # Form Command
    command = ['figlet']
    if font is not None:
        command.extend(['-f', font])
    command.append('%s' % text)

    # Get Text
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    return proc.communicate()[0]


class FigletSelectFontCommand(sublime_plugin.WindowCommand):
    def run(self):
        proc = subprocess.Popen(['figlet', '-I', '2'], stdout=subprocess.PIPE)
        fonts_dir = proc.communicate()[0]

        print fonts_dir

        # proc = subprocess.Popen(['ls', fonts_dir], stdout=subprocess.PIPE)
        fonts = os.listdir(fonts_dir[:-1])
        self.fonts = [f.split('.')[0] for f in fonts]

        self.window.show_quick_panel(self.fonts, self.on_done)

    def on_done(self, index):
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("figlet_font", self.fonts[index])


class FigletCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Text to Figletize:", "",
                                     self.on_done, None, None)
        pass

    def on_done(self, text):
        if text == "":
            return

        text = figlet_text(text)

        # Put into view.
        view = self.window.active_view()

        edit = view.begin_edit()

        self.window.run_command('single_selection')

        cursor = view.sel()[0].a
        view.insert(edit, cursor, text)

        # Select
        view.sel().add(sublime.Region(cursor, cursor + len(text)))

        view.end_edit(edit)


class FigletPythonCommentCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Text to Figletize:", "",
                                     self.on_done, None, None)
        pass

    def on_done(self, text):
        if text == "":
            return

        text = figlet_text(text)

        # Put into view, with correct tabbing + one more, and commentize
        view = self.window.active_view()

        edit = view.begin_edit()

        self.window.run_command('single_selection')

        cursor = view.sel()[0].a
        current_line = view.line(cursor)
        prefix = view.substr(sublime.Region(current_line.a, cursor))

        text = text[:len(text) - 1]
        text = '#\t' + text.replace("\n", "\n" + prefix + '#\t')

        view.insert(edit, cursor, text)

        # view.sel().add(sublime.Region(cursor, cursor + len(text)))

        # self.window.run_command('split_selection_into_lines')
        # self.window.run_command('toggle_comment', {'block': False})

        view.end_edit(edit)
