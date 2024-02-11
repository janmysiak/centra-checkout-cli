import click
import json
from . import constants


def edit_file(filename):
    return click.edit(
        editor="nvim",
        filename=filename,
    )


def get_env():
    with click.open_file(constants.ENV_FILENAME, "r") as file:
        try:
            return json.loads(file.read().strip())
        except:
            return {}
