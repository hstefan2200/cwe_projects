"""
hash generator with salt
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
                'password' VARCHAR NOT NULL,
                'salt' VARCHAR NOT NULL);''')
print("Auth table created successfully")
conn.close()


#Insert commands
def db_in():
    salt = secrets.token_hex(112)
    conn = sqlite3.connect('auth.db')
    username = input("Please enter a username\n")
    password = input("Please enter a password\n")
    s_pw = salt + password
    enc_pw = s_pw.encode()
    hashed_pw = hashlib.sha224(enc_pw).hexdigest()
    script = f"INSERT INTO auth (username,password,salt) VALUES ('{username}', '{hashed_pw}', '{salt}')"
    conn.execute(script)
    conn.commit()
    print("Insert successful")
    conn.close()
    
#login
def login():
    while 1:
        conn = sqlite3.connect('auth.db')
        c = conn.cursor()
        username = input("Please enter a username\n")
        password = input("Please enter a password\n")
        script = f"SELECT username, password, salt FROM auth WHERE username='{username}';" #AND password='{hashed_pw}';"
        c.execute(script)
        try:
            db_uname, db_pword, db_salt = c.fetchone()
            break
        except:
            print("\nUser Not Found")
            continue
    if db_uname is not None:
        enc_pw = (db_salt + password).encode()
        hashed_pw = hashlib.sha224(enc_pw).hexdigest()
        if username == db_uname and hashed_pw == db_pword:
            print("\nLogin Successful!")
        else:
            print("\nLogin Failed")
    else:
        print("\nUser not found")

 
 
#show all users
def select_star():
    conn = sqlite3.connect('auth.db')
    cursor = conn.execute('SELECT username, password, salt FROM auth')
    for row in cursor:
        print("USERNAME:", row[0])
        print("PASSWORD:", row[1])
        print("SALT:", row[2], "\n")
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