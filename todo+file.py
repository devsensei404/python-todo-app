import json

FILENAME = "tasks.json"


def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            tasks = json.load(file)
            task_id = 0
            if tasks:
                for task in tasks:
                    task_id = max(task["id"],task_id )
            task_id+=1
            return tasks, task_id
    except:
        return [], 1


def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file)


def add_task(tasks, task_id):
    title = input("Task title: ")

    print("Priority: 1.Low  2.Medium  3.High")
    p = input("Choose priority: ")

    if p == "1":
        priority = "Low"
    elif p == "2":
        priority = "Medium"
    else:
        priority = "High"

    print("Category: 1.Study  2.Personal  3.Health  4.Other")
    c = input("Choose category: ")

    if c == "1":
        category = "Study"
    elif c == "2":
        category = "Personal"
    elif c == "3":
        category = "Health"
    else:
        category = "Other"

    task = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "category": category,
        "done": False
    }

    tasks.append(task)
    print("Task added successfully!\n")
    return task_id + 1


def show_tasks(tasks, filter_type="all"):
    if not tasks:
        print("No tasks available.\n")
        return

    print("\n--- TASK LIST ---")
    for task in tasks:
        if filter_type == "pending" and task["done"]:
            continue
        if filter_type == "completed" and not task["done"]:
            continue

        if task["done"]:
            status = "Completed"
        else:
            status = "Incomplete"

        print(f"[{task['id']}] {task['title']} | {task['priority']} | {task['category']} | {status}")
    print()


def mark_done(tasks):
    show_tasks(tasks, "pending")
    try:
        tid = int(input("Enter task ID to mark completed: "))
        for task in tasks:
            if task["id"] == tid:
                task["done"] = True
                print("Task marked as completed!\n")
                return
        print("Task ID not found.\n")
    except:
        print("Invalid input.\n")


def delete_task(tasks):
    show_tasks(tasks)
    try:
        tid = int(input("Enter task ID to delete: "))
        for task in tasks:
            if task["id"] == tid:
                tasks.remove(task)
                print("Task deleted!\n")
                return
        print("Task ID not found.\n")
    except:
        print("Invalid input.\n")


def edit_task(tasks):
    show_tasks(tasks)
    try:
        tid = int(input("Enter task ID to edit: "))
        for task in tasks:
            if task["id"] == tid:
                new_title = input("New title (leave blank to keep same): ")
                if new_title != "":
                    task["title"] = new_title
                print("Task updated!\n")
                return
        print("Task ID not found.\n")
    except:
        print("Invalid input.\n")


def search_task(tasks):
    key = input("Enter keyword to search: ").lower()
    print("\n--- SEARCH RESULTS ---")
    for task in tasks:
        if key in task["title"].lower():
            if task["done"]:
                status = "Completed"
            else:
                status = "Incomplete"
            print(f"[{task['id']}] {task['title']} | {status}")
    print()


def stats(tasks):
    total = len(tasks)
    completed = 0

    for t in tasks:
        if t["done"]:
            completed += 1

    pending = total - completed

    print("\n--- STATISTICS ---")
    print("Total tasks :", total)
    print("Completed  :", completed)
    print("Pending    :", pending)
    print()


def menu():
    print("==== SMART TODO APP ====")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Mark Task as Completed")
    print("6. Edit Task")
    print("7. Delete Task")
    print("8. Search Task")
    print("9. Task Statistics")
    print("0. Exit")


def main():
    tasks, task_id = load_tasks()

    while True:
        menu()
        choice = input("Choose option: ")

        if choice == "1":
            task_id = add_task(tasks, task_id)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            show_tasks(tasks, "pending")
        elif choice == "4":
            show_tasks(tasks, "completed")
        elif choice == "5":
            mark_done(tasks)
        elif choice == "6":
            edit_task(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            search_task(tasks)
        elif choice == "9":
            stats(tasks)
        elif choice == "0":
            save_tasks(tasks)
            print("Exiting Todo App")
            break
        else:
            print("Invalid choice.\n")
main()