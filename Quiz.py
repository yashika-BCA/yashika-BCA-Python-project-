import tkinter as tk
from tkinter import messagebox
import mysql.connector as mycon
from mysql.connector import Error
from tkinter import PhotoImage
import os
from tkinter import ttk
import random
import time
from main_window import show_topic_selection_screen

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
    
# create a function to fetch questions from the database sampleproject.questions to display questions,corect answer, option1, ootion2, explanation and level on the quiz window
# The function should take the topic, level and limit as arguments and return a list of questions to display the questions, corect answer, option1, ootion2 according to the level(1-5) and topic selected by the user
def fetch_questions(topic, level):
    mydb = connect_to_db()
    if mydb:
        try:
            db_cur = mydb.cursor()
            db_cur.execute('''
            SELECT question_text, option1, option2, correct_answer, explanation
            FROM questions
            WHERE category=%s AND level=%s
            ''', (topic, level))
            questions = db_cur.fetchall()
            return questions
        except Error as e:
            messagebox.showerror("Error", f"Error fetching questions: {e}")
        finally:
            if mydb.is_connected():
                db_cur.close()
                mydb.close()

# create a function to take the id and name from the table user(id, name, email, password, join_date) if the user is logged in(through login_user of User_login.py) along with score and save it in table leaderboard(leaderboard_id, user_id, score, USERNAME)
def save_score(score):
    username= "current_username"
    mydb = connect_to_db()
    if mydb:
        try:
            db_cur = mydb.cursor()
            db_cur.execute('''
            INSERT INTO leaderboard (score, USERNAME) VALUES (%s, %s)
            ''', (score, username))
            mydb.commit()
            print(f"Saving score: {score} , username: {username}")
        except Error as e:
            messagebox.showerror("Error", f"Error saving score: {e}")
        finally:
            if mydb.is_connected():
                db_cur.close()
                mydb.close()


# create a function to display the questions, option1, option2 and correct answer(as third option) on the quiz window and also display pop-up message if time is up or if the answer is correct or wrong(with explanation) and update the score accordingly
# The function should take the quiz_window, question, options, correct_answer, selected_option, next_question_callback, score_label and score and required things as arguments
def display_question(quiz_window, question, options, correct_answer, next_question_callback, score_label, score):
    question_label = tk.Label(quiz_window, text=question, font=("Helvetica", 20))
    question_label.pack(pady=10)

    def check_answer(selected_option):
        nonlocal score
        if selected_option == correct_answer:
            score += 10
            messagebox.showinfo("Correct!", f"Correct! Your score is: {score}")
        else:
            messagebox.showerror("Wrong!", f"Wrong! Correct answer: {correct_answer}")
        score_label.config(text=f"Score: {score}")
        next_question_callback()

    random.shuffle(options)
    for option in options:
        tk.Button(quiz_window, text=option, font=("Helvetica", 15),
                  command=lambda opt=option: check_answer(opt)).pack(pady=5)

# create a function to display the countdown timer on the quiz window and move to the next question if time is up or if the user has selected the answer
def countdown_timer(quiz_window, duration, next_question_callback):
    time_label = tk.Label(quiz_window, text="", font=("Helvetica", 20))
    time_label.pack()

    def update_timer(remaining):
        if remaining >= 0:
            time_label.config(text=f"Time left: {remaining}s")
            quiz_window.after(1000, update_timer, remaining - 1)
        else:
            messagebox.showinfo("Time's up!", "Moving to the next question.")
            next_question_callback()

    update_timer(duration)

# create a function to start the quiz on the selected topic in levels(1-5) where each level should have 10 questions. quiz must display the questions,  3 random options(option1, option2 and correct_answer(as option3)), timer, option of leaderboard, quit button, explanation (if user choose incorrect answer) and user move to next quesstion if user chooses any option or time is up
# set the bg image
#from main_window import show_topic_selection_screen
def start_quizz(topic, level=1):
    def proceed_to_next_level():
        nonlocal level
        if(score>=50):
            level += 1
            print(f"Proceeding to Level {level}")  # Debug statement
            if level <= 5:  # Continue to the next level if it's within the range
                start_quizz(topic, level)
            else:
                messagebox.showinfo("Quiz Completed", "You've completed all levels. Well done!")
    # Fetch questions based on the selected topic and level
    questions = fetch_questions(topic, level)
    if questions:
        print(f"Questions fetched for Level {level}: {questions}")  # Debug statement
        # Create the quiz window with bg image 
        quiz_window = tk.Toplevel()
        quiz_window.title("Quiz Window")
        quiz_window.geometry("800x600")
        quiz_window.configure(bg="lightblue")
        quiz_window.title(f"Quiz - {topic} (Level {level})")


        score = 0
        question_index = 0

        # Display the current score
        score_label = tk.Label(quiz_window, text=f"Score: {score}", font=("Helvetica", 20))
        score_label.pack(pady=10)

        # Quit button handler
        def quit_quiz():
            if messagebox.askyesno("Quit", "Are you sure you want to quit the quiz?"):
                save_score(score)  # Save the user's score before quitting
                quiz_window.destroy()

        quit_button = tk.Button(quiz_window, text="Quit", font=("Helvetica", 15), command=quit_quiz)
        quit_button.pack(pady=10)

        def next_question():
            nonlocal question_index
            # Clear the quiz window
            for widget in quiz_window.winfo_children():
                if widget != score_label and widget != quit_button:  # Keep the score label
                    widget.destroy()

            if question_index < len(questions):
                # Fetch the current question
                question = questions[question_index]
                question_text = question[0]
                options = [question[1], question[2], question[3]]  # Randomize options
                correct_answer = question[3]
                explanation = question[4]

                random.shuffle(options)  # Shuffle options to randomize order

                # Display the question
                question_label = tk.Label(quiz_window, text=question_text, font=("Helvetica", 20))
                question_label.pack(pady=20)

                # Display the options
                def check_answer(selected_option):
                    nonlocal score
                    if selected_option == correct_answer:
                        score += 10
                        messagebox.showinfo("Correct!", f"Correct! Your score is: {score}")
                    else:
                        messagebox.showerror("Wrong!", f"Wrong! Correct answer: {correct_answer}\nExplanation: {explanation}")
                    score_label.config(text=f"Score: {score}")
                    next_question()

                for option in options:
                    tk.Button(quiz_window, text=option, font=("Helvetica", 15),
                              command=lambda opt=option: check_answer(opt)).pack(pady=5)

                # Start the timer
                countdown_timer(quiz_window, 30, next_question)  # 30 seconds for each question
                question_index += 1
            else:
                # All questions are completed for this level
                save_score(score)
                
                if(score>=50):
                    messagebox.showinfo("Quiz Completed",f"Congratulations! You've completed Level {level}.\nYour score is {score}.")
                else:
                    messagebox.showinfo("Sorry you failed this level '_'",f"Scores upto atleast 50 is needed to pass the level. \nYour current score is {score}")
                    quiz_window.destroy()
                    show_topic_selection_screen()
                quiz_window.destroy()
                proceed_to_next_level()                

        # Start the quiz with the first question
        next_question()
        quiz_window.mainloop()      

    else:
        # Handle case when no questions are available for a level
        print(f"No questions found for Level {level}")  # Debug statement
        messagebox.showinfo("No Questions", f"No questions found for {topic} at Level {level}.")
        if level < 5:
            proceed_to_next_level()  # Skip to the next level if current level lacks questions
        else:
            messagebox.showinfo("Quiz Completed", "No more questions available!")

             
            
