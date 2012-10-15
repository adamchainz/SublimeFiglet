# coding=utf-8
import subprocess
import sublime
import sublime_plugin


class FigletCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Text to Figletize:", "",
                                     self.on_done, None, None)
        pass

    def on_done(self, text):
        if text == "":
            return

        # Form Command

        proc = subprocess.Popen(['figlet', '%s' % text],
                                stdout=subprocess.PIPE)
        text = proc.communicate()[0]

        view = self.window.active_view()

        edit = view.begin_edit()

        self.window.run_command('single_selection')

        cursor = view.sel()[0].a
        view.insert(edit, cursor, text)
        view.sel().add(sublime.Region(cursor, cursor + len(text)))

        view.end_edit(edit)

