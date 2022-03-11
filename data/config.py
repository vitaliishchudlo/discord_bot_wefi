import os

from dotenv import load_dotenv

load_dotenv('../.env.tmp')

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

OWNER_ID = str(os.getenv("OWNER_ID"))
ADMIN_ROLE = str(os.getenv("ADMIN_ROLE"))

ACHIVEMENTS_CHAT_NAME = str(os.getenv("ACHIVEMENTS_CHAT_NAME"))
