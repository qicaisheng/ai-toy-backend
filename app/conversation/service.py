from app.basic.models import User
from app.conversation import crud, models
from sqlmodel import Session

from app.conversation.models import Message


def create_user_message(session: Session, current_user: User, user_message_create: models.UserMessageCreate) -> Message:
    return crud.create_user_message(session=session, user_message_create=user_message_create, user=current_user)
