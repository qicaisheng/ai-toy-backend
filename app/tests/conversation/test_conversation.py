import uuid

from sqlmodel import Session
from datetime import datetime
from app.conversation import crud
from app.conversation.models import Author, Message


def test_create_conversation(db: Session) -> None:
    user_id = uuid.uuid4()
    conversation = crud.create_conversation(session=db, user_id=user_id)

    assert conversation is not None
    assert conversation.id is not None
    assert conversation.user_id == user_id


def test_get_conversation(db: Session) -> None:
    user_id = uuid.uuid4()
    conversation = crud.create_conversation(session=db, user_id=user_id)
    conversation_by_id = crud.get_conversation(session=db, conversation_id=conversation.id)

    assert conversation_by_id is not None
    assert conversation_by_id.id is conversation.id
    assert conversation_by_id.user_id == user_id


def test_create_message(db: Session) -> None:
    conversation_id = uuid.uuid4()
    author = Author(role="user", name="John Doe")
    content = "this is content"
    message = crud.create_message(session=db, conversation_id=conversation_id, content=content, author=author)

    message_by_id = crud.get_message(session=db, message_id=message.id)

    assert message_by_id is not None
    assert message_by_id.conversation_id == conversation_id
    assert message_by_id.content == content
    assert message_by_id.author == dict(author)
    assert isinstance(message_by_id.created_time, datetime)
