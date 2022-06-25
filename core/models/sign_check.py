from pydantic import BaseModel


class SignFileCheck(BaseModel):
    public_key: str
    signature: str
