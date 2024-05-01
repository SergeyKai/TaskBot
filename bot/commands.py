from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


class Commands:
    """
    Основные команды бота
    """
    ADD_TASK = BotCommand(command='add', description='Добавить задачу')
    SHOW_ALL_TASK = BotCommand(command='tsk', description='Показать список всех задач')

    @classmethod
    async def get_commands(cls):
        class_attributes = vars(cls)
        commands_list = [command for key, command in class_attributes.items() if
                         not key.startswith('_') and key.isupper()]
        return commands_list

    @classmethod
    async def set_commands(cls, bot: Bot):
        commands = await cls.get_commands()
        await bot.set_my_commands(commands, BotCommandScopeDefault())
