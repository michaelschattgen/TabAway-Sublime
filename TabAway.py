import sublime_plugin


class TabAwayCommand(sublime_plugin.WindowCommand):
    def run(self):
        groupsCount = self.window.num_groups()
        for i in range(0, groupsCount):
            for file in self.window.views_in_group(i):
                fileName = file.file_name()
                if fileName is not None:
                    if self.getExtension(fileName) == "xbrl":
                        print(fileName)

    def getExtension(self, filename):
        return filename.split('.')[-1]


class TabAwayListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        view.window().run_command("tab_away")
