from app.db.database import (
    SessionLocal,
    init_db,
)

from app.db.chat_repository import (
    create_chat,
    delete_chat,
    get_chat,
    get_chat_messages,
    get_chats_by_subject,
)


def main():

    print("=" * 70)
    print("CHAT REPOSITORY TEST")
    print("=" * 70)

    init_db()

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # Create
        # --------------------------------------------------

        chat = create_chat(
            db=db,
            subject_id="big-data",
        )

        print("\nCreated chat:")
        print(f"ID: {chat.id}")
        print(f"Subject: {chat.subject_id}")
        print(f"Title: {chat.title}")

        # --------------------------------------------------
        # Get
        # --------------------------------------------------

        retrieved = get_chat(
            db,
            chat.id,
        )

        print("\nRetrieved chat:")

        if retrieved:
            print(f"ID: {retrieved.id}")
            print(f"Subject: {retrieved.subject_id}")
            print(f"Title: {retrieved.title}")

        # --------------------------------------------------
        # List by subject
        # --------------------------------------------------

        chats = get_chats_by_subject(
            db,
            "big-data",
        )

        print(
            f"\nChats for big-data: "
            f"{len(chats)}"
        )

        # --------------------------------------------------
        # Messages
        # --------------------------------------------------

        messages = get_chat_messages(
            db,
            chat.id,
        )

        print(
            f"Messages: {len(messages)}"
        )

        # --------------------------------------------------
        # Delete
        # --------------------------------------------------

        deleted = delete_chat(
            db,
            chat.id,
        )

        print(
            f"\nDeleted: {deleted}"
        )

        # --------------------------------------------------
        # Verify deletion
        # --------------------------------------------------

        deleted_chat = get_chat(
            db,
            chat.id,
        )

        print(
            f"Exists after deletion: "
            f"{deleted_chat is not None}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()