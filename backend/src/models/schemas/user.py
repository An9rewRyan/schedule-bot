from pydantic import BaseModel


class UserCreate(BaseModel):
    telegram_id: int
    first_name: str
    second_name: str
    phone_number: str
    age: int


class UserAuth(BaseModel):
    telegram_id: int
