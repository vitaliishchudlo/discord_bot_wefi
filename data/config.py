import os

from dotenv import load_dotenv

PATH_ENV_FILE = '.env.tmp'

load_dotenv(PATH_ENV_FILE)

# # # # # # # # # # # # # # # # # # # # # # #
#                 Variables:                #
# # # # # # # # # # # # # # # # # # # # # # #

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

OWNER_ID = str(os.getenv("OWNER_ID"))
ADMIN_ROLE = str(os.getenv("ADMIN_ROLE"))
MODERATOR_ROLE = str(os.getenv("MODERATOR_ROLE"))
ACHIVEMENTS_CHAT_NAME = str(os.getenv("ACHIVEMENTS_CHAT_NAME"))
ACHIVEMENT_ROLE_NAME = str(os.getenv("ACHIVEMENT_ROLE_NAME"))

PATH_DATABASE = str(os.getenv("PATH_DATABASE"))

DEFENDED_CHATS = [
    str(os.getenv("ACHIVEMENT_CHAT_STATISTIC")),
    str(os.getenv("ACHIVEMENTS_CHAT_INFO"))
]
ADMINS_ROLES = [
    str(os.getenv("MODERATOR_ROLE")),
    str(os.getenv("ADMIN_ROLE_NAME"))
]
