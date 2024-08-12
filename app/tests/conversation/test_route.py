from starlette.testclient import TestClient

from app.core.config import settings


def test_create_message_given_conversation_id(
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


def test_create_message_given_conversation_id_none(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "content": "this is content"
    }
    response = client.post(
        f"{settings.API_V1_STR}/conversations/messages",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["content"] == data["content"]
    assert content["conversation_id"] is not None
    assert content["parent_id"] is None
    assert "id" in content
    assert "created_time" in content


def test_list_messages_by_conversation_id(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data1 = {
        "content": "this is content 1"
    }
    response1 = client.post(
        f"{settings.API_V1_STR}/conversations/messages",
        headers=superuser_token_headers,
        json=data1,
    )
    assert response1.status_code == 200
    content1 = response1.json()
    conversation_id = content1["conversation_id"]
    assert conversation_id is not None
    assert content1["id"] is not None

    data2 = {
        "conversation_id": conversation_id,
        "content": "this is content 2",
        "parent_id": content1["id"]
    }
    response2 = client.post(
        f"{settings.API_V1_STR}/conversations/messages",
        headers=superuser_token_headers,
        json=data2,
    )

    assert response2.status_code == 200
    content2 = response2.json()
    assert content2["conversation_id"] is not None
    assert content2["id"] is not None
    assert content2["parent_id"] is not None

    response3 = client.get(
        f"{settings.API_V1_STR}/conversations/{conversation_id}/messages",
        headers=superuser_token_headers
    )
    assert response3.status_code == 200
    content3 = response3.json()
    assert content3["conversation_id"] is not None
    assert content3["messages"] is not None
    assert len(content3["messages"]) == 2
