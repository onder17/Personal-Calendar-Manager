import calendar
import re
import os
from datetime import datetime
#welcome message
print("\nWelcome to your personal calendar! How can I help you today?")
#function of interactive menu( \033[93m ---> colour of articles-yellow
def interactive_menu():
    while True:
        menu = """
\033[93m1) Display the calendar for any specific year
2) Add an event to any time
3) View events for a selected date
4) Delete the existing event for selected time
5) View all recorded events
6) Exit
"""
        print(menu)
        #operations through to options
        try:
            option = int(input("What do you want?(1-6): "))
            if option == 1:
                year = int(input("\033[94mPlease enter the year for displaying calendar: ")) #colour:blue
                print(calendar.calendar(year))
            elif option == 2:
                add_event()
            elif option == 3:
                view_event()
            elif option == 4:
                delete_event()
            elif option == 5:
                view_all_events()
            elif option == 6:
                print("\033[95mGoodbye! Have a nice day!\033[95m") #colour:purple
                break
            else:
                print("Please select a valid option! (1-5).")
        except ValueError:
            print("Invalid input! Please enter a number!")
#checking operation for dates
def validate_date(date_input):
    #checking format(YYYY-MM-DD)
    if not re.match(r"\d{4}-\d{2}-\d{2}$", date_input):
        return False

    #checking date(e.g.leap year calculations)
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
        return True
    except ValueError:
        return False

#add an event
def add_event():
    date_input = input("\033[91mEnter the date for the event (YYYY-MM-DD): ") #colour:red

    if not validate_date(date_input):
        print("Invalid date format or invalid calendar date! Please use YYYY-MM-DD.")
        return

    description = input("Enter the event name: ").strip()

    if not description:
        print("Event description cannot be empty.")
        return

    #save the event(by open a text file)
    try:
        with open("events.txt", "a") as file:
            file.write(f"{date_input} | {description}\n")
        print("The event was added successfully!")
    except Exception as e:
        print(f"An error occurred while saving the event: {e}")

def view_event():
    date_input = input("\033[96mEnter the date to view events (YYYY-MM-DD): ") #colour:turquoise

    if not validate_date(date_input):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    found = False
    try:
        with open("events.txt", "r") as file:
            print(f"\nEvents on {date_input}:")
            for line in file:
                if line.startswith(date_input):
                    print(" -", line.strip().split(" | ")[1])
                    found = True
        if not found:
            print("No events found for this date. Please try different operation.")
    except FileNotFoundError:
        print("No events found. The events file does not exist yet. Please try different operation")

def delete_event():
    date_input = input("\033[97mEnter the date of the event to delete (YYYY-MM-DD): ") #colour:white
    if not validate_date(date_input):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    description = input("Enter the exact event name to delete: ").strip()

    try:
        if not os.path.exists("events.txt"):
            print("No events file found.")
            return

        deleted = False
        with open("events.txt", "r") as file:
            lines = file.readlines()

        with open("events.txt", "w") as file:
            for line in lines:
                if line.strip() != f"{date_input} | {description}":
                    file.write(line)
                else:
                    deleted = True

        if deleted:
            print("The event was deleted successfully!")
        else:
            print("No matching event found to delete. Please try different operation.")

    except Exception as e:
        print(f"An error occurred while deleting the event: {e}")

def view_all_events():
    try:
        #checking the file and read all recorded files
        with open("events.txt", "r") as file:
            lines = file.readlines()

            if not lines:
                print("\033[92mThere are no events recorded.")
                return

            #sorting the events according to dates
            lines.sort()

            print("\n\033[92mAll Recorded Events:\033[92m\n")
            for line in lines:
                date, description = line.strip().split(" | ")
                print(f"\033[92m{date} → {description}\033[92m") #colour:green
    except FileNotFoundError:
        print("No event file found. Add some events first!")


interactive_menu()

