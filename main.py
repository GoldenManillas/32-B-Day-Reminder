import requests as r
import datetime as dt
import smtplib as SMTP

DAYS_FOR_NOTIFICATION = 20
message_header = "Subject:B-Day Reminder\n\nHey, just a heads up,\n"

#sender_email     = os.environ.get("SENDER_EMAIL")
#reciever_email   = os.environ.get("RECEIVER_EMAIL")
#sender_password  = os.environ.get("PASSWORD")
#date_url         = os.environ.get("DATE")

sender_email = "test.email.af8b3@gmail.com"
reciever_email = "test.email.af8b3@gmail.com"
sender_password = "qfxu ootc ulys oxgf"
date_url = "https://api.sheety.co/958f28b7e1d34536995ee3a6ee84df20/bdays/sheet1"

print("Starting")
resp = r.get(date_url)

resp.raise_for_status()
row_json = resp.json()["sheet1"]

procesed_list = []
events_list = []

for x in row_json:

    now = dt.datetime.now()
    target = now.date().replace(day = x["day"], month=x["month"])
    if (now.date() > target):
        target = target.replace(year=target.year + 1)


    time_delta = target - now.date()
    if "nonBirthdayMessage" in x:

        if(time_delta.days < DAYS_FOR_NOTIFICATION):
            new_dict = {"name":x["name"], "daysUntilB-Day":time_delta.days, "message":x["nonBirthdayMessage"]}
            events_list.append(new_dict)
    else:

        if(time_delta.days < DAYS_FOR_NOTIFICATION):
            new_dict = {"name":x["name"], "daysUntilB-Day":time_delta.days}
            procesed_list.append(new_dict)


ordered_list = {}
for entry in procesed_list:
    if entry["daysUntilB-Day"] in ordered_list:
        ordered_list[entry["daysUntilB-Day"]].append(entry["name"])
    else:
        ordered_list[entry["daysUntilB-Day"]] = [entry["name"]]


final_message_string = ""
for num_days in sorted(ordered_list):
    name_list = ordered_list[num_days]
    if len(name_list) > 1:
        result = ", ".join(name_list[:-1]) + ", and " + name_list[-1]
        posessive = "have"
    else:
        result = "".join(name_list)
        posessive = "has"

    if num_days > 1:
        message_string = f"{result} {posessive} a birthday in {num_days} days. Make sure you're on that!"
    elif num_days == 1:
        message_string = f"{result} {posessive} a birthday tomorrow. Make sure you're on that!"
    else:
        message_string = f"{result} {posessive} a birthday today. Make sure you send a text!"

    final_message_string += message_string + "\n"

final_message_string += "\n"

for event in events_list:
    final_message_string += f"Heads up, {event["name"]} is in {num_days} days. {event["message"]}"


if final_message_string != "":
    connection = SMTP.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_password)
    email_body = f"{message_header}{final_message_string}"
    connection.sendmail(from_addr=sender_email, to_addrs=reciever_email, msg=email_body)
    connection.close()

    
