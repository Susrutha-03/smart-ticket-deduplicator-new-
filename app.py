import streamlit as st

from database import (
    init_db,
    get_all_tickets,
    add_ticket,
    merge_ticket
)
from agent import agent_loop
from cluster import build_clusters

init_db()

st.set_page_config(
    page_title="Smart Ticket Deduplicator",
    page_icon="🎫",
    layout="wide"
)

st.title("🧠 Smart Ticket Deduplicator")

st.caption(
    "AI-powered semantic duplicate detection & ticket merging"
)

tickets = get_all_tickets()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Master Tickets", len(tickets))

duplicates = 0

for ticket in tickets:
    duplicates += ticket["duplicate_count"] - 1

with col2:
    st.metric("Merged Duplicate Tickets", duplicates)

st.divider()

st.subheader("📝 Create Ticket")

ticket = st.text_area(
    "Describe your issue",
    height=120
)

if st.button("Submit Ticket"):

    if ticket.strip() == "":
        st.warning("Please enter a ticket.")

    else:

        database = get_all_tickets()

        result = agent_loop(ticket, database)

        if result["decision"] == "duplicate":

            merge_ticket(
                result["match"]["id"],
                ticket
            )

            st.error("Duplicate Ticket Detected")

            st.write("### Existing Ticket")

            st.success(result["match"]["ticket"])

            st.write(
                "Similarity Score:",
                round(result["score"], 2)
            )

            st.write(
                "Duplicate Count:",
                result["match"]["duplicate_count"] + 1
            )

        else:

            add_ticket(
                ticket,
                result["embedding"]
            )

            st.success("New Ticket Added Successfully")
        st.subheader("🤖 Agent Reasoning")

        for step in result["reasoning"]:
            st.write("✅", step)

        st.info("Decision completed successfully.")

        if st.button("Refresh Dashboard"):
            st.rerun()

st.divider()

st.subheader("🧩 Ticket Clusters")

clusters = build_clusters()

if len(clusters) == 0:

    st.info("No tickets available.")

else:

    for index, cluster in enumerate(clusters):

        st.markdown(
            f"### Cluster {index + 1} ({len(cluster)} tickets)"
        )

        for ticket in cluster:

            st.write(
                "•",
                ticket["ticket"]
            )
            if ticket["duplicate_count"] > 1:

                st.caption(
                    f"Duplicates merged: {ticket['duplicate_count']}"
                )

        st.divider()

st.subheader("📋 Master Tickets")

database = get_all_tickets()

for ticket in database:

    with st.expander(ticket["ticket"]):

        st.write(
            "Duplicate Count:",
            ticket["duplicate_count"]
        )

        if len(ticket["merged_tickets"]) > 0:

            st.write("Merged Tickets")

            for duplicate in ticket["merged_tickets"]:

                st.write("•", duplicate)