from pydantic import BaseModel

class Comment(BaseModel):
    text: str
    blog_id: str
