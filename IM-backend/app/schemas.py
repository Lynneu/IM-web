from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    online: bool

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    chat_name: str

class ChatCreate(ChatBase):
    pass

class MessageBase(BaseModel):
    content: str
    message_type: str  # text, image, file etc.
    file_data: Optional[bytes] = None

class MessageCreate(MessageBase):
    chat_id: int
    sender_id: int

class Message(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class Chat(ChatBase):
    id: int
    messages: List[Message] = []
    class Config:
        orm_mode = True
