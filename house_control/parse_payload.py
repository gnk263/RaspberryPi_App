import urllib.parse as url_parse


def parse(payload):
    params = {}
    format_type = _check_format(payload)

    if format_type == "slash-commands":
        key_value_list = url_parse.unquote(payload.decode(encoding="utf-8")).split("&")
        for item in key_value_list:
            (key, value) = item.split("=")
            params[key] = value
        return params


def _check_format(payload):
    data = url_parse.unquote(payload.decode(encoding="utf-8"))
    if data.startswith("payload="):
        return "interactive_message"
    else:
        return "slash-commands"
