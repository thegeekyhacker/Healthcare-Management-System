from connector import get_db_connection

con, cursor = get_db_connection()


def newpatient():
    cursor.execute("Select * from appointments")
    data = cursor.fetchall()
    count = len(data)
    pat_id = "P"+str(count)
    print(pat_id)
    first_name = input("Enter the patient's first name :")
    middle_name = input("Enter the patient's middle name :")
    last_name = input("Enter the patient's last name :")
    dob = input("Enter the patient's DOB :")
    gender = input("Enter the patient's gender :")
    address = input("Enter the patient's address :")
    medHis = input("Enter the patient's medical history :")
    email_id = input("Enter the patient's email_id :")
    blood_group = input("Enter the patient's blood group :")
    phoneno = input("Enter the patient's phone number :")
    insuranceid = input("Enter the patient's Insurance id :")
    cursor.execute(
        f"insert into patients values ('{pat_id}','{first_name}','{middle_name}','{last_name}','{dob}','{gender}','{address}','{medHis}','{email_id}','{blood_group}','{phoneno}','{insuranceid}')")
    con.commit()
    con.close()
# newpatient()  To test only this file/feature

