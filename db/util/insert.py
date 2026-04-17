import sqlite3


def insert_data(conn):
    try:
        cursor = conn.cursor()

        cursor.execute('''
            DROP TABLE IF EXISTS services
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        # Create a table if it doesn't exist
        services = [
            ('Diagnostics Test', 'Comprehensive vehicle diagnostics to identify engine and system issues.', 170.00),
            ('Engine Service', 'Full engine check-up, oil and filter change, and performance tuning.', 280.99),
            ('Tires Replacement', 'Replacement of worn-out tires with balancing and alignment.', 239.99),
            ('Oil Changing', 'Changing engine oil and replacing the oil filter to improve engine performance.', 15.00),
            ('Brake Repair', 'Inspection and replacement of brake pads, rotors, and fluid for safer driving.', 30.99),
            ('Car Wash & Detailing', 'Thorough interior and exterior cleaning, polishing, and waxing.', 149.99)
        ]


        cursor.executemany('''
            INSERT INTO services (name, description, price) VALUES (?, ?, ?)
        ''', services)

    except sqlite3.Error as e:
        print(f"Error inserting services: {e}")