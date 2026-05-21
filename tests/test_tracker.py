import typing
import datetime
import os

import pytest

import src.backend.tracker as tracker_module
import src.database.db as db_module

@pytest.fixture(autouse=True)
def setup_tracker(monkeypatch: pytest.MonkeyPatch) -> typing.Generator[typing.Any, None, None]:
    # Setup Test DB
    db_module.DB_PATH = "test_tracker.db"
    if os.path.exists(db_module.DB_PATH):
        os.remove(db_module.DB_PATH)
    db_module.init_table()

    # Reset tracker state
    tracker_module.current_app_id = None
    tracker_module.current_start_time = 0.0

    # Mock time
    class TimeMock:
        def __init__(self) -> None:
            self.current = 1000.0

        def time(self) -> float:
            return self.current

    time_mock = TimeMock()
    monkeypatch.setattr(tracker_module.time, "time", time_mock.time)  # type: ignore

    yield time_mock

    # Teardown
    if os.path.exists(db_module.DB_PATH):
        os.remove(db_module.DB_PATH)

def test_parse_window_title() -> None:
    assert tracker_module.parse_window_title(
        "google-chrome", "YouTube - Google Chrome"
    ) == ("google-chrome", "YouTube")
    assert tracker_module.parse_window_title(
        "Firefox", "Search - Mozilla Firefox"
    ) == ("Firefox", "Search")
    assert tracker_module.parse_window_title(
        "code", "main.py - my-project - Visual Studio Code"
    ) == ("code", "my-project")
    assert tracker_module.parse_window_title("kitty", "zsh") == ("kitty", "zsh")

def test_change_of_focus(setup_tracker: typing.Any) -> None:
    time_mock = setup_tracker

    # 1. Initial focus
    tracker_module.Change_of_focus("google-chrome", "YouTube - Google Chrome")
    assert tracker_module.current_app_id is not None
    app1_id = tracker_module.current_app_id

    # 2. Advance time and change focus
    time_mock.current = 1050.0
    tracker_module.Change_of_focus("code", "main.py - project - Visual Studio Code")

    # App1 should have 50s recorded
    assert db_module.get_daytime_of(app1_id, datetime.date.today()) == 50.0

    assert tracker_module.current_app_id is not None
    app2_id = tracker_module.current_app_id
    assert app2_id != app1_id

    # 3. Advance time and blur (desktop focus)
    time_mock.current = 1070.0
    tracker_module.Change_of_focus("", "")

    assert db_module.get_daytime_of(app2_id, datetime.date.today()) == 20.0
    assert tracker_module.current_app_id is None

def test_process_hyprland_event(setup_tracker: typing.Any) -> None:
    time_mock = setup_tracker

    tracker_module.process_hyprland_event("activewindow>>kitty,zsh")
    assert tracker_module.current_app_id is not None
    kitty_id = tracker_module.current_app_id

    time_mock.current = 1010.0
    tracker_module.process_hyprland_event("activewindow>>google-chrome,Google")

    assert db_module.get_daytime_of(kitty_id, datetime.date.today()) == 10.0
    assert tracker_module.current_app_id is not None
