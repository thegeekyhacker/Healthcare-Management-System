from utility.sql_util import (
    fetch_all,
    execute_query,
    commit_transaction,
    close_db_connection,
)
from utility import hash_passwd

users = fetch_all("SELECT User_Id, Password FROM credentials")

for user_id, plain_password in users:
    hashed = hash_passwd(plain_password)
    execute_query("UPDATE credentials SET Password = %s WHERE User_Id = %s",
                  (hashed, user_id))
    print(f"Updated password for {user_id}")

commit_transaction()
close_db_connection()
print("\nAll passwords hashed successfully!")
