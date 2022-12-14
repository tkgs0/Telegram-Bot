from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from utils.log import logger
from src.config import SUPERUSERS
from .utils import Status


def run(application):
    status_handler = CommandHandler(
        'status', status,
        filters.User(SUPERUSERS)
    )
    application.add_handler(status_handler)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg, _ = Status().get_status()
    await update.message.reply_text(msg)
