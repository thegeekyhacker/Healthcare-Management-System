import mysql.connector as sqltor
con = sqltor.connect(host="localhost",user ="root",passwd = "admin",database="hcm")
cursor = con.cursor()

def login(username,password):
    query = f"select Password from credentials where User_Id = '{username}'"
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0:
        print("No such Username")
        print("Kindly enter the correct username or register for a new account")
        return False
    else:
        if password == data[0][0]:
            print("Logged in Successfully")
            return True
        else:
            print("Incorrect Password")
            print(f"Kindly enter the correct password for the username : {username}")
            return False