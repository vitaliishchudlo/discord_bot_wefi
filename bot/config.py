import os

from dotenv import load_dotenv

PATH_ENV_FILE = '.env'

load_dotenv(PATH_ENV_FILE)

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))