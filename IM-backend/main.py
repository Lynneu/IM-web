from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Dict
import json
from datetime import datetime

from app import crud, models, schemas, password
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 设置跨域
origins = [
    "http://localhost:8080",
    "http://172.20.10.2:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/conversations/{user_id}", response_model=List[schemas.Chat])
def read_user_conversations(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.chats

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.User)
def login_for_access_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not password.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    print(user_update)
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = crud.delete_user(db, user_id=user_id)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return response

@app.post("/users/{user_id}/chats/", response_model=schemas.Chat)
def create_chat_for_user(user_id: int, chat: schemas.ChatCreate, db: Session = Depends(get_db)):
    return crud.create_chat(db=db, chat=chat, user_id=user_id)

@app.get("/chats/{chat_id}", response_model=schemas.Chat)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = crud.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

@app.get("/users/{user_id}/friends", response_model=List[schemas.User])
def read_user_friends(user_id: int, db: Session = Depends(get_db)):
    friends = crud.get_friends(db, user_id=user_id)
    return friends

@app.post("/users/{user_id}/messages/", response_model=schemas.Message)
def create_message_for_user(user_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@app.get("/users/{user_id}/messages", response_model=List[schemas.Message])
def read_user_messages(user_id: int, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, user_id=user_id)
    return messages

@app.put("/users/{user_id}/friends/{friend_name}")
def add_friend(user_id: int, friend_name: str, db: Session = Depends(get_db)):
    return crud.add_friend(db, user_id=user_id, friend_name=friend_name)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)

    def disconnect(self, client_id: int, websocket: WebSocket):
        self.active_connections[client_id].remove(websocket)
        if not self.active_connections[client_id]:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: int):
        for websocket in self.active_connections[client_id]:
            await websocket.send_text(message)

    async def send_group_message(self, message: str, group_ids: List[int]):
        for id in group_ids:
            if id in self.active_connections:
                await self.send_personal_message(message, id)

    async def broadcast_online_status(self, client_id: int, db: Session):
        friends = crud.get_friends(db, client_id)
        for friend in friends:
            if friend.id in self.active_connections:
                await self.send_personal_message(json.dumps({
                    'type': 'status',
                    'content': {
                        'user_id': client_id,
                        'status': 'online'
                    }
                }), friend.id)

    async def broadcast_offline_status(self, client_id: int, db: Session):
        friends = crud.get_friends(db, client_id)
        for friend in friends:
            if friend.id in self.active_connections:
                await self.send_personal_message(json.dumps({
                    'type': 'status',
                    'content': {
                        'user_id': client_id,
                        'status': 'offline'
                    }
                }), friend.id)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    await manager.connect(client_id, websocket)
    crud.update_online_status(db, client_id, True)
    await manager.broadcast_online_status(client_id, db)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            receiver_id = message['receiver_id']
            chat = crud.get_or_create_chat(db, client_id, receiver_id)
            users_in_chat = [user.id for user in chat.users]

            timestamp = datetime.now()

            message_json = json.dumps({"sender": client_id, "receiver": receiver_id, "content": message['content'], "type": "text", "timestamp": str(timestamp)})
            await manager.send_group_message(message_json, users_in_chat)
            message_to_create = schemas.MessageCreate(chat_id=chat.id, sender_id=client_id, content=message['content'], message_type='text', timestamp=timestamp)
            background_tasks.add_task(crud.create_message, db, message_to_create)

    except WebSocketDisconnect:
        manager.disconnect(client_id, websocket)
        crud.update_online_status(db, client_id, False)
        await manager.broadcast_offline_status(client_id, db)  # 更新
        # await manager.send_group_message(f"Client #{client_id} left the chat", users_in_chat)

    except json.JSONDecodeError:
        await manager.send_personal_message("Error: Message is not in the correct format.", client_id)

