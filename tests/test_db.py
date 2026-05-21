import typing
import datetime
import os
import sqlite3

import pytest

import src.database.db as db_module
from src.database.db import (
    Write_Aktion,
    get_all_daytime,
    get_daytime_of,
    init_table,
    is_app_registered,
    register_app,
)


@pytest.fixture(autouse=True)
def run_around_tests() -> typing.Generator[None, None, None]:
    # Setup
    db_module.DB_PATH = "test_data.db"
    if os.path.exists(db_module.DB_PATH):
        os.remove(db_module.DB_PATH)
    init_table()

    yield

    # Teardown
    if os.path.exists(db_module.DB_PATH):
        os.remove(db_module.DB_PATH)

def test_init_table() -> None:
    assert os.path.exists(db_module.DB_PATH)
    conn = sqlite3.connect(db_module.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "App" in tables
    assert "Aktionen" in tables
    conn.close()

def test_register_and_is_app_registered() -> None:
    app_id = register_app("Google Chrome", "YouTube")
    assert app_id > 0

    # Check if duplicate is handled correctly
    duplicate_app_id = register_app("Google Chrome", "YouTube")
    assert duplicate_app_id == app_id

    # Check is_app_registered
    fetched_app_id = is_app_registered("Google Chrome", "YouTube")
    assert fetched_app_id == app_id

    # is_app_registered should create an app if it doesn't exist
    new_app_id = is_app_registered("Firefox", "GitHub")
    assert new_app_id != app_id
    assert new_app_id > 0

def test_write_and_get_daytime() -> None:
    app1_id = register_app("Code", "bildschirm-zeit")
    app2_id = register_app("Chrome", "StackOverflow")

    today = datetime.date.today()

    # Valid actions
    Write_Aktion(today, 100.0, 150.0, app1_id) # 50s
    Write_Aktion(today, 200.0, 220.0, app2_id) # 20s
    Write_Aktion(today, 300.0, 310.0, app1_id) # 10s

    # Invalid action (should be ignored)
    Write_Aktion(today, 400.0, 390.0, app1_id)

    # Check daytime of app
    assert get_daytime_of(app1_id, today) == 60.0
    assert get_daytime_of(app2_id, today) == 20.0

    # Check total daytime
    assert get_all_daytime(today) == 80.0

    # Check daytime for another date
    tomorrow = today + datetime.timedelta(days=1)
    assert get_daytime_of(app1_id, tomorrow) == 0.0
    assert get_all_daytime(tomorrow) == 0.0
