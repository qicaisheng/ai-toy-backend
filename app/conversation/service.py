from app.basic.models import User
from app.conversation import crud, models
from sqlmodel import Session

from app.conversation.models import Message


def create_user_message(session: Session, current_user: User, user_message_create: models.UserMessageCreate) -> Message:
    if user_message_create.conversation_id is None:
        conversation = crud.create_conversation(session=session, user_id=current_user.id)
        user_message_create.conversation_id = conversation.id
    return crud.create_user_message(session=session, user_message_create=user_message_create, user=current_user)

