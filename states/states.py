from aiogram.fsm.state import State, StatesGroup



class StartSG(StatesGroup):
    start = State()


class ParcelCostDialogSG(StatesGroup):
    select_box_size = State()
    width = State()
    height = State()
    length = State()
    weight = State()
    departure_index = State()
    destination_index = State()
    calculate = State()
    new_calculate = State()


class TrackingDialogSG(StatesGroup):
    start = State()
