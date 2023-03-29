"""
hash generator with no salt
"""
import secrets
import hashlib
import sys
import sqlite3

#Create DB
conn = sqlite3.connect('auth.db')
print("opened db successfully")

#Create table in DB
conn.execute('''CREATE TABLE  IF NOT EXISTS auth
                ('username' VARCHAR NOT NULL,
                'password' VARCHAR NOT NULL);''')
print("Auth table created successfully")
conn.close()


#Insert commands
def db_in():
    conn = sqlite3.connect('auth.db')
    username = input("Please enter a username\n")
    password = input("Please enter a password\n")
    enc_pw = password.encode()
    hashed_pw = hashlib.sha224(enc_pw).hexdigest()
    script = f"INSERT INTO auth (username,password) VALUES ('{username}', '{hashed_pw}')"
    conn.execute(script)
    conn.commit()
    print("Insert successful")
    conn.close()
    
#login
def login():
    conn = sqlite3.connect('auth.db')
    c = conn.cursor()
    username = input("Please enter a username\n")
    password = input("Please enter a password\n")
    enc_pw = password.encode()
    hashed_pw = hashlib.sha224(enc_pw).hexdigest()
    script = f"SELECT username FROM auth WHERE username='{username}' AND password='{hashed_pw}';"
    c.execute(script)
    if not c.fetchone():
        print("\nLOGIN FAILED.")
    else:
        print("\nLOGIN SUCCESSFUL!")
 
 
#show all users
def select_star():
    conn = sqlite3.connect('auth.db')
    cursor = conn.execute('SELECT username, password FROM auth')
    for row in cursor:
        print("USERNAME:", row[0])
        print("PASSWORD:", row[1], "\n")
    conn.close()
 
#clear table
def clear_table():
    conn = sqlite3.connect('auth.db')
    c = conn.cursor()
    c.execute("DELETE FROM auth;",)
    conn.commit()
    print("Deleted", c.rowcount, "rows from table.")
    conn.close()
    
#menu
def menu():
    print("\nPlease choose an option below:\n")
    while 1:
        try:
            choice = int(input("1: Create a user\n2: Show all users\n3: Login\n4: Clear table\n5: Exit\n"))
            break
        except ValueError:
            print("Please choose '1', '2', '3', '4', or '5'\n")
            continue
        if choice not in (1, 2, 3, 4, 5):
            print("Please choose '1', '2', '3', '4', or '5'\n")
            continue
    if choice == 1:
        print("Please create a user\n")
        db_in()
    elif choice == 2:
        print("Here are all users currently in the table\n")
        select_star()
    elif choice == 3:
        print("Please login\n")
        login()
    elif choice == 4:
        print("Clearing table...")
        clear_table()
    elif choice == 5:
        clear_table()
        sys.exit()
        
def main():
    while 1:
        menu()
        
        
main()