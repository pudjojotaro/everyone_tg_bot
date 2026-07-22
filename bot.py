import logging
import os
import re
import sqlite3

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
DB_PATH = os.environ.get("DB_PATH", "bot.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MENTIONS_PER_MESSAGE = 5

db = sqlite3.connect(DB_PATH)
db.execute(
    """
    CREATE TABLE IF NOT EXISTS seen_users (
        chat_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        display_name TEXT NOT NULL,
        PRIMARY KEY (chat_id, user_id)
    )
    """
)
db.commit()


def escape_markdown(text: str) -> str:
    return re.sub(r"([_*\[\]()~`>#+\-=|{}.!\\])", r"\\\1", text)


async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remember every user who sends a message, so /all has someone to tag."""
    message = update.effective_message
    user = update.effective_user
    if not message or not user or user.is_bot:
        return

    display_name = user.first_name or user.username or "someone"
    db.execute(
        "INSERT INTO seen_users (chat_id, user_id, display_name) VALUES (?, ?, ?) "
        "ON CONFLICT (chat_id, user_id) DO UPDATE SET display_name = excluded.display_name",
        (update.effective_chat.id, user.id, display_name),
    )
    db.commit()


async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rows = db.execute(
        "SELECT user_id, display_name FROM seen_users WHERE chat_id = ?",
        (update.effective_chat.id,),
    ).fetchall()

    if not rows:
        await update.effective_message.reply_text(
            "I haven't seen anyone talk in this chat yet, so I have no one to tag.\n"
            "I remember people once they send at least one message after I've joined."
        )
        return

    mentions = [
        f"[{escape_markdown(name)}](tg://user?id={user_id})" for user_id, name in rows
    ]

    for i in range(0, len(mentions), MENTIONS_PER_MESSAGE):
        chunk = mentions[i : i + MENTIONS_PER_MESSAGE]
        await update.effective_message.reply_text(
            " ".join(chunk), parse_mode=ParseMode.MARKDOWN_V2
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Hi! Add me to a group and make me an admin (any rights are fine) so I can see all "
        "messages. I'll quietly remember who talks, then /all will tag everyone I've seen."
    )


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("all", tag_all))
    # Runs after the command handlers above, so it logs the sender of every message
    # (including commands) without interfering with them.
    application.add_handler(MessageHandler(filters.ALL, track_user), group=1)

    logger.info("Bot starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
