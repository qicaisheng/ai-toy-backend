import uuid
from typing import Optional

from sqlmodel import Session

from app.basic.models import User
from app.conversation.models import Conversation, Message, Author, UserMessageCreate


def create_conversation(*, session: Session, user_id: uuid.UUID) -> Conversation:
    db_obj = Conversation(user_id=user_id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_conversation(session, conversation_id: uuid.UUID):
    return session.query(Conversation).filter(Conversation.id == conversation_id).first()


def create_message(*, session: Session, conversation_id: uuid.UUID, content: str, author: Author,
                   parent_id: Optional[uuid.UUID] = None, audio_id: Optional[int] = None) -> Message:
    author_dict = dict(author)
    db_obj = Message(
        conversation_id=conversation_id,
        content=content,
        author=author_dict,
        parent_id=parent_id,
        audio_id=audio_id
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def create_user_message(*, session: Session, user_message_create: UserMessageCreate, user: User) -> Message:
    name = ""
    if user.full_name is not None:
        name = user.full_name
    author_dict = dict(Author(role='user', name=name))
    db_obj = Message(
        conversation_id=user_message_create.conversation_id,
        content=user_message_create.content,
        author=author_dict,
        parent_id=user_message_create.parent_id,
        audio_id=user_message_create.audio_id
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_message(session, message_id: uuid.UUID) -> Message:
    message = session.get(Message, message_id)
    return message
