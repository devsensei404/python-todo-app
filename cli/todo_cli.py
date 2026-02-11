import json

FILENAME = "tasks.json"


def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            tasks = json.load(file)

            task_id = 0
            if tasks:
                for task in tasks:
                    task_id = max(task["id"], task_id)

            task_id += 1
            return tasks, task_id
    except:
        return [], 1


def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file)


def add_task(tasks, task_id):
    title = input("Enter task title: ")

    task = {
        "id": task_id,
        "title": title,
        "done": False
    }

    tasks.append(task)
    print("Task added!\n")

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

        print(f"[{task['id']}] {task['title']} - {status}")

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


def menu():
    print("==== SIMPLE TODO APP ====")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Mark Task as Completed")
    print("6. Delete Task")
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
            delete_task(tasks)
        elif choice == "0":
            save_tasks(tasks)
            print("Exiting Todo App")
            break
        else:
            print("Invalid choice.\n")


main()
