import pandas as pd
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from anomaly_cluster_check import check_wa_chat_anomaly_level

TOKEN = '6969886688:AAHwxexoZyEk23CkXfGZsq0UFDez9nk_Bfg'
BOT_USERNAME = '@data_anomaly_bot'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!. Akses menu /upload_wa_exported_chat untuk upload file hasil export dari WhatsApp",
        reply_markup=ForceReply(selective=True),
    )


async def upload_wa_exported_chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Silahkan upload file hasil export chat dari WhatsApp dengan ekstensi .txt')


async def handle_upload_wa_exported_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.document.get_file()
    await file.download_to_drive('data.txt')

    result = check_wa_chat_anomaly_level('data.txt')

    await update.message.reply_text(result)


# Handling non-XLSX files separately
async def handle_unknown_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hanya file hasil export dari WhatsApp yang diperbolehkan dengan ekstensi .txt")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main() -> None:
    """Start the bot."""
    print('Starting bot...')
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("upload_wa_exported_chat", upload_wa_exported_chat_message))
    application.add_handler(MessageHandler(filters.Document.FileExtension('txt'), handle_upload_wa_exported_chat))
    application.add_handler(MessageHandler(~filters.Document.FileExtension('txt'), handle_unknown_file))

    # Run the bot until the user presses Ctrl-C
    print('Polling...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()