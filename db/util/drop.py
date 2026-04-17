import sqlite3


def drop_tables(conn):
    """
    Drop tables in the SQLite database.
    """
    try:
        cursor = conn.cursor()
        cursor.executescript('''
            DROP TABLE IF EXISTS transactions;
            DROP TABLE IF EXISTS appointment_tracking;
            DROP TABLE IF EXISTS appointments;
            DROP TABLE IF EXISTS services;
            DROP TABLE IF EXISTS users;
        ''')
        print("Tables dropped successfully.")
    except sqlite3.Error as e:
        print(f"Error dropping tables: {e}")
