from starlette.testclient import TestClient

from app.core.config import settings


def test_create_message(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "conversation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "content": "this is content",
        "parent_id": "4fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
    response = client.post(
        f"{settings.API_V1_STR}/conversations/messages",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["content"] == data["content"]
    assert content["conversation_id"] == data["conversation_id"]
    assert "id" in content
    assert "created_time" in content
