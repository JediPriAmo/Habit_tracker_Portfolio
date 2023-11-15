#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3
from datetime import datetime, timedelta
import pandas as pd
from IPython.display import display

# Establish the pathway to the SQLite database "2new_habit_tracker.db"
# connection acts as globals
conn = sqlite3.connect('D:\\HABIT TRACKER IUBH\\sqlite-tools-win32-x86-3430100\\2new_habit_tracker.db')
cursor = conn.cursor()

class Habit:
    #Constructor: automatically invoked when an object of the class is created
    def __init__(self, habit_name, periodicity, target_times_or_days):
        self.habit_name = habit_name
        self.periodicity = periodicity
        self.target_times_or_days = target_times_or_days
        self.creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class HabitDatabase:
    # The database contains the following tables if they dont exist in the database: habits, habit_completions & habit_streaks
    # NOTE: tables are already completed in the database "2new_habit_tracker"
    def create_table(self):
        cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_name TEXT NOT NULL,
                    periodicity TEXT NOT NULL,
                    target_times_or_days TEXT,
                    creation_date DATETIME NOT NULL
                )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS habit_completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    completion_date DATETIME NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits(id)
                )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS habit_streaks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    streak_start_date DATETIME NOT NULL,
                    streak_end_date DATETIME NOT NULL,
                    streak INTEGER,
                    FOREIGN KEY (habit_id) REFERENCES habits(id)
                )''')

    def create_habit(self, habit_name, periodicity, target_times_or_days):
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO habits (habit_name, periodicity, target_times_or_days, creation_date) VALUES (?, ?, ?, ?)",
                       (habit_name, periodicity, target_times_or_days, creation_date))
        conn.commit()
        print(f"New habit '{habit_name}' created successfully!")

    def delete_habit(self, habit_name):
        cursor.execute("DELETE FROM habits WHERE habit_name=?", (habit_name,))
        conn.commit()
        print(f"Habit '{habit_name}' deleted successfully.")

    def complete_habit(self, habit_name):
        habit_id = self.get_habit_id(habit_name)
        if habit_id:
            completion_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO habit_completions (habit_id, completion_date) VALUES (?, ?)",
                           (habit_id, completion_date))
            conn.commit()
            print(f"Habit '{habit_name}' marked as completed on {completion_date}")

            cursor.execute("SELECT periodicity FROM habits WHERE id=?", (habit_id,))
            habit_periodicity = cursor.fetchone()[0]

            streak = self.check_streak(habit_id, habit_name, habit_periodicity)
            print(f"Current Streak for habit '{habit_name}': {streak}")
        else:
            print(f"Habit '{habit_name}' not found.")

    def get_habit_id(self, habit_name):
        cursor.execute("SELECT id FROM habits WHERE habit_name=?", (habit_name,))
        habit_id = cursor.fetchone()
        return habit_id[0] if habit_id else None

    def check_streak(self, habit_id, habit_name, habit_periodicity):
        cursor.execute("SELECT completion_date FROM habit_completions WHERE habit_id=? ORDER BY completion_date ASC",
                       (habit_id,))
        completion_dates = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') for row in cursor.fetchall()]

        streak = 1
        max_streak = 1

        for i in range(1, len(completion_dates)):
            if habit_periodicity == "daily":
                if (completion_dates[i] - completion_dates[i - 1]).days == 1:
                    streak += 1
                    max_streak = max(max_streak, streak)
                else:
                    streak = 1
            elif habit_periodicity == "weekly":
                if (completion_dates[i] - completion_dates[i - 1]).days <= 7 and completion_dates[i].weekday() ==                         completion_dates[i - 1].weekday():
                    streak += 1
                    max_streak = max(max_streak, streak)
                else:
                    streak = 1

        return max_streak


class Analytics:
    # The '@staticmethod' decorator in Python is used to define the following static methods (without it the solution wouldnt run properly)
    # Each method executes a SQL query to retrieve all habits and their completion status from the database
    # All the methods (except 'view longest streak for habit') use pandas where after creating the DataFrame, they display it using the display function from the IPython library
    @staticmethod #decorator indicating that the following method is a static method (belonging to habit class rather than an instance of it)
    def view_all_habits():
        cursor.execute("SELECT h.id, h.habit_name, h.periodicity, h.target_times_or_days, h.creation_date, c.completion_date "
                       "FROM habits h "
                       "LEFT JOIN habit_completions c ON h.id = c.habit_id")
        all_habits = cursor.fetchall() # Fetches all the results from the executed query

        table_data = []
        for habit in all_habits:
            habit_id, habit_name, periodicity, target_times_or_days, creation_date, completion_date = habit
            completion_status = 'Yes' if completion_date else 'No'
            table_data.append(
                [habit_id, habit_name, periodicity, target_times_or_days, creation_date, completion_status,
                 completion_date])

        df = pd.DataFrame(table_data,
                          columns=["ID", "Habit Name", "Periodicity", "Target Times/Days", "Creation Date", "Completed",
                                   "Completion Date"])
        display(df)

   
    @staticmethod
    def view_longest_streaks():
        cursor.execute("SELECT id, habit_name, periodicity FROM habits")
        habits = cursor.fetchall()

        # Initialise dictionary for the temporary storaging of longest streaks for each habit, and then presents them in a tabular format using Pandas
        habit_streaks = {}  

        for habit in habits:
            habit_id, habit_name, periodicity = habit
            key = (habit_name, periodicity)  # Use habit_name and periodicity as a unique key
            max_streak = HabitDatabase().check_streak(habit_id, habit_name, periodicity)

            # Update the streak in the habit_streaks dictionary
            if key not in habit_streaks or max_streak > habit_streaks[key]:
                habit_streaks[key] = max_streak

        # Transforming information stored in habit_streaks dictionary into a format thats suits the dataframe of pandas
        table_data = []
        for (habit_name, periodicity), max_streak in habit_streaks.items():
            table_data.append([habit_name, periodicity, max_streak])

        df = pd.DataFrame(table_data, columns=["Habit Name", "Periodicity", "Longest Streak (Days)"])
        display(df)

    @staticmethod
    def view_longest_streak_for_habit():
        habit_name = input("Enter the habit name: ")
        periodicity = input("Enter the periodicity (daily/weekly): ")
        habit_id = HabitDatabase().get_habit_id(habit_name)
        if habit_id:
            max_streak = HabitDatabase().check_streak(habit_id, habit_name, periodicity)
            if periodicity == "daily":
                print(f"Longest Streak for habit '{habit_name}' (Daily): {max_streak} days")
            elif periodicity == "weekly":
                print(f"Longest Streak for habit '{habit_name}' (Weekly): {max_streak} weeks")
        else:
            print(f"Habit '{habit_name}' not found.")

    @staticmethod 
    def _get_habits_by_periodicity(periodicity):
         # the'cursor.execute(...):' allows for the execution of the following SQL query on the database
        cursor.execute(f"SELECT h.id, h.habit_name, h.target_times_or_days, h.creation_date, c.completion_date "
                       f"FROM habits h "
                       f"LEFT JOIN habit_completions c ON h.id = c.habit_id "
                       f"WHERE h.periodicity=?",
                       (periodicity,))

        habits = cursor.fetchall()

        # Constructing table
        table_data = []
        for habit in habits:
            habit_id, habit_name, target_times_or_days, creation_date, completion_date = habit
            completion_status = 'Yes' if completion_date else 'No'
            table_data.append(
                [habit_id, habit_name, periodicity, target_times_or_days, creation_date, completion_status,
                 completion_date])

        #creates dataframe for pandas to be displayed
        df = pd.DataFrame(table_data,
                          columns=["ID", "Habit Name", "Periodicity", "Target Times/Days", "Creation Date", "Completed",
                                   "Completion Date"])
        display(df)

    #class methods defined within/utilizing the _get_habits_by_periodicity method
    @classmethod #This decorator is used to define a method that is bound to the class and not the instance of the class
    def view_daily_habits(cls):
        cls._get_habits_by_periodicity('daily')

    @classmethod
    def view_weekly_habits(cls):
        cls._get_habits_by_periodicity('weekly')   
            
# Main menu loop with the following options
while True:
    print("Options:")
    print("1. Create New Habit")
    print("2. Delete Habit")
    print("3. Complete Habit")
    print("4. View All Habits")
    print("5. View All Daily Habits")
    print("6. View All Weekly Habits")
    print("7. View Longest Streak of All Habits")
    print("8. View Longest Streak for a Given Habit")
    print("9. Exit")
    choice = input("Enter your choice: ")

    # 'habit_db' & 'analytics' are instances for database interaction and analytics
    # Creating them in the loop ensures new instances that each iteration of the loop can work with 
    habit_db = HabitDatabase()
    analytics = Analytics()

    # Here, user enters habit name > periodicity > target time/day
    # The instance habit_db of the HabitDatabase class is being used to call the create_habit method
    if choice == '1':
        habit_name = input("Enter habit name: ")
        periodicity = input("Enter periodicity (daily/weekly): ")
        target_times_or_days = input(
            "Enter target times/days (comma-separated, e.g., 5:00 PM,6:30 AM/Monday,Wednesday): ")
        habit_db.create_habit(habit_name, periodicity, target_times_or_days)
    
    # Here, simply enter habit name to delete
    # habit_db instance of the habitDB class is used to call the delete_habit method
    elif choice == '2':
        habit_name = input("Enter habit name to delete: ")
        habit_db.delete_habit(habit_name)
    elif choice == '3':
        habit_name = input("Enter habit name to mark as completed: ")
        habit_db.complete_habit(habit_name)
    
    # The analytics instance of the Analytics class is being used to call the view_all_habits method for option 4, and similarly for the other options respectively
    #options 6 & 7 calls on the Habit class respectively
    elif choice == '4':
        analytics.view_all_habits()
    elif choice == '5':
        analytics.view_daily_habits()
    elif choice == '6':
        analytics.view_weekly_habits()
    elif choice == '7':
        analytics.view_longest_streaks()
    elif choice == '8':
        analytics.view_longest_streak_for_habit()
    
    # Exiting app
    elif choice == '9':
        print("Exiting the Habit Tracker. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# Global close of cursor and connection
cursor.close()
conn.close()


# In[ ]:



