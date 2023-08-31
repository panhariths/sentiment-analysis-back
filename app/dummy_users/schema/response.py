from pydantic import BaseModel, Field


class DummyUsersResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="nick-name")

    class Config:
        orm_mode = True
