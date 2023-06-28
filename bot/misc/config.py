from logging import getLogger

import yaml

BotLoggerName = 'BotLogger'

logger = getLogger(BotLoggerName)


def read_config_yaml():
    with open(CONFIG_FILE_PATH, 'r') as stream:
        try:
            response = yaml.safe_load(stream)
            return response
        except yaml.YAMLError as exc:
            logger.error(exc)

BotStatusText = 'Use me with **/**'

CONFIG_FILE_PATH = 'config.yaml'
PATH_DATABASE = read_config_yaml().get('database').get('PATH_DATABASE')

BOT_PREFIX = read_config_yaml().get('variables').get('BOT_COMMAND_PREFIX')

ID_ROLE_FOR_ACTIVITY_TRACK = read_config_yaml().get(
    'tasks').get('activity').get('id_role_for_activity_track')
ID_TEXT_CHANNEL_FOR_REPORT_ACTIVITY = read_config_yaml().get(
    'tasks').get('activity').get('id_text_channel_for_report')

ID_TEXT_CHANNEL_FOR_WELCOME = read_config_yaml().get('events').get(
    'on_member_join').get('id_text_channel_for_welcome')
CAPTCHAS_SAVING_PATH = read_config_yaml().get('events').get(
    'on_member_join').get('captchas_saving_path')

CAPTCHA_PREFIX = read_config_yaml().get('events').get(
    'on_member_join').get('captcha_prefix')

ID_ROLE_OTHER = read_config_yaml().get('roles_ids').get('other')

ID_ROLE_AFTER_VERIFICATION = ID_ROLE_OTHER

COGS_ACTIVITY_MESSAGE_EXPIRATION_TIME = read_config_yaml().get(
    'cogs').get('activity').get('message_expiration_seconds')

timezone = read_config_yaml().get('timezone')
