import uuid

from backend.app.models.client import Client
from backend.app.models.handoff import HandoffStatus
from backend.app.services.handoff_service import create_handoff_ticket


def test_create_handoff_ticket(db):
    # 1️⃣ Create real client
    client = Client(
        id=uuid.uuid4(),
        email="handoff@test.com",
        hashed_password="x",
        company_name="Test Co",
    )
    db.add(client)
    db.commit()
    db.refresh(client)

    # 2️⃣ Create handoff ticket
    ticket = create_handoff_ticket(
        client_id=client.id,
        query="What is quantum gravity?",
        context="AI response was unclear",
        db=db
    )

    # 3️⃣ Hard assertions (persistence + correctness)
    assert ticket.id is not None
    assert ticket.client_id == client.id

    assert ticket.query_text == "What is quantum gravity?"
    assert ticket.context == "AI response was unclear"

    assert ticket.status == HandoffStatus.OPEN
    assert ticket.status.value == "open"
