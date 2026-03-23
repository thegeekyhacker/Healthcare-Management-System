import mysql.connector as sqltor
import convertdate
from config import SQL

con = sqltor.connect(host=SQL.host, user=SQL.user,
                     passwd=SQL.password, database=SQL.database)
cursor = con.cursor()


def appointment(userid):
    cursor.execute(
        f"select * from appointments where doctor_id = '{userid}' and scheduled = 1")
    data = cursor.fetchall()
    # print(data)
    for i in data:
        date = i[1]
        # date = date.replace("-", " ")
        # date = convertdate.convert_date_format(date)
        text = f"You has an appointment with {i[3]} at {i[2]} on {date}."
        print(text)

# appointment('D1')
