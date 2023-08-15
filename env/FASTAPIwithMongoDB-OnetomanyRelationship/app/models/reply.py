from pydantic import BaseModel

class Reply(BaseModel):
    text: str
    comment_id: str
