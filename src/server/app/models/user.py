from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    # Add any other fields you need for your User model
