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

    # Support Word Wrap settings in ST
    view_settings = sublime.active_window().active_view().settings()
    if view_settings.get('word_wrap') != True:
        # It does not appear that there is a nice way of preventing line
        # breaks in figlet.
        command.extend(['-w', '10000'])
    else:
        output_width = view_settings.get('wrap_width')
        if output_width == None or output_width == 0:
            # Special case, word wrap 0 means window width.
            command.extend(['-t'])
        else:
            command.extend(['-w', str(output_width)])

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
