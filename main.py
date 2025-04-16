import cowsay
import requests
from telegram import Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          ContextTypes, MessageHandler, filters)

from config import config as cfg
from log_writer import log_writer

GPT_BASE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    log_writer.write_log(
        user_id=user.id,
        action="start",
    )
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\nWhat can Annihilator gun do for "
        f"you?\nTo list commands, type /help"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_writer.write_log(
        user_id=update.effective_user.id,
        action="echo",
    )
    await update.message.reply_text(update.message.text)


async def cow_say(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_writer.write_log(
        user_id=update.effective_user.id,
        action="cow_say",
    )
    splitted = update.message.text.split()
    if len(splitted) > 1:
        msg = " ".join(splitted[1:])
    else:
        msg = "Moo!"
    await update.message.reply_html(
        f"<code>{cowsay.get_output_string("cow", msg)}</code>"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_writer.write_log(
        user_id=update.effective_user.id,
        action="help",
    )
    help_text = [
        "/start - Start the bot",
        "/help - Show this help message",
        "/echo - Echo the message",
        "/cow_say - Cow says the message",
        "/annihilator_gun - Annihilator GUN!",
        "Send any message to get a response from the bot",
    ]
    await update.message.reply_text("\n".join(help_text), protect_content=True)


async def annihilator_gun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_writer.write_log(
        user_id=update.effective_user.id,
        action="annihilator_gun",
    )
    await update.message.reply_video(
        open("annihilator_gun.mp4", "rb"),
        caption="Boom!",
    )


async def process_message(update: Update, context: CallbackContext) -> None:
    log_writer.write_log(
        user_id=update.effective_user.id,
        action="message",
    )
    data = {
        "modelUri": f"gpt://{cfg.folder_id}/yandexgpt",
        "completionOptions": {"temperature": 0.3, "maxTokens": 1000},
        "messages": [{"role": "user", "text": f"{update.message.text}"}],
    }

    response = requests.post(
        GPT_BASE_URL,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {cfg.get_iam_token()}",
        },
        json=data,
    ).json()

    answer = (
        response.get(
            "result",
            {},
        )
        .get(
            "alternatives",
            [{}],
        )[0]
        .get(
            "message",
            {},
        )
        .get(
            "text",
            "",
        )
    )
    await update.message.reply_text(answer)


def main() -> None:
    app = Application.builder().token(cfg.tg_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cow_say", cow_say))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(CommandHandler("annihilator_gun", annihilator_gun))
    app.add_handler(MessageHandler(filters.ALL, process_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
