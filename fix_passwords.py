from connector import get_db_connection
from utility import hash_passwd

con, cursor = get_db_connection()

cursor.execute("SELECT User_Id, Password FROM credentials")
users = cursor.fetchall()

for user_id, plain_password in users:
    hashed = hash_passwd(plain_password)
    cursor.execute("UPDATE credentials SET Password = %s WHERE User_Id = %s",
                   (hashed, user_id))
    print(f"Updated password for {user_id}")

con.commit()
con.close()
print("\nAll passwords hashed successfully!")