import sublime_plugin
import sublime
import os


class TabAwayCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Get TabAway settings along with the enabled file extensions
        settings = sublime.load_settings("TabAway.sublime-settings")
        enabled_file_extensions = settings.get('tabaway_file_extensions')

        file_extensions = Utils.get_enabled_extensions(enabled_file_extensions)

        Utils.close_files(self.window, file_extensions)


class Utils():
    def close_files(window, extensions):
        print("Closing " + str(extensions))

        # Iterate over the amount of windows / groups of the editor
        group_count = window.num_groups()
        for i in range(0, group_count):
            for file in window.views_in_group(i):
                path = file.file_name()
                if path is not None:
                    # Check if the file extension is provided by user
                    if Utils.get_extension(path) in extensions:

                        # Close file when
                        #           * extension is provided by user
                        #           * file is not dirty
                        #           * file is not new / unsaved
                        #           * file is not active
                        if (os.path.exists(path) is True and
                            not path == window.active_view_in_group(i) and
                                not file.is_dirty()):

                            window.focus_view(file)
                            window.run_command('close_file')

    def get_extension(path):
        file_extension = path.split('.')[-1]
        return file_extension

    def get_enabled_extensions(enabled_file_extensions):
        file_extensions = enabled_file_extensions.split('|')
        return file_extensions


class TabAwayListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        view.window().run_command("tab_away")
        return


class TabAwaySetterListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if not view.settings().get('is_widget'):
            ListSpecifiedCommand.view = view


class ListSpecifiedCommand(sublime_plugin.WindowCommand):
    def run(self):
        default = ["all"]
        commands = [default]

        for item in ["1", "2"]:
            commands.append(item)
        self.window.show_quick_panel(commands, self.close_specific_file_extension)


class CloseAllFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit, args=None, index=-1, group=-1, **kwargs):
        window = self.view.window()
        views = window.views_in_group(group)
        view = views[index]

        print(self.view.window().num_groups())

        file_name = view.file_name()
        if file_name is None:
            return

        file_extension = Utils.get_extension(file_name)
        Utils.close_files(window, file_extension)
