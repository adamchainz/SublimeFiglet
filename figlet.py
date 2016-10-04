# coding=utf-8
import os
import sublime
import sublime_plugin
import sys

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_PATH)


def figlet_text(text):
    import pyfiglet
    settings = sublime.load_settings("Preferences.sublime-settings")
    font = settings.get('figlet_font', 'standard')

    width = get_width()

    result = pyfiglet.Figlet(font=font, width=width).renderText(text=text)

    # Strip trailing whitespace, because why not?
    if settings.get('figlet_no_trailing_spaces', True):
        result = '\n'.join((line.rstrip() for line in result.split('\n')))

    return result[:len(result) - 1]


def get_width():
    # Return width to wrap at (or large number if wrapping not enabled)
    width = 1000000

    view_settings = sublime.active_window().active_view().settings()
    if view_settings.get('word_wrap'):
        output_width = view_settings.get('wrap_width')
        if output_width not in (None, 0):
            width = output_width

    return width


def add_comment_frame(text, comment_start, comment_end):
    settings = sublime.load_settings("Preferences.sublime-settings")
    padding = settings.get('figlet_comment_padding', 4)

    max_width = get_max_line_length(text)
    comment_line_char = comment_start[-1]
    # Exception HTML
    if comment_start == '<!--':
        comment_line_char = '!'
    # Exception MATLAB
    if comment_start == '%':
        comment_line_char = '#'
    # Exception Pascal
    if comment_start == '{':
        comment_line_char = '#'

    # First row
    horizontal_border = (
        comment_start +
        ((max_width + 2 * padding) * comment_line_char) +
        comment_end
    )
    result = horizontal_border + '\n'
    # Content
    for line in text.split('\n'):
        result += (
            comment_start +
            padding * ' ' +
            line +
            (max_width - len(line) + padding) * ' ' +
            comment_end +
            '\n'
        )
    # Last row
    result += horizontal_border

    return result


def get_max_line_length(text):
    return max(len(line) for line in text.split('\n'))


class FigletSelectFontCommand(sublime_plugin.WindowCommand):
    def run(self):
        import pyfiglet
        self.fonts = pyfiglet.FigletFont.getFonts()
        self.window.show_quick_panel(self.fonts, self.on_done)

    def on_done(self, index):
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("figlet_font", self.fonts[index])
        sublime.save_settings("Preferences.sublime-settings")


class FigletTextCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        sel = view.sel()
        if len(sel) == 1 and sel[0].size() > 0:
            view.run_command('figlet_insert_text', {'text': None})
        else:
            self.window.show_input_panel("Text to Figletize:", "",
                                         self.on_done, None, None)

    def on_done(self, text):
        view = self.window.active_view()
        view.run_command('figlet_insert_text', {'text': text})


class FigletCommentCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        sel = view.sel()
        if len(sel) == 1 and sel[0].size() > 0:
            view.run_command('figlet_insert_text', {'text': None,
                                                    'comment_frame': True})
        else:
            self.window.show_input_panel(
                "Text to Figletize in comment frame:",
                "",
                self.on_done,
                None,
                None
            )

    def on_done(self, text):
        view = self.window.active_view()
        view.run_command(
            'figlet_insert_text',
            {'text': text, 'comment_frame': True},
        )


class FigletInsertTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, text=None, comment_frame=False):
        view = self.view
        sel = view.sel()

        text_length = 0
        if text is None:  # ... then grab selection
            if len(sel) != 1 or sel[0].size() == 0:
                return
            text = view.substr(sel[0])
            text_length = len(text)

        cursor = min(sel[0].a, sel[0].b)

        text = figlet_text(text)

        if comment_frame:
            text = self.add_comment_frame(text)

        # Add tabulation?
        tab = (len(view.line(cursor)) - text_length) * ' '
        text = '\n'.join((tab + line for line in text.split('\n')))
        text = text[len(tab):]

        view.erase(edit, sel[0])
        view.insert(edit, cursor, text)
        sel.clear()
        sel.add(sublime.Region(cursor, cursor + len(text)))

    def add_comment_frame(self, text):
        settings = sublime.load_settings("Preferences.sublime-settings")
        padding = settings.get('figlet_comment_padding', 4)
        comment_start, comment_end = self.get_comment_prefix()

        max_width = get_max_line_length(text)
        comment_line_char = comment_start[-1]
        # Exception HTML
        if comment_start == '<!--':
            comment_line_char = '!'
        # Exception MATLAB
        if comment_start == '%':
            comment_line_char = '#'
        # Exception Pascal
        if comment_start == '{':
            comment_line_char = '#'

        # First row
        horizontal_border = (
            comment_start +
            ((max_width + 2 * padding) * comment_line_char) +
            comment_end
        )
        result = horizontal_border + '\n'
        # Content
        for line in text.split('\n'):
            result += (
                comment_start +
                padding * ' ' +
                line +
                (max_width - len(line) + padding) * ' ' +
                comment_end +
                '\n'
            )
        # Last row
        result += horizontal_border

        return result

    def get_comment_prefix(self):
        view = self.view
        sel = view.sel()
        cursor = min(sel[0].a, sel[0].b)

        # Get comment characters
        meta_infos = view.meta_info('shellVariables', cursor)
        comment_start = None
        comment_end = None
        comment_start_2 = None
        comment_end_2 = None
        comment_start_3 = None
        comment_end_3 = None
        for meta_info in meta_infos:
            if meta_info['name'] == 'TM_COMMENT_START':
                comment_start = meta_info['value']
            if meta_info['name'] == 'TM_COMMENT_END':
                comment_end = meta_info['value']
            if meta_info['name'] == 'TM_COMMENT_START_2':
                comment_start_2 = meta_info['value']
            if meta_info['name'] == 'TM_COMMENT_END_2':
                comment_end_2 = meta_info['value']
            if meta_info['name'] == 'TM_COMMENT_START_3':
                comment_start_2 = meta_info['value']
            if meta_info['name'] == 'TM_COMMENT_END_3':
                comment_end_2 = meta_info['value']
        if comment_end_2 is not None and comment_start_2 is not None:
            comment_start = comment_start_2
            comment_end = comment_end_2
        if comment_end_3 is not None and comment_start_3 is not None:
            comment_start = comment_start_3
            comment_end = comment_end_3
        if comment_start is None:
            # When nothing is set (e.g. Plain text)
            comment_start = ';'
        if comment_end is None:
            comment_end = comment_start[::-1]
        comment_start = comment_start.replace(" ", "")
        comment_end = comment_end.replace(" ", "")

        return comment_start, comment_end
