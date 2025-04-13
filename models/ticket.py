from pydantic import BaseModel
from typing import Optional

class TicketCreateRequest(BaseModel):
    project_id: int
    subject: str
    description: Optional[str] = None
    tracker_id: Optional[int] = None
    assigned_to_id: Optional[int] = None