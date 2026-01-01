"""Admin-facing API routes.

These endpoints provide read-only access to client data for
administrative and operational purposes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.client import Client
from backend.app.schemas.client import ClientResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get(
    "/clients",
    response_model=list[ClientResponse],
)
def list_clients(db: Session = Depends(get_db)):
    """Return a list of all registered clients.

    This endpoint is intended for internal administrative use only.
    """
    return db.query(Client).all()


@router.get(
    "/clients/{client_id}",
    response_model=ClientResponse,
)
def get_client(client_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a single client by its unique identifier.

    Raises a 404 error if the client does not exist.
    """
    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return client
