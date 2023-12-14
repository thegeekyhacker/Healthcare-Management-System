import greeting
import login
import register
import login_face
import doctor
import admin
import passwordhide

while True:
    print("Welcome to the Healthcare Management System")
    print(greeting.greeting())
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    ans = input("Enter the choice you want to perform : ")
    if ans.lower() == 'login':
        print("Kindly choose the method for logging in : ")
        print("1. Face Recognition (face) ")
        print("2. Username and Password (pass) ")
        log_ans = input("Enter your choice : ")
        if log_ans.lower() == "pass":
            while True:
                userid = input("Enter the Username : ")
                passwd = passwordhide.get_hidden_input("Enter the Password : ")
                if login.login(userid,passwd):
                    if userid[0] == 'D':
                        doctor.doctor(userid)
                        break
                    else:
                        admin.admin(userid)
                        break
        elif log_ans.lower() == "face":
            while True:
                userid = input("Enter the Username : ")
                if login_face.login_face(userid):
                    if userid[0] == 'D':
                        doctor.doctor(userid)
                        break
                    else:
                        admin.admin(userid)
                        break

    elif ans.lower() == 'register':
        register.register()
    elif ans.lower() == 'exit':
        print("Have a nice day ahead!")
        exit(0)
    else:
        print('Invalid option')
        print('Kindly enter one of "Login", "Register" or "Exit"')