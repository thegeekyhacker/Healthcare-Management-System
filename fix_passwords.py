import bcrypt
import mysql.connector as sqltor
from config import SQL

SALT_PREFIX = "ujp"
SALT_SUFFIX = "ujp"

con = sqltor.connect(host=SQL.host, user=SQL.user,
                     passwd=SQL.password, database=SQL.database)
cursor = con.cursor()

cursor.execute("SELECT User_Id, Password FROM credentials")
users = cursor.fetchall()

for user_id, plain_password in users:
    peppered = SALT_PREFIX + plain_password + SALT_SUFFIX
    hashed = bcrypt.hashpw(peppered.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE credentials SET Password = %s WHERE User_Id = %s",
                   (hashed.decode('utf-8'), user_id))
    print(f"Updated password for {user_id}")

con.commit()
con.close()
print("\nAll passwords hashed successfully!")