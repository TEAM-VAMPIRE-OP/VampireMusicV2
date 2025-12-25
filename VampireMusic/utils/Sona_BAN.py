from pyrogram import filters

async def _admin_check(_, __, message):
    if not message.from_user:
        return False
    try:
        member = await message.chat.get_member(message.from_user.id)
        return member.status in ("administrator", "creator")
    except:
        return False

admin_filter = filters.create(_admin_check)
