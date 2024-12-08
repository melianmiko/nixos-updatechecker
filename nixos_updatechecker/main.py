import gi

from nixos_updatechecker.controller import UpdateCheckController
from nixos_updatechecker.indicator import UpdateCheckIndicator

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

indicator = UpdateCheckIndicator()
controller = UpdateCheckController.start(indicator)
Gtk.main()
