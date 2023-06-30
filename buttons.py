from datetime import date, datetime, timedelta
import tkinter as tk
import tkinter.messagebox as messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from adjustText import adjust_text


# def validate_date_format(date_str):
#     try:
#         datetime.strptime(date_str, "%m-%d")
#         return True
#     except ValueError:
#         return False


def draw_coordinate(tasks, window):
    window_figure = tk.Toplevel(window)
    window_figure.title("Urgent&Important Matrix")
    listbox_tasks = tk.Listbox(window_figure)
    listbox_tasks.grid(row=0, column=5, columnspan=4, padx=10, pady=10, sticky='NS')
    x = []
    y = []
    task_ids = []
    texts = []

    for task_id, task in tasks.items():
        coordinate = task['Coordinate']
        x.append(coordinate[0])
        y.append(coordinate[1])
        task_ids.append(task_id)

    # Define the x and y coordinates
    x_ticks = [5, 4, 3, 2, 1, 0]
    y_ticks = list(range(1, 11))

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.tick_params(axis='both', labelsize=6, colors='grey')

    ax.set_xlim([max(x_ticks) + 1.5, min(x_ticks) - 1.5])
    ax.set_ylim([min(y_ticks) - 1.5, max(y_ticks) + 1.5])
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)

    ax.spines['left'].set_position(('data', 2.5))
    ax.spines['bottom'].set_position(('data', 5.5))
    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(3)
        ax.spines[axis].set_color("grey")

    plt.scatter(x, y, s=200, c='gold')

    # Add labels to points
    for i, txt in enumerate(task_ids):
        texts.append(plt.annotate(int(txt) + 1, (x[i], y[i]), color='black', xytext=(x[i] + .05, y[i] - .25)))
        info = str(int(txt) + 1) + ' ' + tasks[i]['Name']
        listbox_tasks.insert(tk.END, info)
    group_mark_x = [0, 0, 6, 6]
    group_mark_y = [10, 1, 10, 1]
    for i in range(4):
        plt.annotate(str('Group' + str(i + 1)), (group_mark_x[i], group_mark_y[i]), color='grey',
                     fontsize=15).set_alpha(.4)

    texts.append(plt.xlabel('Urgency', loc='right'))
    texts.append(plt.ylabel('Importance', loc='top'))

    adjust_text(texts)
    plt.title("Urgent&Important Matrix")

    # Show the plot in the pop-up window
    canvas = FigureCanvasTkAgg(fig, master=window_figure)
    canvas.get_tk_widget().grid(row=0, column=0)


def sort_tasks(tasks_full_list):
    # Iterate over the tasks and categorize them into groups
    for task_id, task in tasks_full_list.items():
        days_before_deadline = task['DaysBeforeDeadline']
        importance = task['Importance']

        if days_before_deadline < 3 and importance > 5:
            tasks_full_list[task_id]['Group'] = 1
        elif days_before_deadline >= 3 and importance <= 5:
            tasks_full_list[task_id]['Group'] = 2
        elif days_before_deadline >= 3 and importance > 5:
            tasks_full_list[task_id]['Group'] = 3
        else:
            tasks_full_list[task_id]['Group'] = 4
            tasks_full_list[task_id]['Name'] += '*'

    # Sort tasks from all groups based on urgency and importance
    sorted_tasks = sorted(tasks_full_list.values(),
                          key=lambda x: (x['Group'], x['DaysBeforeDeadline'], -x['Importance']))
    return sorted_tasks


def arrange_tasks(sorted_tasks, listbox_no):
    num_working_days = 5
    hours_per_day = 8

    task_allocation = {}
    work_schedule = [[] for i in range(num_working_days)]
    cannot_do = []

    for task in sorted_tasks:
        task_name = task['Name']
        task_time = task['Time']
        arranged = False

        starting_day = 0 if task['Group'] == 1 else 2

        for day in range(starting_day, num_working_days):
            # Calculate the remaining available work hours for the current day
            remaining_hours = hours_per_day - sum([t['Time'] for t in work_schedule[day]])
            # If the task can be completed within the remaining hours, allocate it to the current day
            if task_time <= remaining_hours:
                work_schedule[day].append({'Name': task_name, 'Time': task_time})
                task_allocation[task_name] = day + 1
                arranged = True
                break

        if not arranged:
            for day in range(starting_day, num_working_days):
                if task_time > 0:
                    # Calculate the remaining available work hours for the current day
                    remaining_hours = hours_per_day - sum([t['Time'] for t in work_schedule[day]])

                    # If there are remaining hours, deduct the task time from the next day
                    if remaining_hours > 0:
                        if remaining_hours >= task_time:
                            work_schedule[day].append({'Name': task_name, 'Time': task_time})
                            task_allocation[task_name] = day + 1
                        else:
                            work_schedule[day].append({'Name': task_name, 'Time': remaining_hours})
                            task_allocation[task_name] = day + 1

                        task_time -= remaining_hours
        if not arranged:
            cannot_do.append(task_name)

    if cannot_do:
        listbox_no.insert(tk.END, 'Tasks cannot be arranged in this week:')
        for item in cannot_do:
            listbox_no.insert(tk.END, item)
    return output_todo_list(work_schedule)


def output_todo_list(work_schedule):
    output = 'To do list for next week.txt'
    print(work_schedule)
    with open(output, 'w') as out:
        for day, tasks in enumerate(work_schedule):
            out.write(f"Day {day + 1}:\n")
            i = 1
            for x in tasks:
                out.write(f"{i}. {x['Name']}, Time: {x['Time']} hours \n")
                i += 1
            out.write(f"----------------------------------------------\n")
        out.write("For the task with '*', you are recommended not to do it, since it is neither important or urgent.")

