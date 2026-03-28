
from utility.sql_util import fetch_all


def appointment(userid):
    data = fetch_all(
        f"select * from appointments where doctor_id = '{userid}' and scheduled = 1")
    # print(data)
    for i in data:
        date = i[1]
        text = f"You has an appointment with {i[3]} at {i[2]} on {date}."
        print(text)

# appointment('D1')  To test only this file/feature
