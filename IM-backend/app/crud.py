from sqlalchemy.orm import Session
from . import models, schemas, password
from fastapi import HTTPException
from .models import User

def get_user(db: Session, user_id: int):
    """
    获取用户
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    获取用户
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    创建新用户
    """
    hashed_password = password.get_password_hash(user.password) # assuming you have a password hashing function defined
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """
    更新用户信息
    """
    user = get_user(db, user_id)
    if user is None:
        return None

    # 检查新的用户名和邮箱是否已经被其他用户使用
    if db.query(User).filter(User.id != user_id, User.username == user_update.username).first():
        raise HTTPException(status_code=400, detail="Username already in use")
    if db.query(User).filter(User.id != user_id, User.email == user_update.email).first():
        raise HTTPException(status_code=400, detail="Email already in use")

    for var, value in vars(user_update).items():
        if value:  # 只有当 value 存在时，才进行赋值
            # 如果更新密码，确保密码被加密
            if var == 'password':
                value = password.get_password_hash(value)
            setattr(user, var, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_online_status(db: Session, user_id: int, online: bool):
    user = get_user(db, user_id=user_id)
    if user:
        user.online = online
        db.commit()

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return {"detail": f"User {user_id} has been deleted."}

def create_chat(db: Session, chat: schemas.ChatCreate, user_id: int):
    db_chat = models.Chat(**chat.dict(), owner_id=user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def get_friends(db: Session, user_id: int):
    """
    获取用户的所有好友
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user.friends

def get_messages(db: Session, user_id: int):
    """
    获取用户的所有消息
    """
    messages = db.query(models.Message).filter(models.Message.sender_id == user_id).all()
    return messages


def create_message(db: Session, message: schemas.MessageCreate):
    """
    创建新的消息
    """
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def add_friend(db: Session, user_id: int, friend_name: str):
    """
    添加好友
    """
    friend_id = get_user_by_username(db, friend_name).id
    if user_id == friend_id:
        raise ValueError("Cannot add oneself as a friend")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    friend = db.query(models.User).filter(models.User.username == friend_name).first()
    if friend not in user.friends:
        user.friends.append(friend)
        friend.friends.append(user)
        db.commit()
    return user

def get_or_create_chat(db: Session, sender_id: int, receiver_id: int):
    """
    根据发送者和接收者的 ID 获取或创建一个聊天
    """
    # 检查这两个用户是否已经有一个聊天了
    chat = db.query(models.Chat).join(models.Chat.users).filter(
        (models.User.id == sender_id) &
        (models.User.id == receiver_id) &
        (models.Chat.chat_type == "private")  # 这里我们设定私聊为 "private"
    ).first()

    # 如果没有找到聊天，那么我们就创建一个新的聊天
    if not chat:
        # 获取两个用户
        sender = get_user(db, sender_id)
        receiver = get_user(db, receiver_id)

        # 创建新的聊天并添加两个用户
        chat = models.Chat(chat_type="private")
        chat.users.append(sender)
        chat.users.append(receiver)

        db.add(chat)
        db.commit()
        db.refresh(chat)

    return chat
