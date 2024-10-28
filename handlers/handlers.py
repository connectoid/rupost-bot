from aiogram.types import Message, CallbackQuery, User
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select


from states.states import StartSG, ParcelCostDialogSG, TrackingDialogSG
from tools.tools import get_parcel_cost, get_parcel_cost_v2, get_index
from settings.settings import parcel_ordinary, parcel_standart, MAX_STANDART_BOX_PARCEL_WEIGTH


parcer = {}
sizes = {
    10: 'S',
    20: 'M',
    30: 'L',
    40: 'XL',
    # 5: 'OVERSIZED'
}



async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


async def start_cost_calculate_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):  # Здесь будут хэндлеры
    await dialog_manager.start(state=ParcelCostDialogSG.select_box_size)


async def start_tracking_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):  # Здесь будут хэндлеры
    await dialog_manager.start(state=TrackingDialogSG.start)


# Это хэндлер, срабатывающий на нажатие кнопки выбора размера посылки
async def box_size_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    print(f'Выбран размер с id={item_id}')
    global parcel 
    parcel = parcel_standart
    parcel['dimension-type'] = item_id
    await dialog_manager.start(state=ParcelCostDialogSG.weight)


# Это хэндлер, срабатывающий на нажатие кнопки выбора указания размера посылки вручную
async def manual_size_selection(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    global parcel
    parcel = parcel_ordinary
    await dialog_manager.start(state=ParcelCostDialogSG.width)


# Хэндлер, который сработает, если пользователь ввел корректный индекс отправителя
async def correct_departure_index_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    
    index = text.split('*')[0]
    address_string = text.split('*')[1]
    if address_string:
        parcel['address-string-from'] = address_string
    parcel['index-from'] = index
    await message.answer(text=f'Найден адрес: {index}, {address_string}')
    await dialog_manager.next()


# Хэндлер, который сработает, если пользователь ввел корректный индекс получателя
async def correct_destination_index_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    
    index = text.split('*')[0]
    address_string = text.split('*')[1]
    if address_string:
        parcel['address-string-to'] = address_string
    parcel['index-to'] = index
    await message.answer(text=f'Найден адрес: {index}, {address_string}')
    await dialog_manager.next()


# Хэндлер, который сработает, если пользователь ввел корректный вес отправления
async def correct_weght_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    max_weight = float(MAX_STANDART_BOX_PARCEL_WEIGTH / 1000)
    if 'dimension-type' in parcel and int(text) > MAX_STANDART_BOX_PARCEL_WEIGTH:
        await message.answer(text=f'Вес посылки в стандартной коробке не может превышать {max_weight} кг.')
        await dialog_manager.switch_to(state=ParcelCostDialogSG.weight)
    else:
        parcel['mass'] = text
        await dialog_manager.next()


# Хэндлер, который сработает, если пользователь ввел корректную ширину посылки
async def correct_width_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    
    # await message.answer(text=f'Вы ввели {text}')
    parcel['dimension']['width'] = str(text)
    await dialog_manager.next()


# Хэндлер, который сработает, если пользователь ввел корректную высоту посылки
async def correct_height_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    
    # await message.answer(text=f'Вы ввели {text}')
    parcel['dimension']['height'] = str(text)
    await dialog_manager.next()


# Хэндлер, который сработает, если пользователь ввел корректную длину посылки
async def correct_length_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    
    # await message.answer(text=f'Вы ввели {text}')
    parcel['dimension']['length'] = str(text)
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного числового значения
async def error_value_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректное значение. Попробуйте еще раз'
    )


# Хэндлер, который сработает на ввод некорректного числового значения
async def error_address_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text=('Индекс введен неправильно или не удалось определить индекс по указанному адресу. \n'
              'Если населенный пункт небольшой, попробуйте указать регион вместе с наименованием населенного пункта. \n'
              'Например "Провидения Чукотский АО".')
    )


# Хэндлер, который производит расчет доставки
async def calculate_cost(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    result = get_parcel_cost_v2(parcel)
    print(result)
    # result = get_parcel_cost(parcel).text
    # await callback.message.answer(result)
    dialog_manager.dialog_data.update(calculation_result=result)
    print(parcel)
    await dialog_manager.next()
