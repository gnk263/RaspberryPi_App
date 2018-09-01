import unittest
import parse_payload


class TestParser(unittest.TestCase):
    maxDiff = None

    def test_slash_commands(self):
        payload = b"token=aaaaaaaaaaaaaaaaaaaaaaaa&team_id=bbbbbbbbb&team_domain=cccccc&channel_id=ddddddddd&channel_name=eeeeeeeeeeee&user_id=fffffffff&user_name=ggg&command=%2Fcontrol&text=aircon&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2Fhhhhhhhhh%2Fiiiiiiiiiiii%2Fjjjjjjjjjjjjjjjjjjjjjjjj"
        expected = {
            "token": "aaaaaaaaaaaaaaaaaaaaaaaa",
            "team_id": "bbbbbbbbb",
            "team_domain": "cccccc",
            "channel_id": "ddddddddd",
            "channel_name": "eeeeeeeeeeee",
            "user_id": "fffffffff",
            "user_name": "ggg",
            "command": "/control",
            "text": "aircon",
            "response_url": "https://hooks.slack.com/commands/hhhhhhhhh/iiiiiiiiiiii/jjjjjjjjjjjjjjjjjjjjjjjj"
        }
        params = parse_payload.parse(payload)
        self.assertDictEqual(expected, params)

    def test_parse_interactive_message(self):
        payload = b"payload=%7B%22type%22%3A%22interactive_message%22%2C%22actions%22%3A%5B%7B%22name%22%3A%22aircon%22%2C%22type%22%3A%22button%22%2C%22value%22%3A%22yes%22%7D%5D%2C%22callback_id%22%3A%22ask_aircon%22%2C%22team%22%3A%7B%22id%22%3A%22aaaaaaaaa%22%2C%22domain%22%3A%22bbbbb%22%7D%2C%22channel%22%3A%7B%22id%22%3A%22ccccccccccccc%22%2C%22name%22%3A%22privategroup%22%7D%2C%22user%22%3A%7B%22id%22%3A%22ddddddd%22%2C%22name%22%3A%22eeeee%22%7D%2C%22action_ts%22%3A%221535800538.222198%22%2C%22message_ts%22%3A%221535800500.000100%22%2C%22attachment_id%22%3A%221%22%2C%22token%22%3A%22fffffffffffffffffffff%22%2C%22is_app_unfurl%22%3Afalse%2C%22original_message%22%3A%7B%22text%22%3A%22%22%2C%22bot_id%22%3A%22gggggg%22%2C%22attachments%22%3A%5B%7B%22callback_id%22%3A%22ask_aircon%22%2C%22text%22%3A%22%5Cu30a8%5Cu30a2%5Cu30b3%5Cu30f3%5Cu3092On%5Cu306b%5Cu3057%5Cu307e%5Cu3059%5Cu304b%5Cuff1f%22%2C%22id%22%3A1%2C%22color%22%3A%223AA3E3%22%2C%22actions%22%3A%5B%7B%22id%22%3A%221%22%2C%22name%22%3A%22aircon%22%2C%22text%22%3A%22Yes%22%2C%22type%22%3A%22button%22%2C%22value%22%3A%22yes%22%2C%22style%22%3A%22%22%7D%2C%7B%22id%22%3A%222%22%2C%22name%22%3A%22aircon%22%2C%22text%22%3A%22No%22%2C%22type%22%3A%22button%22%2C%22value%22%3A%22no%22%2C%22style%22%3A%22%22%7D%5D%2C%22fallback%22%3A%22%5Cu30a8%5Cu30a2%5Cu30b3%5Cu30f3%5Cu3092On%5Cu306b%5Cu3057%5Cu307e%5Cu3059%5Cu304b%5Cuff1f%22%7D%5D%2C%22type%22%3A%22message%22%2C%22subtype%22%3A%22bot_message%22%2C%22ts%22%3A%221535800500.000100%22%7D%2C%22response_url%22%3A%22https%3A%5C%2F%5C%2Fhooks.slack.com%5C%2Factions%5C%2Faaaaaaaaa%5C%2Fhhhhhhh%5C%2Fiiiiiiiiiiiiiiii%22%2C%22trigger_id%22%3A%22jjjjjjjjjjjj.kkkkkkkkkkkk.llllllllllll%22%7D"
        expected = {
            "type": "interactive_message",
            "actions": [
                {
                    "name": "aircon",
                    "type": "button",
                    "value": "yes"
                }
            ],
            "callback_id": "ask_aircon",
            "team": {
                "id": "aaaaaaaaa",
                "domain": "bbbbb"
            },
            "channel": {
                "id": "ccccccccccccc",
                "name": "privategroup"
            },
            "user": {
                "id": "ddddddd",
                "name": "eeeee"
            },
            "action_ts": "1535800538.222198",
            "message_ts": "1535800500.000100",
            "attachment_id": "1",
            "token": "fffffffffffffffffffff",
            "is_app_unfurl": False,
            "original_message": {
                "text": "",
                "bot_id": "gggggg",
                "attachments": [
                    {
                        "callback_id": "ask_aircon",
                        "text": "エアコンをOnにしますか？",
                        "id": 1,
                        "color": "3AA3E3",
                        "actions": [
                            {
                                "id": "1",
                                "name": "aircon",
                                "text": "Yes",
                                "type": "button",
                                "value": "yes",
                                "style": ""
                            },
                            {
                                "id": "2",
                                "name": "aircon",
                                "text": "No",
                                "type": "button",
                                "value": "no",
                                "style": ""
                            }
                        ],
                        "fallback": "エアコンをOnにしますか？"
                    }
                ],
                "type": "message",
                "subtype": "bot_message",
                "ts": "1535800500.000100"
            },
            "response_url": "https://hooks.slack.com/actions/aaaaaaaaa/hhhhhhh/iiiiiiiiiiiiiiii",
            "trigger_id": "jjjjjjjjjjjj.kkkkkkkkkkkk.llllllllllll"
        }
        params = parse_payload.parse(payload)
        self.assertDictEqual(expected, params)


if __name__ == "__main__":
    unittest.main()
