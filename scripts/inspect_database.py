import sqlite3

from app.db.database import DATABASE_PATH


def main():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    )

    tables = cursor.fetchall()

    print("=" * 70)
    print("SQLITE DATABASE INSPECTION")
    print("=" * 70)

    print("\nTables:")

    for (table,) in tables:
        print(f"- {table}")

    connection.close()


if __name__ == "__main__":
    main()