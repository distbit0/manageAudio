#!/usr/bin/env python3
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import os
import gi

gi.require_version("GLib", "2.0")
from gi.repository import GLib


def bluetooth_handler(*args, **kwargs):
    """Handle Bluetooth events."""
    # print("contents of args: ", args)
    status = args[1].get("Connected", None)
    if status is not None:
        if not status:
            os.system("playerctl pause")


if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    bus.add_signal_receiver(
        bluetooth_handler,
        bus_name="org.bluez",
        dbus_interface="org.freedesktop.DBus.Properties",
        signal_name="PropertiesChanged",
        path_keyword="path",
    )
    loop = GLib.MainLoop()
    loop.run()
