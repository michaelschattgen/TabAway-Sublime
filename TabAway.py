import sublime
import sublime_plugin
import os
import time


class TabAwayCommand(sublime_plugin.WindowCommand):
    def run(self):
    	active = self.window.active_view();
    	print("ok")
    	for i in range(0, self.window.num_groups()):
    		print(i)

class TabAwayListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        view.window().run_command("tab_away")