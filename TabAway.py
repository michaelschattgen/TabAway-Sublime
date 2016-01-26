import sublime_plugin
import sublime


class TabAwayCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("TabAway.sublime-settings")
        enabledFileExtensions = settings.get('tabaway_file_extensions')

        fileExtensions = self.getEnabledExtensions(enabledFileExtensions)
        groupsCount = self.window.num_groups()
        for i in range(0, groupsCount):
            for file in self.window.views_in_group(i):
                fileName = file.file_name()
                if fileName is not None:
                    if self.getExtension(fileName) in fileExtensions:
                        # Do something with the files
                        return

    def getExtension(self, filename):
        return filename.split('.')[-1]

    def getEnabledExtensions(self, fileExtensionsSetting):
        fileExtensions = fileExtensionsSetting.split('|')
        return fileExtensions


class TabAwayListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        view.window().run_command("tab_away")
