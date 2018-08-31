
def parse(payload):
    params = {}
    key_value_list = payload.decode(encoding="utf-8").split("&")
    for item in key_value_list:
        (key, value) = item.split("=")
        params[key] = value
    return params
