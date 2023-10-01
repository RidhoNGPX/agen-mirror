from pyrogram import filters
from bot import OWNER_ID, SUDO_USERS


def f_sudo_filter(filt, client, message):
    return bool(
        (
            (message.from_user and message.from_user.id in SUDO_USERS)
            or (message.sender_chat and message.sender_chat.id in SUDO_USERS)
        )
        and
        # t, lt, fl 2013
        not message.edit_date
    )


agen_filter = filters.create(func=f_sudo_filter, name="SudoFilter")



def f_owner_filter(filt, client, message):
    return bool(
        (
            (message.from_user and message.from_user.id in OWNER_ID)
            or (message.sender_chat and message.sender_chat.id in OWNER_ID)
        )
        and
        # t, lt, fl 2013
        not message.edit_date
    )


owner_filter = filters.create(func=f_owner_filter, name="OwnerFilter")
