import sublime
import sublime_plugin

import os
import sys
from .modules.ampy import ampy, pyboard
from textwrap import indent
from os.path import basename
from serial import SerialException


class Settings(object):
    settings = sublime.load_settings("MicroPython.sublime-settings")

    port = settings.get("port", False)
    project_path = settings.get("project_path", None)
    notices = False if settings.get("notices") == "False" else True


class MyBoard(Settings):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type or value:
            sublime.error_message(
                "Failed to access {}. \nPlease check connection or settings.".format(
                    Settings.port
                )
            )
            return False
        self.pyboard.close()
        del self.connection
        return True

    def __repr__(self):
        return "<MicroPython @ {}>".format(self.port)

    def connect(self):
        self.pyboard = pyboard.Pyboard(Settings.port)
        self.connection = ampy.Files(self.pyboard)


class MpGetFileCommand(sublime_plugin.WindowCommand, Settings):

    def run(self):
        with MyBoard() as board:
            board.connect()
            try:
                self.files = board.connection.ls(long_format=False)
                if self.files == []:
                    sublime.message_dialog(
                        "There is no file yet. You need to upload a file before want it."
                    )
                    return
            except NameError:
                sublime.error_message(
                    "Couldn't connect to {} .\n Please check port and re-open sublime text.".format(
                        self.port
                    )
                )
                return

        self.files.append(self.files[0])
        self.files[0] = "Select a file:"

        self.window.show_quick_panel(self.files, self.selected)

    def selected(self, id):
        if id == -1:
            return

        file_name = self.files[id]
        local_files = os.listdir(self.project_path)

        if file_name in local_files:
            selection = sublime.yes_no_cancel_dialog(
                "{filename} is exists in local dir. If you download it local one will kill itself. \n Do you really want do it?".format(
                    filename=file_name
                ),
                "Yes",
                "No",
            )
            if selection == sublime.DIALOG_YES:
                self.do_it(id)
                self.window.status_message("File overwrited.")
            else:
                self.window.status_message("Process cancelled.")

        else:
            self.do_it(id)

    def do_it(self, id):
        file_name = self.files[id]

        if id == 0:
            sublime.message_dialog("Please select a file!")
        elif id == -1:
            sublime.message_dialog("Please select a file!")
        else:
            with MyBoard() as board:
                board.connect()
                try:
                    out = board.connection.get(file_name)
                except RuntimeError as e:
                    sublime.message_dialog(str(e))

                except SerialException:
                    sublime.error_message("Port is not open or wrong port.")
                    return
                else:
                    with open(Settings.project_path + file_name, "w+") as file:

                        out = out.decode("utf-8")
                        out = indent(out, "", lambda line: True)

                        file.write(str(out))

                self.window.open_file(self.project_path + file_name)

                self.window.status_message("{} copied to local.".format(file_name))


class MpPutFileCommand(sublime_plugin.WindowCommand):

    def run(self, path=None):

        if not path:
            file_path = sublime.active_window().active_view().file_name()
        else:
            if len(path) == 1:
                if path[0].split(".")[1] == ".py":
                    file_path = path[0]
                else:
                    return

        if not file_path:
            sublime.error_message("Create a file and save it before try upload.")
        else:
            file_name = basename(file_path)
            file_data = open(file_path, "r").read()

            with MyBoard() as board:
                board.connect()
                try:
                    o = board.connection.put(file_name, file_data)
                    if not o:
                        self.window.status_message(
                            "File uploaded. Named as {}".format(file_name)
                        )
                    else:
                        sublime.error_message(
                            "File couldn't uploaded. An error occurred."
                        )

                except NameError:
                    sublime.error_message(
                        "Couldn't connect to board .\n Please check port and re-open sublime text."
                    )


class MpDeleteFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        with MyBoard() as board:
            board.connect()
            try:
                self.files = board.connection.ls(long_format=False)
                if self.files == []:
                    sublime.message_dialog(
                        "There is no file yet. You need to upload a file before want it."
                    )
                    return None

            except:
                sublime.error_message(
                    "Excepted serial connection error. Probably port using by another app."
                )
                return None

        self.files.append(self.files[0])
        self.files[0] = "Select a file:"

        self.window.show_quick_panel(self.files, self.selected)

    def selected(self, id):
        file_name = self.files[id]

        selection = sublime.yes_no_cancel_dialog(
            "You are deleting {filename} permanently. \n Are you sure?".format(
                filename=file_name
            ),
            "Yes",
            "No",
        )
        if selection == sublime.DIALOG_YES:
            self.do_it(id)
            self.window.status_message("File deleted.")
        else:
            self.window.status_message("Process cancelled.")

    def do_it(self, id):
        file_name = self.files[id]

        if id == 0:
            sublime.message_dialog("Please select a file!")
        elif id == -1:
            sublime.message_dialog("Please select a file!")
        else:
            try:
                with MyBoard() as board:
                    board.connect()
                    out = board.connection.rm(file_name)
            except RuntimeError as e:
                sublime.message_dialog(e)
            else:
                sublime.message_dialog("{} deleted.".format(file_name))

                self.window.status_message("{} copied to local.".format(file_name))


class MpSettingsCommand(sublime_plugin.WindowCommand, Settings):

    def run(self):
        self.window.run_command(
            "edit_settings",
            {"base_file": "${packages}/MicroPython Tools/MicroPython.sublime-settings"},
        )
