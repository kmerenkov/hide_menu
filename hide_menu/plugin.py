import gedit

import gtk


class HideMenuPlugin(gedit.Plugin):
    _plugins = {}

    def activate(self, window):
        self._plugins[window] = Plugin(window)

    def deactivate(self, window):
        plugin = self._plugins.pop(window)
        plugin.cleanup()
        del plugin

    def update_ui(self, window):
        plugin = self._plugins.get(window)
        # Don't know why yet, but update_ui is called earlier than activate
        if plugin:
            plugin.update_ui()


class Plugin(object):
    plugin = None
    window = None


    def __init__(self, window):
        self.window = window
        self.set_menu_visibility(False)
        
    def set_menu_visibility(self, is_visible):
        manager = self.window.get_ui_manager()
        menus = manager.get_toplevels(gtk.UI_MANAGER_MENUBAR)
        for menu in menus:
            menu.show() if is_visible else menu.hide()

    def update_ui(self):
        pass

    def cleanup(self):
        self.set_menu_visibility(True)
