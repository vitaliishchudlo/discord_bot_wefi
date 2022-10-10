import yaml

CONFIG_FILE_PATH = 'config.yaml'


def read_config_yaml():
    with open(CONFIG_FILE_PATH, 'r') as stream:
        try:
            response = yaml.safe_load(stream)
            return response
        except yaml.YAMLError as exc:
            print(exc)


PATH_DATABASE = read_config_yaml()['database']['PATH_DATABASE']

BOT_PREFIX = read_config_yaml()['variables']['BOT_COMMAND_PREFIX']


ID_ROLE_FOR_ACTIVITY_TRACK = read_config_yaml(
)['tasks']['activity']['id_role_for_activity_track']
ID_TEXT_CHANNEL_FOR_REPORT_ACTIVITY = read_config_yaml(
)['tasks']['activity']['id_text_channel_for_report']
