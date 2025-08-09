import json
import os
import sys

Task_file = "tasks.json"

def load_task():
    if not os.path.exists(Task_file):
        with open (Task_file, 'w') as f:
            json.dump([], f)   #create an empty list in json
    with open (Task_file,'r') as f :
        
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []  # Return empty
        # return json.load(f)
    

def save_task(tasks):
    with open (Task_file, 'w') as f :
        json.dump(tasks,f,indent=4)
def add_task(title):
    tasks = load_task()
    task_id = max([task['id'] for task in tasks], default=0) + 1
    task = {
        'id': task_id,
        'title': title,
        'status': 'Not Done'
    }
    tasks.append(task)
    save_task(tasks)  # ✅ FIXED here
    print(f"Task added: {task}")

def update_task(task_id, new_title):
    tasks=load_task()
    for task in tasks:
        if task['id']==task_id:
            task['title']=new_title
            save_task(tasks)
            print(f"task updated: {task}")
            return
    return("task not found")

def delete_task(task_id):
    tasks=load_task()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_task(tasks)
    print(f"Task {task_id} deleted.")
def change_status(task_id, status):
    tasks = load_task()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            save_task(tasks)
            print(f"Task status updated: {task}")
            return
    print("Task not found.")

def list_tasks(filter_status=None):
    tasks = load_task()
    if filter_status:
        tasks = [task for task in tasks if task['status'] == filter_status]
    if not tasks:
        print("No tasks found.")
    for task in tasks:
        print(f"[{task['id']}] {task['title']} - {task['status']}")
# run from terminal using sys
def print_usage():
    print(
        """
     python task_tracker.py add "Task title"
  python task_tracker.py update <task_id> "New title"
  python task_tracker.py delete <task_id>
  python task_tracker.py mark_done <task_id>
  python task_tracker.py mark_progress <task_id>
  python task_tracker.py list

        """
    )


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    try:
        if command == 'add':
            title = sys.argv[2]
            add_task(title)

        elif command == 'update':
            task_id = int(sys.argv[2])
            new_title = sys.argv[3]
            update_task(task_id, new_title)

        elif command == 'delete':
            task_id = int(sys.argv[2])
            delete_task(task_id)

        elif command == 'mark_done':
            task_id = int(sys.argv[2])
            change_status(task_id, 'done')

        elif command == 'mark_progress':
            task_id = int(sys.argv[2])
            change_status(task_id, 'in progress')

        elif command == 'list':
            if len(sys.argv) == 3:
                status = sys.argv[2]
                status_map = {
                    'done': 'done',
                    'not_done': 'not done',
                    'in_progress': 'in progress'
                }
                if status not in status_map:
                    print("Invalid list filter.")
                    return
                list_tasks(status_map[status])
            else:
                list_tasks()

        else:
            print("Unknown command.")
            print_usage()

    except IndexError:
        print("Missing arguments.")
        print_usage()
    except ValueError:
        print("Invalid task ID. It should be a number.")
        print_usage()
    

if __name__ == "__main__":
    main()