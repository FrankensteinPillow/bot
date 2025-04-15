import csv
import datetime
import os

import requests


class Config:

    def __init__(self):
        self.tg_token = os.getenv("TG_TOKEN", "")
        self.oauth_token = os.getenv("OAUTH_TOKEN", "")
        self.folder_id = os.getenv("FOLDER_ID", "")

    def get_iam_token(self):
        response = requests.post(
            "https://iam.api.cloud.yandex.net/iam/v1/tokens",
            json={"yandexPassportOauthToken": self.oauth_token},
        )
        response.raise_for_status()
        response_json = response.json()
        print(response_json)
        return response_json["iamToken"]


class UserLogWriter:

    def __init__(self, file_name="user_actions.csv"):
        self._file_name = file_name
        self._file = open(self._file_name, "a", newline="")
        self._writer = csv.DictWriter(
            self._file,
            fieldnames=["user_id", "datetime", "action"],
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        try:
            if os.stat(self._file_name).st_size == 0:
                self._writer.writeheader()
                self._file.flush()
        except FileNotFoundError:
            self._writer.writeheader()
            self._file.flush()

    def write_log(self, user_id: str, action: str):
        now = datetime.datetime.now()
        self._writer.writerow(
            {
                "user_id": user_id,
                "datetime": now.strftime("%d-%m-%Y %H:%M:%S"),
                "action": action,
            }
        )
        self._file.flush()


config = Config()
log_writer = UserLogWriter(file_name="user_actions.csv")
