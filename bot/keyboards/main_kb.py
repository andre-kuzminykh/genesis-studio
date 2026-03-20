"""Main keyboard layouts for the Genesis Studio bot.

Bot = UI only layer.
"""
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Create Product"), KeyboardButton(text="My Products")],
            [KeyboardButton(text="Help")],
        ],
        resize_keyboard=True,
    )


def feature_actions_keyboard(feature_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Generate PRD Draft", callback_data=f"prd_draft:{feature_id}")],
            [InlineKeyboardButton(text="Approve Stories", callback_data=f"approve_stories:{feature_id}")],
            [InlineKeyboardButton(text="Generate UX Preview", callback_data=f"gen_ux:{feature_id}")],
            [InlineKeyboardButton(text="Generate Use Cases", callback_data=f"gen_uc:{feature_id}")],
            [InlineKeyboardButton(text="Generate Requirements", callback_data=f"gen_req:{feature_id}")],
            [InlineKeyboardButton(text="Generate Tests", callback_data=f"gen_tests:{feature_id}")],
            [InlineKeyboardButton(text="Generate Code", callback_data=f"gen_code:{feature_id}")],
            [InlineKeyboardButton(text="Push to GitHub", callback_data=f"push_gh:{feature_id}")],
            [InlineKeyboardButton(text="Deploy Locally", callback_data=f"deploy:{feature_id}")],
        ]
    )


def approval_keyboard(prefix: str, item_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Approve", callback_data=f"{prefix}_approve:{item_id}"),
                InlineKeyboardButton(text="Edit", callback_data=f"{prefix}_edit:{item_id}"),
                InlineKeyboardButton(text="Reject", callback_data=f"{prefix}_reject:{item_id}"),
            ]
        ]
    )
