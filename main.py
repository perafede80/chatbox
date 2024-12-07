import asyncio
import os
from typing import Annotated

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Load the dotenv file for openai
load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")
openai.api_key = apikey

templates = Jinja2Templates(directory="templates")
chat_responses = []


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "chat_responses": chat_responses}
    )


chat_log = [
    {
        "role": "system",
        "content": "You are a Python tutor AI, completely dedicated to teach users how to learn \
                Python from scratch.Please provide clear instructions on Python conceprts, \
                best practices and syntax. Help create a path of learning for users to be able \
                to create real life, production ready python applications",
    }
]


@app.websocket("/ws")
async def chat(websocket: WebSocket):

    await websocket.accept()

    while True:
        user_input = await websocket.receive_text()
        chat_log.append({"role": "user", "content": user_input})
        chat_responses.append(user_input)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini", messages=chat_log, temperature=0.6, stream=True
            )

            ai_response = ""

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    ai_response += chunk.choices[0].delta.content
                    await websocket.send_text(chunk.choices[0].delta.content)
                    await asyncio.sleep(0.001)
            chat_responses.append(ai_response)

        except Exception as e:
            await websocket.send_text(f'Error: {str(e)}')
            break


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({"role": "user", "content": user_input})
    chat_responses.append(user_input)
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_log,
        temperature=0.6,
    )

    bot_response = completion.choices[0].message.content
    chat_log.append({"role": "assistant", "content": bot_response})
    chat_responses.append(bot_response)
    return templates.TemplateResponse(
        "home.html", {"request": request, "chat_responses": chat_responses}
    )


@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})


# The image generations endpoint allows you to create an original image given a text prompt.
# When using DALL·E 3, images can have a size of 1024x1024, 1024x1792 or 1792x1024 pixels.
@app.post("/image", response_class=HTMLResponse)
async def create_image(request: Request, user_input: Annotated[str, Form()]):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=user_input,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    return templates.TemplateResponse(
        "image.html", {"request": request, "image_url": image_url}
    )
