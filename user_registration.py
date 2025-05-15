import mysql.connector as mycon
from mysql.connector import Error
import hashlib
from tkinter import messagebox  # Import messagebox to show alerts in GUI

def register_user(name, email, password):
     # Minimum password length
    MIN_PASSWORD_LENGTH = 8

    if len(password) < MIN_PASSWORD_LENGTH:
        messagebox.showerror("Error", f"Password must be at least {MIN_PASSWORD_LENGTH} characters long.")
        return
    try:
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print("\nPassword hashed.")

        
        mydb = mycon.connect(
            host="localhost",
            user="root",
            password="root@2024",
            database="sampleproject"
        )
        print("Connected to MySQL Database.")

        db_cur = mydb.cursor()
        print("Cursor created.")

        
        db_cur.execute('''
        INSERT INTO user(name, email, password, join_date)
        VALUES (%s, %s, %s, CURDATE())
        ''', (name, email, hashed_password))
        print("User details inserted.")

        mydb.commit()
        print("User registered successfully!")
        messagebox.showinfo("Success", "User registered successfully!")

    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", str(e))

    finally:
        if mydb.is_connected():
            db_cur.close()
            mydb.close()
            print("MySQL connection is closed")

