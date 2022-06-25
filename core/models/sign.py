from pydantic import BaseModel


class SignFile(BaseModel):
    public_key: str
    signature: str
