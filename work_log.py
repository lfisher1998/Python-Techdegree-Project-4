# Python Techdegree Project 4 - Worklog Database
# Developed by: Luke Fisher

import os
import datetime


from peewee import *


intro_message = "Welcome to the Database Work Log!"

db = SqliteDatabase('entry.db')

class Database(Model):
    employee_field = CharField(max_length=100)
    name = CharField(max_length=100)
    time = IntegerField(default=0)
    date = DateField(default=datetime.datetime.now)
    notes = TextField()
    
    
    class Meta:
        database = db    
        
# Verified with Chris I could opt out of testing this.
def create_database(): # pragma: no cover 
    db.connect()
    db.create_tables([Database], safe=True)
    

def clear():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
    return None


def get_valid_time():
    while True:
        try:
            time = int(input("Please enter an integer value for how many minutes were worked on this task: "))
            clear()
            break
        except ValueError:
            clear()
            print("Please enter a number value! (Ex: 25, 12): ")
    return time


def main(): 
    #loop until the user decides to quit the program
    while True:
        # Display a series of choices so the user knows their option.
        print("Here are your options:")
        print("1. Add an entry")
        print("2. Look up previous entry")
        print("3. Quit the program")
        # Ask that user for their option.
        # Validate that option.
        try:
            choice = int(input("Please enter a number for your choice: "))
            if choice < 1 or choice > 3:
                clear()
                # if not valid: Print an appropriate message.
                print("Please enter a 1, 2, or 3")
            elif choice == 1:
                clear()
                # Add Entry
                employee_field = input("Please enter an employee name for this task: ")
                clear()
                name = input("Please enter a task name: ")
                time = get_valid_time()
                notes = input("Please enter any notes for this task (optional): ")
                entry = add_entry(employee_field, name, time, notes)
                
                print("Entry: {} added!".format(entry.name))
            elif choice == 2:
                search_entries_menu()
                choice2 = search_entries_input()
                
                if choice2 == 1:
                    clear()
                    print("Here are all the dates that have entries included: ")
                    for dates in all_dates():
                        print(dates)
                    user_input = input("Please enter a date in YYYY-MM-DD format: ")
                    result = search_by_date(user_input)
                elif choice2 == 2:
                    while True:
                        try:
                            user_input = int(input("Please enter an integer of minutes worked on task: "))
                            break
                        except ValueError:
                            clear()
                            print("Enter an integer!")
                    clear()
                    result = search_by_time(user_input)
                elif choice2 == 3:
                    while True:
                        user_input = input("Please type a phrase to search: ")
                        if user_input:
                            break
                            clear()
                        elif user_input.strip() == '':
                            clear()
                            print("You didn't type anything!! ")
                            user_input = None
                    result = search_by_exact(user_input)
                elif choice2 == 4:
                    print("Here are all the employees who have entries: ")
                    for name in all_employees():
                        print(name)
                    user_input = input("Please enter the name of the employee you'd like to see entries about: ")
                    result = search_by_employee(user_input)                
                clear()
                display_results(result)                
            elif choice == 3:
                break
        except ValueError:
            clear()
            # if not valid: Print an appropriate message.
            print("Please enter a number as an option!")
        
        
def add_entry(employee, name, time, notes):
    return Database.create(employee_field=employee, name=name, time=time, notes=notes)
        
        
def search_entries_menu():
    clear()
    # when the user wants to search for an entry, these are the options displayed
    print("These are your options for searching:\n"
          "1. Search by Date\n"
          "2. Search by the Time Spent on task\n"
          "3. Search by Exact Search\n"
          "4. Search by Employee\n"
          "5. Return to Main Menu\n"
          )
    return None


def search_entries_input():
    # ask for user input
    while True:
        try:
            search_choice = int(input("Please type your decision with its corresponding number (Ex. 1, 2, 3): "))
            if search_choice > 5 or search_choice < 1:
                clear()
                search_choice = None
                search_entries_menu()
                print("Please enter a number between and including 1-5!")
            # Search by date option
            elif search_choice == 1:
                break
            # Search by time option
            elif search_choice == 2:
                break
            #Search by exact match option
            elif search_choice == 3:
                break
            # Search by exact pattern or expression
            elif search_choice == 4:
                break 
            # Go back to main menu option
            elif search_choice == 5:
                clear()
                return None
        except ValueError:
            clear()
            search_choice = None
            search_entries_menu()
            print("Please enter a number value! (Ex: 1, 2, 3, 4, 5): ")
    return search_choice
    
            
def search_by_date(user_input):
    result_set = date_query(user_input)
    return result_set
            
    
def all_dates():
    dates = Database.select().order_by(Database.date.desc())
    dates_list = []
    for single_date in dates:
        format = single_date.date.strftime('%Y-%m-%d')
        if format not in dates_list:
            dates_list.append(format)
    return dates_list
                           
                           
def date_query(user_input):
    database = Database.select().order_by(Database.date.desc())
    return database.where(Database.date==user_input)
        
        
def search_by_time(user_input):
    result_set = time_query(user_input)
    return result_set
        
    
def time_query(user_input):
    database = Database.select().order_by(Database.date.desc())
    return database.where(Database.time == user_input)
    
        
def search_by_exact(user_input):
    result_set = exact_query(user_input)
    return result_set
    
    
def exact_query(user_input):
    return Database.select().where(
        (Database.name.contains(user_input)) |
        (Database.notes.contains(user_input)) |
        (Database.employee_field.contains(user_input)))
        
        
def search_by_employee(user_input):
    result_set = employee_query(user_input)
    return result_set
            
        
def all_employees():
    employee_query = Database.select().order_by(Database.employee_field.asc())
    employees = []
    for employee in employee_query:
        if employee.employee_field not in employees:
            employees.append(employee.employee_field)
    return employees

        
def employee_query(user_input):
    employees = Database.select().order_by(Database.employee_field.asc())
    return employees.where(Database.employee_field==user_input)
    
                        
def display_results(result):        
# initialize a count for how many matches there are
    clear()
    if result:
        count = 0
        print("Here are your results!\n")
        # for loop to give each match it's own set of information
        for match in result:
            print("Employee Name: {}\n"
                  "Task Name: {}\n"
                  "Task Time: {}\n"
                  "Task Notes: {}\n"
                  "Task Date: {}\n\n".format(match.employee_field, match.name, match.time, match.notes, match.date)
                  )
            # increment the count
            count += 1
        # display the total number of matches using the count variable
        print("Total amount of matches: {}\n".format(count))
        # return back to the search option menu        
    else:
        clear()
        print("No results!")    
    return None
            
# Verified with Chris I could opt out of testing this.        
if __name__ == "__main__": # pragma: no cover
    print(intro_message)
    create_database()
    main()
    
