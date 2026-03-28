from utility.sql_util import fetch_one
from utility import verify


def login(username, password):
    query = f"select Password from credentials where User_Id = '{username}'"
    row = fetch_one(query)
    if row is None:
        print("No such Username")
        print("Kindly enter the correct username or register for a new account")
        return False
    else:
        temp_passwd = row[0]
        # temp_passwd = encode.decrypt_password(temp_passwd)
        if verify(password, temp_passwd):
            print("Logged in Successfully")
            return True
        else:
            print("Incorrect Password")
            print(
                f"Kindly enter the correct password for the username : {username}")
            return False


# login()  To test only this file/feature
