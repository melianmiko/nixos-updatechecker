import os
import re
import threading

from gi.repository import GLib

DEFAULT_CONFIG_DIR = "/etc/nixos/"

def ui_func(f):
    def wrapped(result, event, args, kwargs):
        result.append(f(*args, **kwargs))
        event.set()

    def full(*args, **kwargs):
        event = threading.Event()
        result = []

        GLib.idle_add(wrapped, result, event, args, kwargs)
        event.wait()
        return result[0]

    return full

def get_config_dir():
    config_dir = DEFAULT_CONFIG_DIR
    if (nix_path := os.environ.get("NIX_PATH")) is not None:
      paths = re.split("=|:", nix_path)
      idx = paths.index("nixos-config") + 1
      if idx < len(paths):
        config_dir = os.path.dirname(paths[idx])
    return config_dir
