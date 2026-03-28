from utility.sql_util import (
    fetch_all,
    execute_query,
    commit_transaction,
    close_db_connection,
)


def newpatient():
    data = fetch_all("Select * from appointments")
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
    execute_query(
        f"insert into patients values ('{pat_id}','{first_name}','{middle_name}','{last_name}','{dob}','{gender}','{address}','{medHis}','{email_id}','{blood_group}','{phoneno}','{insuranceid}')")
    commit_transaction()
    close_db_connection()
# newpatient()  To test only this file/feature
