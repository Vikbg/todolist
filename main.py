# To-Do list mini-project in Python.
# Je parle français but I will do it in english parceque ça fait plus dev experimenté mdrr
# Alors que c'est mon premier projet concret miskine
# Created at Wed 29 Oct 2025 10:06:20 PM CET by @viktor_srhk on Instagram (Go sub NOW!!!).

# Imports

import shutil
import time
import os
from getpass import getpass

class User:
    def __init__(self, username, password):
        self.id = id(self)
        self.username = username
        self.password = password

    def create_user_storage(self):

        user_dir = f"users/{self.username}"

        os.makedirs(user_dir, exist_ok=True)

        with open(f"{user_dir}/credentials.txt", "w") as f:
            f.write(self.password)
            f.close
        
        print(f"\n{self.username}'s storage create.\n")


# Task class

class Task:
    def __init__(self, name, complete_before ,description=None):
        self.id = int(time.time() * 1000)
        self.name = name
        self.description = description
        self.last_modified = float(time.time())
        self.complete_before = (complete_before*86400) + self.last_modified
        self.completed = False


# ToDoList class to store tasks

class ToDoList:
    def __init__(self):
        self.tasks = []

    def save_data_file(self, username):
        data_file = f'users/{username}/data.txt'
        try:
            with open(data_file, "w") as f:
                for task in self.tasks:
                    line = f"{task.name}|{task.description}|{task.complete_before}|{task.last_modified}|{task.completed}\n"
                    f.write(line)
            print("Data file saved successfully.")
        except FileNotFoundError:
            print("Data file not found, initializing data file.")
            self.init_data_file(username)


    def init_data_file(self, username):
        data_file = f'users/{username}/data.txt'
        try:
            os.mkdir(f'users/{username}/')
            try:
                with open(f"{data_file}", "x"):
                    print("Data file succesfully created.")
                    self.save_data_file(username=username)
            except FileExistsError:
                print("Data file already exist, pass.")
        except FileExistsError:
            print("User directory already exist, pass.")
            try:
                with open(f"{data_file}/data.txt", "x"):
                    print("Data file succesfully created.")
                    self.save_data_file(username=username)
            except FileExistsError:
                print("Data file already exist, pass.")

    def load_from_data_file(self, username):
        data_file = f'users/{username}/data.txt'
        try:
            with open(data_file, "r") as f:
                lines = f.readlines()
                # Clear current tasks
                self.tasks = []
                for line in lines:
                    name, description, complete_before, last_modified, completed = line.strip().split("|")
                    task = Task(name, float(complete_before), description if description != "None" else None)
                    task.last_modified = float(last_modified)
                    task.completed = completed == "True"
                    self.tasks.append(task)
        except FileNotFoundError:
            print("Data file not find !")
            self.init_data_file(username)

    def add_task(self, name, complete_before, description=None):
        new_task = Task(name, complete_before, description)
        self.tasks.append(new_task)
        print(f"Added a task : {name}\n")

    def print_tasks(self, username):
                self.load_from_data_file(username=username)
                print("\n------------------ All Tasks ------------------\n")

                if not self.tasks:
                    print("No tasks available.")
                    return

                for index, task in enumerate(self.tasks, start=1):
                    name = task.name
                    desc = task.description
                    last_modified_days = (time.time() - task.last_modified) / 86400  # en jours

                    if task.completed:
                        status = "Completed!"
                    else:
                        remaining_days = (task.complete_before - time.time()) / 86400
                        if remaining_days < 0:
                            status = "Overdue!"
                        else:
                            status = f"Need to complete in {remaining_days:.2f} days."
                            # Print with or without description
                            if desc:
                                print(f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified_days:.2f} days ago")
                            else:
                                print(f"{index} - {name}. {status} - Last Modified : {last_modified_days:.2f} days ago")

    def show_tasks(self, username, users):
            self.print_tasks(username=username)

            print("\n| 1 - Show only completed")
            print("| 2 - Show only uncompleted")
            print("| 3 - Sort By Echeance Date")
            print("| 4 - Sort By Modification Date")
            print("| 5 - Search by terms")
            print("| 0 - Return\n")

            options = [0, 1, 2, 3, 4, 5]
            option = int(input("(int) > "))
            index = 0

            try:
                if option not in options:
                    raise ValueError
                if option == 0:
                    connected_menu(username=username, users=users)
                if option == 1:
                    print("\n------------------ Completed Tasks ------------------\n")
                    for i in self.tasks:
                        index += 1
                        name = i.name
                        desc = i.description
                        last_modified = (time.time() - i.last_modified) / 86400
        
                        # Print with or without description
                        if i.completed:
                            status = "Completed !"
                            if desc:
                                print(f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified:.2f} days ago")
                            else:
                                print(f"{index} - {name}. {status} - Last Modified : {last_modified:.2f} days ago")
                    else:
                        print("No tasks completed")
                if option == 2:
                    print("\n------------------ UnCompleted Tasks ------------------\n")
                    for i in self.tasks:
                        index += 1
                        name = i.name
                        desc = i.description
                        last_modified = (time.time() - i.last_modified) / 86400
                        if not i.completed:
                            remaining_days = (i.complete_before - time.time()) / 86400
                            status = f"Need to complete in {remaining_days:.2f} days."
                            if desc:
                                print(f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified:.2f} days ago")
                            else:
                                print(f"{index} - {name}. {status} - Last Modified : {last_modified:.2f} days ago")
                if option == 3:
                    sorted_tasks = sorted(todolist.tasks, key=lambda  todolist: todolist.complete_before)
                    for i in sorted_tasks:
                        index += 1
                        name = i.name
                        desc = i.description
                        last_modified = (time.time() - i.last_modified) / 86400
                        if i.completed:
                            status = "Completed !"
                        else:
                            remaining_days = (i.complete_before - time.time()) / 86400
                            status = f"Need to complete in {remaining_days:.2f} days."

                        print("\n------------------ Sorted Tasks By Echance Date ------------------\n")
        
                        # Print with or without description
                        if desc:
                            print(f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified:.2f} days ago")
                        else:
                            print(f"{index} - {name}. {status} - Last Modified : {last_modified:.2f} days ago")
                if option == 4:
                    sorted_tasks = sorted(todolist.tasks, key=lambda  todolist: todolist.last_modified)
                    for i in sorted_tasks:
                        index += 1
                        name = i.name
                        desc = i.description
                        last_modified = (time.time() - i.last_modified) / 86400
                        if i.completed:
                            status = "Completed !"
                        else:
                            remaining_days = (i.complete_before - time.time()) / 86400
                            status = f"Need to complete in {remaining_days:.2f} days."

                        print("\n------------------ Sorted Tasks By Last Modification Date ------------------\n")
        
                        # Print with or without description
                        if desc:
                            print(f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified:.2f} days ago")
                        else:
                            print(f"{index} - {name}. {status} - Last Modified : {last_modified:.2f} days ago")
                if option == 5:
                    print("\n------------------ Search Tasks By Given Terms ------------------\n")
                    print("Enter some terms to search themin tasks.\n")
                    search_terms = input("(terms) > ")
                    for i in self.tasks:
                        if search_terms in i.name or search_terms in i.description:
                            index += 1
                            name = i.name
                            desc = i.description
                            last_modified = (time.time() - i.last_modified) / 86400
                            if i.completed:
                                status = "Completed !"
                            else:
                                remaining_days = (i.complete_before - time.time()) / 86400
                                status = f"Need to complete in {remaining_days:.2f} days."
        
                            # Print with or without description
                            if desc:
                               print(f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified:.2f} days ago")
                            else:
                               print(f"{index} - {name}. {status} - Last Modified : {last_modified:.2f} days ago")

            except ValueError:
                print("Invalid value, I authorize you to buy glasses.")

    def modify_task(self, input_id, name=None, description=None, complete_before=None, completed=None):

        complete_before_days: float | None

        complete_before_days = complete_before

        id = input_id - 1
        
        has_changed = True

        old_name = self.tasks[id].name
        old_description = self.tasks[id].description

        old_complete_before = self.tasks[id].complete_before
        old_complete_before = (old_complete_before - time.time()) / 86400
        old_completed = self.tasks[id].completed

        if name is not None:
            self.tasks[id].name = name
            print(f"Change from {old_name} to {name}")
        if description is not None:
            self.tasks[id].description = description
            print(f"Change from {old_description} to {description}")
        if complete_before_days is not None:
            complete_before = float(complete_before_days) * 86400 + time.time()

            self.tasks[id].complete_before = complete_before
            print(f"Change from {old_complete_before:.2f} to {complete_before_days}")
        if completed != old_completed:
            self.tasks[id].completed = completed
            if completed is False and complete_before is not None and complete_before < old_complete_before:
                try:
                    complete_before = float(input("Before when you wanna end this new task: "))
                    if complete_before.__class__ is not float:
                        raise TypeError
                    print(f"Now, task {self.tasks[id].name} need to be completed before {complete_before}")
                    complete_before = float(complete_before) * 86400 + time.time()
                    self.tasks[id].complete_before = complete_before
                except TypeError:
                    print("Type error, except a float number ! Like a number 1.0, 1.335, 2.0, 3.0 ect...")
            elif completed is not None:
                self.tasks[id].completed = True
                print(f"Now, task {self.tasks[id].name} is Completed !")
            else:
                self.tasks[id].completed = False
                print(f"Now, task {self.tasks[id].name} is UnCompleted !")
        else:
            has_changed = False
            print("No change saved.\n")
            return has_changed
        
        if has_changed:
            self.tasks[id].last_modified = time.time()
    
    def delete_task(self, input_id, username):

        input_id = int(input_id)

        id = input_id - 1
        name = self.tasks[id].name
        del self.tasks[id]

        todolist.save_data_file(username=username)

        print(f"Task \"{name}\" deleted")

    def save_backup(self, username):
        """
            Save a backup of users/{username}/data.txt file in users/{username}/backups/{timestamp}/data.txt.
            
            Args:
                username (str): The username for which to create a backup.
        """
        user_data_path = os.path.join("users", username, "data.txt")
        backup_dir = os.path.join("users", username, "backups")
        timestamp = str(int(time.time()))  # Use timestamp as directory name for backup
        backup_path = os.path.join(backup_dir, timestamp)
        backup_file_path = os.path.join(backup_path, "data.txt")
            
        # Check if the user's data file exists
                 
        if not os.path.exists(user_data_path):
            print(f"\nError: User data file not found at {user_data_path}")
            return
        
        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        # Create the timestamped backup directory
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
                                    
        # Copy the data file to the backup location
        try:
            shutil.copy2(user_data_path, backup_file_path) #copy2 preserves metadata
            print(f"\nBackup created successfully at {backup_file_path}")
        except Exception as e:
            print(f"\nError creating backup: {e}")

    def load_from_backup(self, username, timestamp):
        backup_file_path = os.path.join("users", username, "backups", timestamp, "data.txt")
        user_data_path = os.path.join("users", username, "data.txt")
        
        # Check if the backup file exists
        if not os.path.exists(backup_file_path):
            print(f"\nError: Backup file not found at {backup_file_path}")
            return
        
        # Restore the backup by copying it to the user's data file location
        try:
            shutil.copy2(backup_file_path, user_data_path) #copy2 preserves metadata
            print(f"\nBackup restored successfully from {backup_file_path}")
        except Exception as e:
            print(f"\nError restoring backup: {e}")

    def show_backups(self, username):
        backup_dir = os.path.join("users", username, "backups")
        
        try:
            backups = os.listdir(backup_dir)
            i = 0
            if not backups:
                print("\nNo backups available.")
                return
            print("\nAvailable Backups:")
            for backup in backups:
                i += 1
                print(f" {i} - {backup}")
        except FileNotFoundError:
            print("\nNo backups directory found.")

    def delete_backup(self, username, timestamp):
        backup_file_path = os.path.join("users", username, "backups", timestamp)
        
        try:
            shutil.rmtree(backup_file_path)
            print(f"\nBackup {timestamp} deleted successfully.")
        except Exception as e:
            print(f"\nError deleting backup: {e}")

def print_title(str):
    print("\n", "-"*5, " ", str, " ", "-"*5)

def make_clickable(text=None, url=""):
    if text is None:
        text = url  # Use the URL itself as the display text if none is provided
    return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'


def show_networks(username):
    if username == 'Viktor':
        print_title("My Networks")
        print("\nHello buddy, I'm Viktor the devlopper !")
        print("Check my networks : ")
        print(f"     Github : {make_clickable('Vikbg', 'https://github.com/Vikbg/')} & {make_clickable('viktor_srhk', 'https://github.com/viktorsrhk/')}")
        print(f"     Instagram : {make_clickable('viktor.wow', 'https://instagram.com/viktor.wow/')} (public) & {make_clickable('viktor_srhk', 'https://instagram.com/viktor_srhk/')} (private)")
        print(f"     TikTok : {make_clickable('viktor_srhk', 'https://www.tiktok.com/@viktor_srhk')}")
        print(f"     YouTube : {make_clickable('viktor', 'https://www.youtube.com/@viktorsrhk')}")
        print(f"     Linkedin : {make_clickable('viktor_srhk', 'https://www.linkedin.com/in/viktorsrhk/')}")
        print(f"     Replit : {make_clickable('VikS0', 'https://replit.com/@VikS0/')}")
        print(f"     Portfolio : {make_clickable(None, 'In The Pipeline.')}")


def show_credits():
    print_title("Credits")
    print("\nToDoList app developed with love by viktor_srhk.")
    show_networks(username='Viktor')


def update_users_list():
    try:
        users = os.listdir("users/")
        return users
    except FileNotFoundError:
        os.mkdir("users")
        users = os.listdir("users/")
        return users

def list_users():
    i = 0
    no_user = False
    users_list = []

    update_users_list()
    users = update_users_list()

    print("\n------------------ USERS ------------------")

    if users == []:
        no_user = True
        print("\nNo users available. Create one !\n")
        return no_user
    else:
        no_user = False
        print("\nAll available users : ")
        print("--------------------------------")
        for user in users:
            i += 1
            users_list.append(user)
            print(f"    {i} - {user}")
        print("--------------------------------\n")
        return users_list, no_user
    
def create_user(username, password):

    new_user = User(username, password)
    new_user.create_user_storage()

    update_users_list()

    print(f"User {username} created !")

def creation_user_modal():
    try:
        print("Leave username blank to cancel.")
        username = input("(username) > ")
        if username == '' or username is None:
            raise ValueError
        try:
            password = getpass("(password) > ")
            if password == '' or password is None:
                raise ValueError
            create_user(username=username, password=password)
        except ValueError:
            print("Password cannot be empty")
    except ValueError:
        print("Action Cancled")
        menu(False)

def modify_user_username(username):
    try:
        current_password: str
        password: str
        new_username: str
        confirm_new_username: str
        print(f"\nYou will change username for {username} user, think before act !")
        print("Please enter your current password.\n")
        current_password = str(getpass("(password) > "))
        with open(f"users/{username}/credentials.txt", "r") as f:
            password = f.read().strip()
            f.close
        if current_password is None or current_password == '':
            raise ValueError
        if current_password.__class__ is str:
            try:
                if current_password == password:
                    try:
                        print("\nAccept.")
                        print("Enter the new username.\n")
                        new_username = str(input("(username) > "))
                        confirm_new_username = str(input("(confirm) > "))
                        if new_username.__class__ is str and confirm_new_username.__class__ is str:
                            if new_username == confirm_new_username:
                                os.rename(f"users/{username}", f"users/{new_username}")
                                print("\nUsername changed sucessfully.")
                            else:
                                raise ValueError
                        else:
                            raise TypeError
                    except ValueError:
                        print("\nUsername Dismatch !")
                                
                    except TypeError:
                        print("\nPassword need to be a string value")
                else:
                    raise ValueError
            except ValueError:
                print("\nWrong Password !")
    except ValueError:
        print("\nPassword cannot be Empty !")

def modify_user_password(username):
    try:
        current_password: str
        password: str
        new_password: str
        confirm_new_password: str
        print(f"\nYou will change password for {username} user, think before act !")
        print("Please enter your current password.\n")
        current_password = str(getpass("(password) > "))
        with open(f"users/{username}/credentials.txt", "r") as f:
            password = f.read().strip()
            f.close
        if current_password is None or current_password == '':
            raise ValueError
        if current_password.__class__ is str:
            try:
                if current_password == password:
                    try:
                        print("\nAccept.")
                        print("Enter the new password.\n")
                        new_password = str(getpass("(password) > "))
                        confirm_new_password = str(input("(confirm) > "))
                        if new_password.__class__ is str and  confirm_new_password.__class__ is str:
                            if new_password == confirm_new_password:
                                with open(f"users/{username}/credentials.txt", "w") as f:
                                    f.write(new_password)
                                    print("\nPassword changed sucessfully.")
                            else:
                                raise ValueError
                        else:
                            raise TypeError
                    except ValueError:
                        print("\nPasswords Dismatch !")
                                
                    except TypeError:
                        print("\nPassword need to be a string value")
                else:
                    raise ValueError
            except ValueError:
                print("\nWrong Password !")
    except ValueError:
        print("\nPassword cannot be Empty !")

def modify_user_modal(user, users):
    print_title("Modify User")
    list_users()
    selected_user = 1
    users_list = []
    for user in users:
        users_list.append(user)
    selected_user = int(input("Select a user. (ex : 1 for 1 - viktor_srhk.) >  "))
    i = selected_user - 1
    username = users_list[i]
    print(f"\nYou selected {username}, enter the password.\n")
    password = getpass("(password) > ")
    with open(f"users/{username}/credentials.txt") as f:
        user_password = f.read()
    try:
        if password is None or password == '':
            raise ValueError
        else:
            if user_password == password:
                print_title(f"Modify {username}")
                print("| 1 - Modify Username")
                print("| 2 - Modify Password")
                print("| 3 - Modify User Tasks")
                print(f"| 4 - Connect to {username}")
                print("| 0 - Return")

                options = [0, 1, 2 ,3]
                option = int(input("(int) > "))
                
                try:
                    if option in options:
                        if option == 0:
                            users_gestion_menu(user, users=users)
                        if option == 1:
                            modify_user_username(username=username)
                        if option == 2:
                            modify_user_password(username=username)
                        if option == 3:
                            tasks_gestion_menu(username=username, users=users)
                        if option == 4:
                            login(username=username, password=password)
                    else:
                        raise ValueError
                except ValueError:
                    print("Invalid value.")
    except ValueError:
        print("\nPassword cannot be empty.\n")


def wipe_data_for_user(username, users):
    try:
        current_password: str
        password: str
        print(f"\nYou will wipe data for {username} user, please think before act !")
        print(f"Please enter {username} current password.\n")
        current_password = str(getpass("(password) > "))
        with open(f"users/{username}/credentials.txt", "r") as f:
            password = f.read().strip()
            f.close
        if current_password is None or current_password == '':
            raise ValueError
        if current_password.__class__ is not str:
            try:
                if current_password == password:
                    try:
                        print("\nAccept.")
                        todolist.show_tasks(username=username, users=users)
                        print(f"\nAre you sure to wipe {username} data ?.\n")
                        confirmation = str(input("(yes/no) > "))
                        confirmation = confirmation.lower().strip()
                        if confirmation not in ['yes', 'no']:
                            raise ValueError
                        confirm_confirmation = str(input("(confirm) > "))
                        confirm_confirmation = confirm_confirmation.lower().strip()
                        if confirm_confirmation not in ['yes', 'no']:
                            raise ValueError
                        if confirmation == 'no':
                            pass
                        else:
                            if confirm_confirmation == 'no':
                                pass
                            else:
                                os.remove(f"users/{username}/data.txt")
                                print("Data Wiped.")
                                menu(True)
                    except ValueError:
                        print("\nIt's just no or yes bro !")
                else:
                    raise ValueError
            except ValueError:
                print("\nWrong Password !")
    except ValueError:
        print("\nPassword cannot be Empty !")

def delete_user(username, users):
    try:
        current_password: str
        password: str
        print(f"\nYou will delete {username} user, please think before act !")
        print(f"Please enter {username} current password.\n")
        current_password = str(getpass("(password) > "))
        with open(f"users/{username}/credentials.txt", "r") as f:
            password = f.read().strip()
            f.close
        if current_password is None or current_password == '':
            raise ValueError
        if current_password.__class__ is str:
            try:
                if current_password == password:
                    try:
                        print("\nAccept.")
                        todolist.show_tasks(username=username, users=users)
                        print(f"\nAre you sure to delete {username} account ?.\n")
                        confirmation = str(input("(yes/no) > "))
                        confirmation = confirmation.lower().strip()
                        if confirmation not in ['yes', 'no']:
                            raise ValueError
                        confirm_confirmation = str(input("(confirm) > "))
                        confirm_confirmation = confirm_confirmation.lower().strip()
                        if confirm_confirmation not in ['yes', 'no']:
                            raise ValueError
                        if confirmation == 'no':
                            print("\nAction Canceled.")
                        else:
                            if confirm_confirmation == 'no':
                                print("\nAction cancled.")
                            else:
                                os.remove(f"users/{username}/")
                                print("\nUser Deleted.")
                                menu(False)
                    except ValueError:
                        print("\nIt's just no or yes bro !")
                else:
                    raise ValueError
            except ValueError:
                print("\nWrong Password !")
    except ValueError:
        print("\nPassword cannot be Empty !")

def login(username, password):

    logged = False
    user = username
    users = update_users_list()

    if user in users:

        with open(f"users/{username}/credentials.txt", "r", newline="\n") as f:
            get_password = f.read().strip()    # First line is the password
        if get_password == password:
            logged = True
            print(f"\nUser {username} logged !\n")
            menu(True, username=username)
            return logged
        else:
            print("\nPassword is incorrect.. Sorry buddy..")
    else:
        print(f"\nUser {username} don't exists. Buy glasses.\n")
    
def logout(username):
    print(f"User {username} logged out.\n")
    return menu(False)

def initialization():

    os.makedirs("users", exist_ok=True)

    with open("./initialization.txt", "w") as f:
        f.write("True")
    
    print("\nHello buddy, I'm Viktor the devlopper of the ToDoList app !")
    print("Check my networks : ")
    print(f"     Github : {make_clickable('Vikbg', 'https://github.com/Vikbg/')} & {make_clickable('viktor_srhk', 'https://github.com/viktorsrhk/')}")
    print(f"     Instagram : {make_clickable('viktor.wow', 'https://instagram.com/viktor.wow/')} (public) & {make_clickable('viktor_srhk', 'https://instagram.com/viktor_srhk/')} (private)")
    print(f"     TikTok : {make_clickable('viktor_srhk', 'https://www.tiktok.com/@viktor_srhk')}")
    print(f"     YouTube : {make_clickable('viktor', 'https://www.youtube.com/@viktorsrhk')}")
    print(f"     Linkedin : {make_clickable('viktor_srhk', 'https://www.linkedin.com/in/viktorsrhk/')}")
    print(f"     Replit : {make_clickable('VikS0', 'https://replit.com/@VikS0/')}")
    print(f"     Portfolio : {make_clickable(None, 'In The Pipeline.')}")
    print("Before we start, I need to ask you a few questions.")
    print("So....")
    print("Let's create your profile of my new bestest user of the year (joke) !")
    print("How want you to name ?\n")

    username = input("Your name ?? > ")

    print(f"\nWow, your name {username} is fantastic, nice to meet you !!")
    print("Ok now you need to tell me a very top secret secret...")
    print("what password want you ?")
    print("shhh !\n")

    password = getpass("(password) > ")

    print("\nOk I think we're good, not you ? So I will let you take place in the fantastic world of my ToDoList app ! Bye bye !\n")

    create_user(username=username, password=password)
    login(username=username, password=password)

    return username, password

todolist = ToDoList()

def deconnected_menu(users):
    try:
            print_title("ToDoList by viktor_srhk - Menu")
            print("\n| 1 - Login")
            print("| 2 - Sign Up")
            print("| 3 - Credits")
            print("| 0 - Quit\n")

            options = [0, 1, 2, 3]
            option = int(input("Enter a option (intergers only) > "))

            if option.__class__ is not int or option not in options:
                raise ValueError
                

            if option == 0:
                print("Bye Bye !!")
                return exit()
            elif option == 1:
                list_users()
                if users == []:
                    no_user = True
                else:
                    no_user = False
                if no_user:
                    print("0 - Return\n")
                    print("Enter a option (intergers only).\n")
                    option = int(input("(int) > "))

                    if option == 0:
                        menu(False)
                    else:
                        raise ValueError
                else:
                    selected_user = 1
                    users_list = []
                    for user in users:
                        users_list.append(user)
                    selected_user = int(input("Select a user. (ex : 1 for 1 - viktor_srhk.) >  "))
                    i = selected_user - 1
                    username = users_list[i]
                    print(f"\nYou selected {username}, enter the password.\n")
                    password = getpass("(password) > ")
                    login(username=username, password=password)

            elif option == 2:
                print("\nSign up.\n")
                creation_user_modal()
            elif option == 3:
                show_credits()
                if input("\nPress Enter to return to menu..."):
                    menu(False)
    except ValueError:
        print("\nInvalid value.")

def connected_menu(username, users):
        try:
            print("\n| 1 - Tasks Gestion")
            print("| 2 - Users Gestion")
            print("| 3 - Settings")
            print("| 4 - Credits")
            print("| 9 - Logout")
            print("| 0 - Quit\n")

            options = [0, 1, 2, 3, 4, 9]
            option = int(input("Enter a option (intergers only): "))

            if option not in options:
                raise ValueError

            if option == 0:
                print("Bye Bye !!")
                return exit()
            elif option == 9:
                logout(username=username)
            elif option == 1:
                tasks_gestion_menu(username=username, users=users)
            elif option == 2:
                users_gestion_menu(username=username, users=users)
            elif option == 3:
                settings_menu(username=username, users=users)
            elif option == 4:
                show_credits()
                if input("\nPress Enter to return to menu..."):
                    menu(False)
        except ValueError:
            print("Incorrect Value.")

def tasks_gestion_menu(username, users):
            try:
                print_title("Tasks Gestion")
                print("| 1 - Add task")
                print("| 2 - Delete Task")
                print("| 3 - Modify Task")
                print("| 4 - Show all tasks.")
                print("| 5 - Manage Backups")
                print("| 0 - Return\n")

                option = int(input("Enter a option (intergers only): "))

                options = [1, 2, 3, 4, 5, 0]

                if option not in options:
                    raise ValueError
                
                if option == 0:
                    menu(True)

                elif option == 1:
                    try:
                        print("\nEnter the name of the task (tape \"q\" to cancel).")
                        task_name = input("(name) > ")
                        if task_name.lower() == 'q':
                           raise ValueError
                        print("\nEnter a description (facultatif, tape \"q\" to cancel).")
                        task_description = input("(description) > ")
                        if task_description.lower() == 'q':
                            raise ValueError
                        print("Before when you need to complete it ? (in days, tape \"q\" to cancel).")
                        task_complete_to = float(input("(days) > "))
                        if task_complete_to == 'q':
                            raise ValueError
                        elif task_complete_to.__class__ is not float and task_complete_to.__class__ is not int:
                            raise TypeError
                        
                        todolist.add_task(name=task_name, complete_before=task_complete_to, description=task_description)
                        todolist.save_data_file(username=username)

                    except ValueError:
                        print("Cancelled task creation.\n")
                    except TypeError:
                        print("Type error, except a float number or a interger ! Like a number 1 or 1.0, 1.335, 2, 3 ect...")
    
                elif option == 2:
                    todolist.print_tasks(username=username)
                    try:
                        print("Enter the id of the task to delete (ex: 1 for 1 - Do my Homeworks, enter \"q\" to cancel).")
                        task_to_delete = input("(task) > ")
                        if task_to_delete.lower() == 'q':
                            raise ValueError
                        elif int(task_to_delete).__class__ is int:
                            task_to_delete = int(task_to_delete)
                            todolist.delete_task(task_to_delete, username=username)
                        else:
                            raise TypeError
                    except TypeError:
                        print("\nTask Not found.")
                    except ValueError:
                        print("\nCancelled task creation.")

                elif option == 3:
                    todolist.load_from_data_file(username=username)
                    todolist.show_tasks(username=username, users=users)

                    n_tasks: int
                    n_tasks = int(todolist.tasks.__len__())
                    
                    if n_tasks == 0:
                        print("No Task Found")
                        tasks_gestion_menu(username=username, users=users)
                    else:
                        try:
                            print("Enter the id of the task you want to change the info. (Ex: 1 for 1 - Do my Homeworks, enter 'q' to cancel).")
                            task_id = input("(id) > ")

                            if task_id.lower() == 'q':
                                print("Action canceled.")
                                return

                            try:
                                task_id = int(task_id)
                            except ValueError:
                                print("Invalid ID — must be a number.")
                                return

                            tasks_id = [i + 1 for i in range(n_tasks)]

                            if task_id not in tasks_id:
                                print("This task ID does not exist.")
                                return

                            new_name = input("Enter the new name (leave blank to skip): ") or None
                            new_description = input("Enter the new description (leave blank to skip): ") or None

                            new_completed = input("Is it completed ? (yes/no, leave blank to skip): ").lower()
                            if new_completed == 'yes':
                                new_completed = True
                            elif new_completed == 'no':
                                new_completed = False
                            elif new_completed == '':
                                new_completed = None
                            else:
                                print("Invalid input for completion status.")
                                return

                            new_complete_before = input("Before when do you want to end this task? (leave blank to skip): ")
                            if new_complete_before == '':
                                new_complete_before = None
                            else:
                                try:
                                    new_complete_before = float(new_complete_before)
                                except ValueError:
                                    print("Invalid number for 'complete before'. Skipped.")
                                new_complete_before = None

                            todolist.modify_task(task_id, new_name, new_description, new_complete_before, completed=new_completed)

                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")


                elif option == 4:
                    todolist.load_from_data_file(username=username)
                    todolist.show_tasks(username=username, users=users)
                elif option == 5:
                    print_title("Backups Gestion")
                    print("| 1 - Create Backup")
                    print("| 2 - Restore Backup")
                    print("| 3 - Delete Backup")
                    print("| 0 - Return\n")

                    backup_options = [0, 1, 2, 3]
                    backup_option = int(input("(int) > "))

                    try:
                        if backup_option in backup_options:
                            if backup_option == 0:
                                tasks_gestion_menu(username=username, users=users)
                            elif backup_option == 1:
                                todolist.save_backup(username=username)
                            elif backup_option == 2:
                                todolist.show_backups(username=username)
                                print("\nEnter the timestamp of the backup you want to restore (ex : 1700000000), enter \"q\" to cancel.\n")
                                selected_backup = input("(timestamp) > ")
                                if selected_backup.lower() == 'q':
                                    raise ValueError
                                todolist.load_from_backup(username=username, timestamp=selected_backup)
                            elif backup_option == 3:
                                todolist.show_backups(username=username)
                                print("\nEnter the timestamp of the backup you want to delete (ex : 1700000000), enter \"q\" to cancel.\n")
                                selected_backup = input("(timestamp) > ")
                                if selected_backup.lower() == 'q':
                                    raise ValueError
                                todolist.delete_backup(username=username, timestamp=selected_backup)
                        else:
                            raise ValueError
                    except ValueError:
                        print("\nIncorrect Value.")
            except ValueError:
                print("\nIncorrect Value.")

def settings_menu(username, users):
            print_title("Settings")
            print("| 1 - Change Username")
            print("| 2 - Change Password")
            print("| 3 - Delete My Data")
            print("| 5 - Delete My Account")
            print("| 0 - Return\n")

            options = [0, 1, 2, 3, 4, 5]
            option = int(input("(int) > "))

            try:
                if option.__class__ is int:
                    try:
                        if option in options:
                            if option == 0:
                                menu(True)
                            elif option == 1:
                                modify_user_username(username=username)
                            elif option == 2:
                                modify_user_password(username=username)
                            elif option == 3:
                                wipe_data_for_user(username=username, users=users)
                            elif option == 4:
                                delete_user(username=username, users=users)
                        else:
                            raise ValueError
                    except ValueError:
                        print("\nSeriously buy glasses buddy, you need to choose between a few nums what's complicated ??")
                else:
                    raise TypeError
            except TypeError:
                print("\nYou need to enter a interger number like 1, 2, 3 ... , idiot.")

def users_gestion_menu(username, users):
    print_title("User Gestion")
    print("| 1 - Add User")
    print("| 2 - Modify User")
    print("| 3 - Delete User")
    print("| 4 - Wipe Selected User Data")
    print("| 0 - Return")

    options = [0, 1, 2, 3, 4]

    option = input("\n(option) > ")

    try:
        if option in options:
            if option == 0:
                connected_menu(username=username, users=users)
            elif option == 1:
                print("\nYou will create a new user.\n")
                creation_user_modal()
            elif option == 2:
                modify_user_modal(user=username, users=users)
            elif option == 3:
                try:
                    print_title("Delete User")
                    list_users()
                    selected_user = 1
                    users_list = []
                    for user in users:
                        users_list.append(user)
                    selected_user = int(input("Select a user. (ex : 1 for 1 - viktor_srhk.) >  "))
                    if selected_user in users:
                        i = selected_user - 1
                        username = users_list[i]
                        delete_user(username=username, users=users)
                    else:
                        raise ValueError
                except ValueError:
                    print("User Not Found.")

            elif option == 4:
                try:
                    print_title("Wipe User Data")
                    list_users()
                    selected_user = 1
                    users_list = []
                    for user in users:
                        users_list.append(user)
                    selected_user = int(input("Select a user. (ex : 1 for 1 - viktor_srhk.) >  "))
                    if selected_user in users:
                        i = selected_user - 1
                        username = users_list[i]
                        wipe_data_for_user(username=username, users=users)
                    else:
                        raise ValueError
                except ValueError:
                    print("User Not Found.")
        else:
            raise ValueError
    except ValueError:
        pass


def menu(logged, username=None):
    try:
        grettings = True
        update_users_list()
        users = update_users_list()
        while True:
            while logged is False:
                deconnected_menu(users=users)

            
            try:
                if grettings is True:
                    print(f"Hello, {username}, what's up !")
                    grettings = False

                connected_menu(username=username, users=users)
            except KeyboardInterrupt:
                print(f"\n\nBye Bye {username}!\n")
                exit()
    except KeyboardInterrupt:
        print("\nBye Bye !")
        exit()

def main():
    try:
        with open("./initialization.txt", "r") as f:
            if f.read().split() == ['False']:
                initialized = False
            else:
                initialized = True
    except FileNotFoundError:
        with open("./initialization.txt", "+x") as f:
            f.write("False")
            initialized = False

    if initialized is False:
        print("Initialization of the App !")
        try:
            user_accept = input("Do you want to continue ? (yes/no default: yes): ")

            if user_accept == '' or user_accept.lower() == 'yes':
                if 'users' in os.listdir("./"):
                    print("\nUsers detected, no initialization needed.")
                    with open("./initialization.txt", "+wt") as f:
                        f.write("True")
                        initialized = True
                    menu(False)
                else:
                    initialization()
                    menu(True)
            elif user_accept.lower() == 'no':
                continue_init = False
                return continue_init
            else:
                raise ValueError
        except ValueError:
            print("Incorrect value.. Bro it's just no or yes..")
    else:
        menu(False)

if __name__ == "__main__":
    main()

# Ajouter une confirmation avant de supprimer un utilisateur : Fait
# Ajouter une option pour que l'utilisateur puisse changer son mot de passe : Fait
# Ajouter une option pour que l'utilisateur puisse supprimer son compte : Fait
# Ajouter une option pour marquer une tache comme complétée : Fait
# Ajouter une option pour voir les tasks complétées et non complétées séparément : Fait
# Ajouter une option pour trier les tasks par date d'échéance : Fait
# Ajouter une option pour trier les tasks par date de modification : Fait
# Ajouter une option pour rechercher une tache par nom ou description : Fait
# Ajouter une option pour exporter les tasks au format CSV ou JSON : Non-Fait (Peut-Etre Plus Tard)
# Ajouter une interface graphique avec Tkinter ou PyQt : Non-Fait (Pas Prevu)
# Ajouter une base de données pour stocker les utilisateurs et les tasks : Non-Fait (Peut-Etre Plus Tard)
# Ajouter des tests unitaires pour le code : Non-Fait
# Ajouter une documentation pour le code : Non-Fait
# Ajouter un fichier README pour le projet : Non-Fait
# Ajouter une licence pour le projet : Non-Fait
# Ajouter un système de journalisation pour suivre les actions de l'utilisateur : Fait
# Ajouter une option pour sauvegarder automatiquement les tasks à chaque modification : Fait
# Ajouter une option pour restaurer les tasks à partir d'une sauvegarde précédente : Fait
# Ajouter une option pour définir des rappels pour les tasks : Non-Fait (Pas Prevu)
# Ajouter une option pour personnaliser l'apparence de l'application : Non-Fait
# Ajouter une option pour partager les tasks avec d'autres utilisateurs : Non-Fait (Pas Prevu)
# Ajouter une option pour synchroniser les tasks avec un service cloud : Non-Fait (Pas Prevu)
# Ajouter une option pour importer des tasks à partir d'un fichier externe : Non-Fait
# Ajouter une option pour archiver les tasks complétées : Non-Fait
# Ajouter une option pour définir des priorités pour les tasks : Non-Fait (Pas Prevu)
# Ajouter une option pour filtrer les tasks par priorité ou date d'échéance : Non-Fait (Pas Prevu)
# Ajouter une option pour créer des sous-tasks pour une tache principale : Non-Fait (Pas Prevu)
# Ajouter une option pour attribuer des tasks à d'autres utilisateurs : Non-Fait (Pas Prevu)
# Ajouter une option pour suivre le temps passé sur chaque tache : Non-Fait (Pas Prevu)
# Ajouter une option pour générer des rapports sur les tasks complétées et en cours : Non-Fait  (Pas Prevu)
# Ajouter une option pour définir des objectifs hebdomadaires ou mensuels pour les tasks : Non-Fait (Pas Prevu)
# Ajouter une option pour recevoir des notifications par email pour les tasks à venir : Non-Fait (Pas Prevu)
# Ajouter une option pour intégrer l'application avec un calendrier externe : Non-Fait (Pas Prevu)
# Ajouter une option pour personnaliser les notifications et les rappels : Non-Fait (Pas Prevu)
# Ajouter une option pour créer des modèles de tasks récurrentes : Non-Fait (Pas Prevu)
# Ajouter une option pour suivre les progrès sur les tasks à long terme : Non-Fait (Pas Prevu)
# Ajouter une option pour collaborer sur des tasks avec d'autres utilisateurs en temps réel : Non-Fait (Pas Prevu)