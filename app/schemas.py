from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

# ----- Post Schemas -----
class PostCreate(BaseModel):
    title: str
    body: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be blank")
        return v.strip()  # Also cleans whitespace on the way in

class PostResponse(BaseModel):
    id: int
    title: str
    body: Optional[str] = None
    author_id: int          # FK reference — useful for the frontend
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
# ----- User Schemas -----

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}
    
# ----- Auth Schemas -----

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"