import buttons as b
from datetime import date, datetime
import tkinter as tk
import tkinter.messagebox as messagebox

# Create the GUI window
window = tk.Tk()
window.title("Task Manager")
dot_counter = 0  # Counter for numbering tasks
tasks_full_list = {}  # Dictionary for all tasks

def add_task():
    global dot_counter

    task_name = entry_name.get()
    task_time = entry_time.get()
    task_deadline = entry_deadline.get()
    task_importance = entry_importance.get()

    try:
        datetime.strptime(task_deadline, "%m-%d")
        task_time = int(task_time)
        task_importance = int(task_importance)
    except:
        messagebox.showerror(message="Input parameters in required formats. Time to finish: 0~20 hr (integers). Deadline:"
                                       "MM-DD, eg,7-1. Importance: non-important 0 to 10 most-important (integers). Thanks! ")

    task_time = int(task_time)
    task_importance = int(task_importance)

    if not task_time in range(0,20):
        messagebox.showerror(message="Do a task with reasonable hours")
        return
    if not task_importance in range(1,11):
        messagebox.showerror(message="How important you would tell for it from 1 to 10?")
        return

    task_time = int(task_time)
    task_importance = int(task_importance)
    # Calculate the number of days before the deadline
    deadline = datetime.strptime(task_deadline, "%m-%d").date()
    deadline_date = f"{date.today().year}-{deadline.month}-{deadline.day}"
    deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d").date()
    today = date.today()
    if deadline_date <= today:
        messagebox.showerror("", "Oh, no!! You already missed the due! Please enter a future task to do!")
        return
    days_before_deadline = (deadline_date - today).days

    if days_before_deadline > 5:
        listbox_no.insert(tk.END, task_name)

    else:
        # Create a new task dictionary
        task = {
            'Name': task_name,
            'Time': task_time,
            'Deadline': task_deadline,
            'Importance': task_importance,
            'DaysBeforeDeadline': days_before_deadline,
            'Coordinate': None  # Placeholder for coordinate
        }

        # Assign coordinates based on days before deadline and importance
        # x_coord = 2.5 - days_before_deadline
        # y_coord = 5 - (int(task_importance) / 2)
        # coordinate = (x_coord,y_coord)
        coordinate = (days_before_deadline,int(task_importance))
        task['Coordinate'] = coordinate
        # print(task['Coordinate'])
        # print(tasks)
        # Store task in the dictionary with numbered dot
        tasks_full_list[dot_counter] = task
        listbox_tasks.insert(tk.END, task_name)
        dot_counter += 1
        # Clear the input fields
    entry_name.delete(0, tk.END)
    entry_time.delete(0, tk.END)
    entry_deadline.delete(0, tk.END)
    entry_importance.delete(0, tk.END)

def delete_task():
    selected_task_index_now = listbox_tasks.curselection()
    selected_task_index_future = listbox_no.curselection()
    if selected_task_index_now:
        listbox_tasks.delete(selected_task_index_now)
    if selected_task_index_future:
        listbox_no.delete(selected_task_index_future)

label_name = tk.Label(window, text="Task:")
label_name.grid(row=0, column=0, sticky=tk.W)
entry_name = tk.Entry(window)
entry_name.grid(row=0, column=1)

label_time = tk.Label(window, text="Time to finish (hr):")
label_time.grid(row=1, column=0, sticky=tk.W)
entry_time = tk.Entry(window)
entry_time.grid(row=1, column=1)

label_deadline = tk.Label(window, text="Deadline (MM-DD):")
label_deadline.grid(row=2, column=0, sticky=tk.W)
entry_deadline = tk.Entry(window)
entry_deadline.grid(row=2, column=1)

label_importance = tk.Label(window, text="Importance (1 to 10):")
label_importance.grid(row=3, column=0, sticky=tk.W)
entry_importance = tk.Entry(window)
entry_importance.grid(row=3, column=1)

#  Task listboxes: to do in the next week, later
label_list = tk.Label(window, text="Tasks to do this week:")
label_list.grid(row=5, column=0, sticky=tk.W)
listbox_tasks = tk.Listbox(window)
listbox_tasks.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='EW')

label_list_no = tk.Label(window, text="Not allocated:")
label_list_no.grid(row=13, column=0, sticky=tk.W)
listbox_no = tk.Listbox(window)
listbox_no.grid(row=14, column=0, columnspan=4, padx=10, pady=10, sticky='EW')
listbox_no.insert(tk.END, 'To do in the future:')

button_add = tk.Button(window, text="Add a task", command=add_task)
button_add.grid(row=15, column=0, padx=10, pady=5)

# Create the Delete Task button
button_delete = tk.Button(window, text="Delete a task", command=delete_task)
button_delete.grid(row=15, column=1, padx=10, pady=5)

button_draw = tk.Button(window, text="Draw an Urgent&Important matrix quadrant",
                        command=lambda: b.draw_coordinate(tasks_full_list, window))
button_draw.grid(row=16, column=0, padx=10, pady=5)

button_arrange = tk.Button(window, text='Arrange them!',
                           command=lambda: b.arrange_tasks(b.sort_tasks(tasks_full_list), listbox_no))
button_arrange.grid(row=16, column=1, padx=10, pady=5)
# Start the GUI event loop
window.mainloop()














