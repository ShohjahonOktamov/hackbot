# TOKEN: str = "6770819978:AAGIbXZoAPyrwDRmPKxJiZB-ByW_jtkRY1g"

from decouple import config

TOKEN: str = config('TOKEN', default="", cast=str)
ipinfo_access_token: str = config('TOKEN', default="", cast=str)
django_api_key: str = config("django_api_key", default=TOKEN, cast=str)
url :str = config('url', default="", cast=str)
