import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class Task:
    """Class to represent a task with description and completion status"""
    def __init__(self, description, completed=False, created_at=None):
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def toggle_completed(self):
        """Toggle the completion status of the task"""
        self.completed = not self.completed
    
    def to_dict(self):
        """Convert task to dictionary for saving"""
        return {
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary"""
        return cls(data["description"], data["completed"], data["created_at"])

class TodoApp:
    """Main To-Do List Application"""
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Data storage
        self.tasks = []
        self.data_file = "tasks.json"
        self.load_tasks()
        
        # Create UI elements
        self.create_widgets()
        
        # Display tasks
        self.refresh_task_list()
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(pady=10, padx=20, fill="x")
        
        title_label = tk.Label(
            header_frame, 
            text="My To-Do List", 
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack()
        
        # Input section
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10, padx=20, fill="x")
        
        self.task_entry = tk.Entry(
            input_frame, 
            font=("Arial", 12),
            width=40
        )
        self.task_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        add_button = tk.Button(
            input_frame,
            text="Add Task",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            command=self.add_task
        )
        add_button.pack(side="right")
        
        # Filter buttons
        filter_frame = tk.Frame(self.root, bg="#f0f0f0")
        filter_frame.pack(pady=5, padx=20, fill="x")
        
        self.all_btn = tk.Button(
            filter_frame,
            text="All",
            font=("Arial", 9),
            bg="#2196F3",
            fg="white",
            command=lambda: self.filter_tasks("all")
        )
        self.all_btn.pack(side="left", padx=(0, 5))
        
        self.active_btn = tk.Button(
            filter_frame,
            text="Active",
            font=("Arial", 9),
            bg="#cccccc",
            command=lambda: self.filter_tasks("active")
        )
        self.active_btn.pack(side="left", padx=(0, 5))
        
        self.completed_btn = tk.Button(
            filter_frame,
            text="Completed",
            font=("Arial", 9),
            bg="#cccccc",
            command=lambda: self.filter_tasks("completed")
        )
        self.completed_btn.pack(side="left")
        
        # Clear completed button
        clear_button = tk.Button(
            filter_frame,
            text="Clear Completed",
            font=("Arial", 9),
            bg="#f44336",
            fg="white",
            command=self.clear_completed
        )
        clear_button.pack(side="right")
        
        # Task list
        list_frame = tk.Frame(self.root, bg="#f0f0f0")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Create canvas and scrollbar for task list
        self.canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Task counter
        self.counter_label = tk.Label(
            self.root,
            text="0 tasks remaining",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666"
        )
        self.counter_label.pack(pady=(0, 20))
        
        # Set current filter
        self.current_filter = "all"
    
    def add_task(self):
        """Add a new task to the list"""
        description = self.task_entry.get().strip()
        if not description:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return
        
        task = Task(description)
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_task_list()
    
    def toggle_task(self, index):
        """Toggle the completion status of a task"""
        self.tasks[index].toggle_completed()
        self.save_tasks()
        self.refresh_task_list()
    
    def delete_task(self, index):
        """Delete a task from the list"""
        del self.tasks[index]
        self.save_tasks()
        self.refresh_task_list()
    
    def filter_tasks(self, filter_type):
        """Filter tasks based on status"""
        self.current_filter = filter_type
        
        # Update button styles
        buttons = {
            "all": self.all_btn,
            "active": self.active_btn,
            "completed": self.completed_btn
        }
        
        for key, btn in buttons.items():
            if key == filter_type:
                btn.configure(bg="#2196F3", fg="white")
            else:
                btn.configure(bg="#cccccc", fg="black")
        
        self.refresh_task_list()
    
    def clear_completed(self):
        """Remove all completed tasks"""
        self.tasks = [task for task in self.tasks if not task.completed]
        self.save_tasks()
        self.refresh_task_list()
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        # Clear existing task widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filter tasks based on current filter
        if self.current_filter == "active":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        elif self.current_filter == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        else:  # all
            filtered_tasks = self.tasks
        
        # Display tasks
        for i, task in enumerate(filtered_tasks):
            # Find the actual index in the main tasks list
            actual_index = self.tasks.index(task)
            
            task_frame = tk.Frame(self.scrollable_frame, bg="white", pady=5)
            task_frame.pack(fill="x", padx=10, pady=2)
            
            # Checkbox
            checkbox = tk.Checkbutton(
                task_frame,
                bg="white",
                command=lambda idx=actual_index: self.toggle_task(idx)
            )
            checkbox.pack(side="left")
            if task.completed:
                checkbox.select()
            
            # Task description
            description_style = {"font": ("Arial", 11), "bg": "white"}
            if task.completed:
                description_style["fg"] = "#888"
                description_style["font"] = ("Arial", 11, "overstrike")
            else:
                description_style["fg"] = "#333"
            
            desc_label = tk.Label(
                task_frame,
                text=task.description,
                **description_style
            )
            desc_label.pack(side="left", padx=(5, 10))
            
            # Delete button
            delete_btn = tk.Button(
                task_frame,
                text="×",
                font=("Arial", 12, "bold"),
                bg="#f44336",
                fg="white",
                width=2,
                command=lambda idx=actual_index: self.delete_task(idx)
            )
            delete_btn.pack(side="right")
            
            # Creation date
            date_label = tk.Label(
                task_frame,
                text=task.created_at.split()[0],  # Just the date part
                font=("Arial", 8),
                bg="white",
                fg="#999"
            )
            date_label.pack(side="right", padx=(0, 10))
        
        # Update task counter
        active_count = len([task for task in self.tasks if not task.completed])
        self.counter_label.config(text=f"{active_count} tasks remaining")
    
    def save_tasks(self):
        """Save tasks to a JSON file"""
        data = [task.to_dict() for task in self.tasks]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from a JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(item) for item in data]
            except Exception as e:
                print(f"Error loading tasks: {e}")
                self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()