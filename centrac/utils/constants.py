import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = f"{SCRIPT_PATH}/.config/centrac"
ENV_FILENAME = f"{CONFIG_DIR}/.env.json"
DATA_FILENAME = f"{CONFIG_DIR}/data.json"
RESULT_FILENAME = f"{CONFIG_DIR}/result.json"
