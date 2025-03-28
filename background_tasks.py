from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
import logging
import asyncio

app = FastAPI()


logging.basicConfig(level=logging.INFO)

class Email(BaseModel):
    email: str = Field(..., title="Email")
    name: str = Field(..., title="Ім'я")
    message: str = Field(..., title="Повідомлення")

def send_email(email: Email):
    asyncio.run(async_send_email(email))

async def async_send_email(email: Email):
    await asyncio.sleep(2)
    logging.info(f"Відправлено email з повідомленням: {email.message}")

def log_user(email: Email):
    logging.info(f"Користувач {email.name} з email {email.email} надіслав листа")

@app.post("/send-email/")
async def send_email_route(email: Email, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email)
    background_tasks.add_task(log_user, email)
    return {"message": "Відправлення листа"}
