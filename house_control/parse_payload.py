import json
import urllib.parse as url_parse


def parse(payload):
    format_type = _check_format(payload)

    if format_type == "slash_commands":
        return _parse_slash_commands(payload)
    elif format_type == "interactive_message":
        return _parse_interactive_message(payload)
    else:
        return {}


def _check_format(payload):
    data = url_parse.unquote(payload.decode(encoding="utf-8"))
    if data.startswith("payload="):
        return "interactive_message"
    else:
        return "slash_commands"


def _parse_slash_commands(payload):
    params = {}
    key_value_list = url_parse.unquote(payload.decode(encoding="utf-8")).split("&")
    for item in key_value_list:
        (key, value) = item.split("=")
        params[key] = value
    return params


def _parse_interactive_message(payload):
    data = url_parse.unquote(payload.decode(encoding="utf-8")).lstrip("payload=")
    return json.loads(data)

