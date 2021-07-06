from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging
import asyncio

import datetime

from aiogram import executor
from aiogram import types

import os
from dotenv import load_dotenv

load_dotenv()

bot_token = str(os.getenv("BOT_TOKEN"))
provider_token = str(os.getenv("PROVIDER_TOKEN"))

bot = Bot(
    token=bot_token,
    parse_mode=types.ParseMode.HTML
)
storage = MemoryStorage()

dp = Dispatcher(
    bot,
    storage=storage
)


@dp.message_handler(commands="start")
async def send_message(message: types.Message):

    PRICE = types.LabeledPrice(
        label='Оплата',
        amount=16500
    )

    TIME_MACHINE_IMAGE_URL = 'https://telegra.ph/file/3aaaaa7bc38272d645e69.jpg'


    await bot.send_invoice(
        message.chat.id,
        title="Как найти деньги на свою идею",
        description="Узнаешь о том как найти $ на идею благо или бизнес без долгов, кредитов и возврата инвестиций через RazomGO.com от создателя платформы Алексы Айшпур.\n\n165 грн - мастер-класс 1,5 часа.\n275 грн - прослушать мастер-класс и получить онлайн консультацию идеи.",
        provider_token=provider_token,
        currency='uah',
        photo_height=512,  # !=0/None, иначе изображение не покажется
        photo_width=512,
        photo_url=TIME_MACHINE_IMAGE_URL,
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[PRICE],
        start_parameter='hot-to-get',
        payload="Как найти деньги на свою идею",
        need_name=True,
        need_email=True,
        need_phone_number=True,
        max_tip_amount=16500,
        suggested_tip_amounts=[11000]
    )



@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):

    await bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True
    )

    time = datetime.datetime.now()

    data = pre_checkout_query.order_info

    data_and_time = []
    info = []

    data_and_time.append(f"<b>Время</b>: {time.strftime('%H:%M')}")
    data_and_time.append(f"<b>Дата</b>: {time.strftime('%d-%m-%Y')}")


    replace = {

        "name": "Имя",
        "phone_number": "Телефон",
        "email": "Имейл"

    }


    for item in data.iter_keys():
        info.append(f"<b>{replace[item]}</b>: {data[item]}")


    await bot.send_message(
        chat_id=-1001598180481,
        text="<b>Название</b>: {}\n\n{}\n\n{}\n\n<b>Сумма оплаты</b>: {},{} грн.".format(
            pre_checkout_query.invoice_payload,
            "\n".join(data_and_time),
            "\n".join(info),
            str(pre_checkout_query["total_amount"])[:-2],
            str(pre_checkout_query["total_amount"])[-2:]
        )
    )




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
