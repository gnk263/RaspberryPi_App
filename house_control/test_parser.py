import unittest
import parse_payload

class TestParser(unittest.TestCase):
    def test_controll_aircon(self):
        payload = b"token=aaaaaaaaaaaaaaaaaaaaaaaa&team_id=bbbbbbbbb&team_domain=cccccc&channel_id=ddddddddd&channel_name=eeeeeeeeeeee&user_id=fffffffff&user_name=ggg&command=%2Fcontrol&text=aircon&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2Fhhhhhhhhh%2Fiiiiiiiiiiii%2Fjjjjjjjjjjjjjjjjjjjjjjjj"
        expected = {
            "token": "aaaaaaaaaaaaaaaaaaaaaaaa",
            "team_id": "bbbbbbbbb",
            "team_domain": "cccccc",
            "channel_id": "ddddddddd",
            "channel_name": "eeeeeeeeeeee",
            "user_id": "fffffffff",
            "user_name": "ggg",
            "command": "%2Fcontrol",
            "text": "aircon",
            "response_url": "https%3A%2F%2Fhooks.slack.com%2Fcommands%2Fhhhhhhhhh%2Fiiiiiiiiiiii%2Fjjjjjjjjjjjjjjjjjjjjjjjj"
        }
        params = parse_payload.parse(payload)
        self.assertDictEqual(expected, params)


if __name__ == "__main__":
    unittest.main()
