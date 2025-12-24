import time
from collections import defaultdict
from pyrogram import Client, filters

user_flood = defaultdict(list)

@Client.on_message(filters.group & filters.text)
async def antispam_handler(client, message):
    try:
        if not message.from_user:
            return
        if message.from_user.is_bot:
            return

        # Admin bypass
        member = await client.get_chat_member(
            message.chat.id, message.from_user.id
        )
        if member.status in ("administrator", "creator"):
            return

        uid = message.from_user.id
        now = time.time()

        # Flood check (5 sec window)
        user_flood[uid].append(now)
        user_flood[uid] = [t for t in user_flood[uid] if now - t < 5]

        if len(user_flood[uid]) >= 6:
            await message.delete()
            return

        text = message.text or ""

        # Link spam
        if "http://" in text or "https://" in text or "t.me/" in text:
            await message.delete()
            return

        # CAPS spam
        if text.isupper() and len(text) > 8:
            await message.delete()
            return

    except Exception:
        return
