import yaml

CONFIG_FILE_PATH = 'config.yaml'


def read_config_yaml():
    with open(CONFIG_FILE_PATH, "r") as stream:
        try:
            response = yaml.safe_load(stream)
            return response
        except yaml.YAMLError as exc:
            print(exc)


PATH_DATABASE = read_config_yaml()['database']['PATH_DATABASE']

BOT_PREFIX = read_config_yaml()['variables']['BOT_COMMAND_PREFIX']


ROLE_ID_FOR_ACTIVITY_TRACK = read_config_yaml()['tasks']['activity']['role_id_for_activity_track']