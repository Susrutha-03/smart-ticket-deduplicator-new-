from database import init_db, add_ticket, merge_ticket, get_all_tickets
from deduplicator import detect_duplicate

init_db()

tickets = [

    "Unable to login to account",

    "Can't sign into my account",

    "Login failed after password reset",

    "Payment failed while purchasing",

    "Transaction was unsuccessful",

    "Payment gateway error",

    "Server timeout",

    "Connection timeout",

    "Unable to connect to server"

]

for ticket in tickets:

    database = get_all_tickets()

    result = detect_duplicate(ticket, database)

    if result["duplicate"]:

        merge_ticket(
            result["match"]["id"],
            ticket
        )

    else:

        add_ticket(
            ticket,
            result["embedding"]
        )

print("Sample data inserted successfully")