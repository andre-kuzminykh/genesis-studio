"""Main keyboard layouts for the Genesis Studio bot.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.core.vocab import Vocab


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=Vocab.BTN_CREATE_PRODUCT),
                KeyboardButton(text=Vocab.BTN_MY_PRODUCTS),
            ],
            [KeyboardButton(text=Vocab.BTN_HELP)],
        ],
        resize_keyboard=True,
    )


def feature_actions_keyboard(feature_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=Vocab.BTN_GEN_PRD, callback_data=f"prd_draft:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_APPROVE_STORIES, callback_data=f"approve_stories:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_GEN_UX, callback_data=f"gen_ux:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_GEN_UC, callback_data=f"gen_uc:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_GEN_REQ, callback_data=f"gen_req:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_GEN_TESTS, callback_data=f"gen_tests:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_GEN_CODE, callback_data=f"gen_code:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_PUSH_GH, callback_data=f"push_gh:{feature_id}")],
            [InlineKeyboardButton(text=Vocab.BTN_DEPLOY, callback_data=f"deploy:{feature_id}")],
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
