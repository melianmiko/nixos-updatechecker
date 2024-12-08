import os
from threading import Event

import gi

gi.require_version('AppIndicator3', '0.1')

from gi.repository import AppIndicator3, Gtk
from nixos_updatechecker.utils import ui_func
from nixos_updatechecker.config import APP_CONFIG


class UpdateCheckIndicator:
    def __init__(self):
        self.changes = []
        self.recheck_ev = Event() # Must be overridden by controller

        self.icon = AppIndicator3.Indicator.new(
            "nix_updater",
            APP_CONFIG["icon-pending"],
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.icon.set_status(AppIndicator3.IndicatorStatus.PASSIVE)

        self.menu = Gtk.Menu()

        self.menu_view_changes = Gtk.MenuItem(label="What's changed")
        self.menu_view_changes.connect("activate", self._preview_changes)
        self.menu_view_changes.show()
        self.menu.append(self.menu_view_changes)

        self.menu_check_now = Gtk.MenuItem(label="Check for updates")
        self.menu_check_now.connect("activate", lambda _: self.recheck_ev.set())
        self.menu_check_now.show()
        self.menu.append(self.menu_check_now)

        self.menu.show()
        self.icon.set_menu(self.menu)
        self._show_status([], True)

    @ui_func
    def show_status(self, *args, **kwargs):
        return self._show_status(*args, **kwargs)

    def _show_status(self, changes: list[str], pending: bool):
        self.changes = changes

        if pending:
            self.icon.set_title("NixOS: Checking for updates...")
            self.icon.set_icon(APP_CONFIG["icon-pending"])
            if not APP_CONFIG["always-active"]:
                self.icon.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
            # TODO: Icon, hide
        elif len(changes) == 0:
            self.icon.set_title("NixOS: No updates")
            self.icon.set_icon(APP_CONFIG["icon-no-updates"])
            if not APP_CONFIG["always-active"]:
                self.icon.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
        else:
            self.icon.set_title(f"NixOS: Available {len(changes)} updates")
            self.icon.set_icon(APP_CONFIG["icon-updates"])
            self.icon.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def _preview_changes(self, *_):
        with open("/tmp/updates_list_preview.txt", "w") as f:
            f.write("\n".join(self.changes) + "\n")

        os.system(APP_CONFIG["preview-command"].replace("{}", "/tmp/updates_list_preview.txt"))
