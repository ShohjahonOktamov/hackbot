# imports ________________________________________________________
# aiogram
from aiogram import Router


# setting up routers _____________________________________________


# function for setting up routers
def setup_routers() -> Router:
    # importing handlers
    from .users import start, mainmenu

    router = Router()

    router.include_routers(start.router, mainmenu.router)

    return router
