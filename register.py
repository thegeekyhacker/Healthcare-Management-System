import mysql.connector as sqltor
import re
import capture
import passwordhide
con = sqltor.connect(host="localhost",user="root",passwd="admin",database="hcm")
cursor = con.cursor()

def is_space(str1):
    if str1 == " ":
        return True
    return False

def is_valid_password(password):
    if len(password) < 10:
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not re.search(r'[!@#$%^&*?]', password):
        return False
    return True


def register():
    print("Are you registering for : ")
    print("1. Administration Staff Account(admin)")
    print("2. Doctor Account(doctor)")
    choice = input("Kindly enter your choice : ")
    if choice.lower() == 'admin':
        query = f"select admin_id from administrativestaff"
        cursor.execute(query)
        data = cursor.fetchall()
        new_num = int(data[-1][0][1:]) + 1
        new_id = 'A' + str(new_num)
        print(f"Your username is : {new_id}")
        password = passwordhide.get_hidden_input("Enter your password : ")
        while not is_valid_password(password):
            print("Password is not strong enough")
            print("A strong password must have atleast 1 number, 1 special character, 1 lowercase character, 1 uppercase character and should be atleast 10 characters long")
            password = input("Enter your password : ")
        cursor.execute(f"insert into credentials values('{new_id}','{password}')")
        print("Kindly enter your details (Fields with (*) are compulsory to enter. Enter a space for others where you want to leave the field empty)")
        fname = input("Enter your First Name : (*)")
        while is_space(fname):
            print("Kindly enter a valid first name")
            fname = input("Enter your First Name : (*)")
        mname = input("Enter your Middle Name : ")
        if is_space(mname):
            mname = 'NULL'
        lname = input("Enter your Last Name : (*)")
        while is_space(lname):
            print("Kindly enter a valid name")
            lname = input("Enter your First Name : (*)")
        dob = input("Enter your Date of Birth(dd/mm/yyyy) : (*)")
        while is_space(dob):
            print("Kindly enter a valid Date of Birth")
            dob = input("Enter your Date of Birth(dd/mm/yyyy) : (*)")
        gender = input("Enter your Gender : (*)")
        while is_space(gender):
            print("Kindly enter a valid gender")
            gender = input("Enter your Gender : (*)")
        address = input("Enter your Address : (*)")
        while is_space(address):
            print("Kindly enter a valid address")
            address = input("Enter your Address : (*)")
        position = input("Enter your position : (*)")
        while is_space(position):
            print("Kindly enter a valid position")
            position = input("Enter your Position : (*)")
        phone = input("Enter your Phone Number : (*)")
        while is_space(phone):
            print("Kindly enter a valid phone number")
            phone = input("Enter your Phone Number : (*)")
        email = input("Enter your Email : (*)")
        while is_space(email):
            print("Kindly enter a valid email")
            email = input("Enter your Email : (*)")
        ip = input("Enter your IP Address : (*)")
        while is_space(ip):
            print("Kindly enter a valid IP Address")
            ip = input("Enter your IP Address : (*)")
        cursor.execute(f"insert into administrativestaff values ('{new_id}','{fname}','{mname}','{lname}','{dob}','{gender}','{address}','{position}','{phone}','{email}','{ip}')")
        print("Account created successfully")
        con.commit()
        print("Kindly take a picture for facial recognition")
        print("When the webcam window opens press 's' after you are happy with your face in the webcam and save the picture.")
        print("Else press 'q' to quit")
        capture.capture_image(new_id)

    elif choice.lower() == 'doctor':
        query = f"select doctor_id from doctors"
        cursor.execute(query)
        data = cursor.fetchall()
        if len(data) == 0:
            new_id = 'D1'
        else:
            new_num = int(data[-1][0][1:]) + 1
            new_id = 'D' + str(new_num)
        print(f"Your username is : {new_id}")
        password = passwordhide.get_hidden_input("Enter your password : ")
        while not is_valid_password(password):
            print("Password is not strong enough")
            print("A strong password must have atleast 1 number, 1 special character, 1 lowercase character, 1 uppercase character and should be atleast 10 characters long")
            password = input("Enter your password : ")
        cursor.execute(f"insert into credentials values('{new_id}','{password}')")
        print("Kindly enter your details (Fields with (*) are compulsory to enter. Enter a space for other s where you want to leave the field empty)")
        fname = input("Enter your First Name : (*)")
        while is_space(fname):
            print("Kindly enter a valid name")
            fname = input("Enter your First Name : (*)")
        mname = input("Enter your Middle Name : ")
        if is_space(mname):
            mname = ''
        lname = input("Enter your Last Name : (*)")
        while is_space(lname):
            print("Kindly enter a valid name")
            lname = input("Enter your First Name : (*)")
        dname = fname + ' ' + mname + ' ' + lname
        dob = input("Enter your Date of Birth(dd/mm/yyyy) : (*)")
        while is_space(dob):
            print("Kindly enter a valid Date of Birth")
            dob = input("Enter your Date of Birth(dd/mm/yyyy) : (*)")
        gender = input("Enter your Gender : (*)")
        while is_space(gender):
            print("Kindly enter a valid gender")
            gender = input("Enter your Gender : (*)")
        address = input("Enter your Address : (*)")
        while is_space(address):
            print("Kindly enter a valid address")
            address = input("Enter your Address : (*)")
        specialization = input("Enter your Specialization : (*)")
        while is_space(specialization):
            print("Kindly enter a valid Specialization")
            specialization = input("Enter your Specialization : (*)")
        license_num = input("Enter your License Number : (*)")
        while is_space(license_num):
            print("Kindly enter a valid License number")
            phone = input("Enter your License Number : (*)")
        age = int(input("Enter your Age : (*)"))
        experience = input("Enter your Experience : (*)")
        while is_space(experience):
            print("Kindly enter a valid experience")
            experience = input("Enter your Experience : (*)")
        department = input("Enter your Department : (*)")
        while is_space(department):
            print("Kindly enter a valid department")
            department = input("Enter your Department : (*)")
        email = input("Enter your Email ID : (*)")
        while is_space(email):
            print("Kindly enter a valid email id")
            email = input("Enter your Email ID : (*)")
        mobile = input("Enter your Mobile Number : (*)")
        while is_space(mobile):
            print("Kindly enter a valid mobile number")
            mobile = input("Enter your Mobile Number : (*)")
        language = input("Enter your Languages : (*)")
        while is_space(experience):
            print("Kindly enter a valid language")
            language = input("Enter your Language : (*)")
        visitation_charge = float(input("Enter your Visitation Charge : (*)(Enter in two decimal places)"))
        while is_space(visitation_charge):
            print("Kindly enter a valid visitation charge")
            visitation_charge = float(input("Enter your Visitation Charge : (*)(Enter in two decimal places)"))
        ip = input("Enter your IP Address : (*)")
        while is_space(ip):
            print("Kindly enter a valid ip address")
            ip = input("Enter your IP Address : (*)")
        cursor.execute(f"insert into doctors values ('{new_id}','{dname}','{dob}','{gender}','{address}','{specialization}','{license_num}','{age}','{experience}','{department}','{email}','{mobile}','{language}','{visitation_charge}','{ip}')")
        print("Account created successfully")
        con.commit()
        print("Kindly take a picture for facial recognition")
        print("When the webcam window opens press 's' after you are happy with your face in the webcam and save the picture.")
        print("Else press 'q' to quit")
        capture.capture_image(new_id)
        print("User Registered Successfully")
    else:
        print("Invalid Choice")
        print("Kindly enter either 'admin' or 'doctor'")