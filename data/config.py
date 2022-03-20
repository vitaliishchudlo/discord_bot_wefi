import os

from dotenv import load_dotenv

PATH_ENV_FILE = '.env'

load_dotenv(PATH_ENV_FILE)

# # # # # # # # # # # # # # # # # # # # # # #
#                 Variables:                #
# # # # # # # # # # # # # # # # # # # # # # #

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

BOT_PREFIX = ''
CAPTCHA_PREFIX = ''

ID_OWNER = 0
ID_ROLE_ADMIN = 0
ID_ROLE_MODERATOR = 0

ID_CHAT_ACHIEVEMENT_STATISTICS = 0
ID_CHAT_ACHIEVEMENT_INFO = 0
ID_ROLE_ACHIEVEMENTS = 0  # WeFi
ID_ROLE_OTHER = 0  # Other

ID_CHAT_WELCOME = 0

DEFENDED_CHATS = [
    ID_CHAT_ACHIEVEMENT_STATISTICS,
    ID_CHAT_ACHIEVEMENT_INFO
]

ID_ROLES_ACHIEVEMENTS_EDITORS = [
    ID_ROLE_ADMIN,
    ID_ROLE_MODERATOR
]

TEST_LIST = [
    ID_ROLE_ADMIN,
    ID_ROLE_MODERATOR,
    ID_ROLE_ACHIEVEMENTS
]

PATH_DATABASE = ''

CAPTCHA_BODY = [
    ''
]

VERSION_PREFIX = 'BETA'
VERSION_NUBMER = '0.1'
