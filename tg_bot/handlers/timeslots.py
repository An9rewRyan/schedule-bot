from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.keyboards.days_keyboard import get_days_keyboard
from tg_bot.keyboards.time_keyboard import get_time_keyboard
from tg_bot.keyboards.user_bookings_keyboard import get_user_bookings_keyboard
from tg_bot.api.timeslots import get_free_days, get_available_slots
from tg_bot.api.bookings import book_slots, get_bookings_for_user
from tg_bot.api.bookings import delete_booking
from tg_bot.helpers import *
from aiogram import Router, F
from datetime import datetime, timedelta, time

router = Router()

logger = logging.getLogger('SuperBot')


@router.callback_query(F.data == "choose_day")
async def choose_day_callback(callback: CallbackQuery):
    """
    Хендлер для callback-запроса на кнопку «Выбрать день».
    Отправляет клавиатуру с доступными днями недели.
    """
    try:
        telegram_id = callback.from_user.id
        # Получаем доступные дни через API
        available_days = await get_free_days(telegram_id=telegram_id)

        # Проверяем, есть ли доступные дни
        if not available_days:
            await callback.message.edit_text("К сожалению, нет доступных дней для записи.")
            await callback.answer()
            return

        # Генерируем клавиатуру с доступными днями
        keyboard = get_days_keyboard(available_days)

        # Отправляем клавиатуру пользователю
        await callback.message.edit_text(
            "На какой день недели хотите записаться?",
            reply_markup=keyboard
        )
        await callback.answer()
    except Exception as e:
        # Обработка ошибки, если что-то пошло не так
        await callback.message.edit_text("Произошла ошибка при получении доступных дней.")
        await callback.answer()
        print(f"Ошибка в choose_day_callback: {e}")


@router.callback_query(F.data == "user_bookings")
async def get_user_bookings(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    bookings = await get_bookings_for_user(telegram_id=telegram_id)
    if not bookings:
        await callback.message.edit_text("У вас нет запланированных тренировок")
    else:
        await callback.message.edit_text("Ваши брони:", reply_markup=get_user_bookings_keyboard(bookings))


@router.callback_query(lambda c: c.data.startswith("DAY_"))
async def choose_time_callback(callback: CallbackQuery):
    """
    Хендлер для выбора времени на основе выбранного дня.
    """
    try:
        selected_day = callback.data.split("_")[1]  # Извлекаем выбранный день из callback_data
        telegram_id = callback.from_user.id
        # Запрашиваем доступные слоты через API
        available_slots = await get_available_slots(selected_date=selected_day, telegram_id=telegram_id)
        slots_strike = []
        good_start_times = []
        for i in range(len(available_slots) - 1):
            if len(slots_strike) == 3:
                good_start_times.append(slots_strike.pop(0))
            if available_slots[i]['end_time'] == available_slots[i + 1]['start_time']:
                slots_strike.append(available_slots[i])
            else:
                if available_slots[i]['start_time'] == available_slots[i - 1]['end_time'] and len(slots_strike) == 2:
                    good_start_times.append(slots_strike.pop(0))
                slots_strike = []
        # Извлекаем подходящее начальное время для тренировки
        # start_times = extract_start_times_for_training(available_slots)

        # Проверяем, есть ли доступное время
        if not available_slots:
            await callback.message.edit_text(f"На {selected_day} нет доступного времени для записи.")
            await callback.answer()
            return

        # Генерируем клавиатуру с подходящим временем
        keyboard = get_time_keyboard(good_start_times, selected_day)

        # Отправляем клавиатуру пользователю
        await callback.message.edit_text(
            f"Вы выбрали день: {selected_day}. Доступное время:",
            reply_markup=keyboard
        )
        await callback.answer()
    except Exception as e:
        # Обработка ошибки
        await callback.message.edit_text("Произошла ошибка при получении доступного времени.")
        await callback.answer()
        print(f"Ошибка в choose_time_callback: {e}")


@router.callback_query(lambda c: c.data.startswith("TIME_"))
async def confirm_booking_callback(callback: CallbackQuery):
    """
    Хендлер для подтверждения бронирования слотов.
    """
    try:
        telegram_id = callback.from_user.id
        data_parts = callback.data.split("_")
        selected_day = data_parts[1]  # Извлекаем день
        selected_time = data_parts[2]  # Извлекаем время

        # Запрашиваем доступные слоты через API
        available_slots = await get_available_slots(selected_date=selected_day, telegram_id=telegram_id)
        slots_to_book = []
        # for i in range(1, 3):
        #     requested_time = selected_time + timedelta(minutes=30)

        # Извлекаем slot_ids для выбранного времени
        # selected_slot_ids = get_slots_for_time(available_slots, selected_time)

        # # Проверяем, найдены ли слоты
        # if not selected_slot_ids:
        #     await callback.message.edit_text("К сожалению, выбранное время больше недоступно.")
        #     await callback.answer()
        #     return

        # Сохраняем информацию для подтверждения
        await callback.message.edit_text(
            f"Вы выбрали запись на {selected_day} в {selected_time}. "
            f"Подтвердите, чтобы забронировать.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Подтвердить",
                            callback_data=f"CONFIRM_{selected_day}_{selected_time}"
                        ),
                        InlineKeyboardButton(text="Отменить", callback_data="CANCEL")
                    ]
                ]
            )
        )
        await callback.answer()
    except Exception as e:
        await callback.message.edit_text("Произошла ошибка при подтверждении записи.")
        await callback.answer()
        print(f"Ошибка в confirm_booking_callback: {e}")


@router.callback_query(lambda c: c.data.startswith("CONFIRM_"))
async def book_slots_callback(callback: CallbackQuery):
    """
    Хендлер для бронирования слотов.
    """
    try:
        data_parts = callback.data.split("_")
        selected_day = data_parts[1]
        start_time = data_parts[2]
        user_id = callback.from_user.id  # ID пользователя из Telegram
        # slots = await get_available_slots(selected_date=selected_day, telegram_id=user_id)
        # selected_slot_ids = []
        # first_slot = None
        # for idx, slot in enumerate(slots):
        #     if slot['start_time'] == selected_time:
        #         selected_slot_ids.append(slot['id'])
        #         if len(slots[idx + 1]['visitors']) < 4 and len(slots[idx + 2]['visitors']) < 4:
        #             selected_slot_ids.append(slots[idx + 1]['id'])
        #             selected_slot_ids.append(slots[idx + 2]['id'])
        # if len(selected_slot_ids) < 3:
        #     await callback.message.edit_text("Ошибка при бронировании слотов. Попробуйте снова.")
        #     await callback.answer()
        #     return

        # Пытаемся забронировать слоты
        result = await book_slots(start_time=start_time,
                                  end_time=str(
                                      (datetime.strptime(start_time, "%H:%M:%S") + timedelta(minutes=90)).time()),
                                  selected_day=selected_day, user_id=user_id)

        # Сообщаем пользователю о результате
        await callback.message.edit_text(
            f"Успешно забронировано на {selected_day} в {start_time}! {result}"
        )
        await callback.answer()
    except Exception as e:
        await callback.message.edit_text("Ошибка при бронировании слотов. Попробуйте снова.")
        await callback.answer()


@router.callback_query(F.data.startswith("CANCEL_"))
async def cancel_booking(callback: CallbackQuery):
    booking_id = int(callback.data.split("_")[1])
    telegram_id = callback.from_user.id
    booking_deleted = await delete_booking(booking_id, telegram_id)

    if not booking_deleted:
        await callback.answer("Бронирование не найдено или уже удалено.", show_alert=True)
        return

    await callback.message.edit_text(f"❌ Бронирование #{booking_id} отменено.")
    await callback.answer("Ваше бронирование успешно отменено.", show_alert=True)


@router.callback_query(F.data.startswith("RESCHEDULE_"))
async def reschedule_booking(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    # Получаем доступные дни через API
    booking_id = int(callback.data.split("_")[1])
    available_days = await get_free_days(telegram_id=telegram_id)
    booking_deleted = await delete_booking(booking_id, telegram_id)

    if not booking_deleted:
        await callback.answer("Бронирование не найдено или уже удалено.", show_alert=True)
        # return

    # Проверяем, есть ли доступные дни
    if not available_days:
        await callback.message.edit_text("К сожалению, нет доступных дней для записи.")
        await callback.answer()
        return

    # Генерируем клавиатуру с доступными днями
    keyboard = get_days_keyboard(available_days)

    # Отправляем клавиатуру пользователю
    await callback.message.edit_text(
        "На какой день недели хотите записаться?",
        reply_markup=keyboard
    )
