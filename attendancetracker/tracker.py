import random
import pickle
import sys
from colorama import Fore, Style

def add_record(records: dict, student: str) -> None:
    ''' Add a record to the records. '''
    records[student] = []

def load_records(file: str='records.pkl') -> dict:
    ''' Load the records from the file. '''
    try:
        with open(file, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(Fore.RED + 'IT WAS NOT LOADED IN CORRECTLY!')
        print(Style.RESET_ALL)
        return {}

def save_records(records: dict, file: str='records.pkl') -> None:
    ''' Save the records to the file. '''
    try:
        with open(file, 'wb') as file:
            pickle.dump(records, file)
    except pickle.PickleError as e:
        print(Fore.RED + 'IT WAS NOT SAVED CORRECTLY!')
        print(Style.RESET_ALL)
        print(e)

def get_weights(students: dict) -> list:
    """Get the weights of each student."""
    total = sum(students.values())
    return [students[student] / total for student in students.keys()]

def pick_someone(students: dict) -> str:
    """Pick a random student from the list of students."""
    return random.choices(list(students.keys()))[0]

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
    else:
        return False

def question_response(students: dict, student: str) -> None:
    """Loop for the interaction."""
    valid_options = ["answered", "passed", "absent", "exit"]
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

def death_knell(students: dict, file: str='records.pkl') -> None:
    """Print a message to the user."""
    save_records(records=students, file=file)


def user_loop() -> None:
    """Loop for the user interaction."""
    # TODO: see scratch for how to ensure save on atexit
    student_records = load_records()
    # TODO: add a way to add a student
    while True:
        picked = input("Type in \'next\' to continue or \'exit\'.\n? ")
        if picked == 'next':
            student = pick_someone(student_records)
            print(f"The student is {student}.")
            question_response(student_records, student)
        elif picked == 'exit':
            death_knell(student_records)
            print(Fore.GREEN + "The records have been saved." + Style.RESET_ALL)
            exit()
        else:
            print(Fore.YELLOW + "Invalid response. Please try again." + Style.RESET_ALL + "\n")

if __name__ == "__main__":
    student_data = {
        "Alice": 1000000000,
        "Bob": 20,
        "Charlie": 30,
        "David": 40,
    }
    print(pick_someone(student_data))
