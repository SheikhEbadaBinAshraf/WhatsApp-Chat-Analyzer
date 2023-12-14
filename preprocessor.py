import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dates_without_unicode = [date.replace('\u202f', '') for date in dates]

    df = pd.DataFrame({"user_messages": messages, "messages_date": dates_without_unicode})
    # Concert message_date type
    df["messages_date"] = pd.to_datetime(df["messages_date"], format="%m/%d/%y, %I:%M%p")

    df.rename(columns={"messages": "dates_without_unicode"}, inplace=True)

    users = []
    messages = []

    for message in df["user_messages"]:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_Notification")
            messages.append(entry[0])

    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_messages"], inplace=True)

    df["date"] = df["messages_date"].dt.date

    df["year"] = df["messages_date"].dt.year

    df["month_num"] = df["messages_date"].dt.month

    df["Month"] = df["messages_date"].dt.month_name()

    df["Day"] = df["messages_date"].dt.day

    df["day_name"] = df["messages_date"].dt.day_name()

    df["Hour"] = df["messages_date"].dt.hour

    df["Minute"] = df["messages_date"].dt.minute

    return df