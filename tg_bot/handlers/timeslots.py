from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.keyboards.days_keyboard import get_days_keyboard
from tg_bot.keyboards.time_keyboard import get_time_keyboard
from tg_bot.api.timeslots import get_free_days, get_available_slots, book_slots
from tg_bot.helpers import *
from aiogram import Router, F

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

        # Извлекаем подходящее начальное время для тренировки
        start_times = extract_start_times_for_training(available_slots)

        # Проверяем, есть ли доступное время
        if not start_times:
            await callback.message.edit_text(f"На {selected_day} нет доступного времени для записи.")
            await callback.answer()
            return

        # Генерируем клавиатуру с подходящим временем
        keyboard = get_time_keyboard(start_times, selected_day)

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

        # Извлекаем slot_ids для выбранного времени
        selected_slot_ids = get_slots_for_time(available_slots, selected_time)

        # Проверяем, найдены ли слоты
        if not selected_slot_ids:
            await callback.message.edit_text("К сожалению, выбранное время больше недоступно.")
            await callback.answer()
            return

        # Сохраняем информацию для подтверждения
        await callback.message.edit_text(
            f"Вы выбрали запись на {selected_day} в {selected_time}. "
            f"Подтвердите, чтобы забронировать: {selected_slot_ids}.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Подтвердить",
                            callback_data=f"CONFIRM_{selected_day}_{selected_time}_{','.join(map(str, selected_slot_ids))}"
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
        selected_time = data_parts[2]
        slot_ids = list(map(int, data_parts[3].split(",")))  # Список slot_ids
        user_id = callback.from_user.id  # ID пользователя из Telegram

        # Пытаемся забронировать слоты
        result = await book_slots(selected_slots=slot_ids, user_id=user_id)

        # Сообщаем пользователю о результате
        await callback.message.edit_text(
            f"Успешно забронировано на {selected_day} в {selected_time}! {result}"
        )
        await callback.answer()
    except Exception as e:
        await callback.message.edit_text("Ошибка при бронировании слотов. Попробуйте снова.")
        await callback.answer()
        print(f"Ошибка в book_slots_callback: {e}")