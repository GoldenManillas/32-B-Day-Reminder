# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import smtplib as SMTP
import pandas as p
import os
from io import StringIO
import datetime as dt

sender_email = os.environ.get("SENDER_EMAIL")
reciever_email = os.environ.get("RECEIVER_EMAIL")
sender_password = os.environ.get("PASSWORD")
dates = p.read_csv(StringIO(os.environ.get("DATES")))

message_header = "Subject:B-Day Reminder\n\nHey, just a heads up,"

date_dict = {}
for (index, data_row) in dates.iterrows():
    new_key = (data_row.month, data_row.day)
    if new_key in date_dict:
        current_names = date_dict[new_key]
        current_names.append(data_row["name"])
        date_dict[new_key] = current_names
    else:
        date_dict[new_key] = [data_row["name"]]

tuples_for_the_next_week = []
now = dt.datetime.now()
for x in range(0, 8):
    end_date = now + dt.timedelta(days=x)
    tuples_for_the_next_week.append((end_date.month, end_date.day))

message_body = ""
counter = 0
for date_tuple in tuples_for_the_next_week:
    if date_tuple in date_dict:
        name_array = date_dict[date_tuple]
        name_string = ""
        match(len(name_array)):
            case 0:
                pass
            case 1:
                name_string += name_array[0] + "'s"
            case 2:
                name_string += name_array[0] + " and " + name_array[1] + "'s"
            case _:
                last_index = len(name_array) - 1
                
                for name in name_array[0:last_index]:
                    name_string += name + ", "
                name_string += "and " + name_array[last_index] + "'s"


        match counter:
            case 0:
                message_body += f"It's {name_string} Birthday today, you should get on that." + "\n"
            case _:
                message_body += f"{name_string} Birthday is in {counter} days, FYI." + "\n"
    counter+=1


if message_body != "":
    connection = SMTP.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_password)
    email_body = f"{message_header}{message_body}"
    connection.sendmail(from_addr=sender_email, to_addrs=reciever_email, msg=email_body)
    connection.close()
