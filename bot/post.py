# import asyncio
# from typing import Any

# import aiohttp

# # async def get(url: str) -> Callable[[int], Coroutine[Any, Any, aiohttp.ClientResponse]]:
# #     async def fetch(pk: int, url: str = url) -> aiohttp.ClientResponse:
# #         async with aiohttp.ClientSession(trust_env=True) as session:
# #             url += str(pk) + "/"
# #             print(url)
# #             async with session.get(url=url) as response:
# #                 return response

# #     return fetch


# # async def get_api_setup(url: str) -> Callable:
# #     async def get_api(pk: int, url: str = url) -> aiohttp.ClientResponse:
# #         async with aiohttp.ClientSession(trust_env=True) as session:

# #             url += str(pk)
# #             print(url)
# #             async with session.get(url=url) as response:
# #                 return response

# #     return get_api


# # async def main():
# #     api_url = "http://192.168.1.18:8000/api/"
# #     tguser_get: Callable = await get_api_setup(url=f"{api_url}tguser/get/")
# #     print(await tguser_get(pk=1))


# # asyncio.run(main())
# url: str = "http://localhost:8000/"


# async def create_session():
#     async with aiohttp.ClientSession() as session:
#         return session


# async def post_tguser(session: aiohttp.ClientSession, data: dict[str, Any]) -> None:
#     await session.post(url=f"{url}/api/tguser/post/", data=data)


# async def main() -> None:
#     pk: int = 1
#     first_name: str = 'a'
#     last_name: str = 'b'
#     username: str = 'c'
#     data: dict[str, Any] = {
#         "user_id": pk,
#         "first_name": first_name,
#         "last_name": last_name,
#         "username": username
#     }

#     print(await post_tguser(session=session, data=data))


# asyncio.run(main())

# import requests
# import json

# data = {"height": 185}
# reponse = requests.put(
#     url="https://nutritionxorazm.pythonanywhere.com/api/person/getupdate/1/", json=data
# )

# print(reponse.json())

# import ipinfo
# import pprint

# iphandler = ipinfo.getHandler(access_token="5224df998182f6")

# details = iphandler.getDetails(ip_address="84.54.72.133").details

# pprint.pprint(details)


# from selenium import webdriver
# from time import sleep

# driver = webdriver.Firefox()
# driver.get("https://")
# driver.get_screenshot_as_file("screenshot.png")
# driver.quit()
# print("end...")
