from asyncio import sleep

from pyrogram import enums, filters
from pyrogram.types import CallbackQuery, Message

from MissCutie import LOGGER
from MissCutie.bot_class import Bot
from MissCutie.database.lang_db import Langs
from MissCutie.tr_engine import lang_dict, tlang
from MissCutie.utils.custom_filters import admin_filter, command
from MissCutie.utils.kbhelpers import ikb


async def gen_langs_kb():
    langs = sorted(list(lang_dict.keys()))
    return [
        [
            (
                f"{lang_dict[lang]['main']['language_flag']} {lang_dict[lang]['main']['language_name']} ({lang_dict[lang]['main']['lang_sample']})",
                f"set_lang.{lang}",
            )
            for lang in langs
        ],
        [
            (
                "🌎 Help us with translations!",
                "https://crowdin.com/project/MissCutie_Bot",
                "url",
            ),
        ],
    ]


@Bot.on_callback_query(filters.regex("^chlang$"))
async def chlang_callback(_, q: CallbackQuery):
    kb = await gen_langs_kb()
    kb.append([(f"« {(tlang(q, 'general.back_btn'))}", "start_back")])

    await q.message.edit_text(
        (tlang(q, "langs.changelang")),
        reply_markup=ikb(kb),
    )
    await q.answer()
    return


@Bot.on_callback_query(filters.regex("^close$"), group=3)
async def close_btn_callback(_, q: CallbackQuery):
    await q.message.delete()
    try:
        await q.message.reply_to_message.delete()
    except Exception as ef:
        LOGGER.error(f"Error: Cannot delete message\n{ef}")
    await q.answer()
    return


@Bot.on_callback_query(filters.regex("^set_lang."))
async def set_lang_callback(_, q: CallbackQuery):
    lang_code = q.data.split(".")[1]

    Langs(q.message.chat.id).set_lang(lang_code)
    await sleep(0.1)

    if q.message.chat.type == enums.ChatType.PRIVATE:
        keyboard = ikb([[(f"« {(tlang(q, 'general.back_btn'))}", "start_back")]])
    else:
        keyboard = None
    await q.message.edit_text(
        f"🌐 {((tlang(q, 'langs.changed')).format(lang_code=lang_code))}",
        reply_markup=keyboard,
    )
    await q.answer()
    return


@Bot.on_message(
    command(["lang", "setlang"]) & (admin_filter | filters.private),
    group=7,
)
async def set_lang(_, m: Message):
    args = m.text.split()

    if len(args) > 2:
        await m.reply_text(tlang(m, "langs.correct_usage"))
        return
    if len(args) == 2:
        lang_code = args[1]
        avail_langs = set(lang_dict.keys())
        if lang_code not in avail_langs:
            await m.reply_text(
                f"Please choose a valid language code from: {', '.join(avail_langs)}",
            )
            return
        Langs(m.chat.id).set_lang(lang_code)
        LOGGER.info(f"{m.from_user.id} change language to {lang_code} in {m.chat.id}")
        await m.reply_text(
            f"🌐 {((tlang(m, 'langs.changed')).format(lang_code=lang_code))}",
        )
        return
    await m.reply_text(
        (tlang(m, "langs.changelang")),
        reply_markup=ikb(await gen_langs_kb()),
    )
    return


__PLUGIN__ = "language"

__alt_name__ = ["lang", "langs", "languages"]
__buttons__ = [
    [
        (
            "🌎 Help us with translations!",
            "https://crowdin.com/project/MissCutie_Bot",
            "url",
        ),
    ],
]
