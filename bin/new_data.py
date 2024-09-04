'''
@Author: Prabhas Kumar
@Assistant: GitHub Copilot, ChatGPT 4o

@Created: September 3'24
@Updated: None

@Project: Personal Time-Table Version 1
@File: dataset API & dev app (new_data) [Python 3(.12) script]
'''

import json
from datetime import datetime

# Initialize an empty dictionary to store the data
data = {
    "0": [],
    "1": [],
    "2": [],
    "3+": []
}

dataset = "./Dataset.json"

class Format_API:
    def __init__(self) -> None:
        self.data = data

    def add_1Hour_task(self, task_name, task_description) -> bool:
        try:
            self.data["1"].append({task_name: task_description})
            return True
        except:
            print(task_name, task_description, sep="\n\n")
            return False
        
    def add_2Hour_task(self, task_name, task_description) -> bool:
        try:
            self.data["2"].append({task_name: task_description})
            return True
        except:
            print(task_name, task_description, sep="\n\n")
            return False
        
    def add_3Hour_task(self, task_name, task_description) -> bool:
        try:
            self.data["3+"].append({task_name: task_description})
            return True
        except:
            print(task_name, task_description, sep="\n\n")
            return False
        
    def add_deadline(self, task_name, task_description, deadline_date, required_days) -> bool:

        if isinstance(required_days, float):
            # Convert the float to integer using banker's algorithm
            required_days = round(required_days)

        if not isinstance(required_days, int):
            print(f"required_days is not integer: {required_days}")
            return False
        
        # Convert the date string to a datetime object
        try: 
            deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d")
        except ValueError:
            print(f"Invalid date format. Please use YYYY-MM-DD format. {deadline_date}")
            return False

        try:
            self.data['0'].append({task_name: {
                "description": task_description,
                "date": deadline_date.strftime("%Y-%m-%d"),
                "required_days": required_days
            }})
            return True
        except:
            print(task_name, task_description, deadline_date, required_days, sep="\n\n")
            return False
        
    def commit(self) -> list:
        try:
            # Save the data to dataset.json
            with open(dataset, "w") as file:
                json.dump(self.data, file, indent=4)

            return [200]
        
        except Exception as e:
            return [500, e]


class Append_API:

    def __init__(self) -> None:
        
        data = json.load(open(dataset, "r"))

        self.data = data


    def add_1Hour_task(self, task_name, task_description) -> bool:
        try:
            self.data["1"].append({task_name: task_description})
            return True
        except:
            print(task_name, task_description, sep="\n\n")
            return False
        
    def add_2Hour_task(self, task_name, task_description) -> bool:
        try:
            self.data["2"].append({task_name: task_description})
            return True
        except:
            print(task_name, task_description, sep="\n\n")
            return False
        
    def add_3Hour_task(self, task_name, task_description) -> bool:
        try:
            self.data["3+"].append({task_name: task_description})
            return True
        except:
            print(task_name, task_description, sep="\n\n")
            return False
        
    def add_deadline(self, task_name, task_description, deadline_date, required_days) -> bool:

        if isinstance(required_days, float):
            # Convert the float to integer using banker's algorithm
            required_days = round(required_days)

        if not isinstance(required_days, int):
            print(f"required_days is not integer: {required_days}")
            return False
        
        # Convert the date string to a datetime object
        try: 
            deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d")
        except ValueError:
            print(f"Invalid date format. Please use YYYY-MM-DD format. {deadline_date}")
            return False

        try:
            self.data['0'].append({task_name: {
                "description": task_description,
                "date": deadline_date.strftime("%Y-%m-%d"),
                "required_days": required_days
            }})
            return True
        except:
            print(task_name, task_description, deadline_date, required_days, sep="\n\n")
            return False
        
    def commit(self) -> list:
        try:
            # Save the data to dataset.json
            with open(dataset, "w") as file:
                json.dump(self.data, file, indent=4)

            return [200]
        
        except Exception as e:
            return [500, e]


class Delete_API:

    def __init__(self) -> None:
        
        data = json.load(open(dataset, "r"))

        self.data = data


    def delete_1Hour_task(self, task_name) -> bool:
        try:
            for task in self.data["1"]:
                if task_name in task:
                    self.data["1"].remove(task)
                    return True
            return False
        except:
            return False
        
    def delete_2Hour_task(self, task_name) -> bool:
        try:
            for task in self.data["2"]:
                if task_name in task:
                    self.data["2"].remove(task)
                    return True
            return False
        except:
            return False
        
    def delete_3Hour_task(self, task_name) -> bool:
        try:
            for task in self.data["3+"]:
                if task_name in task:
                    self.data["3+"].remove(task)
                    return True
            return False
        except:
            return False
        
    def delete_deadline(self, task_name) -> bool:
        if task_name.lower().strip().startswith("exam"):
            print("Forbbiden!")
            return False
        try:
            for task in self.data["0"]:
                if task_name in task:
                    self.data["0"].remove(task)
                    return True
            return False
        except:
            return False
        
    def commit(self) -> list:
        try:
            # Save the data to dataset.json
            with open(dataset, "w") as file:
                json.dump(self.data, file, indent=4)

            return [200]
        
        except Exception as e:
            return [500, e]        




if __name__ == "__main__":

    # Function to get user input for each list 
    def get_task_input(list_name) -> None:
        while True:
            task_name = input(f"Enter task name for {list_name} (or type 'done' to finish): ")
            if task_name.lower() == 'done':
                break
            task_description = input(f"Enter description for {task_name}: ")
            data[list_name].append({task_name: task_description})

    def get_deadline_input() -> None:
        while True:
            deadline = input("Enter the deadline for the task (or type 'done' to finish): ")
            if deadline.lower() == 'done':
                break
            deadline_description = input(f"Enter description for {deadline}: ")

            deadline_deadline = input(f"Enter the date for {deadline} (YYYY-MM-DD): ")

            # Convert the date string to a datetime object
            try: 
                deadline_date = datetime.strptime(deadline_deadline, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format. Removing this entry.")
                continue

            deadline_required = int(input(f"How many minimum days {deadline} is required to be completed? "))
            
            data['0'].append({deadline: {
                "description": deadline_description,
                "date": deadline_date.strftime("%Y-%m-%d"),
                "required_days": deadline_required
            }})

    # Loop through each list and get user input
    for list_name in data.keys():
        print(f"\nEntering tasks for {list_name}:")

        if list_name == '0':
            get_deadline_input()

        else:
            get_task_input(list_name)

    # Save the data to dataset.json
    with open('../' + dataset, "w") as file:
        json.dump(data, file, indent=4)

    print("Data saved to dataset.json")