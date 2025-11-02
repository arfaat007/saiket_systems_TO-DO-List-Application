import os

class Task:
    """Class to represent a task with description and completion status"""
    def __init__(self, description):
        self.description = description
        self.completed = False
    
    def mark_completed(self):
        """Mark the task as completed"""
        self.completed = True
    
    def mark_active(self):
        """Mark the task as active (not completed)"""
        self.completed = False
    
    def __str__(self):
        """String representation of the task"""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.description}"

class TodoList:
    """Class to manage a collection of tasks"""
    def __init__(self):
        self.tasks = []
    
    def add_task(self, description):
        """Add a new task to the list"""
        task = Task(description)
        self.tasks.append(task)
        print(f"✅ Added task: {description}")
    
    def list_tasks(self):
        """Display all tasks with their indices"""
        if not self.tasks:
            print("📭 No tasks in the list.")
            return
        
        print("\n📝 Your To-Do List:")
        print("━" * 50)
        for i, task in enumerate(self.tasks):
            # Add visual distinction for completed tasks
            if task.completed:
                print(f"  {i + 1}. \033[9m{task}\033[0m")  # Strikethrough for completed
            else:
                print(f"  {i + 1}. {task}")
        print("━" * 50)
    
    def mark_completed(self, task_index):
        """Mark a task as completed"""
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_completed()
            print(f"✅ Marked task '{self.tasks[task_index].description}' as completed.")
        else:
            print("❌ Invalid task number.")
    
    def mark_active(self, task_index):
        """Mark a task as active"""
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_active()
            print(f"🔄 Marked task '{self.tasks[task_index].description}' as active.")
        else:
            print("❌ Invalid task number.")
    
    def delete_task(self, task_index):
        """Delete a task from the list"""
        if 0 <= task_index < len(self.tasks):
            deleted_task = self.tasks.pop(task_index)
            print(f"🗑️  Deleted task: {deleted_task.description}")
        else:
            print("❌ Invalid task number.")
    
    def show_stats(self):
        """Show statistics about tasks"""
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task.completed])
        active = total - completed
        
        print(f"\n📊 Task Statistics:")
        print("━" * 30)
        print(f"📈 Total tasks: {total}")
        print(f"✅ Completed: {completed}")
        print(f"📝 Active: {active}")
        print("━" * 30)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print a nicely formatted header"""
    print("\033[1;34;40m" + "╔" + "═" * 48 + "╗\033[0m")
    print("\033[1;34;40m" + "║" + " " * 15 + "TO-DO LIST APP" + " " * 15 + "║\033[0m")
    print("\033[1;34;40m" + "╚" + "═" * 48 + "╝\033[0m")

def print_menu():
    """Print the main menu with better formatting"""
    print("\n📋 \033[1mMAIN MENU\033[0m")
    print("━" * 30)
    print("  1️⃣  ➤ Add a new task")
    print("  2️⃣  ➤ List all tasks")
    print("  3️⃣  ➤ Mark task as completed")
    print("  4️⃣  ➤ Mark task as active")
    print("  5️⃣  ➤ Delete a task")
    print("  6️⃣  ➤ Show task statistics")
    print("  7️⃣  ➤ Exit")
    print("━" * 30)

def main():
    """Main function to run the to-do list application"""
    todo = TodoList()
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\n👉 Enter your choice (1-7): ").strip()
        
        # Using conditional statements to handle user choices
        if choice == "1":
            description = input("📝 Enter task description: ").strip()
            if description:
                todo.add_task(description)
            else:
                print("❌ Task description cannot be empty.")
            input("\nPress Enter to continue...")
                
        elif choice == "2":
            todo.list_tasks()
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            todo.list_tasks()
            if todo.tasks:
                try:
                    task_num = int(input("✅ Enter task number to mark as completed: ")) - 1
                    todo.mark_completed(task_num)
                except ValueError:
                    print("❌ Please enter a valid number.")
            input("\nPress Enter to continue...")
                    
        elif choice == "4":
            todo.list_tasks()
            if todo.tasks:
                try:
                    task_num = int(input("🔄 Enter task number to mark as active: ")) - 1
                    todo.mark_active(task_num)
                except ValueError:
                    print("❌ Please enter a valid number.")
            input("\nPress Enter to continue...")
                    
        elif choice == "5":
            todo.list_tasks()
            if todo.tasks:
                try:
                    task_num = int(input("🗑️  Enter task number to delete: ")) - 1
                    todo.delete_task(task_num)
                except ValueError:
                    print("❌ Please enter a valid number.")
            input("\nPress Enter to continue...")
                    
        elif choice == "6":
            todo.show_stats()
            input("\nPress Enter to continue...")
            
        elif choice == "7":
            clear_screen()
            print("\033[1;32m" + "👋 Thank you for using the To-Do List Application!" + "\033[0m")
            print("\033[3m" + "   Have a productive day!" + "\033[0m")
            break
            
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 7.")
            input("\nPress Enter to continue...")

# Run the application
if __name__ == "__main__":
    main()