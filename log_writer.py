import csv
import datetime
import os

cur_dir = os.path.dirname(__file__)
class UserLogWriter:

    def __init__(self, file_name=f"{cur_dir}/user_actions.csv"):
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


log_writer = UserLogWriter(file_name=f"{cur_dir}/user_actions.csv")
