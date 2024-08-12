import uuid

from app.basic.models import User
from app.conversation import crud, models
from sqlmodel import Session

from app.conversation.models import Message, ConversationMessages


def create_user_message(session: Session, current_user: User, user_message_create: models.UserMessageCreate) -> Message:
    if user_message_create.conversation_id is None:
        conversation = crud.create_conversation(session=session, user_id=current_user.id)
        user_message_create.conversation_id = conversation.id
    return crud.create_user_message(session=session, user_message_create=user_message_create, user=current_user)


def list_messages(session: Session, current_user: User, conversation_id: uuid.UUID):
    conversation = crud.get_conversation(session=session, conversation_id=conversation_id)
    messages = crud.get_messages_by_conversation_id(session=session, conversation_id=conversation_id)

    return ConversationMessages(conversation_id=conversation_id,
                                user_id=current_user.id,
                                messages=messages,
                                created_time=conversation.created_time)
