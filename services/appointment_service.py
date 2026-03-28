from utility.sql_util import (
    fetch_all,
    execute_query,
    commit_transaction,
    close_db_connection,
)


def appointment(userid):
    data = fetch_all(
        f"select * from appointments where doctor_id = '{userid}' and scheduled = 1")
    for i in data:
        date = i[1]
        text = f"You has an appointment with {i[3]} at {i[2]} on {date}."
        print(text)


def createapp():
    data = fetch_all("Select * from appointments")
    count = len(data)
    app_id = count + 1
    app_date = input("Enter the appointment date in YYYY-MM-DD format : ")
    app_time = input("Enter the appointment time in HH:MM:SS format : ")
    pname = input("Enter the patient name : ")
    scheduled = 1
    canceled = 0
    completed = 0
    specialization = input("Enter the specialization : ")
    department = input("Enter the department : ")
    patientid = input("Enter patient id : ")
    doctorid = input("Enter doctor id : ")
    execute_query(
        f"insert into appointments values ({app_id},'{app_date}','{app_time}','{pname}',{scheduled},{canceled},{completed},'{specialization}','{department}','{patientid}','{doctorid}')")
    print("Appointment scheduled successfully")
    commit_transaction()
    close_db_connection()
