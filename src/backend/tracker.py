import datetime
import logging
import os
import socket
import threading
import time
from typing import Optional, Tuple

from src.database.db import Write_Aktion, init_table, is_app_registered

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables to track the current state
current_app_id: Optional[int] = None
current_start_time: float = 0.0

def Get_current_time() -> float:
    return time.time()

def Get_current_date() -> datetime.date:
    return datetime.date.today()

def parse_window_title(app_class: str, title: str) -> Tuple[str, str]:
    """
    Parses the window title to extract the specific tab or project name
    based on the application class.
    Returns a tuple of (name_fenster, name_tab).
    """
    app_class_lower = app_class.lower()

    if (
        "chrome" in app_class_lower
        or "firefox" in app_class_lower
        or "brave" in app_class_lower
    ):
        # Format usually is: "Tab Title - Google Chrome"
        parts = title.split(" - ")
        if len(parts) > 1:
            name_tab = " - ".join(parts[:-1]) # Rejoin in case tab title has " - "
        else:
            name_tab = title
        return (app_class, name_tab)

    elif "code" in app_class_lower:
        # VS Code format usually is: "file - project - Visual Studio Code"
        parts = title.split(" - ")
        if len(parts) >= 2:
            name_tab = parts[-2]  # project name is usually before "Visual Studio Code"
        else:
            name_tab = title
        return (app_class, name_tab)

    # Default fallback
    return (app_class, title)

def Change_of_focus(app_class: str, title: str) -> None:
    """
    Handles a change of window focus.
    Logs the time spent in the previous window and starts tracking the new one.
    """
    global current_app_id, current_start_time

    current_time = Get_current_time()
    current_date = Get_current_date()

    # 1. Write the action for the previous app if there was one
    if current_app_id is not None and current_start_time > 0:
        Write_Aktion(current_date, current_start_time, current_time, current_app_id)

    # 2. Start tracking the new app
    if not app_class and not title:
        # Can happen if focus is lost (e.g., desktop)
        current_app_id = None
        current_start_time = 0.0
        return

    name_fenster, name_tab = parse_window_title(app_class, title)
    current_app_id = is_app_registered(name_fenster, name_tab)
    current_start_time = current_time

def process_hyprland_event(event_line: str) -> None:
    """
    Processes a single line of Hyprland IPC event.
    """
    # event looks like: activewindow>>app_class,window_title
    if event_line.startswith("activewindow>>"):
        data = event_line[len("activewindow>>"):]
        parts = data.split(",", 1)
        if len(parts) == 2:
            app_class, title = parts
            Change_of_focus(app_class, title)
        elif len(parts) == 1:
             Change_of_focus(parts[0], "")

def start_tracker() -> None:
    """
    Starts listening to the Hyprland IPC socket.
    """
    init_table()

    his = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR")

    if not his or not xdg_runtime_dir:
        logger.error(
            "HYPRLAND_INSTANCE_SIGNATURE or XDG_RUNTIME_DIR variables not set. "
            "Are you running Hyprland?"
        )
        # Just loop to keep thread alive if running outside hyprland for tests
        return

    socket_path = os.path.join(xdg_runtime_dir, "hypr", his, ".socket2.sock")

    if not os.path.exists(socket_path):
        logger.error(f"Hyprland socket not found at {socket_path}")
        return

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(socket_path)
        logger.info(f"Connected to Hyprland socket: {socket_path}")

        buffer = ""
        while True:
            data = sock.recv(4096)
            if not data:
                break

            buffer += data.decode('utf-8')
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                process_hyprland_event(line)

    except Exception as e:
        logger.error(f"Error while connecting to Hyprland socket: {e}")
    finally:
        sock.close()
        # Save any final tracked time if disconnecting
        Change_of_focus("", "")
        logger.info("Tracker disconnected.")

def run_tracker_in_background() -> threading.Thread:
    thread = threading.Thread(target=start_tracker, daemon=True)
    thread.start()
    return thread
