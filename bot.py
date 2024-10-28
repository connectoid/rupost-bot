import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User, BotCommand
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Button, Select, Group
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput

from dotenv import load_dotenv

from tools.tools import index_check, weight_check, size_check
from handlers.handlers import (go_start, correct_departure_index_handler, correct_destination_index_handler,
                               correct_weght_handler, error_value_handler, start_cost_calculate_handler,
                               start_tracking_handler, calculate_cost, correct_height_handler, 
                               correct_length_handler, correct_width_handler, box_size_selection,
                               manual_size_selection, error_address_handler)
from states.states import StartSG, ParcelCostDialogSG, TrackingDialogSG


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()


async def set_commands_menu(bot: Bot):
    await bot.delete_my_commands()
    main_menu_commands = [BotCommand(
                            command='/start',
                            description='Запуск бота')
                        ]
    await bot.set_my_commands(main_menu_commands)
    return None


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'username': event_from_user.username}


async def calculation_result_getter(dialog_manager: DialogManager, **kwargs):
    calculation_result = dialog_manager.dialog_data.get('calculation_result')
    return {'calculation_result': calculation_result}


async def get_box_sizes(**kwargs):
    sizes = [
        ('S', 10),
        ('M', 20),
        ('L', 30),
        ('XL', 40),
        # ('Негабарит', 5),
    ]
    return {'sizes': sizes}


# Это стартовый диалог
start_dialog = Dialog(
    Window(
        Multi(
            Format('Привет, {username}!'),
            Const('Выберите режим работы бота'),
            Const('Расчет стоимости отправления по заданным параметрам '
                  'или отслеживание отправления по трек-номеру'),
            sep='\n'
        ),

        Button(
            text=Const('💳 Расчет стоимости'),
            id='button_cost_calculation_mode',
            on_click=start_cost_calculate_handler),

        Button(
            text=Const('🚛 Отслеживание'),
            id='button_tracking_mode',
            on_click=start_tracking_handler,),

        getter=username_getter,
        state=StartSG.start
    ),
)


cost_calculation_dialog = Dialog(
    Window(
        Const(text='Выберите размер коробки или введите размер посылки'),
        Group(
            Select(
                Format('{item[0]}'),
                id='box_size',
                item_id_getter=lambda x: x[1],
                items='sizes',
                on_click=box_size_selection
            ),
            width=4,
        ),
        Button(Const('📐 Ввести размеры вручную'), id='manual_size', on_click=manual_size_selection),
        getter=get_box_sizes,
        state=ParcelCostDialogSG.select_box_size,
    ),
    Window(
        Const(text='Введите ширину посылки в сантиметрах'),
        TextInput(
            id='width_input',
            type_factory=size_check,
            on_success=correct_width_handler,
            on_error=error_value_handler,
        ),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=ParcelCostDialogSG.width,
    ),
    Window(
        Const(text='Введите высоту посылки в сантиметрах'),
        TextInput(
            id='height_input',
            type_factory=size_check,
            on_success=correct_height_handler,
            on_error=error_value_handler,
        ),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=ParcelCostDialogSG.height,
    ),
    Window(
        Const(text='Введите длину посылки в сантиметрах'),
        TextInput(
            id='length_input',
            type_factory=size_check,
            on_success=correct_length_handler,
            on_error=error_value_handler,
        ),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=ParcelCostDialogSG.length,
    ),
    Window(
        Const(text='Введите вес отправления в граммах'),
        TextInput(
            id='weight_input',
            type_factory=weight_check,
            on_success=correct_weght_handler,
            on_error=error_value_handler,
        ),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=ParcelCostDialogSG.weight,
    ),
    Window(
        Const(text='Введите индекс или адрес пункта отправления.\n(можно указать полный адрес или наименование населенного пункта)'),
        TextInput(
            id='index_departure_input',
            type_factory=index_check,
            on_success=correct_departure_index_handler,
            on_error=error_address_handler,
        ),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=ParcelCostDialogSG.departure_index
    ),
    Window(
        Const(text='Введите индекс или адрес пункта назначения.\n(можно указать полный адрес или наименование населенного пункта)'),
        TextInput(
            id='index_destiantion_input',
            type_factory=index_check,
            on_success=correct_destination_index_handler,
            on_error=error_address_handler,
        ),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=ParcelCostDialogSG.destination_index
    ),
    Window(
        Const(text='Все необходимые данные собраны. Произвести рассчет?'),
        Button(Const('💳 Рассчитать'), id='button_calculate', on_click=calculate_cost),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=ParcelCostDialogSG.calculate,
    ),
    Window(
        Format('{calculation_result}'),
        Button(Const('💳 Новый расчет'), id='button_new_calculate', on_click=start_cost_calculate_handler),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        getter=calculation_result_getter,
        state=ParcelCostDialogSG.new_calculate,
    ),

)


tracking_dialog = Dialog(
    Window(
        Format('Здесь будет диалог про отслеживание посылки'),
        Button(Const('⬅️ Выйти в главное меню'), id='button_start', on_click=go_start),
        state=TrackingDialogSG.start
    ),
)


# Этот классический хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


def main():
    dp.startup.register(set_commands_menu)
    dp.include_router(router)
    dp.include_routers(start_dialog, cost_calculation_dialog, tracking_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)


if __name__ == '__main__':
    main()