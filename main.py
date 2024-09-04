'''
@Author: Prabhas Kumar
@Assistant: GitHub Copilot, ChatGPT 4o

@Created: September 3'24
@Updated: None

@Project: College Personal Time-Table Version 1
@File: terminal app [Python 3(.12) script
'''


# Importing necessary modules
from InquirerPy import prompt
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from datetime import datetime
import json

from bin.new_data import Append_API, Delete_API, Format_API

class App:

    def __init__(self) -> None:
        self.data = []
        self.console = Console()

    def main(self):
        self.console.print("Welcome to the Personal Time-Table App", style="deep_pink2")

        options = [
            {"name": "Add a new deadline", "value": "add_deadline"},
            {"name": "View tasks", "value": "view_tasks"},
            {"name": "Dev mode", "value": "dev_mode"},
            {"name": "Exit", "value": "exit"} 
        ]
        
        questions = [
            {
                "type": "list",
                "message": "Select an option",
                "name": "selected_option",
                "choices": options
            }
        ]

        answers = prompt(questions)
        selected_option = answers["selected_option"]

        if selected_option == "add_deadline":
            self.console.print("Adding a new deadline...", style="green")
            self.add_deadline()

        elif selected_option == "view_tasks":
            self.console.print("Viewing tasks...", style="magenta")
            self.renderer()

        elif selected_option == "dev_mode":
            self.console.print("Entering dev mode...", style="bold yellow")
            self.dev()

        elif selected_option == "exit":
            self.console.print("Exiting the app...", style="deep_pink2")
            return
        
    def add_deadline(self):
        API = Append_API()
        
        name = Prompt.ask("\nEnter the name of the deadline")
        description = Prompt.ask("Enter a description for the deadline")

        while True:
            try:
                deadline_input = Prompt.ask("Enter the deadline date (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))
                _ = datetime.strptime(deadline_input, "%Y-%m-%d").date()
                break
            except ValueError:
                self.console.print("Invalid date format. Please use YYYY-MM-DD.", style="red")

        min_days_required = int(Prompt.ask("Enter the minimum days required before the deadline"))

        if API.add_deadline(name, description, deadline_input, min_days_required):
            self.console.print("\nCollected Deadline Information.", style="green")
        else:
            self.console.print("\nFailed to add the deadline.", style="red")

        if API.commit()[0] == 200:
            self.console.print("Deadline Information Saved.", style="yellow")
        else:
            self.console.print("\nFailed to save the deadline information.", style="red")

    def renderer(self):
        while True:
            try:
                hours = float(Prompt.ask("How many hours do we have, sir?"))
                hours = round(hours)
                break
            except ValueError:
                self.console.print(f"Input is not a valid number", style="red")

        if hours > 4:
            self.console.print("We have more than 4 hours, Sir. Let's plan for 4 hours first and then we will plan for the remaining hours.", style="deep_pink2")

        with open("./Dataset.json", "r") as file:
            self.data = json.load(file)

        if self.data['0']:
            have_deadlines_coming = False
            for task in self.data['0']:
                for key, value in task.items():
                    if (datetime.strptime(value['date'], "%Y-%m-%d").date() - datetime.now().date()).days <= value['required_days']:
                        have_deadlines_coming = True
                        break

            if have_deadlines_coming:
                self.console.print("\nWe have past deadlines with us, Sir.", style="blue")

                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Title")
                table.add_column("Description")
                table.add_column("Deadline", style="dim", width=12)
                table.add_column("Remaining Days")

                for task in self.data['0']:
                    for key, value in task.items():
                        if (datetime.strptime(value['date'], "%Y-%m-%d").date() - datetime.now().date()).days <= value['required_days']:
                            table.add_row(
                                str(key), 
                                str(value['description']), 
                                str(value['date']),
                                str((datetime.strptime(value['date'], "%Y-%m-%d").date() - datetime.now().date()).days)
                            )

                self.console.print(table)

                if Prompt.ask("[deep_pink2]Please complete these deadlines first. [!!Press X to overwrite this warning / Press anything to acknowledge this warning!!][/deep_pink2]").lower() != 'x':
                    self.console.print("Exiting the app...", style="deep_pink2")
                    return

            self.console.print("\nWe have some deadlines with us, Sir.", style="magenta")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Title")
            table.add_column("Description")
            table.add_column("Deadline", style="dim", width=12)
            table.add_column("Remaining Days")

            for task in self.data['0']:
                for key, value in task.items():
                    table.add_row(
                        str(key), 
                        str(value['description']), 
                        str(value['date']),
                        str((datetime.strptime(value['date'], "%Y-%m-%d").date() - datetime.now().date()).days)
                    )

            self.console.print(table)

            end = Prompt.ask("Do we wish to go with one of these deadlines, Sir? [Y/n]")

            if end.lower() == "y":
                self.console.print("Exiting the app...", style="deep_pink2")
                return
            elif end.lower() != "n":
                self.console.print("Invalid input. Exiting the app...", style="red")
                return

        self._show_tasks_for_hours(hours)

    def _show_tasks_for_hours(self, hours):
        if hours == 1:
            data = self.data["1"]
            if self._show_tasks(data): return
        elif hours == 2:
            data = self.data["2"]
            if self._show_tasks(data): return
        elif hours >= 3:
            data = self.data["3+"]
            if self._show_tasks(data): return

    def _show_tasks(self, data):
        x = 0
        options = []

        while len(data) - x > 5:
            for i in data[x:x+5]:
                for key, value in i.items():
                    options.append({"name": str(key) + ': ' + str(value), "value": key})  # Set both name and value to key

            options.append({"name": "No: I would like to see the next 5 tasks.", "value": "No"})

            questions = [
                {
                    "type": "list",
                    "message": "Do you like any of these tasks, Sir?",
                    "name": "selected_task",
                    "choices": options
                }
            ]

            answers = prompt(questions)
            selected_task = answers["selected_task"]

            if selected_task == "No":
                x += 5
                continue
            else:
                self.console.print(f"\nTask selected: {selected_task}", style="green")
                self.console.print("\nExiting the app...", style="deep_pink2")
                return True

        for i in data[x:]:
            for key, value in i.items():
                options.append({"name": str(key) + ': ' + str(value), "value": key})  # Set both name and value to key

        options.append({"name": "No: I would much rather chill.", "value": "No"})

        questions = [
            {
                "type": "list",
                "message": "Do you like any of these tasks, Sir?",
                "name": "selected_task",
                "choices": options
            }
        ]

        answers = prompt(questions)
        selected_task = answers["selected_task"]

        if selected_task == "No":
            self.console.print("Exiting the app...", style="deep_pink2")
            return True
        else:
            self.console.print(f"\nTask selected: {selected_task}", style="green")
            self.console.print("\nExiting the app...", style="deep_pink2")
            return True

    def dev(self):
        self.console.print("Welcome to Developer Mode, Sir.", style="bold yellow")

        options = [
            {"name": "Add a new task", "value": "add_task"},
            {"name": "Delete a task", "value": "delete_task"},
            {"name": "Format the dataset", "value": "format_dataset"},
            {"name": "Exit", "value": "exit"}
        ]

        questions = [
            {
                "type": "list",
                "message": "Select an option",
                "name": "selected_option",
                "choices": options
            }
        ]

        answers = prompt(questions)
        selected_option = answers["selected_option"]

        if selected_option == "add_task":
            self.console.print("Adding a new task...", style="green")
            
            API = Append_API()

            options = [
                {"name": "1 hour task", "value": "1"},
                {"name": "2 hour task", "value": "2"},
                {"name": "3+ hour task", "value": "3+"}
            ]

            questions = [
                {
                    "type": "list",
                    "message": "Select the type of task",
                    "name": "selected_type",
                    "choices": options
                }

            ]

            answers = prompt(questions)
            selected_type = answers["selected_type"]

            name = Prompt.ask("Enter the name of the task")
            description = Prompt.ask("Enter a description for the task")

            if selected_type == "1":
                if API.add_1Hour_task(name, description):
                    self.console.print("Task added successfully.", style="green")
                else:
                    self.console.print("Failed to add the task.", style="red")

            elif selected_type == "2":
                if API.add_2Hour_task(name, description):
                    self.console.print("Task added successfully.", style="green")
                else:
                    self.console.print("Failed to add the task.", style="red")

            elif selected_type == "3+":
                if API.add_3Hour_task(name, description):
                    self.console.print("Task added successfully.", style="green")
                else:
                    self.console.print("Failed to add the task.", style="red")

            if API.commit()[0] == 200:
                self.console.print("Task Information Saved.", style="yellow")
            else:
                self.console.print("Failed to save the task information.", style="red")

        elif selected_option == "delete_task":
            self.console.print("Deleting a task...", style="red")

            API = Delete_API()

            options = [
                {"name": "1 hour task", "value": "1"},
                {"name": "2 hour task", "value": "2"},
                {"name": "3+ hour task", "value": "3+"},
                {"name": "Deadlines", "value": "0"}
            ]

            questions = [
                {
                    "type": "list",
                    "message": "Select the type of task",
                    "name": "selected_type",
                    "choices": options
                }

            ]

            answers = prompt(questions)
            selected_type = answers["selected_type"]

            data = API.data

            if selected_type == '1':
                options = []
                for i in data['1']:
                    for key, value in i.items(): 
                        options.append({'name': key, 'value': key})

                questions = [
                    {
                        "type": "list",
                        "message": "Select the task to delete",
                        "name": "selected_task",
                        "choices": options
                    }
                ]

                answers = prompt(questions)
                selected_task = answers["selected_task"]

                if API.delete_1Hour_task(selected_task):
                    self.console.print("Task deleted successfully.", style="green")
                else:
                    self.console.print("Failed to delete the task.", style="red")

                if API.commit()[0] == 200:
                    self.console.print("Task Information Saved.", style="yellow")
                else:
                    self.console.print("Failed to save the task information.", style="red")

            elif selected_type == '2':
                options = []
                for i in data['2']:
                    for key, value in i.items(): 
                        options.append({'name': key, 'value': key})

                questions = [
                    {
                        "type": "list",
                        "message": "Select the task to delete",
                        "name": "selected_task",
                        "choices": options
                    }
                ]

                answers = prompt(questions)
                selected_task = answers["selected_task"]

                if API.delete_2Hour_task(selected_task):
                    self.console.print("Task deleted successfully.", style="green")
                else:
                    self.console.print("Failed to delete the task.", style="red")

                if API.commit()[0] == 200:
                    self.console.print("Task Information Saved.", style="yellow")
                else:
                    self.console.print("Failed to save the task information.", style="red")

            elif selected_type == '3+':
                options = []
                for i in data['3+']:
                    for key, value in i.items(): 
                        options.append({'name': key, 'value': key})

                questions = [
                    {
                        "type": "list",
                        "message": "Select the task to delete",
                        "name": "selected_task",
                        "choices": options
                    }
                ]

                answers = prompt(questions)
                selected_task = answers["selected_task"]

                if API.delete_3Hour_task(selected_task):
                    self.console.print("Task deleted successfully.", style="green")
                else:
                    self.console.print("Failed to delete the task.", style="red")

                if API.commit()[0] == 200:
                    self.console.print("Task Information Saved.", style="yellow")
                else:
                    self.console.print("Failed to save the task information.", style="red")

            elif selected_type == '0':
                options = []
                for i in data['0']:
                    for key, value in i.items(): 
                        options.append({'name': key, 'value': key})

                questions = [
                    {
                        "type": "list",
                        "message": "Select the deadline to delete",
                        "name": "selected_task",
                        "choices": options
                    }
                ]

                answers = prompt(questions)
                selected_task = answers["selected_task"]

                if API.delete_deadline(selected_task):
                    self.console.print("Deadline deleted successfully.", style="green")
                else:
                    self.console.print("Failed to delete the deadline.", style="red")

                if API.commit()[0] == 200:
                    self.console.print("Deadline Information Saved.", style="yellow")
                else:
                    self.console.print("Failed to save the deadline information.", style="red")

        elif selected_option == "format_dataset":
            self.console.print("Formatting the dataset...", style="bold yellow")

            API = Format_API()

            while True:

                options = [
                    {"name": "1 hour task", "value": "1"},
                    {"name": "2 hour task", "value": "2"},
                    {"name": "3+ hour task", "value": "3+"}, 
                    {"name": "Commit", "value": "0"}
                ]

                questions = [
                    {
                        "type": "list",
                        "message": "Select the type of task",
                        "name": "selected_type",
                        "choices": options
                    }
                ]

                answers = prompt(questions)
                selected_type = answers["selected_type"]

                if selected_type == "0":
                    break

                name = Prompt.ask("Enter the name of the task")
                description = Prompt.ask("Enter a description for the task")

                if selected_type == "1":
                    if API.add_1Hour_task(name, description):
                        self.console.print("Task added successfully.", style="green")
                    else:
                        self.console.print("Failed to add the task.", style="red")

                elif selected_type == "2":
                    if API.add_2Hour_task(name, description):
                        self.console.print("Task added successfully.", style="green")
                    else:
                        self.console.print("Failed to add the task.", style="red")

                elif selected_type == "3+":
                    if API.add_3Hour_task(name, description):
                        self.console.print("Task added successfully.", style="green")
                    else:
                        self.console.print("Failed to add the task.", style="red")


            if API.commit()[0] == 200:
                    self.console.print("Task Information Saved.", style="yellow")
            else:
                    self.console.print("Failed to save the task information.", style="red")


if __name__ == "__main__":
    # Initialize the app
    app = App()

    # Run the main function
    try: app.main()

    except KeyboardInterrupt:
        app.console.print("Exiting the app...", style="deep_pink2")
        exit(0)