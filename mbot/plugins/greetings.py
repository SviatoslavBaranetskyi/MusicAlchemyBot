from datetime import datetime
from os import execvp, sys

from pyrogram import filters, Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from mbot import AUTH_CHATS, LOG_GROUP, OWNER_ID, SUDO_USERS, Mbot

api_id = 'your_api_id'
api_hash = "your_api_hash"
bot_token = "your_bot_token"

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

subscribed_channels = [-1001183917303, -1001989547742, -1001659755474]

async def check_subscriptions(user_id):
    subscribed = True
    async with app:
        try:
            for channel_id in subscribed_channels:
                member = await app.get_chat_member(channel_id, user_id)
                if member.status == 'kicked':
                    subscribed = False
                    break
        except UserNotParticipant:
            return False
    return subscribed


@Mbot.on_message(filters.command("start"))
async def start(client, message):
    reply_markup = [
        [
            InlineKeyboardButton(text="1 Channel",
                                 url="https://t.me/muzzloman"),
            InlineKeyboardButton(text="2 Channel",
                                 url="https://t.me/xGloryToUkrainex"),
            InlineKeyboardButton(text="3 Channel",
                                 url="https://t.me/News0fUkraine"),
        ],
        [
            InlineKeyboardButton(text="Download Music", callback_data="helphome"),
        ],
    ]
    if LOG_GROUP:
        invite_link = await client.create_chat_invite_link(
            chat_id=(
                int(LOG_GROUP)
                if str(LOG_GROUP).startswith("-100")
                else LOG_GROUP
            )
        )
        reply_markup.append(
            [InlineKeyboardButton("LOG Channel", url=invite_link.invite_link)]
        )
    if (
            message.chat.type != "private"
            and message.chat.id not in AUTH_CHATS
            and message.from_user.id not in SUDO_USERS
    ):
        return await message.reply_text(
            "This Bot Will Not Work In Groups Unless It's Authorized.",
            reply_markup=InlineKeyboardMarkup(reply_markup),
        )

    return await message.reply_text(
        f"Hello {message.from_user.first_name}, Welcome to MusicAlchemy!\nI can Download Music from Streaming Services for You.",
        reply_markup=InlineKeyboardMarkup(reply_markup),
    )


@Mbot.on_message(
    filters.command("restart") & filters.chat(OWNER_ID) & filters.private
)
async def restart(_, message):
    await message.delete()
    execvp(sys.executable, [sys.executable, "-m", "mbot"])


@Mbot.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_, message):
    await message.reply_document("bot.log")


@Mbot.on_message(filters.command("ping"))
async def ping(client, message):
    start = datetime.now()
    #await client.send(Ping(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    await message.reply_text(f"**Pong!**\nResponse time: `{ms} ms`")


HELP = {
    "Youtube": "Send **Youtube** Link in Chat to Download Song.",
    "Spotify": "Send **Spotify** Track/Playlist/Album/Show/Episode's Link. I'll Download It For You.",
    "Deezer": "Send Deezer Playlist/Album/Track Link. I'll Download It For You.",
    "Jiosaavn": "Not Implemented yet",
    "SoundCloud": "Not Implemented yet",
    "Group": "Will add later.",
}


@Mbot.on_message(filters.command("help"))
async def help(_, message):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    user_id = message.from_user.username
    subscribed = await check_subscriptions(user_id)
    if subscribed:
        await message.reply_text(
            f"Hello **{message.from_user.first_name}**, I'm **@MusicAlchemyBot**.\nI'm Here to download your music.",
            reply_markup=InlineKeyboardMarkup(button),
        )
    else:
        await message.reply_text(
            "Please subscribe to all the required channels to proceed.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="1 Channel",
                                      url="https://t.me/muzzloman"),
                 InlineKeyboardButton(text="2 Channel",
                                      url="https://t.me/xGloryToUkrainex"),
                 InlineKeyboardButton(text="3 Channel",
                                      url="https://t.me/News0fUkraine")],
                [InlineKeyboardButton(text="Download Music",
                                      callback_data="helphome")],
            ]),)


@Mbot.on_callback_query(filters.regex(r"help_(.*?)"))
async def helpbtn(_, query):
    i = query.data.replace("help_", "")
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Back", callback_data="helphome")]]
    )
    text = f"Help for **{i}**\n\n{HELP[i]}"
    await query.message.edit(text=text, reply_markup=button)


@Mbot.on_callback_query(filters.regex(r"helphome"))
async def help_home(_, query):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    user_id = query.from_user.username
    subscribed = await check_subscriptions(user_id)
    if subscribed:
        await query.message.edit(
            f"Hello **{query.from_user.first_name}**, I'm **@MusicAlchemyBot**.\nI'm Here to download your music.",
            reply_markup=InlineKeyboardMarkup(button),
        )
    else:
        await query.message.edit(
            "Please subscribe to all the required channels to proceed.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="1 Channel",
                                      url="https://t.me/muzzloman"),
                 InlineKeyboardButton(text="2 Channel",
                                      url="https://t.me/xGloryToUkrainex"),
                 InlineKeyboardButton(text="3 Channel",
                                      url="https://t.me/News0fUkraine")],
                [InlineKeyboardButton(text="Download Music",
                                      callback_data="helphome")],
            ]),)
