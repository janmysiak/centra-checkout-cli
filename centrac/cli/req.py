import click
import json
import requests
from .cli import cli
from ..utils import constants, utils


def get_request_endpoint(env, endpoint):
    return f"{env['url']}/{endpoint}"


def get_request_headers(env):
    return {
        "Content-Type": "application/json",
        "Api-Token": env.get("token", "none"),
        "Authorization": f"Bearer {env.get('secret')}",
    }


@cli.command("req")
@click.argument("endpoint", required=True)
@click.option("-o", "--output", help="File to output to")
@click.option(
    "--get", "method", flag_value="get", default=True, help="GET request (default)"
)
@click.option("--post", "method", flag_value="post", help="POST request")
@click.option("--put", "method", flag_value="put", help="PUT request")
@click.option("--delete", "method", flag_value="delete", help="DELETE request")
def req(
    endpoint,
    output,
    method,
):
    env = utils.get_env()

    if not env.get("secret"):
        raise Exception("No secret found in env")
    if not env.get("url"):
        raise Exception("No URL found in env")

    full_endpoint = get_request_endpoint(env, endpoint)
    headers = get_request_headers(env)

    result = ""

    if method == "get":
        result = requests.get(full_endpoint, headers=headers).json()
    else:
        # Edit command doesn't seem to be returning the contents unless the file is temporary?
        # https://click.palletsprojects.com/en/8.1.x/api/#click.edit
        # data = click.edit(text="{}", require_save=True, editor="nvim", extension=".json")

        utils.edit_file(constants.DATA_FILENAME)
        data = click.open_file(constants.DATA_FILENAME).read() or "{}"

        result = requests.request(
            url=full_endpoint, headers=headers, data=data, method=method
        ).json()

    if output:
        json.dump(result, open(output, "w"), indent=2)
    else:
        click.echo(json.dumps(result))
