import json
from typing import Any

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

from app.deps import SessionDep, CurrentUser
from app.conversation import conversation, service
from app.conversation.models import UserMessageCreate, Message
router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Children AI Assistant</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <div id='messages'>
        </div>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/v1/conversations/ws");
            var round = 0
            ws.onmessage = function(event) {
                var response = JSON.parse(event.data)
                var messages = document.getElementById('messages')
                var message = document.getElementsByClassName(response.round + " assistant")
                if (message.length == 1) {
                    message[0].textContent = message[0].textContent + response.output
                } else {
                    message = document.createElement('div')
                    message.setAttribute("class", response.round + " " + "assistant")
                    message.textContent = 'Assistant: ' + response.output   
                    messages.appendChild(message)
                }
            };
            function sendMessage(event) {
                round = round + 1
                var input = document.getElementById("messageText")
                ws.send(JSON.stringify({"round": round, "input": input.value}))
                var messages = document.getElementById('messages')
                var message = document.createElement('div')
                var user = document.createTextNode("User: ")
                var content = document.createTextNode(input.value)
                message.appendChild(user)
                message.appendChild(content)
                messages.appendChild(message)

                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/page")
async def list_conversations():
    return HTMLResponse(html)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        request = await websocket.receive_text()
        round = json.loads(request)['round']
        user_input = json.loads(request)['input']
        print(f"""User: {user_input}""")

        stream_response = conversation.answer(user_input)

        print("Assistant: ", end="")
        for output_text in stream_response:
            print(output_text, end="")
            await websocket.send_json({"round": round, "output": output_text})
        print("")


@router.post("/messages", response_model=Message)
async def create_message(session: SessionDep, current_user: CurrentUser, user_message_create: UserMessageCreate) -> Any:
    return service.create_user_message(session, current_user, user_message_create)
