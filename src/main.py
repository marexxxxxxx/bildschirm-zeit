import sys

import gi

from src.backend.tracker import run_tracker_in_background  # noqa: E402
from src.database.db import init_table  # noqa: E402

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402


def on_activate(app: Gtk.Application) -> None:
    win = Gtk.ApplicationWindow(application=app)
    win.set_title("Bildschirm-Zeit")
    win.set_default_size(800, 600)

    label = Gtk.Label(
        label="Welcome to Bildschirm-Zeit!\nTracking is running in the background."
    )
    win.set_child(label)

    win.present()

def main() -> None:
    # Initialize the database
    init_table()

    # Start tracking window focus
    run_tracker_in_background()

    # Start the GTK application
    app = Gtk.Application(application_id="org.example.BildschirmZeit")
    app.connect("activate", on_activate)
    app.run(sys.argv)

if __name__ == "__main__":
    main()
