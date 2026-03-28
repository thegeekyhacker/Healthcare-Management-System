import os
from datetime import date, datetime

from utility.sql_util import fetch_all, execute_query, commit_transaction, close_db_connection


def calculate_age(birthdate_str):
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
    current_date = date.today()
    age = current_date.year - birthdate.year - \
        ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    return age


def details(patientid):
    data = fetch_all(
        f"select first_name, middle_name, last_name, date_of_birth, gender, medical_history, blood_group from patients where patient_id = '{patientid}'")

    pname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]
    age = calculate_age(data[0][3])
    gender = data[0][4]
    past_complications = data[0][5]
    blood_group = data[0][6]

    folder_name = "prescriptions"
    files = os.listdir(folder_name)

    matching_files = [file for file in files if file.split('_')[
        0] == patientid]

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time_string = datetime.now().strftime("%H:%M:%S")
    print(f"Current Date: {current_date}")
    print(f"Current Time: {current_time_string}")

    print(f"Patient Name: {pname}")
    print(f"Age: {age} years")
    print(f"Gender: {gender}")
    print(f"Past Complications: {past_complications}")
    print(f"Blood Group: {blood_group}")

    for file_name in matching_files:
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'r') as file:
            file_contents = file.read()
            print(f"\nFile Contents for {file_name}:\n{file_contents}")


def newpatient():
    data = fetch_all("Select * from appointments")
    count = len(data)
    pat_id = "P" + str(count)
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


def get_patient_phone(patient_id):
    rows = fetch_all(
        f"select phone_number from patients where patient_id = '{patient_id}'")
    if not rows:
        return None
    return rows[0][0]
