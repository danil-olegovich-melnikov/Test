import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from .get_exchange_rate import get_exchange_rate


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_data_from_sheet() -> pd.DataFrame:
    credentials = ServiceAccountCredentials.from_json_keyfile_name("order/utils/gs_credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Test").sheet1

    rows = sheet.get_values()
    translations = {
        "№": "number",
        "заказ №": "order_number",
        "стоимость,$": "cost_dollar",
        "срок поставки": "delivery_date",
        "стоимость в руб.": "cost_rubles",
    }

    headers = [translations[name] for name in rows[0]]

    df = pd.DataFrame(rows[1:], columns=headers)
    df["number"] = df["number"].astype(int)
    df["order_number"] = df["order_number"].astype(int)
    df["cost_dollar"] = df["cost_dollar"].astype(int)
    df["cost_rubles"] = df["cost_dollar"] * df["delivery_date"].apply(get_exchange_rate)
    df["cost_rubles"] = df["cost_rubles"].round(0).astype(int)
    df["delivery_date"] = pd.to_datetime(df["delivery_date"], format="%d.%m.%Y").dt.date

    return df
