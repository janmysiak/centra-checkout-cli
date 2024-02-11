import click
import os
from .cli import *
from .utils import constants


def main():
    if not os.path.exists(constants.CONFIG_DIR):
        os.makedirs(constants.CONFIG_DIR)
    if not os.path.exists(constants.DATA_FILENAME):
        click.open_file(constants.DATA_FILENAME, "w").close()
    if not os.path.exists(constants.ENV_FILENAME):
        click.open_file(constants.ENV_FILENAME, "w").close()

    try:
        cli()
        exit(0)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
