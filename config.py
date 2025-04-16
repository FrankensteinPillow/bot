import os

import requests


class Config:

    def __init__(self):
        self.tg_token = os.getenv("TG_TOKEN", "")
        self.oauth_token = os.getenv("OAUTH_TOKEN", "")
        self.folder_id = os.getenv("FOLDER_ID", "")
        self.yd_token = os.getenv("YANDEX_DISK_OAUTH_TOKEN", "")

    def get_iam_token(self):
        response = requests.post(
            "https://iam.api.cloud.yandex.net/iam/v1/tokens",
            json={"yandexPassportOauthToken": self.oauth_token},
        )
        response.raise_for_status()
        response_json = response.json()
        print(response_json)
        return response_json["iamToken"]


config = Config()
