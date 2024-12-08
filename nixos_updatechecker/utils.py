import threading

from gi.repository import GLib


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
