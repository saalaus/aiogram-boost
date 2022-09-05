from aiogram import Dispatcher
from aiogram.types import {type_title}


async def {name}({type}: {type_title}):
    await {type}.answer("Hello, admin!")


def register_{name}(dp: Dispatcher):
    dp.register_{type}_handler({name})