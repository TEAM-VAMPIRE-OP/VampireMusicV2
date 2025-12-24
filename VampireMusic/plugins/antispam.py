import time
from collections import defaultdict
from pyrogram import Client, filters

# ================= CONFIG =================

# Flood data
USER_FLOOD = defaultdict(list)

# Chats where antispam is enabled
ANTISPAM_CHATS = set()

# ========================================


@Client.on_message(filters.command("antispam") & filters.group)
async def antispam_toggle(client, message):
    try:
        member = await client.get_chat_member(
            message.chat.id, message.from_user.id
        )
        if member.status not in ("administrator", "creator"):
            return

        chat_id = message.chat.id
        text = message.text.lower()

        if "on" in text:
            ANTISPAM_CHATS.add(chat_id)
            await message.reply("✅ **ANTISPAM ON**")

        elif "off" in text:
            ANTISPAM_CHATS.discard(chat_id)
            await message.reply("❌ **ANTISPAM OFF**")

        else:
            await message.reply(
                "**Use:**\n"
                "`/antispam on`\n"
                "`/antispam off`"
            )

    except Exception:
        return


@Client.on_message(filters.group & filters.text)
async def antispam_handler(client, message):
    try:
        chat_id = message.chat.id

        # ❌ Antispam disabled
        if chat_id not in ANTISPAM_CHATS:
            return

        if not message.from_user or message.from_user.is_bot:
            return

        # Admin bypass
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status in ("administrator", "creator"):
            return

        text = message.text or ""

        # Command bypass
        if text.startswith(("/", "!", ".")):
            return

        uid = message.from_user.id
        now = time.time()

        # -------- FLOOD CHECK (5 sec) --------
        USER_FLOOD[uid].append(now)
        USER_FLOOD[uid] = [t for t in USER_FLOOD[uid] if now - t < 5]

        if len(USER_FLOOD[uid]) >= 6:
            await message.delete()
            return

        # -------- LINK SPAM --------
        if "http://" in text or "https://" in text or "t.me/" in text:
            await message.delete()
            return

        # -------- CAPS SPAM --------
        if text.isupper() and len(text) > 8:
            await message.delete()
            return

    except Exception:
        return
