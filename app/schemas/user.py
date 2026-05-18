from pydantic import BaseModel, ConfigDict, Field
from typing import List
from datetime import date

class UserCreate(BaseModel):
    name: str = Field(min_length=1) # Validation 활요 가능
    gender: str
    birth_date: date

class UserRead(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    total: int
    users: List[UserRead]