import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402


def on_activate(app: Gtk.Application) -> None:
    win = Gtk.ApplicationWindow(application=app)
    win.set_title("Bildschirm-Zeit")
    win.set_default_size(800, 600)

    label = Gtk.Label(label="Welcome to Bildschirm-Zeit!")
    win.set_child(label)

    win.present()


def main() -> None:
    app = Gtk.Application(application_id="org.example.BildschirmZeit")
    app.connect("activate", on_activate)
    app.run(sys.argv)


if __name__ == "__main__":
    main()
