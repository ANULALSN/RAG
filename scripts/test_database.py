from app.db.database import (
    DATABASE_PATH,
    engine,
)


def main():

    print("=" * 70)
    print("SQLITE DATABASE TEST")
    print("=" * 70)

    print(f"\nDatabase path:")
    print(DATABASE_PATH)

    print("\nDatabase URL:")
    print(engine.url)

    print("\nSQLite foundation loaded successfully.")


if __name__ == "__main__":
    main()