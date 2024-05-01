from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from bot.db.models import Task
from bot.states import AddTaskStatesGroup

from bot.db.crud import TaskCrud, UserCrud

router = Router()


def task_message_trepr(task: Task):
    return (f'<b>Задача</b>\n'
            f'{task.text}\n'
            f'создана: {task.created_at.strftime("%d.%m.%Y %H:%M")}')


@router.message(Command('add'))
async def add_task(message: Message, state: FSMContext):
    """
    Добавление задачи

    :param message:
    :param state:
    :return:
    """

    user_id = message.from_user.id

    u_crud = UserCrud()

    print('=' * 30)
    print(await u_crud.get(pk=user_id))
    print('=' * 30)

    if not await u_crud.get(pk=user_id):
        await u_crud.create(id=user_id)

    await message.answer('Отлично! Теперь введи текст задачи')
    await state.set_state(AddTaskStatesGroup.GET_NAME)


@router.message(AddTaskStatesGroup.GET_NAME)
async def get_task_name(message: Message, state: FSMContext):
    """
    Получение текста задачи от пользователя
    :param message:
    :param state:
    :return:
    """

    user = await UserCrud().get(pk=message.from_user.id)
    task = await TaskCrud().create(
        user=user,
        text=message.text,
    )

    # await message.answer(task_message_trepr(task))
    await message.answer('Задача учпешно создана!')
    await state.clear()


@router.message(Command('tsk'))
async def show_tasks(message: Message):
    """
    Выводит список всех задач

    :param message:
    :return:
    """
    tasks = await TaskCrud().filter_by_user(message.from_user.id)

    if not tasks:
        await message.answer('Похоже у тебя нет ни одной задачи. Хочешь добавить?!')
    else:
        for task in tasks:
            await message.answer(task_message_trepr(task))
