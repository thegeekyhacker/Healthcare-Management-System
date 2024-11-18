import encode
import mysql.connector as sqltor
con = sqltor.connect(host="localhost", user="root",
                     passwd="admin", database="healthcare_management")
cursor = con.cursor()


def login(username, password):
    query = f"select Password from credentials where User_Id = '{username}'"
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0:
        print("No such Username")
        print("Kindly enter the correct username or register for a new account")
        return False
    else:
        temp_passwd = data[0][0]
        # temp_passwd = encode.decrypt_password(temp_passwd)
        if encode.verify(password, temp_passwd):
            print("Logged in Successfully")
            return True
        else:
            print("Incorrect Password")
            print(
                f"Kindly enter the correct password for the username : {username}")
            return False


# login()
