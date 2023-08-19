from pyrogram.types import Message

from MissCutie.bot_class import Bot
from MissCutie.database.antispam_db import GBan
from MissCutie.database.approve_db import Approve
from MissCutie.database.blacklist_db import Blacklist
from MissCutie.database.chats_db import Chats
from MissCutie.database.disable_db import Disabling
from MissCutie.database.filters_db import Filters
from MissCutie.database.greetings_db import Greetings
from MissCutie.database.notes_db import Notes, NotesSettings
from MissCutie.database.pins_db import Pins
from MissCutie.database.rules_db import Rules
from MissCutie.database.users_db import Users
from MissCutie.database.warns_db import Warns, WarnSettings
from MissCutie.utils.custom_filters import command


@Bot.on_message(command("stats", dev_cmd=True))
async def get_stats(_, m: Message):
    # initialise
    bldb = Blacklist
    gbandb = GBan()
    notesdb = Notes()
    rulesdb = Rules
    grtdb = Greetings
    userdb = Users
    dsbl = Disabling
    appdb = Approve
    chatdb = Chats
    fldb = Filters()
    pinsdb = Pins
    notesettings_db = NotesSettings()
    warns_db = Warns
    warns_settings_db = WarnSettings

    replymsg = await m.reply_text("<b><i>Fetching Stats...</i></b>", quote=True)
    rply = (
        f"<b>Users:</b> <code>{(userdb.count_users())}</code> in <code>{(chatdb.count_chats())}</code> chats\n"
        f"<b>Anti Channel Pin:</b> <code>{(pinsdb.count_chats('antichannelpin'))}</code> enabled chats\n"
        f"<b>Clean Linked:</b> <code>{(pinsdb.count_chats('cleanlinked'))}</code> enabled chats\n"
        f"<b>Filters:</b> <code>{(fldb.count_filters_all())}</code> in <code>{(fldb.count_filters_chats())}</code> chats\n"
        f"    <b>Aliases:</b> <code>{(fldb.count_filter_aliases())}</code>\n"
        f"<b>Blacklists:</b> <code>{(bldb.count_blacklists_all())}</code> in <code>{(bldb.count_blackists_chats())}</code> chats\n"
        "    <b>Action Specific:</b>\n"
        f"        <b>None:</b> <code>{(bldb.count_action_bl_all('none'))}</code> chats\n"
        f"        <b>Kick</b> <code>{(bldb.count_action_bl_all('kick'))}</code> chats\n"
        f"        <b>Warn:</b> <code>{(bldb.count_action_bl_all('warn'))}</code> chats\n"
        f"        <b>Ban</b> <code>{(bldb.count_action_bl_all('ban'))}</code> chats\n"
        f"<b>Rules:</b> Set in <code>{(rulesdb.count_chats_with_rules())}</code> chats\n"
        f"    <b>Private Rules:</b> <code>{(rulesdb.count_privrules_chats())}</code> chats\n"
        f"<b>Warns:</b> <code>{(warns_db.count_warns_total())}</code> in <code>{(warns_db.count_all_chats_using_warns())}</code> chats\n"
        f"    <b>Users Warned:</b> <code>{(warns_db.count_warned_users())}</code> users\n"
        "    <b>Action Specific:</b>\n"
        f"        <b>Kick</b>: <code>{(warns_settings_db.count_action_chats('kick'))}</code>\n"
        f"        <b>Mute</b>: <code>{(warns_settings_db.count_action_chats('mute'))}</code>\n"
        f"        <b>Ban</b>: <code>{warns_settings_db.count_action_chats('ban')}</code>\n"
        f"<b>Notes:</b> <code>{(notesdb.count_all_notes())}</code> in <code>{(notesdb.count_notes_chats())}</code> chats\n"
        f"    <b>Private Notes:</b> <code>{(notesettings_db.count_chats())}</code> chats\n"
        f"<b>GBanned Users:</b> <code>{(gbandb.count_gbans())}</code>\n"
        f"<b>Welcoming Users in:</b> <code>{(grtdb.count_chats('welcome'))}</code> chats"
        f"<b>Approved People</b>: <code>{(appdb.count_all_approved())}</code> in <code>{(appdb.count_approved_chats())}</code> chats\n"
        f"<b>Disabling:</b> <code>{(dsbl.count_disabled_all())}</code> items in <code>{(dsbl.count_disabling_chats())}</code> chats.\n"
        "<b>Action:</b>\n"
        f"     <b>Del:</b> Applied in <code>{(dsbl.count_action_dis_all('del'))}</code> chats.\n"
    )
    await replymsg.edit_text(rply)
    return
