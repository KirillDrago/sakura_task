import asyncio
import time

from telethon import TelegramClient
from dotenv import load_dotenv
from telethon.tl.functions.messages import ToggleDialogPinRequest

load_dotenv()

API_ID = "API_ID"  # should to be int
API_HASH = "API_HASH"
PHONE = "PHONE"


client = TelegramClient("session", API_ID, API_HASH)


async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        await client.sign_in(PHONE, input("Введите код из СМС: "))

    chats = await client.get_dialogs()
    groups = []
    for chat in chats:
        if chat.is_group:
            groups.append(chat)

    for group in groups:
        await client.edit_folder(group, 1)
        time.sleep(1)
        await client(ToggleDialogPinRequest(
            peer=group,
            pinned=True
        ))
        print(f"{group.title} добавлен в архив и закреплен")
        time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
