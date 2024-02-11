import click
import json
import re
from .cli import cli
from ..utils import constants, utils


def update_env(key, value):
    env = utils.get_env()

    with click.open_file(constants.ENV_FILENAME, "w") as file:
        env[key] = value
        file.write(json.dumps(env, indent=2))


@cli.group()
def env():
    pass


@env.command("edit")
def edit():
    """Edit current env"""

    utils.edit_file(constants.ENV_FILENAME)


@env.command("secret")
@click.argument("secret", required=True)
def secret(secret):
    """Set Checkout API secret"""

    update_env("secret", secret)


@env.command("token")
@click.argument("token", required=True)
def token(token):
    """Set Checkout API token"""

    update_env("token", token)


@env.command("url")
@click.argument("url", required=True)
def url(url):
    """Set Checkout API URL"""

    update_env("url", url)


@env.command("auto")
@click.argument("filename", required=True, type=click.Path(exists=True))
def auto(filename):
    """Attempt to automatically populate env file"""

    file = open(filename)
    lines = file.readlines()
    file.close()

    # Attempt to find secret
    secret = [
        line.strip().split("=")[1]
        for line in lines
        if re.search(r"CHECKOUT_API_(SECRET|KEY)=", line)
    ][0]

    if not secret:
        raise Exception("Failed to locate secret in env file")

    # Attempt to find URL
    url = [
        line.strip().split("=")[1]
        for line in lines
        if re.search(r"CHECKOUT_API=", line)
    ][0]

    if not url:
        raise Exception("Failed to locate URL field in env file")

    # Write to .env.json
    update_env("secret", secret)
    update_env("url", url)
