import datetime
import sqlite3

DB_PATH = "data.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_table() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # Create App table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS App (
            AppID INTEGER PRIMARY KEY AUTOINCREMENT,
            name_fenster TEXT NOT NULL,
            name_tab TEXT NOT NULL,
            UNIQUE(name_fenster, name_tab)
        )
    ''')

    # Create Aktionen table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Aktionen (
            AktionsID INTEGER PRIMARY KEY AUTOINCREMENT,
            Datum DATE NOT NULL,
            Beginn_Aktion REAL NOT NULL,
            Ende_Aktion REAL NOT NULL,
            AppID INTEGER NOT NULL,
            FOREIGN KEY(AppID) REFERENCES App(AppID)
        )
    ''')

    conn.commit()
    conn.close()

def register_app(name_fenster: str, name_tab: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO App (name_fenster, name_tab) VALUES (?, ?)',
            (name_fenster, name_tab)
        )
        conn.commit()
        app_id: int = cursor.lastrowid or 0
    except sqlite3.IntegrityError:
        # If it already exists, just return the existing ID
        cursor.execute(
            'SELECT AppID FROM App WHERE name_fenster = ? AND name_tab = ?',
            (name_fenster, name_tab)
        )
        result = cursor.fetchone()
        app_id = int(result['AppID'])

    conn.close()
    return app_id

def is_app_registered(name_fenster: str, name_tab: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT AppID FROM App WHERE name_fenster = ? AND name_tab = ?',
        (name_fenster, name_tab)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return int(result['AppID'])
    else:
        return register_app(name_fenster, name_tab)

def Write_Aktion(
    datum: datetime.date, beginn_aktion: float, ende_aktion: float, app_id: int
) -> None:
    if ende_aktion <= beginn_aktion:
        return # invalid action

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO Aktionen (Datum, Beginn_Aktion, Ende_Aktion, AppID) '
        'VALUES (?, ?, ?, ?)',
        (datum.strftime("%Y-%m-%d"), beginn_aktion, ende_aktion, app_id)
    )

    conn.commit()
    conn.close()

def get_daytime_of(app_id: int, datum: datetime.date) -> float:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT SUM(Ende_Aktion - Beginn_Aktion) as total_time
        FROM Aktionen
        WHERE AppID = ? AND Datum = ?
    ''', (app_id, datum.strftime("%Y-%m-%d")))

    result = cursor.fetchone()
    conn.close()

    if result and result['total_time'] is not None:
        return float(result['total_time'])
    return 0.0

def get_all_daytime(datum: datetime.date) -> float:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT SUM(Ende_Aktion - Beginn_Aktion) as total_time
        FROM Aktionen
        WHERE Datum = ?
    ''', (datum.strftime("%Y-%m-%d"),))

    result = cursor.fetchone()
    conn.close()

    if result and result['total_time'] is not None:
        return float(result['total_time'])
    return 0.0
