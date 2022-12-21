import datetime

#Получение сегодняшней и завтрашней даты
def get_tomorrow_date() -> str:
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y.%m.%d")
    return tomorrow

def get_today_date() -> str:
    today = datetime.datetime.now().strftime("%Y.%m.%d")
    return today

#Напоминалка
def delta_time(reminder_time: str) -> float:
    try:
        [year, month, day, hour, minute] = map(int, reminder_time.split('.'))
        delta = datetime.datetime(year, month, day, hour, minute) - datetime.datetime.now()
        return delta.total_seconds()
    except:
        return -1