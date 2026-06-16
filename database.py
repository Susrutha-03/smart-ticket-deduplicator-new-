import sqlite3
import json

DB_NAME = "tickets.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket TEXT NOT NULL,

            embedding TEXT NOT NULL,

            duplicate_count INTEGER DEFAULT 1,

            merged_tickets TEXT DEFAULT '[]'

        )
    """)

    conn.commit()
    conn.close()


def add_ticket(ticket, embedding):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tickets
        (ticket, embedding, duplicate_count, merged_tickets)

        VALUES (?, ?, ?, ?)
        """,
        (
            ticket,
            json.dumps(embedding.tolist()),
            1,
            json.dumps([])
        )
    )

    conn.commit()
    conn.close()


def get_all_tickets():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")

    rows = cursor.fetchall()

    conn.close()

    tickets = []

    for row in rows:

        tickets.append({

            "id": row[0],

            "ticket": row[1],

            "embedding": json.loads(row[2]),

            "duplicate_count": row[3],

            "merged_tickets": json.loads(row[4])

        })

    return tickets


def merge_ticket(ticket_id, new_ticket):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT duplicate_count,
        merged_tickets

        FROM tickets

        WHERE id=?
        """,

        (ticket_id,)
    )

    duplicate_count, merged = cursor.fetchone()

    merged = json.loads(merged)

    merged.append(new_ticket)

    duplicate_count += 1

    cursor.execute(

        """
        UPDATE tickets

        SET duplicate_count=?,
        merged_tickets=?

        WHERE id=?
        """,

        (
            duplicate_count,
            json.dumps(merged),
            ticket_id
        )
    )

    conn.commit()
    conn.close()