from typing import Any

from bot import session
from config import url, django_api_key

headers: dict[str, str] = {
    "auth": django_api_key
}


async def get_tguser(pk: int) -> dict[str, bool | str | int | dict[str, str | int | bool] | None]:
    async with session.request(
            method="get", url=f"{url}/api/tguser/getput/{pk}/", headers=headers
    ) as response:
        if response.status == 200:
            return {"exists": True, "tguser": await response.json()}
        return {"exists": False, "tguser": None}


async def post_tguser(data: dict[str, Any]) -> None:
    await session.post(url=f"{url}/api/tguser/post/", data=data, headers=headers)


async def patch_tguser(pk: int, data: dict[str, Any]) -> None:
    await session.patch(url=f"{url}/api/tguser/getput/{pk}/", data=data, headers=headers)
