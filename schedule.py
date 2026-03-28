from utility.sql_util import fetch_all


def schedule(userid):
    data = fetch_all(
        f"select day,type_of_work,time from doctorschedules where doctor_id = '{userid}'")
    result = fetch_all(
        f"SELECT doctor_name from doctors where doctor_id = '{userid}'")
    # print(data)
    for i in data:
        text = f"{result[0][0]} has {i[1]} on {i[0]} from {i[2]}."
        print(text)


# schedule('D1')  To test only this file/feature
