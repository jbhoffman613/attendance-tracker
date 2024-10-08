import random
import pickle
import sys
import atexit
import argparse
import pandas as pd
from colorama import Fore, Style

RECORDS_FNAME = 'records.pkl'

def display_names(records: dict) -> None:
    ''' Display the records. '''
    print("The students are:\n" + Fore.GREEN)
    for student in records.keys():
        print(student)
    print(Style.RESET_ALL)

def add_record(records: dict, student: str) -> None:
    ''' Add a record to the records. '''
    records[student] = []

def load_records(file: str=RECORDS_FNAME) -> dict:
    ''' Load the records from the file. '''
    try:
        with open(file, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(Fore.RED + 'IT WAS NOT LOADED IN CORRECTLY!')
        print(Style.RESET_ALL)
        return {}

def save_records(records: dict, file: str=RECORDS_FNAME) -> None:
    ''' Save the records to the file. '''
    try:
        with open(file, 'wb') as file:
            pickle.dump(records, file)
    except pickle.PickleError as e:
        print(Fore.RED + 'IT WAS NOT SAVED CORRECTLY!')
        print(Style.RESET_ALL)
        print(e)

def make_empty_records() -> dict:
    ''' Make an empty records dictionary. '''
    save_records(records={})
    return {}

def pick_someone(students: dict) -> str:
    """Pick a random student from the list of students."""
    return random.choices(list(students.keys()))[0]

def test_picker(students: dict, iters: int=1000) -> None:
    """Test the picker."""
    counter = {}
    for _ in range(iters):
        student = pick_someone(students)
        if student in counter:
            counter[student] += 1
        else:
            counter[student] = 1
        if len(counter.keys()) == len(students.keys()):
            counts = list(counter.values())
            print(f"Got all students after {sum(counts)} iterations.")
            print(pd.Series(counts).describe())
            return
    print("Did not get all students.")
    return

def update_attendance(students: dict, student: str, response: str="noop") -> bool:
    """Update the attendance of a student."""
    if response == "answered":
        students[student].append(1)
        return True
    elif response == "passed":
        students[student].append(0.5)
        return True
    elif response == "absent":
        students[student].append(0)
        return True
    elif response == "excused":
        return True
    else:
        return False

def question_response(students: dict, student: str) -> None:
    """Loop for the interaction."""
    valid_options = ["answered", "passed", "absent", "excused", "exit"]
    valid_response = False
    # TODO: Test this loop and all possible paths
    while not valid_response:
        query = (f"How did the {student} respond? The options are: "
                 f"{valid_options[0]}, {valid_options[1]}, {valid_options[2]}, "
                 f"or {valid_options[3]}.\n? ")
        response = input(query)
        if response == "exit":
            save_records(students)
            print(Fore.GREEN + "The records have been saved." + Style.RESET_ALL)
            sys.exit()
        valid_response = update_attendance(students, student, response)
        if not valid_response:
            print(Fore.YELLOW + "Invalid response. Please try again." + Style.RESET_ALL + "\n")

def death_knell(students: dict, file: str=RECORDS_FNAME) -> None:
    """Print a message to the user."""
    save_records(records=students, file=file)


def user_loop(student_records: dict) -> None:
    """Loop for the user interaction."""
    # TODO: see scratch for how to ensure save on atexit
    # TODO: add a way to add a student
    while True:
        picked = input("Type in \'next\' to continue, \'add\' to add a student, \'display\' to show all students, or \'exit\'.\n? ")
        picked = picked.lower()
        if picked == 'next':
            student = pick_someone(student_records)
            print(f"The student is {student}.")
            question_response(student_records, student)
        elif picked == 'exit':
            death_knell(student_records)
            print(Fore.GREEN + "The records have been saved." + Style.RESET_ALL)
            exit()
        elif picked == 'add':
            student = input("Type in the student's name: ")
            add_record(student_records, student)
        elif picked == 'display':
            display_names(student_records)
        elif picked == 'test':
            test_picker(student_records)
        else:
            print(Fore.YELLOW + "Invalid response. Please try again." + Style.RESET_ALL + "\n")

def lifecycle_loop() -> None:
    """The main loop for the program."""
    record_name = RECORDS_FNAME
    input_name = input("Type in the file name to load in the records: ")
    if input_name != '':
        record_name = input_name

    records = load_records(record_name)

    if len(records.keys()) == 0:
        print(Fore.YELLOW
              + "Did not successfully load in a set of records. WARNING IT IS EMPTY"
              + Style.RESET_ALL)

    # death_knell(students: dict, file: str=RECORDS_FNAME)
    atexit.register(death_knell, students=records, file=record_name)

    # Run the loop using the loaded in records
    user_loop(records)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--make', type=bool,
                        help='make an empty file that will overwrite the current records file',)
    args = parser.parse_args()
    if args.make:
        make_empty_records()
        sys.exit()

    # Call the main function
    lifecycle_loop()
