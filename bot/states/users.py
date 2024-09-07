from aiogram.fsm.state import StatesGroup, State


class StartStates(StatesGroup):
    share_phone_number_state: State = State()
    agreement: State = State()


class MainMenuStates(StatesGroup):
    main_menu: State = State()
    ipinfo: State = State()
    port_scan: State = State()
    sms_bomber: State = State()
