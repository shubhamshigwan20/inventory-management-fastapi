from pydantic import BaseModel, Field

class RegisterReq(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=6, max_length=255)

class LoginReq(BaseModel):
    email: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=6, max_length=255)