#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pyrogram import (
    Client,
    Filters,
    Message
)
from bot import (
    AUTH_USERS,
    IS_BLACK_LIST_ED_MESSAGE_TEXT
)
from bot.sql.users_sql import (
    add_user_to_db
)
from bot.sql.blacklist_sql import (
    check_is_black_list
)


@Client.on_message(
    ~Filters.chat(AUTH_USERS)
)
async def on_pm_s(_, message: Message):
    check_ban = check_is_black_list(message.from_user.id)
    if check_ban:
        await message.reply_text(
            text=IS_BLACK_LIST_ED_MESSAGE_TEXT.format(
                reason=check_ban.reason
            )
        )
        return

    fwded_mesg = await message.forward(
        AUTH_USERS[0]
    )
    # just store, we don't need to SPAM users
    # mimick LiveGramBot, not @LimitatiBot ..!
    add_user_to_db(
        fwded_mesg.message_id,
        message.from_user.id,
        message.message_id
    )
