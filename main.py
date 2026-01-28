# To-Do list mini-project in Python.
# Je parle français but I will do it in english parceque ça fait plus dev experimenté mdrr
# Alors que c'est mon premier projet concret miskine
# Created at Wed 29 Oct 2025 10:06:20 PM CET by @viktor_srhk on Instagram (Go sub NOW!!!).

# Imports

import shutil
import time
import os
from getpass import getpass
import bcrypt
from datetime import datetime, timedelta


class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        # Generate a salt and hash the password
        # bcrypt.gensalt() generates a new salt each time, making it secure
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def create_user_storage(self):
        user_dir = f"users/{self.username}"

        os.makedirs(user_dir, exist_ok=True)

        with open(f"{user_dir}/credentials.txt", "w") as f:
            f.write(self.password_hash)

        print(f"\n{self.username}'s storage created.\n")


# Task class


class Task:
    def __init__(self, name, complete_before, description=None):
        self.id = int(time.time() * 1000) # Keeping original id generation for now
        self.name = name
        self.description = description
        self.last_modified = datetime.now()
        # complete_before is expected in days, so add it as a timedelta
        self.complete_before = datetime.now() + timedelta(days=complete_before)
        self.completed = False


# ToDoList class to store tasks


class ToDoList:
    def __init__(self):
        self.tasks = []

    def save_data_file(self, username):
        data_file = f"users/{username}/data.txt"
        try:
            with open(data_file, "w") as f:
                for task in self.tasks:
                    # Convert datetime objects to Unix timestamps (float) for storage
                    last_modified_timestamp = task.last_modified.timestamp()
                    complete_before_timestamp = task.complete_before.timestamp()
                    line = f"{task.name}|{task.description}|{complete_before_timestamp}|{last_modified_timestamp}|{task.completed}\n"
                    f.write(line)
            print("Data file saved successfully.")
        except Exception as e:
            print(f"Error saving data file: {e}")

    def init_data_file(self, username):
        user_dir = f"users/{username}"
        data_file = f"{user_dir}/data.txt"
        
        os.makedirs(user_dir, exist_ok=True) # Ensure user directory exists

        if not os.path.exists(data_file):
            try:
                with open(data_file, "w"): # Create an empty file if it doesn't exist
                    pass
                print(f"Data file for {username} successfully created.")
            except Exception as e:
                print(f"Error creating data file for {username}: {e}")
        else:
            print(f"Data file for {username} already exists, skipping creation.")

    def load_from_data_file(self, username):
        data_file = f"users/{username}/data.txt"
        try:
            with open(data_file, "r") as f:
                lines = f.readlines()
                # Clear current tasks
                self.tasks = []
                for line in lines:
                    name, description, complete_before_ts, last_modified_ts, completed = (
                        line.strip().split("|")
                    )
                    # Convert timestamps back to datetime objects
                    complete_before_dt = datetime.fromtimestamp(float(complete_before_ts))
                    last_modified_dt = datetime.fromtimestamp(float(last_modified_ts))
                    
                    # When loading, the 'complete_before' parameter in Task __init__ expects days,
                    # but we have a datetime object. We'll reconstruct the Task object and then
                    # explicitly set its datetime attributes.
                    # A dummy value for complete_before (days) is passed to the constructor,
                    # which will be immediately overwritten by complete_before_dt.
                    task = Task(
                        name,
                        (complete_before_dt - datetime.now()).days if complete_before_dt > datetime.now() else 0, # Placeholder
                        description if description != "None" else None,
                    )
                    task.complete_before = complete_before_dt
                    task.last_modified = last_modified_dt
                    task.completed = completed == "True"
                    self.tasks.append(task)
        except FileNotFoundError:
            print(f"Data file for {username} not found. Initializing...")
            self.init_data_file(username)
            # After initialization, attempt to load again (it will be empty)
            self.load_from_data_file(username) 
        except Exception as e:
            print(f"Error loading data file: {e}")

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
            desc = task.description if task.description else "No description"
            
            # Calculate duration since last modified
            time_since_modified = datetime.now() - task.last_modified
            last_modified_str = f"{time_since_modified.days} days ago"

            if task.completed:
                status = "Completed!"
            else:
                time_remaining = task.complete_before - datetime.now()
                if time_remaining.total_seconds() < 0:
                    status = "Overdue!"
                else:
                    days_remaining = time_remaining.days
                    hours_remaining = time_remaining.seconds // 3600
                    minutes_remaining = (time_remaining.seconds % 3600) // 60
                    if days_remaining > 0:
                        status = f"Need to complete in {days_remaining} days, {hours_remaining} hours."
                    elif hours_remaining > 0:
                        status = f"Need to complete in {hours_remaining} hours, {minutes_remaining} minutes."
                    else:
                        status = f"Need to complete in {minutes_remaining} minutes."
            
            # Print with or without description
            if desc:
                print(
                    f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified_str}"
                )
            else:
                print(
                    f"{index} - {name}. {status} - Last Modified : {last_modified_str}"
                )

    def show_tasks(self, username, users):
        self.load_from_data_file(username=username)
        
        def _display_tasks_list(tasks_to_display, title="Tasks"):
            print(f"\n------------------ {title} ------------------\n")
            if not tasks_to_display:
                print("No tasks available.")
                return

            for index, task in enumerate(tasks_to_display, start=1):
                name = task.name
                desc = task.description if task.description else "No description"
                
                time_since_modified = datetime.now() - task.last_modified
                last_modified_str = f"{time_since_modified.days} days ago"

                if task.completed:
                    status = "Completed!"
                else:
                    time_remaining = task.complete_before - datetime.now()
                    if time_remaining.total_seconds() < 0:
                        status = "Overdue!"
                    else:
                        days_remaining = time_remaining.days
                        hours_remaining = time_remaining.seconds // 3600
                        minutes_remaining = (time_remaining.seconds % 3600) // 60
                        if days_remaining > 0:
                            status = f"Need to complete in {days_remaining} days, {hours_remaining} hours."
                        elif hours_remaining > 0:
                            status = f"Need to complete in {hours_remaining} hours, {minutes_remaining} minutes."
                        else:
                            status = f"Need to complete in {minutes_remaining} minutes."
                
                if desc:
                    print(
                        f"{index} - {name}. {desc}. {status} - Last Modified : {last_modified_str}"
                    )
                else:
                    print(
                        f"{index} - {name}. {status} - Last Modified : {last_modified_str}"
                    )

        _display_tasks_list(self.tasks, "All Tasks")

        print("\n| 1 - Show only completed")
        print("| 2 - Show only uncompleted")
        print("| 3 - Sort By Due Date")
        print("| 4 - Sort By Modification Date")
        print("| 5 - Search by terms")
        print("| 0 - Return\n")

        options = [0, 1, 2, 3, 4, 5]
        try:
            option = int(input("(int) > "))

            if option not in options:
                raise ValueError
            
            if option == 0:
                return # Return to the calling menu

            elif option == 1:
                completed_tasks = [task for task in self.tasks if task.completed]
                _display_tasks_list(completed_tasks, "Completed Tasks")
            
            elif option == 2:
                uncompleted_tasks = [task for task in self.tasks if not task.completed]
                _display_tasks_list(uncompleted_tasks, "Uncompleted Tasks")
            
            elif option == 3:
                # Sort by complete_before (due date)
                sorted_tasks = sorted(self.tasks, key=lambda task: task.complete_before)
                _display_tasks_list(sorted_tasks, "Sorted Tasks By Due Date")
            
            elif option == 4:
                # Sort by last_modified date
                sorted_tasks = sorted(self.tasks, key=lambda task: task.last_modified, reverse=True)
                _display_tasks_list(sorted_tasks, "Sorted Tasks By Last Modification Date")
            
            elif option == 5:
                print(
                    "\n------------------ Search Tasks By Given Terms ------------------\n"
                )
                search_terms = input("Enter some terms to search them in tasks.\n(terms) > ")
                matching_tasks = [
                    task for task in self.tasks 
                    if search_terms.lower() in task.name.lower() or 
                       (task.description and search_terms.lower() in task.description.lower())
                ]
                _display_tasks_list(matching_tasks, f"Search Results for '{search_terms}'")
        except ValueError:
            print("Invalid value, please enter a number from the options.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def modify_task(
        self,
        input_id,
        name=None,
        description=None,
        complete_before=None, # This will be days from now
        completed=None,
    ):
        task_index = input_id - 1

        if not (0 <= task_index < len(self.tasks)):
            print(f"Error: No task found with ID {input_id}.")
            return False

        task = self.tasks[task_index]
        has_changed = False

        # Store old values for printing changes
        old_name = task.name
        old_description = task.description
        old_complete_before_dt = task.complete_before
        old_completed = task.completed

        if name is not None and name != old_name:
            task.name = name
            print(f"Changed name from '{old_name}' to '{name}'.")
            has_changed = True
        
        if description is not None and description != old_description:
            task.description = description
            print(f"Changed description from '{old_description}' to '{description}'.")
            has_changed = True

        if complete_before is not None:
            try:
                # complete_before is expected in days
                new_complete_before_dt = datetime.now() + timedelta(days=float(complete_before))
                if new_complete_before_dt != old_complete_before_dt:
                    task.complete_before = new_complete_before_dt
                    print(f"Changed completion date from '{old_complete_before_dt.strftime('%Y-%m-%d')}' to '{new_complete_before_dt.strftime('%Y-%m-%d')}'.")
                    has_changed = True
            except ValueError:
                print(f"Invalid input for 'complete before' days: {complete_before}. Must be a number.")
        
        if completed is not None and completed != old_completed:
            task.completed = completed
            print(f"Changed completion status for '{task.name}' to {'Completed' if completed else 'Uncompleted'}.")
            has_changed = True
            
            # If marked uncompleted, prompt for a new complete_before date if the old one is in the past
            if not completed and task.complete_before < datetime.now():
                while True:
                    try:
                        new_days_str = input("Task marked uncompleted and is overdue. Enter new days to complete (e.g., 5 for 5 days from now): ")
                        new_days = float(new_days_str)
                        task.complete_before = datetime.now() + timedelta(days=new_days)
                        print(f"New completion date for '{task.name}' set to '{task.complete_before.strftime('%Y-%m-%d')}'.")
                        has_changed = True
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
        
        if has_changed:
            task.last_modified = datetime.now()
            print("Task modified successfully.")
            return True
        else:
            print("No significant change detected or saved.")
            return False

    def delete_task(self, input_id, username):
        input_id = int(input_id)

        id = input_id - 1
        name = self.tasks[id].name
        del self.tasks[id]

        todolist.save_data_file(username=username)

        print(f'Task "{name}" deleted')

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
            shutil.copy2(user_data_path, backup_file_path)  # copy2 preserves metadata
            print(f"\nBackup created successfully at {backup_file_path}")
        except Exception as e:
            print(f"\nError creating backup: {e}")

    def load_from_backup(self, username, timestamp):
        backup_file_path = os.path.join(
            "users", username, "backups", timestamp, "data.txt"
        )
        user_data_path = os.path.join("users", username, "data.txt")

        # Check if the backup file exists
        if not os.path.exists(backup_file_path):
            print(f"\nError: Backup file not found at {backup_file_path}")
            return

        # Restore the backup by copying it to the user's data file location
        try:
            shutil.copy2(backup_file_path, user_data_path)  # copy2 preserves metadata
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
    print("\n", "-" * 5, " ", str, " ", "-" * 5)


def make_clickable(text=None, url=""):
    if text is None:
        text = url  # Use the URL itself as the display text if none is provided
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def show_networks(username):
    if username == "Viktor":
        print_title("My Networks")
        print("\nHello buddy, I'm Viktor the devlopper !")
        print("Check my networks : ")
        print(
            f"     Github : {make_clickable('Vikbg', 'https://github.com/Vikbg/')} & {make_clickable('viktor_srhk', 'https://github.com/viktorsrhk/')}"
        )
        print(
            f"     Instagram : {make_clickable('viktor.wow', 'https://instagram.com/viktor.wow/')} (public) & {make_clickable('viktor_srhk', 'https://instagram.com/viktor_srhk/')} (private)"
        )
        print(
            f"     TikTok : {make_clickable('viktor_srhk', 'https://www.tiktok.com/@viktor_srhk')}"
        )
        print(
            f"     YouTube : {make_clickable('viktor', 'https://www.youtube.com/@viktorsrhk')}"
        )
        print(
            f"     Linkedin : {make_clickable('viktor_srhk', 'https://www.linkedin.com/in/viktorsrhk/')}"
        )
        print(f"     Replit : {make_clickable('VikS0', 'https://replit.com/@VikS0/')}")
        print(f"     Portfolio : {make_clickable(None, 'In The Pipeline.')}")


def show_credits():
    print_title("Credits")
    print("\nToDoList app developed with love by viktor_srhk.")
    show_networks(username="Viktor")


def update_users_list():
    try:
        users = os.listdir("users/")
        return users
    except FileNotFoundError:
        os.mkdir("users")
        users = []
        return users


def list_users():
    i = 0
    
    users = update_users_list() # Call only once
    users_list = users # The update_users_list already returns a list of usernames or []

    print("\n------------------ USERS ------------------")

    if not users_list: # Check if the list is empty
        print("\nNo users available. Create one !\n")
        return [], True # Consistent return: empty list and True for no_user
    else:
        print("\nAll available users : ")
        print("--------------------------------")
        for user in users_list:
            i += 1
            print(f"    {i} - {user}")
        print("--------------------------------\n")
        return users_list, False # Consistent return: list of users and False for no_user


def create_user(username, password):
    new_user = User(username, password)
    new_user.create_user_storage()

    update_users_list()

    print(f"User {username} created !")


def creation_user_modal():
    try:
        print("Leave username blank to cancel.")
        username = input("(username) > ").strip()
        if username == "":
            print("Action Cancelled.")
            return # Exit modal gracefully
        
        # Check if username already exists
        if os.path.exists(f"users/{username}"):
            print(f"Error: User '{username}' already exists. Please choose a different username.")
            return
            
        password = getpass("(password) > ")
        if password == "":
            print("Error: Password cannot be empty.")
            return # Exit modal gracefully
        
        create_user(username=username, password=password)
        print(f"User {username} created successfully!")
    except Exception as e:
        print(f"An unexpected error occurred during user creation: {e}")


def _verify_password(username, provided_password):
    """
    Verifies a provided password against the stored hashed password for a given username.
    Returns True if the password matches, False otherwise.
    """
    try:
        with open(f"users/{username}/credentials.txt", "r") as f:
            stored_hash = f.read().strip()
        
        if provided_password is None or provided_password == "":
            print("\nError: Password cannot be empty.")
            return False
        
        # Ensure provided_password is a string before encoding
        if not isinstance(provided_password, str):
            provided_password = str(provided_password)

        if bcrypt.checkpw(provided_password.encode("utf-8"), stored_hash.encode("utf-8")):
            return True
        else:
            print("\nError: Wrong Password !")
            return False
    except FileNotFoundError:
        print(f"\nError: User {username} credentials file not found.")
        return False
    except Exception as e:
        print(f"\nAn unexpected error occurred during password verification: {e}")
        return False

def modify_user_username(username):
    try:
        print(f"\nYou will change username for {username} user, think before act !")
        print("Please enter your current password.\n")
        current_password = str(getpass("(password) > "))
        
        if _verify_password(username, current_password):
            try:
                print("\nAccept.")
                print("Enter the new username.\n")
                new_username = str(input("(username) > "))
                confirm_new_username = str(input("(confirm) > "))
                
                if new_username == "" or new_username is None:
                    raise ValueError("New username cannot be empty.")

                if new_username == confirm_new_username:
                    # Check if new username already exists
                    if os.path.exists(f"users/{new_username}"):
                        raise ValueError(f"User with username '{new_username}' already exists.")
                    
                    os.rename(f"users/{username}", f"users/{new_username}")
                    print("\nUsername changed successfully.")
                    # Update menu with new username if current user changed their own username
                    # This logic needs to be handled outside, as `modify_user_username` doesn't know the current logged in user directly
                else:
                    raise ValueError("Usernames Dismatch !")
            except ValueError as e:
                print(f"\nError: {e}")
            except TypeError:
                print("\nError: Username needs to be a string value")
        # _verify_password already prints error messages for incorrect password
    except ValueError as e:
        print(f"\nError: {e}")


def modify_user_password(username):
    try:
        print(f"\nYou will change password for {username} user, think before act !")
        print("Please enter your current password.\n")
        current_password = str(getpass("(password) > "))
        with open(f"users/{username}/credentials.txt", "r") as f:
            stored_hash = f.read().strip()
        
        if current_password is None or current_password == "":
            raise ValueError("Password cannot be empty")
        
        if bcrypt.checkpw(current_password.encode("utf-8"), stored_hash.encode("utf-8")):
            print("\nAccept.")
            print("Enter the new password.\n")
            new_password = str(getpass("(password) > "))
            confirm_new_password = str(input("(confirm) > "))
            
            if new_password is None or new_password == "":
                raise ValueError("New password cannot be empty")

            if new_password == confirm_new_password:
                new_password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                with open(f"users/{username}/credentials.txt", "w") as f:
                    f.write(new_password_hash)
                print("\nPassword changed successfully.")
            else:
                raise ValueError("Passwords do not match !")
        else:
            raise ValueError("Wrong current password !")
    except ValueError as e:
        print(f"\nError: {e}\n")


def modify_user_modal(user_calling_func, all_users):
    print_title("Modify User")
    
    users_info = list_users() # This function returns (users_list, no_user) or just no_user
    if users_info is True: # no_user case
        print("No users to modify.")
        return

    users_list, no_user_flag = users_info

    if no_user_flag or not users_list:
        print("No users available to modify.")
        return

    while True:
        try:
            print("Select a user to modify:")
            for idx, u_name in enumerate(users_list, 1):
                print(f"    {idx} - {u_name}")
            print("0 - Return")

            choice = input("(int) > ")
            if choice == "0":
                return # Exit this modal

            selected_index = int(choice) - 1
            if not (0 <= selected_index < len(users_list)):
                raise ValueError("Invalid user selection.")
            
            username_to_modify = users_list[selected_index]
            print(f"\nYou selected {username_to_modify}. Please enter their password.\n")
            password_to_verify = getpass("(password) > ")
            
            if _verify_password(username_to_modify, password_to_verify):
                print_title(f"Modify {username_to_modify}")
                print("| 1 - Modify Username")
                print("| 2 - Modify Password")
                print("| 3 - Modify User Tasks")
                print(f"| 4 - Connect to {username_to_modify}")
                print("| 0 - Return")

                option_choice = input("(int) > ")
                options_map = {
                    "1": lambda: modify_user_username(username=username_to_modify),
                    "2": lambda: modify_user_password(username=username_to_modify),
                    "3": lambda: tasks_gestion_menu(username=username_to_modify, users=all_users),
                    "4": lambda: login(username=username_to_modify, password=password_to_verify) # Pass original plaintext password for login
                }
                
                if option_choice == "0":
                    return # Go back to user gestion menu
                elif option_choice in options_map:
                    options_map[option_choice]()
                    return # Action performed, return to previous menu
                else:
                    print("Invalid option. Please choose from 0-4.")
            else:
                print("Incorrect password for the selected user.")
            return # After attempt, return to user selection
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def wipe_data_for_user(username, users):
    try:
        print(f"\nYou will wipe data for {username} user, please think before act !")
        print(f"Please enter {username} current password.\n")
        current_password = str(getpass("(password) > "))
        
        if _verify_password(username, current_password):
            print("\nAccept.")
            todolist.show_tasks(username=username, users=users)
            print(f"\nAre you sure to wipe {username} data ?.\n")
            confirmation = str(input("(yes/no) > "))
            confirmation = confirmation.lower().strip()
            if confirmation not in ["yes", "no"]:
                raise ValueError("Invalid confirmation. Please type 'yes' or 'no'.")
            
            confirm_confirmation = str(input("(confirm) > "))
            confirm_confirmation = confirm_confirmation.lower().strip()
            if confirm_confirmation not in ["yes", "no"]:
                raise ValueError("Invalid confirmation. Please type 'yes' or 'no'.")
            
            if confirmation == "yes" and confirm_confirmation == "yes":
                data_file_path = f"users/{username}/data.txt"
                if os.path.exists(data_file_path):
                    os.remove(data_file_path)
                    print("Data Wiped.")
                    # It's better to return to the connected menu or a similar state rather than calling menu(True) directly
                else:
                    print(f"No data file found for user {username}.")
            else:
                print("\nAction Cancelled.")
        # _verify_password already prints error messages for incorrect password
    except ValueError as e:
        print(f"\nError: {e}\n")


def delete_user(username, users):
    try:
        print(f"\nYou will delete {username} user, please think before act !")
        print(f"Please enter {username} current password.\n")
        current_password = str(getpass("(password) > "))
        
        if _verify_password(username, current_password):
            print("\nAccept.")
            todolist.show_tasks(username=username, users=users)
            print(f"\nAre you sure to delete {username} account ?.\n")
            confirmation = str(input("(yes/no) > "))
            confirmation = confirmation.lower().strip()
            if confirmation not in ["yes", "no"]:
                raise ValueError("Invalid confirmation. Please type 'yes' or 'no'.")
            
            confirm_confirmation = str(input("(confirm) > "))
            confirm_confirmation = confirm_confirmation.lower().strip()
            if confirm_confirmation not in ["yes", "no"]:
                raise ValueError("Invalid confirmation. Please type 'yes' or 'no'.")
            
            if confirmation == "yes" and confirm_confirmation == "yes":
                user_dir = f"users/{username}"
                if os.path.exists(user_dir):
                    shutil.rmtree(user_dir)
                    print("\nUser Deleted.")
                else:
                    print(f"User directory for {username} not found.")
            else:
                print("\nAction Cancelled.")
        # _verify_password already prints error messages for incorrect password
    except ValueError as e:
        print(f"\nError: {e}\n")


def login(username, password):

    if os.path.exists(f"users/{username}/credentials.txt"):
        with open(f"users/{username}/credentials.txt", "r") as f:
            stored_hash = f.read().strip()
        
        if stored_hash.startswith(b'$2b$'.decode('utf-8')) or stored_hash.startswith(b'$2a$'.decode('utf-8')):
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                print(f"\nUser {username} logged !\n")
                return (True, username)
            else:
                print("\nPassword is incorrect.. Sorry buddy..")
        else:
            if stored_hash == password:
                print("\nWarning: Using an old, unhashed password. Please update your password for better security.")
                print(f"\nUser {username} logged !\n")
                return (True, username)
            else:
                print("\nPassword is incorrect.. Sorry buddy..")
    else:
        print(f"\nUser {username} don't exists. Buy glasses.\n")
    return None


def logout(username):
    print(f"User {username} logged out.\n")
    return (False, None)


def initialization():
    os.makedirs("users", exist_ok=True)

    print("\nHello buddy, I'm Viktor the devlopper of the ToDoList app !")
    print("Check my networks : ")
    print(
        f"     Github : {make_clickable('Vikbg', 'https://github.com/Vikbg/')} & {make_clickable('viktor_srhk', 'https://github.com/viktorsrhk/')}"
    )
    print(
        f"     Instagram : {make_clickable('viktor.wow', 'https://instagram.com/viktor.wow/')} (public) & {make_clickable('viktor_srhk', 'https://instagram.com/viktor_srhk/')} (private)"
    )
    print(
        f"     TikTok : {make_clickable('viktor_srhk', 'https://www.tiktok.com/@viktor_srhk')}"
    )
    print(
        f"     YouTube : {make_clickable('viktor', 'https://www.youtube.com/@viktorsrhk')}"
    )
    print(
        f"     Linkedin : {make_clickable('viktor_srhk', 'https://www.linkedin.com/in/viktorsrhk/')}"
    )
    print(f"     Replit : {make_clickable('VikS0', 'https://replit.com/@VikS0/')}")
    print(f"     Portfolio : {make_clickable(None, 'In The Pipeline.')}")
    print("Before we start, I need to ask you a few questions.")
    print("So....")
    print("Let's create your profile of my new bestest user of the year (joke) !")
    print("How want you to name ?\n")

    username = input("Your name ?? > ").strip()

    print(f"\nWow, your name {username} is fantastic, nice to meet you !!")
    print("Ok now you need to tell me a very top secret secret...")
    print("what password want you ?")
    print("shhh !\n")

    password = getpass("(password) > ")

    print(
        "\nOk I think we're good, not you ? So I will let you take place in the fantastic world of my ToDoList app ! Bye bye !\n"
    )

    create_user(username=username, password=password)
    print(f"User {username} created. Please log in to continue.")


todolist = ToDoList()


def deconnected_menu(users):
    while True: # Loop until a state change or exit
        try:
            print_title("ToDoList by viktor_srhk - Menu")
            print("\n| 1 - Login")
            print("| 2 - Sign Up")
            print("| 3 - Credits")
            print("| 0 - Quit\n")

            option = input("Enter an option (integers only) > ").strip()
            
            if option == "0":
                print("Bye Bye !!")
                exit() # Exit the program directly
            elif option == "1":
                users_list, no_user_flag = list_users()
                if no_user_flag:
                    print("No users to log in. Please sign up first.")
                    input("\nPress Enter to return to menu...")
                    continue # Stay in deconnected menu
                
                while True: # Loop for user selection and login
                    try:
                        selected_user_input = input("Select a user by number (ex: 1 for 1 - viktor_srhk.) or '0' to return > ").strip()
                        if selected_user_input == '0':
                            break # Go back to deconnected menu options
                        
                        selected_index = int(selected_user_input) - 1
                        if not (0 <= selected_index < len(users_list)):
                            raise ValueError("Invalid user number.")
                        
                        username = users_list[selected_index]
                        print(f"\nYou selected {username}, enter the password.\n")
                        password = getpass("(password) > ")
                        login_result = login(username=username, password=password)
                        if login_result:
                            return login_result # Return (True, username) to main menu
                        else:
                            input("\nPress Enter to try again or return to menu...")
                            # continue to allow user to re-enter password or select another user
                    except ValueError as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred during login attempt: {e}")
            elif option == "2":
                print("\nSign up.\n")
                creation_user_modal()
                input("\nPress Enter to return to menu...")
            elif option == "3":
                show_credits()
                input("\nPress Enter to return to menu...")
            else:
                print("Invalid option selected. Please choose from 0, 1, 2, 3.")
                input("\nPress Enter to try again...")
        except ValueError as e:
            print(f"\nInvalid input: {e}")
            input("\nPress Enter to try again...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return None # Should ideally not be reached if there's a loop or exit


def connected_menu(username, users):
    while True: # Loop until a state change (logout) or exit
        try:
            print("\n| 1 - Tasks Gestion")
            print("| 2 - Users Gestion")
            print("| 3 - Settings")
            print("| 4 - Credits")
            print("| 9 - Logout")
            print("| 0 - Quit\n")

            option = input("Enter an option (integers only): ").strip()

            if option == "0":
                print("Bye Bye !!")
                exit()
            elif option == "9":
                return logout(username=username) # Returns (False, None)
            elif option == "1":
                tasks_gestion_menu(username=username, users=users)
                input("\nPress Enter to return to main menu...")
            elif option == "2":
                users_gestion_menu(username=username, users=users)
                input("\nPress Enter to return to main menu...")
            elif option == "3":
                settings_menu(username=username, users=users)
                input("\nPress Enter to return to main menu...")
            elif option == "4":
                show_credits()
                input("\nPress Enter to return to main menu...")
            else:
                print("Invalid option. Please choose from 0, 1, 2, 3, 4, 9.")
                input("\nPress Enter to try again...")
        except ValueError as e:
            print(f"Incorrect Value: {e}")
            input("\nPress Enter to try again...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    # If for some reason the loop breaks without logout/exit, return None
    return None


def tasks_gestion_menu(username, users):
    while True:
        try:
            print_title("Tasks Gestion")
            print("| 1 - Add task")
            print("| 2 - Delete Task")
            print("| 3 - Modify Task")
            print("| 4 - Show all tasks.")
            print("| 5 - Manage Backups")
            print("| 0 - Return\n")

            option = input("Enter an option (integers only): ").strip()

            if option == "0":
                return # Return to connected_menu

            elif option == "1":
                try:
                    print('\nEnter the name of the task (type "q" to cancel).')
                    task_name = input("(name) > ").strip()
                    if task_name.lower() == "q":
                        raise ValueError("Task creation cancelled.")
                    if not task_name:
                        raise ValueError("Task name cannot be empty.")
                    
                    print('\nEnter a description (optional, type "q" to cancel).')
                    task_description = input("(description) > ").strip()
                    if task_description.lower() == "q":
                        task_description = None # Set to None if cancelled
                    
                    print(
                        'Before when do you need to complete it? (in days, type "q" to cancel).'
                    )
                    task_complete_to_str = input("(days) > ").strip()
                    if task_complete_to_str.lower() == "q":
                        raise ValueError("Task creation cancelled.")
                    
                    task_complete_to = float(task_complete_to_str)
                    if task_complete_to < 0:
                        raise ValueError("Days to complete must be a non-negative number.")

                    todolist.add_task(
                        name=task_name,
                        complete_before=task_complete_to,
                        description=task_description,
                    )
                    todolist.save_data_file(username=username)
                    input("\nPress Enter to return to tasks menu...")

                except ValueError as ve:
                    print(f"Error: {ve}\n")
                    input("\nPress Enter to return to tasks menu...")
                except TypeError:
                    print(
                        "Type error: Please enter a valid number for days (e.g., 1, 1.5, 2).\n"
                    )
                    input("\nPress Enter to return to tasks menu...")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}\n")
                    input("\nPress Enter to return to tasks menu...")

            elif option == "2":
                todolist.print_tasks(username=username)
                try:
                    if not todolist.tasks:
                        print("No tasks to delete.")
                        input("\nPress Enter to return to tasks menu...")
                        continue

                    task_to_delete_str = input(
                        'Enter the ID of the task to delete (e.g., 1 for "1 - Do my Homeworks", type "q" to cancel).'
                    ).strip()
                    if task_to_delete_str.lower() == "q":
                        print("Deletion cancelled.")
                        input("\nPress Enter to return to tasks menu...")
                        continue
                    
                    task_to_delete = int(task_to_delete_str)
                    if not (0 < task_to_delete <= len(todolist.tasks)):
                        raise ValueError("Invalid task ID.")

                    todolist.delete_task(task_to_delete, username=username)
                    todolist.save_data_file(username=username) # Save changes after deletion
                    input("\nPress Enter to return to tasks menu...")
                except ValueError as ve:
                    print(f"Error: {ve}\n")
                    input("\nPress Enter to return to tasks menu...")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}\n")
                    input("\nPress Enter to return to tasks menu...")

            elif option == "3":
                todolist.load_from_data_file(username=username)
                todolist.print_tasks(username=username)

                n_tasks = len(todolist.tasks)

                if n_tasks == 0:
                    print("No tasks found to modify.")
                    input("\nPress Enter to return to tasks menu...")
                    continue
                else:
                    try:
                        task_id_str = input(
                            "Enter the ID of the task you want to change (e.g., 1 for '1 - Do my Homeworks', type 'q' to cancel)."
                        ).strip()

                        if task_id_str.lower() == "q":
                            print("Modification cancelled.")
                            input("\nPress Enter to return to tasks menu...")
                            continue

                        task_id = int(task_id_str)
                        if not (0 < task_id <= n_tasks):
                            raise ValueError("Invalid ID: Must be within task list range.")

                        current_task = todolist.tasks[task_id - 1]
                        print(f"\nModifying task: {current_task.name}")

                        new_name = input(f"Enter new name (current: '{current_task.name}', leave blank to skip): ").strip()
                        new_name = new_name if new_name else None

                        new_description = input(f"Enter new description (current: '{current_task.description if current_task.description else 'None'}', leave blank to skip): ").strip()
                        new_description = new_description if new_description else None

                        new_completed_str = input(
                            f"Is it completed? (current: {'yes' if current_task.completed else 'no'}, type 'yes'/'no', leave blank to skip): "
                        ).lower().strip()
                        new_completed = None
                        if new_completed_str == "yes":
                            new_completed = True
                        elif new_completed_str == "no":
                            new_completed = False
                        elif new_completed_str != "":
                            raise ValueError("Invalid input for completion status. Type 'yes', 'no', or leave blank.")

                        new_complete_before_str = input(
                            f"Before when do you want to end this task? (current due: {current_task.complete_before.strftime('%Y-%m-%d')}, enter days from now, leave blank to skip): "
                        ).strip()
                        new_complete_before = None
                        if new_complete_before_str:
                            new_complete_before = float(new_complete_before_str)

                        if todolist.modify_task(
                            task_id,
                            new_name,
                            new_description,
                            new_complete_before,
                            completed=new_completed,
                        ):
                            todolist.save_data_file(username=username) # Save changes if modification occurred
                        input("\nPress Enter to return to tasks menu...")

                    except ValueError as ve:
                        print(f"Error: {ve}\n")
                        input("\nPress Enter to return to tasks menu...")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}\n")
                        input("\nPress Enter to return to tasks menu...")

            elif option == "4":
                todolist.load_from_data_file(username=username)
                todolist.show_tasks(username=username, users=users)
                input("\nPress Enter to return to tasks menu...")
            elif option == "5":
                print_title("Backups Gestion")
                print("| 1 - Create Backup")
                print("| 2 - Restore Backup")
                print("| 3 - Delete Backup")
                print("| 0 - Return\n")

                backup_option_str = input("(int) > ").strip()

                if backup_option_str == "0":
                    input("\nPress Enter to return to tasks menu...")
                    continue # Go back to tasks menu
                
                try:
                    backup_option = int(backup_option_str)

                    if backup_option == 1:
                        todolist.save_backup(username=username)
                        input("\nPress Enter to return to tasks menu...")
                    elif backup_option == 2:
                        todolist.show_backups(username=username)
                        if not os.path.exists(os.path.join("users", username, "backups")) or not os.listdir(os.path.join("users", username, "backups")):
                            input("\nPress Enter to return to tasks menu...")
                            continue

                        selected_backup = input(
                            '\nEnter the timestamp of the backup you want to restore (e.g., 1700000000), type "q" to cancel).\n(timestamp) > '
                        ).strip()
                        if selected_backup.lower() == "q":
                            print("Restore cancelled.")
                            input("\nPress Enter to return to tasks menu...")
                            continue
                        # Validate timestamp format if possible
                        todolist.load_from_backup(
                            username=username, timestamp=selected_backup
                        )
                        todolist.load_from_data_file(username=username) # Reload tasks after restoring backup
                        input("\nPress Enter to return to tasks menu...")
                    elif backup_option == 3:
                        todolist.show_backups(username=username)
                        if not os.path.exists(os.path.join("users", username, "backups")) or not os.listdir(os.path.join("users", username, "backups")):
                            input("\nPress Enter to return to tasks menu...")
                            continue

                        selected_backup = input(
                            '\nEnter the timestamp of the backup you want to delete (e.g., 1700000000), type "q" to cancel).\n(timestamp) > '
                        ).strip()
                        if selected_backup.lower() == "q":
                            print("Deletion cancelled.")
                            input("\nPress Enter to return to tasks menu...")
                            continue
                        # Validate timestamp format if possible
                        todolist.delete_backup(
                            username=username, timestamp=selected_backup
                        )
                        input("\nPress Enter to return to tasks menu...")
                    else:
                        print("Invalid backup option.")
                        input("\nPress Enter to try again...")
                except ValueError as ve:
                    print(f"Error: {ve}\n")
                    input("\nPress Enter to return to tasks menu...")
                except Exception as e:
                    print(f"An unexpected error occurred during backup management: {e}\n")
                    input("\nPress Enter to return to tasks menu...")
            else:
                print("Invalid option selected. Please enter a number from 0 to 5.")
                input("\nPress Enter to try again...")
        except ValueError as ve:
            print(f"Error: {ve}\n")
            input("\nPress Enter to try again...")
        except Exception as e:
            print(f"An unexpected error occurred in tasks management: {e}\n")
            input("\nPress Enter to try again...")


def settings_menu(username, users):
    while True:
        print_title("Settings")
        print("| 1 - Change Username")
        print("| 2 - Change Password")
        print("| 3 - Delete My Data")
        print("| 4 - Delete My Account") # Corrected option number
        print("| 0 - Return\n")

        option = input("(int) > ").strip()

        try:
            if option == "0":
                return # Return to connected_menu
            elif option == "1":
                modify_user_username(username=username)
                input("\nPress Enter to return to settings menu...")
            elif option == "2":
                modify_user_password(username=username)
                input("\nPress Enter to return to settings menu...")
            elif option == "3":
                wipe_data_for_user(username=username, users=users)
                input("\nPress Enter to return to settings menu...")
            elif option == "4": # Corrected option number
                delete_user(username=username, users=users)
                return # User deleted, should force logout and return to main deconnected menu
            else:
                print(
                    "\nInvalid option. Please choose between 0, 1, 2, 3, 4."
                )
                input("\nPress Enter to try again...")
        except ValueError as ve:
            print(f"\nError: {ve}")
            input("\nPress Enter to try again...")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            input("\nPress Enter to try again...")


def users_gestion_menu(username, users):
    while True:
        print_title("User Gestion")
        print("| 1 - Add User")
        print("| 2 - Modify User")
        print("| 3 - Delete User")
        print("| 4 - Wipe Selected User Data")
        print("| 0 - Return")

        option = input("\n(option) > ").strip()

        try:
            if option == "0":
                return # Return to connected_menu
            elif option == "1":
                print("\nYou will create a new user.\n")
                creation_user_modal()
                input("\nPress Enter to return to user gestion menu...")
            elif option == "2":
                modify_user_modal(user_calling_func=username, all_users=users)
                input("\nPress Enter to return to user gestion menu...")
            elif option == "3":
                try:
                    print_title("Delete User")
                    users_list, no_user_flag = list_users()
                    if no_user_flag:
                        print("No users to delete.")
                        input("\nPress Enter to return to user gestion menu...")
                        continue

                    selected_user_input = input(
                        "Select a user by number (ex : 1 for 1 - viktor_srhk.) or '0' to return >  "
                    ).strip()
                    if selected_user_input == '0':
                        print("Deletion cancelled.")
                        input("\nPress Enter to return to user gestion menu...")
                        continue

                    selected_index = int(selected_user_input) - 1
                    if not (0 <= selected_index < len(users_list)):
                        raise ValueError("Invalid user selection.")
                    
                    user_to_delete = users_list[selected_index]
                    delete_user(username=user_to_delete, users=users)
                    input("\nPress Enter to return to user gestion menu...")
                except ValueError as ve:
                    print(f"Error: {ve}")
                    input("\nPress Enter to return to user gestion menu...")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    input("\nPress Enter to return to user gestion menu...")

            elif option == "4":
                try:
                    print_title("Wipe User Data")
                    users_list, no_user_flag = list_users()
                    if no_user_flag:
                        print("No user data to wipe.")
                        input("\nPress Enter to return to user gestion menu...")
                        continue

                    selected_user_input = input(
                        "Select a user by number (ex : 1 for 1 - viktor_srhk.) or '0' to return >  "
                    ).strip()
                    if selected_user_input == '0':
                        print("Wipe data cancelled.")
                        input("\nPress Enter to return to user gestion menu...")
                        continue

                    selected_index = int(selected_user_input) - 1
                    if not (0 <= selected_index < len(users_list)):
                        raise ValueError("Invalid user selection.")
                    
                    user_to_wipe_data = users_list[selected_index]
                    wipe_data_for_user(username=user_to_wipe_data, users=users)
                    input("\nPress Enter to return to user gestion menu...")
                except ValueError as ve:
                    print(f"Error: {ve}")
                    input("\nPress Enter to return to user gestion menu...")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    input("\nPress Enter to return to user gestion menu...")
            else:
                print("Invalid option. Please choose from 0, 1, 2, 3, 4.")
                input("\nPress Enter to try again...")
        except ValueError as ve:
            print(f"Error: {ve}")
            input("\nPress Enter to try again...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            input("\nPress Enter to try again...")


def menu():
    logged = False
    username = None
    grettings = True

    while True:
        try:
            current_users = update_users_list() # Get the latest list of users
            if not logged:
                # deconnected_menu should return a tuple (logged, username) or None
                result = deconnected_menu(current_users)
                if result: # If deconnected_menu returned something (i.e., a login attempt)
                    logged, username = result
                    grettings = True # Reset greetings for new login
            else:
                if grettings:
                    print(f"\nHello, {username}, what's up !")
                    grettings = False
                
                # connected_menu should return a tuple (logged, username) or None
                result = connected_menu(username, current_users)
                if result: # If connected_menu returned something (e.g., logout)
                    logged, username = result
                    if not logged: # If logged out
                        grettings = True # Reset greetings
        except KeyboardInterrupt:
            if username:
                print(f"\n\nBye Bye {username}!\n")
            else:
                print("\n\nBye Bye !\n")
            exit()


def main():
    # Check if the application has been initialized (i.e., if there are any users)
    is_initialized = False
    if os.path.exists("users") and os.listdir("users"):
        is_initialized = True

    if not is_initialized:
        print("Initialization of the App !")
        try:
            user_accept = input("Do you want to continue with initialization? (yes/no default: yes): ").strip().lower()

            if user_accept == "" or user_accept == "yes":
                initialization() # This will create the first user and log them in
            elif user_accept == "no":
                print("Application not initialized. Exiting.")
                return
            else:
                raise ValueError("Incorrect value. Please respond 'yes' or 'no'.")
        except ValueError as ve:
            print(f"Error: {ve}")
            return # Exit if initialization was not accepted or had an error
        except Exception as e:
            print(f"An unexpected error occurred during initialization: {e}")
            return # Exit on unexpected error

    # Start the main menu loop
    menu()

if __name__ == "__main__":
    main()
