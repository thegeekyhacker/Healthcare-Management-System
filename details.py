import mysql.connector as sqltor
import os
# import datetime
from datetime import date, datetime

con = sqltor.connect(host="localhost", user="root",
                     passwd="admin", database="healthcare_management")
cursor = con.cursor()


def calculate_age(birthdate_str):
    # Parse the input string into a datetime.date object
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()

    # Get the current date
    current_date = date.today()

    # Calculate the age
    age = current_date.year - birthdate.year - \
        ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

    return age


def details(patientid):
    cursor.execute(
        f"select first_name, middle_name, last_name, date_of_birth, gender, medical_history, blood_group from patients where patient_id = '{patientid}'")
    data = cursor.fetchall()

    pname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]
    age = calculate_age(data[0][3])
    gender = data[0][4]
    past_complications = data[0][5]
    blood_group = data[0][6]

    # Get the list of files in the "prescriptions" folder
    folder_name = "prescriptions"
    files = os.listdir(folder_name)

    # Filter files based on everything before the '_' matching with patient id
    matching_files = [file for file in files if file.split('_')[
        0] == patientid]

    # Print current date and time
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time_string = datetime.now().strftime("%H:%M:%S")
    print(f"Current Date: {current_date}")
    print(f"Current Time: {current_time_string}")

    # Print patient details
    print(f"Patient Name: {pname}")
    print(f"Age: {age} years")
    print(f"Gender: {gender}")
    print(f"Past Complications: {past_complications}")
    print(f"Blood Group: {blood_group}")

    # Print contents of matching files
    for file_name in matching_files:
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'r') as file:
            file_contents = file.read()
            print(f"\nFile Contents for {file_name}:\n{file_contents}")

# Example usage
# details('P1')
#
