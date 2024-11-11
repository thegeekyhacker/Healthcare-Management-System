import mysql.connector as sqltor
con = sqltor.connect(host="localhost", user="root",
                     passwd="admin", database="healthcare_management")
cursor = con.cursor()


def createapp():
    cursor.execute("Select * from appointments")
    data = cursor.fetchall()
    count = len(data)
    app_id = count+1
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
    cursor.execute(
        f"insert into appointments values ({app_id},'{app_date}','{app_time}','{pname}',{scheduled},{canceled},{completed},'{specialization}','{department}','{patientid}','{doctorid}')")
    print("Appointment scheduled successfully")
    con.commit()
    con.close()
# createapp()
