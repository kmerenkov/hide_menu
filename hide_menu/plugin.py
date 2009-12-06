import gedit

import gtk


TOGGLE_HOTKEY = gtk.accelerator_parse("<Ctrl>F10")
STD_MENUBAR_HOTKEY = gtk.accelerator_parse("F10")


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
    accel_group = gtk.AccelGroup()


    def __init__(self, window):
        self.window = window
        self.set_menu_visibility(False)
        self.setup_hotkeys()

    def set_menu_visibility(self, is_visible):
        manager = self.window.get_ui_manager()
        menus = manager.get_toplevels(gtk.UI_MANAGER_MENUBAR)
        for menu in menus:
            menu.show() if is_visible else menu.hide()

    def toggle_visibility(self):
        manager = self.window.get_ui_manager()
        menus = manager.get_toplevels(gtk.UI_MANAGER_MENUBAR)
        for menu in menus:
            menu.props.visible = not menu.props.visible

    def setup_hotkeys(self):
        f_toggle = lambda _1, _2, _3, _4: self.toggle_visibility()
        self.accel_group.connect_group(TOGGLE_HOTKEY[0], TOGGLE_HOTKEY[1], 0, f_toggle)
        self.accel_group.connect_group(STD_MENUBAR_HOTKEY[0], STD_MENUBAR_HOTKEY[1], 0, f_toggle)
        self.window.add_accel_group(self.accel_group)

    def remove_hotkeys(self):
        self.window.remove_accel_group(self.accel_group)

    def update_ui(self):
        pass

    def cleanup(self):
        self.set_menu_visibility(True)
        self.remove_hotkeys()
