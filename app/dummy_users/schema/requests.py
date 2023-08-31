from typing import Optional
from pydantic import BaseModel, Field


class DummyUserRequestSchema(BaseModel):
    email: Optional[str] = Field(None, description="Email")
    nickname: Optional[str] = Field(None, description="nick-name")
