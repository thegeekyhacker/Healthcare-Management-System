import mysql.connector as sqltor
from config import SQL

con = sqltor.connect(host=SQL.host, user=SQL.user,
                     passwd=SQL.password, database=SQL.database)
cursor = con.cursor()


def schedule(userid):
    cursor.execute(
        f"select day,type_of_work,time from doctorschedules where doctor_id = '{userid}'")
    data = cursor.fetchall()
    cursor.execute(
        f"SELECT doctor_name from doctors where doctor_id = '{userid}'")
    result = cursor.fetchall()
    # print(data)
    for i in data:
        text = f"{result[0][0]} has {i[1]} on {i[0]} from {i[2]}."
        print(text)


# schedule('D1')
