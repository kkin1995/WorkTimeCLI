import warnings

warnings.filterwarnings("ignore")
import datetime
import pandas as pd
import os
import numpy as np

tasks_file = "tasks.csv"
historical_tasks_file = "historical_tasks.csv"

while True:
    print("----------------------------------------------------------------")
    print("------------------------Task Logger-----------------------------")
    print("What would you like to do?")
    print("(1) Add a new task")
    print("(2) Enter end time for current task")
    print("(3) Create summary of tasks (pdf)")
    print("(4) Exit")
    print("Enter your choice (1, 2, 3, 4): ", end="")
    choice = int(input())

    if choice == 4:
        print("Exiting...")
        break
    elif choice == 1:
        try:
            df = pd.read_csv(tasks_file, index_col=None)
        except FileNotFoundError:
            df = pd.DataFrame()

        current_tasks = {}

        print("Adding a new task...")
        print("Enter task name: ", end="")
        task_name = input()
        print("Start Time will be set to current time")
        start_time = datetime.datetime.now()

        current_tasks["Task_Name"] = [task_name]
        current_tasks["Start_Time"] = [start_time]
        current_tasks["End_Time"] = [np.nan]

        df = pd.concat([df, pd.DataFrame(current_tasks)], axis=0)
        df.to_csv(tasks_file, index=False)

        print("Task added successfully!")
    elif choice == 2:
        try:
            df = pd.read_csv(tasks_file, index_col=None)
        except FileNotFoundError:
            print("No open tasks found! Use option 1 to add a new task.")
            continue

        print("Current Tasks without end time:")
        current_tasks_without_end_time = df.loc[df.loc[:, "End_Time"].isna(), :]
        print(current_tasks_without_end_time)

        print("Enter index of task to enter end time: ", end="")
        task_id = int(input())

        print("End time will be set to current time")

        df.loc[task_id, "End_Time"] = datetime.datetime.now()
        df.to_csv(tasks_file, index=False)

        print("Task updated successfully!")
        del df

    elif choice == 3:
        df = pd.read_csv(tasks_file, index_col=None)

        df.loc[:, "Start_Time"] = pd.to_datetime(df.loc[:, "Start_Time"])
        df.loc[:, "End_Time"] = pd.to_datetime(df.loc[:, "End_Time"])
        df.loc[:, "Duration"] = df.loc[:, "End_Time"] - df.loc[:, "Start_Time"]

        tasks = list(set(df.loc[:, "Task_Name"].values))
        current_date = datetime.datetime.now().date().strftime("%d_%m_%y")
        seperator = "-" * 100 + "\n"

        print("Creating Summary of Tasks")

        with open(f"summary_tasks_{current_date}.txt", "w") as f:
            from_date = df.loc[:, "Start_Time"].min()
            to_date = df.loc[:, "Start_Time"].max()
            f.write(seperator)
            f.write(
                f"From {from_date.day}/{from_date.month}/{from_date.year} to {to_date.day}/{to_date.month}/{to_date.year}\n"
            )
            f.write(seperator)
            for task in tasks:
                f.write(f"Task: {task}\n")
                f.write(seperator)
                total_time_spent_on_task = (
                    df.loc[df.loc[:, "Task_Name"] == task, "Duration"]
                    .sum()
                    .total_seconds()
                )
                total_time_spent_on_task /= 3600  # Convert to hours
                f.write(
                    f"\tTotal time spent on task: {total_time_spent_on_task} hours\n"
                )
        print("Summary created successfully!")

        if os.path.exists(historical_tasks_file):
            historical_df = pd.read_csv(historical_tasks_file, index_col=None)
            historical_df = pd.concat([historical_df, df], axis=0)
            historical_df.to_csv(historical_tasks_file, index=False)
        else:
            df.to_csv(historical_tasks_file, index=False)

        os.remove(tasks_file)
