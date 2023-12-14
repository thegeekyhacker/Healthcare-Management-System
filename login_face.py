import verify

def login_face(username):
    check,name = verify.verify()
    if check == True:
        if name == username:
            print("Logged in Successfully")
            return True
        else:
            print("Invalid Username")
            return False
    else:
        print("No such user exists")
        return False