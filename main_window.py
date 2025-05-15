import mysql.connector as mycon
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
import hashlib 
from user_registration import register_user
from Quiz import *


def connect_to_db():
    try:
        mydb = mycon.connect(
            host="localhost",
            user="root",
            password="root@2024",
            database="sampleproject"
        )
        return mydb
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
        return None
    
# create function submit_feedback to insert the feedback in feedback table
def submit_feedback(username, feedback_text):
    mydb = connect_to_db()  # Establish connection
    if mydb:
        try:
            cursor = mydb.cursor()

            # SQL query to insert feedback
            sql_query = "INSERT INTO feedbacks (user_name, feedback_text) VALUES (%s, %s)"
            cursor.execute(sql_query, (username, feedback_text))

            mydb.commit()  # Save changes
            cursor.close()
            mydb.close()

            messagebox.showinfo("Success", "Feedback submitted successfully!")  # User confirmation
        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")


# create a function to show the feedback screen whaere user can give feedback and it gets stored in the feedbacks table
def show_feedback_screen():
    clear_screen()  # Call function to clear the screen
    global bg_image7_img
    bg_image7_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\feedback.png")
    bg_image7 = tk.Label(main_window, image=bg_image7_img)
    bg_image7.place(relheight=1, relwidth=1)

    # Create label with text, font & grid using tk
    tk.Label(main_window, text="FEEDBACK", font=("Helvetica", 50, "bold"), bg="silver", fg="black").grid(row=0, columnspan=2, pady=20)

   
    # crete the label and entry for name and feedback using ttk
    ttk.Label(main_window, text="USER NAME:", font=("Modern No. 20", 30, "italic")).grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_name = ttk.Entry(main_window, width=50)
    entry_name.grid(row=1, column=1, padx=20, pady=10)
    ttk.Label(main_window, text="FEEDBACK:", font=("Modern No. 20", 30, "italic")).grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_feedback = ttk.Entry(main_window, width=50)
    entry_feedback.grid(row=2, column=1, padx=20, pady=10)
    # Create the Submit and Back buttons with increased size
    ttk.Button(main_window, text="SUBMIT", command=lambda: submit_feedback(entry_name.get(), entry_feedback.get()), width=30).grid(row=3, columnspan=2, pady=20, ipadx=20, ipady=10)
    ttk.Button(main_window, text="BACK", command=lambda: choose(user=None), width=30).grid(row=4, columnspan=2, pady=10, ipadx=20, ipady=10)


def fetch_notes(sub):
    mydb = connect_to_db()
    if mydb:
        try:
            db_cur = mydb.cursor()
            db_cur.execute("SELECT note_text FROM learn WHERE category=%s", (sub,))
            learn = db_cur.fetchall()
            print("Notes fetched successfully")
            return learn
        except Error as e:
            messagebox.showerror("Error", f"Error fetching notes: {e}")
            print("Error fetching notes")
        finally:
            if mydb.is_connected():
                db_cur.close()
                mydb.close()
                print("Database connection closed")
 
    
def show_notes_screen(subject):
    clear_screen()
    
    global bg_image6_img
    bg_image6_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\learn.png")
    bg_image6 = tk.Label(main_window, image=bg_image6_img)
    bg_image6.place(relheight=1, relwidth=1)

    tk.Label(main_window, text="NOTES", font=("Helvetica", 50, "bold"), bg="silver", fg="black").grid(row=0, columnspan=2, pady=20)

    # Create a frame for the notes and add a scrollbar
    notes_frame = tk.Frame(main_window, bg="silver")
    notes_frame.place(relwidth=1, relheight=0.8, rely=0.1)  # Adjusted to fit the window size
    
    canvas = tk.Canvas(notes_frame, bg="silver")
    scrollbar = ttk.Scrollbar(notes_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="silver")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fetch and display notes
    notes = fetch_notes(subject)
    if notes:
        for index, note in enumerate(notes):
            tk.Label(scrollable_frame, text=note[0], font=("Helvetica", 20), fg="black").pack(pady=10, padx=10, anchor="w")
    else:
        tk.Label(scrollable_frame, text="No notes available for this subject.", font=("Helvetica", 20), bg="light blue").pack(pady=10, padx=10)

    # Back button to return to learning module
    ttk.Button(main_window, text="BACK", command=show_learn_screen, width=40).place(relx=0.5, rely=0.95, anchor="center")  # Positioned at the bottom center


def show_learn_screen():
    clear_screen()  # Call function to clear the screen
    global bg_image5_img
    bg_image5_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\learn.png")
    bg_image5=tk.Label(main_window, image=bg_image5_img)
    bg_image5.place(relheight=1,relwidth=1)

    # Create label with text, font & grid using tk
    tk.Label(main_window, text="LEARN", font=("Helvetica", 50, "bold"), bg="silver", fg="black").grid(row=0, columnspan=2, pady=20)

    subjects = ["SCIENCE", "MATH", "COMPUTER SCIENCE", "SOCIAL SCIENCE"]

    for index, subject in enumerate(subjects):
        ttk.Button(main_window, text=subject, command=lambda s=subject: show_notes_screen(s), width=40).grid(row=index + 1, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

    # Create the Back button
    ttk.Button(main_window, text="BACK", command=lambda: choose(user=None), width=50).grid(row=len(subjects) + 1, columnspan=2, pady=20, ipadx=20, ipady=10)
        
def show_leaderboard_screen(human):
    clear_screen()  # Call function to clear the screen
    global bg_image6_img

    # Connect to the database
    mydb = connect_to_db()
    if mydb:
        bg_image6_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\leaderboard.png")
        bg_image6=tk.Label(main_window, image=bg_image6_img)
        bg_image6.place(relheight=1,relwidth=1)

        try:
            # Fetch leaderboard data
            db_cur = mydb.cursor()
            db_cur.execute('''
            SELECT * FROM leaderboard ORDER BY leaderboard_id DESC
                    LIMIT 5''')
            leaderboard = db_cur.fetchall()

            # Add heading
            tk.Label(
                main_window,
                text="LEADERBOARD",
                font=("Helvetica", 30, "bold"),
                bg="silver",
                fg="black"
            ).grid(row=0, column=0, columnspan=2, pady=20)

            # Display leaderboard records
            if leaderboard:
                for index, record in enumerate(leaderboard):
                    tk.Label(
                        main_window,
                        text=f"{index + 1}. {record[3]} - {record[2]}",
                        font=("Helvetica", 20),
                        bg="silver",
                        fg="black"
                    ).grid(row=index + 3, column=0, columnspan=2, pady=5)
            else:
                tk.Label(
                    main_window,
                    text="No records found.",
                    font=("Helvetica", 20),
                    bg="silver",
                    fg="black"
                ).pack(pady=10)

        except Error as e:
            messagebox.showerror("Error", f"Error fetching leaderboard: {e}")
        finally:
            if mydb.is_connected():
                db_cur.close()
                mydb.close()

        # Add a Back button
        tk.Button(
            main_window,
            text="Back",
            font=("Helvetica", 15),
            bg="silver",
            fg="gold",
            command=lambda: choose(user=human)
        ).grid(row=len(leaderboard) + 2, column=0, columnspan=2, pady=20)

def show_topic_selection_screen(person):
    print(person)
    clear_screen()  # Call function to clear the screen
    global bg_image8_img
    bg_image8_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\topic.png")
    bg_image8=tk.Label(main_window, image=bg_image8_img)
    bg_image8.place(relheight=1,relwidth=1)

    # Create label with text, font & grid using tk
    tk.Label(main_window, text="SELECT A TOPIC", font=("Helvetica", 50, "bold"), bg="light blue").grid(row=0, columnspan=2, pady=20)

    # topics, this should be fetched from the database
    topics = ["SCIENCE", "MATH", "COMPUTER SCIENCE", "SOCIAL SCIENCE"]

    # Display topics using ttk buttons
    for index, topic in enumerate(topics):
        ttk.Button(main_window, text=topic, command=lambda t=topic: start_quiz(t), width=40).grid(row=index+1, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

    # Create the Back button
    ttk.Button(main_window, text="BACK", command=lambda: choose(user=person), width=50, style="Custom.TButton").grid(row=len(topics)+1, columnspan=2, pady=20, ipadx=20, ipady=10)

def start_quiz(topic):
    print(f"STARTING QUIZ ON TOPIC: {topic}")
    messagebox.showinfo("QUIZ", f"STARTING QUIZ ON TOPIC: {topic}")
    start_quizz(topic)


def next_window(way,curent_user):
    import logging
    logging.info(f"Current user: {curent_user}")
    if way == "LEARN":
        print("Learn selected")
        # Call the function to show the learn screen
        show_learn_screen()
    elif way == "Quiz":
        print("Quiz selected")
        # Call the function to show the topics screen
        show_topic_selection_screen(person=curent_user)
    elif way == "LEADERBOARD":
        print("Leaderboard selected")
        # Call the function to show the leaderboard screen
        show_leaderboard_screen(human=curent_user)
    elif way == "FEEDBACK":
        print("Feedback selected")
        # Call the function to show the feedback screen
        show_feedback_screen()
    else:
        print("Invalid selection")
        messagebox.showerror("Error", "Invalid selection. Please choose a valid option from the menu.")
        # Optionally, you can redirect to a default screen or show an error message
    # Log the navigation to a new page
    print("Navigated to a new page.")
    print("new page")


def show_qna_screen():
    print()
    clear_screen()

    global bg_image_qna_img
    bg_image_qna_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\qna.png")  
    bg_image_qna = tk.Label(main_window, image=bg_image_qna_img)
    bg_image_qna.place(relheight=1, relwidth=1)

    tk.Label(main_window, text="USER Q&A", font=("Helvetica", 50, "bold"), bg="silver", fg="black").grid(row=0, columnspan=2, pady=20)

    # Questions related to the application
    qna_list = [
        ("What is this application used for?", "It is a quiz and learning platform."),
        ("How does the leaderboard work?", "It ranks users based on quiz performance."),
        ("Can I give feedback?", "Yes, there is a feedback section for users."),
        ("What are the available quiz types?", "MCQs."),
        ("How do I start a quiz?", "Select 'Quiz' and choose a topic."),
        ("What happens if I fail a level?", "You must retry the level until passing."),
        ("Is there a learning section?", "Yes, it provides notes on 4 topics."),
        ("How do I know my progress?", "Not yet."),
        ("What is timer in the application?", "user have to give answer in given time."),
        ("Can I quit a quiz midway?", "Yes, there is a quit option in every quiz."),
    ]

    # Display questions and answers dynamically
    for index, (question, answer) in enumerate(qna_list):
        tk.Label(main_window, text=f"Q{index+1}: {question}", font=("Helvetica", 15, "bold"), bg="light blue").grid(row=index+1, column=0, padx=20, pady=5, sticky="w")
        tk.Label(main_window, text=f"A: {answer}", font=("Helvetica", 13), bg="lightyellow").grid(row=index+1, column=1, padx=20, pady=5, sticky="w")

    # Back button to return to Choose Your Way menu
    ttk.Button(main_window, text="BACK", command=lambda: choose(user=None), width=40).grid(row=len(qna_list)+2, columnspan=2, pady=20, ipadx=20, ipady=10)


def show_about_screen():
    print()
    clear_screen()

    global bg_image_about_img
    bg_image_about_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\about.png")  
    bg_image_about = tk.Label(main_window, image=bg_image_about_img)
    bg_image_about.place(relheight=1, relwidth=1)

    tk.Label(main_window, text="ABOUT APPLICATION", font=("Helvetica", 50, "bold"), bg="silver", fg="black").grid(row=0, columnspan=2, pady=20)

    # Information about the application
    about_text = """
    This application is created by Yashika and team (Manish Rana, Arvind, Devendra).
    
    📌 **Application Overview**:
    - A learning and quiz-based platform that enhances user knowledge.
    - Designed to provide educational notes, quizzes, leaderboards, and feedback options.

    📌 **Application Structure**:
    - Includes multiple windows such as **Login Screen, Learning Section, Quiz Section, Leaderboard, Feedback, and Choose Your Way**.
    - Interactive UI design using **Tkinter** for smooth navigation.
    
    📌 **Usage & Benefits**:
    - Helps users **learn, practice, and improve knowledge** in various subjects.
    - Tracks **user progress and quiz scores** via a **leaderboard system**.
    - Supports **real-time learning** with structured **notes and revision sections**.
    
    📌 **Technical Aspects**:
    - Developed using **Python** (Tkinter for UI design).
    - **SQL integration** to store user data, quiz performance, and feedback.
    - **Modular architecture** ensuring maintainability and expansion.

    🏆 **A powerful educational tool empowering learning through technology!**
    """

    tk.Label(main_window, text=about_text, font=("Helvetica", 13), bg="lightyellow", justify="left", wraplength=750).grid(row=1, columnspan=2, padx=20, pady=10)

    # Back Button to return to Choose Your Way menu
    ttk.Button(main_window, text="BACK", command=lambda: choose(user=None), width=40).grid(row=2, columnspan=2, pady=20, ipadx=20, ipady=10)


def choose(user):
    clear_screen()  
    print(user)
    global bg_image4_img

    bg_image4_img= tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\choose.png")
    bg_image4= tk.Label(image=bg_image4_img)
    bg_image4.place(relheight=1,relwidth=1)

    style = ttk.Style()
    style.configure("Custom.TButton", font=("Helvetica", 15), background="#D5F5E3", foreground="#154360", padding=10)

    # Create label with text, font & grid using tk
    tk.Label(main_window, text="CHOOSE YOUR WAY", font=("Helvetica", 50, "bold"), bg="silver", fg="black").grid(row=0, columnspan=2, pady=20)
    
   
    way = ["LEARN", "Quiz", "LEADERBOARD", "FEEDBACK"]
 
    # Display topics using ttk buttons
    for index, option in enumerate(way):
        ttk.Button(main_window, text=option, command=lambda w=option: next_window(way=w,curent_user=user), width=40).grid(row=index+1, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)
    # create additional buttons for Q&A and About
    ttk.Button(main_window, text="Q&A", command=show_qna_screen, width=40).grid(row=5, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)
    ttk.Button(main_window, text="ABOUT", command=show_about_screen, width=40).grid(row=6, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)
    
    # Create the Back button
    ttk.Button(main_window, text="BACK", command=show_login_screen, width=50,style="Custom.TButton").grid(row=len(way)+3, columnspan=4, pady=20, ipadx=20, ipady=10)

def login_user(email, password):
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        mydb = mycon.connect(
            host="localhost",
            user="root",
            password="root@2024",
            database="sampleproject"
        )
        db_cur = mydb.cursor()
        db_cur.execute('''
        SELECT * FROM user WHERE email=%s AND password=%s
        ''', (email, hashed_password))
        user = db_cur.fetchone()
        if user:
            db_cur.execute('''
            SELECT name FROM user WHERE email=%s AND password=%s
            ''', (email, hashed_password))
            user_name = db_cur.fetchone()
            user_name = user_name[0]  # Unpack the tuple to get the actual name
            print(f"LOGIN SUCCESSFUL! {user_name}")
            messagebox.showinfo(user_name, "LOGIN SUCCESSFUL!")
            choose(user=user_name)
#            show_topic_selection_screen()  # Call topic selection screen
        else:
            print("Invalid email or password.")
            messagebox.showerror("Error", "Invalid email or password.")
    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", str(e))
    finally:
        if mydb.is_connected():
            db_cur.close()
            mydb.close()
            print("MySQL connection is closed")

def show_register_screen():
    clear_screen()  # Call function to clear the screen
    global bg_image3_img
    bg_image3_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\registration.png")
    bg_image3=tk.Label(main_window, image=bg_image3_img)
    bg_image3.place(relheight=1,relwidth=1)

    # Create label with text, font & grid using tk
    tk.Label(main_window, text="REGISTRATION", font=("Times New Roman", 50, "bold"), bg="silver",fg="Black").grid(row=0, columnspan=2, pady=20)

    # Create the label and entry for name using ttk
    ttk.Label(main_window, text="NAME:", font=("Modern No. 20", 30,"italic")).grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_name = ttk.Entry(main_window, width=50)
    entry_name.grid(row=1, column=1, padx=20, pady=10)

    # Create the label and entry for email using ttk
    ttk.Label(main_window, text="EMAIL:", font=("Modern No. 20", 30,"italic")).grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_email = ttk.Entry(main_window, width=50)
    entry_email.grid(row=2, column=1, padx=20, pady=10)

    # Create the label and entry for password using ttk
    ttk.Label(main_window, text="PASSWORD:", font=("Modern No. 20", 30,"italic")).grid(row=3, column=0, padx=20, pady=10, sticky="e")
    entry_password = ttk.Entry(main_window, show='*', width=50)
    entry_password.grid(row=3, column=1, padx=20, pady=10)

    # Create the Register and Back buttons with increased size
    ttk.Button(main_window, text="REGISTER", command=lambda: register_user(entry_name.get(), entry_email.get(), entry_password.get()), width=30).grid(row=4, columnspan=2, pady=20, ipadx=20, ipady=10)
    ttk.Button(main_window, text="BACK", command=show_start_screen, width=30).grid(row=5, columnspan=2, pady=10, ipadx=20, ipady=10)


def show_login_screen():
    clear_screen()  # Call function to clear the screen
    
    global bg_image2_img
    bg_image2_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\login.png")
    bg_image2=tk.Label(main_window, image=bg_image2_img)
    bg_image2.place(relheight=1,relwidth=1)

    # Create label with text, font & grid using tk
    tk.Label(main_window, text="LOGIN",font=("Times New Roman", 50, "bold"), bg="silver",fg="black").grid(row=0, columnspan=2, pady=20, padx=10)

    # Create the label and entry for email using ttk
    ttk.Label(main_window, text="EMAIL:", font=("Modern No. 20", 30,"italic")).grid(row=1, column=0, padx=20, pady=10, sticky="W")
    entry_login_email = ttk.Entry(main_window, width=50)
    entry_login_email.grid(row=1, column=1, padx=20, pady=10)

    # Create the label and entry for password using ttk
    ttk.Label(main_window, text="PASSWORD:", font=("Modern No. 20", 30,"italic")).grid(row=2, column=0, padx=20, pady=10, sticky="W")
    entry_login_password = ttk.Entry(main_window, show='*', width=50)
    entry_login_password.grid(row=2, column=1, padx=20, pady=10)

    # Create the Login and Back buttons with increased size
    ttk.Button(main_window, text="LOGIN", command=lambda: login_user(entry_login_email.get(), entry_login_password.get()), width=40).grid(row=3, columnspan=2, pady=20, ipadx=20, ipady=10)
    ttk.Button(main_window, text="BACK", command=show_start_screen, width=40).grid(row=4, columnspan=2, pady=10, ipadx=20, ipady=10)


def show_start_screen():
    clear_screen()
    # Ensure the image reference is kept
    global bg_image1_img  
    bg_image1_img = tk.PhotoImage(file=r"C:\Users\lenovo\Pictures\user_au.png")
    bg_image1=tk.Label(main_window, image=bg_image1_img)
    bg_image1.place(relheight=1,relwidth=1)
    
    tk.Label(main_window, text="USER AUTHENTICATION", font=("Times New Roman", 50, "bold"), bg="silver",fg="black").place(relx=0.5, rely=0.4, anchor="center")
    tk.Button(main_window, text="REGISTER", command=show_register_screen,font=("Times New Roman",25,"bold"),bg="silver",fg="gold",width=30).place(relx=0.5, rely=0.80, anchor="center")
    tk.Button(main_window, text="LOGIN", command=show_login_screen, font=("Times New Roman",25,"bold"),bg="silver",fg="gold",width=30).place(relx=0.5, rely=0.65, anchor="center")


def clear_screen():
    for widget in main_window.winfo_children():
        widget.destroy()


main_window=tk.Tk()
main_window.title("Quiz Application")
image_path = PhotoImage(file=r"C:\Users\lenovo\Pictures\home_bgg.png")
bg_image=tk.Label(main_window, image=image_path)
bg_image.place(relheight=1,relwidth=1)
Main_label=tk.Label(main_window, text="Welcome to Quiz application",font=("Britannic Bold",70,"italic","bold",),bg="silver",fg="black").pack(pady=0)
main_window.geometry('1000x800')
Welcome=tk.Button(main_window, text="Enter", command=show_start_screen, font=("Britannic Bold",50,"italic","bold"),bg="silver",fg="black").pack(pady=150)
main_window.mainloop()