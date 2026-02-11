import json
import tkinter as tk
from tkinter import simpledialog, messagebox

FILENAME = "tasks.json"

def load_tasks(username):
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
    except:
        data = {}

    tasks = data.get(username, [])
    task_id = 0
    for task in tasks:
        task_id = max(task_id, task["id"])

    return tasks, task_id + 1

def save_tasks(username, tasks):
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[username] = tasks

    with open(FILENAME, "w") as f:
        json.dump(data, f)


def refresh(tasks, listbox, filter_type="all"):
    listbox.delete(0, tk.END)
    for task in tasks:
        if filter_type == "pending" and task["done"]:
            continue
        if filter_type == "completed" and not task["done"]:
            continue

        status = "Completed" if task["done"] else "Incomplete"
        listbox.insert(tk.END, f"[{task['id']}] {task['title']} {status}")


def main():
    
    root = tk.Tk()
    
    root.withdraw()

    username = simpledialog.askstring("Login", "Enter username:")
    if not username:
        return

    root.deiconify()  # show main window

    tasks, task_id = load_tasks(username)

    root.title(f"Todo App - {username}")
    root.geometry("500x350")

    listbox = tk.Listbox(root, width=60)
    listbox.pack(pady=10)

    def add_task():
        nonlocal task_id
        title = simpledialog.askstring("Add Task", "Task title:")
        if not title:
            return

        tasks.append({
            "id": task_id,
            "title": title,
            "done": False
        })
        task_id += 1
        refresh(tasks, listbox)

    def delete_task():
        if not listbox.curselection():
            messagebox.showwarning("Error", "Select a task")
            return

        tid = int(listbox.get(listbox.curselection()).split("]")[0][1:])
        for task in tasks:
            if task["id"] == tid:
                tasks.remove(task)
                break
        refresh(tasks, listbox)

    def mark_done():
        if not listbox.curselection():
            messagebox.showwarning("Error", "Select a task")
            return

        tid = int(listbox.get(listbox.curselection()).split("]")[0][1:])
        for task in tasks:
            if task["id"] == tid:
                task["done"] = True
                break
        refresh(tasks, listbox)

    btn_frame = tk.Frame(root)
    btn_frame.pack()

    tk.Button(btn_frame, text="Add", command=add_task).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_task).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Mark Done", command=mark_done).grid(row=0, column=2, padx=5)

    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=5)

    tk.Button(filter_frame, text="All",
              command=lambda: refresh(tasks, listbox)).grid(row=0, column=0, padx=5)
    tk.Button(filter_frame, text="Pending",
              command=lambda: refresh(tasks, listbox, "pending")).grid(row=0, column=1, padx=5)
    tk.Button(filter_frame, text="Completed",
              command=lambda: refresh(tasks, listbox, "completed")).grid(row=0, column=2, padx=5)

    def on_exit():
        save_tasks(username, tasks)
        root.destroy()

    tk.Button(root, text="Save & Exit", command=on_exit).pack(pady=10)

    refresh(tasks, listbox)
    root.mainloop()


main()
