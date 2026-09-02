from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    login: str = Field(..., min_length=3, max_length=50, examples=["admin"])
    password: str = Field(..., min_length=8, max_length=128, examples=["strongpassword"])


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIs..."])


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"