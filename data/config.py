import os

from dotenv import load_dotenv

PATH_ENV_FILE = '.env'

load_dotenv(PATH_ENV_FILE)

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
BOT_PREFIX = '.'

PATH_DATABASE = 'database/database.db'

CAPTCHA_BODY = [
    'slavaukraini',
    'fuckrussia',
    'bandera',
    'bayraktar',
    'javelin',
    'himars'
]

VERSION_PREFIX = 'TESTING'
VERSION_NUBMER = ''

ID_OWNER = 398567252061978628

# # # # # # # # # # # # # # # # # # # # # # #
#   #   #   #   #   #   #   #   #   #   #   #
# # # # # # # # # # # # # # # # # # # # # # #

ID_ROLE_ADMIN = None
ID_ROLE_MODERATOR = 952960220714401863

ID_CHAT_ACHIEVEMENT_STATISTICS = 916003184063963176
ID_CHAT_ACHIEVEMENT_INFO = 917522912980893757
ID_ROLE_ACHIEVEMENTS = 952280483759292456  # WeFi
ID_ROLE_OTHER = 952282700780281938  # Other

ID_CHAT_WELCOME = 952278528458641438

DEFENDED_CHATS = [
    ID_CHAT_ACHIEVEMENT_STATISTICS,
    ID_CHAT_ACHIEVEMENT_INFO
]

ID_ROLES_ACHIEVEMENTS_EDITORS = [
    ID_ROLE_ADMIN,
    ID_ROLE_MODERATOR
]

ADMINS_ROLES = [
    ID_ROLE_ADMIN,
    ID_ROLE_MODERATOR,
]

cogs = [
    {"cogs_manager": [None]},

    # Systems:
    {"system.clear_chat": [*ADMINS_ROLES]},
    {"system.json": [None]},

    # Events:
    {"events.on_member_join": [None]},
    {"events.on_ready": [None]},

    # Achievements:
    {"achievements.achievements": [None]},
    {"achievements.refresh": [None]}
]
