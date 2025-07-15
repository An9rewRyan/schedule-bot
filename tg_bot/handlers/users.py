from keyboards.start_keyboard import get_start_keyboard
from keyboards.register_keyboard import get_cancel_keyboard, get_confirmation_keyboard
from api.users import register_user
from aiogram.filters.state import StateFilter
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states import RegisterStates

router = Router()


@router.message(F.text == "Начать регистрацию", default_state)
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:", reply_markup=get_cancel_keyboard())
    await state.set_state(RegisterStates.first_name)


@router.message(RegisterStates.first_name)
async def register_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(RegisterStates.second_name)


@router.message(RegisterStates.second_name)
async def register_second_name(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(RegisterStates.phone_number)


@router.message(RegisterStates.phone_number)
async def register_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Введите ваш возраст:")
    await state.set_state(RegisterStates.age)


@router.message(RegisterStates.age)
async def register_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 0 or age > 120:
            raise ValueError
        await state.update_data(age=age)
        user_data = await state.get_data()
        confirmation_text = (
            f"Ваши данные:\n"
            f"Имя: {user_data['first_name']}\n"
            f"Фамилия: {user_data['second_name']}\n"
            f"Телефон: {user_data['phone_number']}\n"
            f"Возраст: {user_data['age']}\n\n"
            "Подтвердите отправку данных."
        )
        await message.answer(confirmation_text, reply_markup=get_confirmation_keyboard())
        await state.set_state(RegisterStates.confirmation)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст.")


@router.message(RegisterStates.confirmation, F.text == "Подтвердить")
async def confirm_registration(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_data['telegram_id'] = message.from_user.id
    # Отправляем данные на FastAPI API
    response = await register_user(user_data)
    if response.status_code == 200:
        await message.answer(
            f"Привет, {user_data['first_name']}, пора пострелять!",
            reply_markup=get_start_keyboard(is_admin=False, telegram_id=user_data['telegram_id'])
        )
    else:
        await message.answer("Ошибка при регистрации. Попробуйте снова позже.")
    await state.clear()


@router.message(RegisterStates.confirmation, F.text == "Изменить")
async def modify_registration(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:", reply_markup=get_cancel_keyboard())
    await state.set_state(RegisterStates.first_name)


@router.message(StateFilter(default_state), F.text == "Отмена")
async def cancel_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Регистрация отменена.")
