import sqlite3
import datetime
import bcrypt
import config


def init_db():
    """Initialize SQLite database."""

    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

       
        # Chats Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        # Users Table

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create Default Admin

        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        if count == 0:
            password_hash = bcrypt.hashpw(
                "apexyam123".encode(),
                bcrypt.gensalt()
            ).decode()

            cursor.execute("""
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
            """, ("admin", password_hash))

            print("Default admin account created.")
            print("Username: admin")
            print("Password: apexyam123")

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Database init error: {e}")


def save(session: str, role: str, message: str):
    """Save a chat message."""

    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

        timestamp = datetime.datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO chats (session, role, message, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (session, role, message, timestamp)
        )

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Save error: {e}")


def get_recent(session: str, limit: int = 20) -> list:
    """Get recent chat messages."""

    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role, message, timestamp
            FROM chats
            WHERE session = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session, limit)
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "role": row[0],
                "message": row[1],
                "timestamp": row[2]
            }
            for row in reversed(rows)
        ]

    except Exception as e:
        print(f"Get recent error: {e}")
        return []


def search(keyword: str) -> list:
    """Search chat history."""

    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT session, role, message, timestamp
            FROM chats
            WHERE message LIKE ?
            ORDER BY id DESC
            """,
            (f"%{keyword}%",)
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "session": row[0],
                "role": row[1],
                "message": row[2],
                "timestamp": row[3]
            }
            for row in rows
        ]

    except Exception as e:
        print(f"Search error: {e}")
        return []


def clear(session: str = None):
    """Clear chat history."""

    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

        if session:
            cursor.execute(
                "DELETE FROM chats WHERE session = ?",
                (session,)
            )
        else:
            cursor.execute("DELETE FROM chats")

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Clear error: {e}")