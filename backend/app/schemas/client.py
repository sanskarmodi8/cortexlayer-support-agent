"""Pydantic schemas for Client-related API responses.

These schemas define the exact structure of client data exposed
through admin-facing APIs and intentionally exclude sensitive fields
such as passwords and payment identifiers.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from backend.app.models.client import BillingStatus, PlanType


class ClientResponse(BaseModel):
    """Public, read-only representation of a client entity.

    This schema is used by admin APIs and omits sensitive internal
    fields such as hashed passwords and Stripe identifiers.
    """

    id: UUID
    email: EmailStr
    company_name: str

    plan_type: PlanType
    billing_status: BillingStatus

    is_active: bool
    is_disabled: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration.

        Enables loading data directly from ORM model attributes.
        """

        from_attributes = True
