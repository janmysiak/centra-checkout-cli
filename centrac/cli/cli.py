import click
import json
import requests
from ..utils import constants, utils


def make_request(method, endpoint):
    env = utils.get_env()
    secret = env.get("secret")
    token = env.get("token")
    url = env.get("url")

    if not secret:
        raise Exception("No secret found in env")
    if not url:
        raise Exception("No URL found in env")

    url = f"{url}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Api-Token": token,
        "Authorization": f"Bearer {secret}",
    }

    data = ""
    if method in ["delete", "post", "put"]:
        utils.edit_file(constants.DATA_FILENAME)
        data = click.open_file(constants.DATA_FILENAME).read() or "{}"

    response = requests.request(data=data, method=method, url=url, headers=headers)
    result = response.json()

    return result


def handle_result(result, output):
    if output:
        json.dump(result, open(output, "w"), indent=2)
    else:
        click.echo(json.dumps(result))


@click.group()
def cli():
    pass


@cli.command("delete")
@click.argument("endpoint")
@click.option("-o", "--output", help="File to output to")
def delete(endpoint, output):
    """DELETE Request"""

    result = make_request("delete", endpoint)
    handle_result(result, output)


@cli.command("get")
@click.argument("endpoint")
@click.option("-o", "--output", help="File to output to")
def get(endpoint, output):
    """GET Request"""

    result = make_request("get", endpoint)
    handle_result(result, output)


@cli.command("post")
@click.argument("endpoint")
@click.option("-o", "--output", help="File to output to")
def post(endpoint, output):
    """POST Request"""

    result = make_request("post", endpoint)
    handle_result(result, output)


@cli.command("put")
@click.argument("endpoint")
@click.option("-o", "--output", help="File to output to")
def put(endpoint, output):
    """PUT Request"""

    result = make_request("put", endpoint)
    handle_result(result, output)
