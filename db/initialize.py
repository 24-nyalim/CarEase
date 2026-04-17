from util.create import create_tables
from util.insert import insert_data
from util.drop import drop_tables
import sqlite3

def initialize():

    try:
        conn = sqlite3.connect("CarEase.db")
        drop_tables(conn)
        create_tables(conn)
        insert_data(conn)
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

initialize()

