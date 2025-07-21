import asyncio
import sys
from backend.src.repository.db import async_session
from sqlalchemy import text

async def delete_user(telegram_id: int):
    """
    Удаляет пользователя и все связанные с ним данные из базы данных

    Args:
        telegram_id (int): Telegram ID пользователя для удаления
    """
    print(f'Удаление пользователя с Telegram ID: {telegram_id}')

    async with async_session() as session:
        try:
            # Проверяем существование пользователя
            result = await session.execute(
                text('SELECT id, first_name, second_name FROM user WHERE telegram_id = :telegram_id'),
                {'telegram_id': telegram_id}
            )
            user = result.fetchone()

            if not user:
                print(f'❌ Пользователь с Telegram ID {telegram_id} не найден')
                return False

            user_id = user.id
            print(f'✅ Найден пользователь: {user.first_name} {user.second_name}')

            # Удаляем все связи пользователя с таймслотами
            print('Удаление связей пользователя с таймслотами...')
            await session.execute(
                text('DELETE FROM usertimeslotlink WHERE user_id = :user_id'),
                {'user_id': user_id}
            )

            # Удаляем все бронирования пользователя
            print('Удаление бронирований пользователя...')
            await session.execute(
                text('DELETE FROM bookingtimeslotlink WHERE booking_id IN (SELECT id FROM booking WHERE user_id = :user_id)'),
                {'user_id': user_id}
            )
            await session.execute(
                text('DELETE FROM booking WHERE user_id = :user_id'),
                {'user_id': user_id}
            )

            # Удаляем самого пользователя
            print('Удаление пользователя...')
            await session.execute(
                text('DELETE FROM user WHERE id = :user_id'),
                {'user_id': user_id}
            )

            await session.commit()
            print(f'✅ Пользователь {user.first_name} {user.second_name} успешно удален')
            return True

        except Exception as e:
            await session.rollback()
            print(f'❌ Ошибка при удалении пользователя: {e}')
            return False

async def list_users():
    """Выводит список всех пользователей в базе данных"""
    print('Список всех пользователей:')
    print('-' * 80)
    print(f'{"ID":<5} {"Telegram ID":<12} {"Имя":<15} {"Фамилия":<15} {"Возраст":<8} {"Админ":<6}')
    print('-' * 80)

    async with async_session() as session:
        try:
            result = await session.execute(
                text('SELECT id, telegram_id, first_name, second_name, age, is_admin FROM user ORDER BY id')
            )
            users = result.fetchall()

            if not users:
                print('Пользователи не найдены')
                return

            for user in users:
                admin_status = "Да" if user.is_admin else "Нет"
                print(f'{user.id:<5} {user.telegram_id:<12} {user.first_name:<15} {user.second_name:<15} {user.age:<8} {admin_status:<6}')

        except Exception as e:
            print(f'❌ Ошибка при получении списка пользователей: {e}')

def print_usage():
    """Выводит инструкцию по использованию"""
    print('Использование:')
    print('  python delete_user.py <telegram_id>  - удалить пользователя по Telegram ID')
    print('  python delete_user.py --list         - показать список всех пользователей')
    print('  python delete_user.py --help         - показать эту справку')
    print()
    print('Примеры:')
    print('  python delete_user.py 123456789      - удалить пользователя с Telegram ID 123456789')
    print('  python delete_user.py --list         - показать всех пользователей')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print_usage()
        sys.exit(0)

    if sys.argv[1] == '--list' or sys.argv[1] == '-l':
        asyncio.run(list_users())
        sys.exit(0)

    try:
        telegram_id = int(sys.argv[1])
        success = asyncio.run(delete_user(telegram_id))
        sys.exit(0 if success else 1)
    except ValueError:
        print(f'❌ Ошибка: {sys.argv[1]} не является корректным числом')
        print_usage()
        sys.exit(1)
    except KeyboardInterrupt:
        print('\n❌ Операция прервана пользователем')
        sys.exit(1)