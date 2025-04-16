import yadisk
import pandas as pd
from config import config as cfg
import os

print('Starting Yandex Disk upload...')
client = yadisk.Client(token=cfg.yd_token)
print("Client created")

with client:
    cur_dir = os.path.dirname(__file__)
    df = pd.read_csv(f"{cur_dir}/user_actions.csv")
    df["datetime"] = pd.to_datetime(df["datetime"], format="%d-%m-%Y %H:%M:%S")
    print("Readed csv file...")
    df.to_excel(f"{cur_dir}/user_actions.xlsx", index=False)
    print("Converted .csv to .xlsx file")
    client.upload(
        f"{cur_dir}/user_actions.xlsx",
        "/bot_logs/user_actions.xlsx",
        overwrite=True
    )
    print("file user_actions.xlsx uploaded to Yandex disc")
    if os.path.exists(f"{cur_dir}/user_actions.xlsx"):
        os.remove(f"{cur_dir}/user_actions.xlsx")
        print("Deleted local file user_actions.xlsx")
