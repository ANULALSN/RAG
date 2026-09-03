from app.db.database import (
    DATABASE_PATH,
    init_db,
)


def main():

    print("=" * 70)
    print("INITIALIZING SQLITE DATABASE")
    print("=" * 70)

    init_db()

    print(f"\nDatabase:")
    print(DATABASE_PATH)

    print("\nTables created:")
    print("- chat_sessions")
    print("- chat_messages")

    print("\nDatabase initialization successful.")


if __name__ == "__main__":
    main()