from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.deps import get_current_active_superuser
from app.basic.models import NotifyMessage
from app.basic.utils import generate_test_email, send_email

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> NotifyMessage:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return NotifyMessage(message="Test email sent")
