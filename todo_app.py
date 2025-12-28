import tkinter as tk
from tkinter import messagebox, font
import json
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ My To-Do List")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Color scheme
        self.bg_gradient_top = "#667eea"
        self.bg_gradient_bottom = "#764ba2"
        self.accent_color = "#f093fb"
        self.text_color = "#ffffff"
        self.task_bg = "#ffffff"
        self.task_text = "#333333"
        
        # Load tasks
        self.tasks = self.load_tasks()
        
        self.setup_ui()
        self.display_tasks()
        
    def setup_ui(self):
        # Main canvas for gradient background
        self.canvas = tk.Canvas(self.root, width=500, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Create gradient background
        self.create_gradient()
        
        # Title
        title_font = font.Font(family="Arial", size=28, weight="bold")
        self.canvas.create_text(250, 50, text="✨ My Tasks", 
                               font=title_font, fill=self.text_color)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.bg_gradient_top)
        input_frame.place(x=30, y=100, width=440, height=50)
        
        # Task entry
        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), 
                                   relief="flat", bg=self.task_bg, 
                                   fg=self.task_text, insertbackground=self.task_text)
        self.task_entry.place(x=10, y=10, width=310, height=30)
        self.task_entry.insert(0, "Enter a new task...")
        self.task_entry.bind("<FocusIn>", self.clear_placeholder)
        self.task_entry.bind("<FocusOut>", self.add_placeholder)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(input_frame, text="➕ Add", font=("Arial", 11, "bold"),
                           bg=self.accent_color, fg=self.text_color, 
                           relief="flat", cursor="hand2", command=self.add_task)
        add_btn.place(x=330, y=10, width=100, height=30)
        
        # Tasks frame with scrollbar
        self.tasks_canvas = tk.Canvas(self.root, bg=self.bg_gradient_bottom, 
                                     highlightthickness=0)
        self.tasks_canvas.place(x=30, y=170, width=440, height=430)
        
        scrollbar = tk.Scrollbar(self.root, orient="vertical", 
                                command=self.tasks_canvas.yview)
        scrollbar.place(x=470, y=170, height=430)
        
        self.tasks_frame = tk.Frame(self.tasks_canvas, bg=self.bg_gradient_bottom)
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_frame.bind("<Configure>", 
                             lambda e: self.tasks_canvas.configure(
                                 scrollregion=self.tasks_canvas.bbox("all")))
        
        # Stats label
        self.stats_label = tk.Label(self.root, text="", font=("Arial", 10),
                                   bg=self.bg_gradient_bottom, fg=self.text_color)
        self.stats_label.place(x=30, y=610, width=440, height=30)
        
    def create_gradient(self):
        """Create a gradient background"""
        width = 500
        height = 650
        limit = height
        
        r1, g1, b1 = self.hex_to_rgb(self.bg_gradient_top)
        r2, g2, b2 = self.hex_to_rgb(self.bg_gradient_bottom)
        
        for i in range(limit):
            r = int(r1 + (r2 - r1) * i / limit)
            g = int(g1 + (g2 - g1) * i / limit)
            b = int(b1 + (b2 - b1) * i / limit)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def clear_placeholder(self, event):
        if self.task_entry.get() == "Enter a new task...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg=self.task_text)
    
    def add_placeholder(self, event):
        if not self.task_entry.get():
            self.task_entry.insert(0, "Enter a new task...")
            self.task_entry.config(fg="#999999")
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text and task_text != "Enter a new task...":
            task = {
                "text": task_text,
                "completed": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.tasks.append(task)
            self.save_tasks()
            self.display_tasks()
            self.task_entry.delete(0, tk.END)
            self.add_placeholder(None)
    
    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.display_tasks()
    
    def delete_task(self, index):
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            self.tasks.pop(index)
            self.save_tasks()
            self.display_tasks()
    
    def display_tasks(self):
        # Clear existing tasks
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        if not self.tasks:
            no_task_label = tk.Label(self.tasks_frame, text="No tasks yet! Add one above 😊",
                                    font=("Arial", 12), bg=self.bg_gradient_bottom,
                                    fg=self.text_color)
            no_task_label.pack(pady=50)
        
        for i, task in enumerate(self.tasks):
            self.create_task_widget(i, task)
        
        # Update stats
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        self.stats_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {total - completed}")
    
    def create_task_widget(self, index, task):
        task_frame = tk.Frame(self.tasks_frame, bg=self.task_bg, relief="flat", bd=0)
        task_frame.pack(fill="x", padx=10, pady=5)
        
        # Add shadow effect
        shadow = tk.Frame(self.tasks_frame, bg="#cccccc", height=2)
        shadow.pack(fill="x", padx=12)
        
        # Checkbox
        check_var = tk.IntVar(value=1 if task["completed"] else 0)
        checkbox = tk.Checkbutton(task_frame, variable=check_var, bg=self.task_bg,
                                 activebackground=self.task_bg,
                                 command=lambda idx=index: self.toggle_task(idx))
        checkbox.pack(side="left", padx=10, pady=10)
        
        # Task text
        text_style = "overstrike" if task["completed"] else "normal"
        task_label = tk.Label(task_frame, text=task["text"], 
                             font=("Arial", 11, text_style),
                             bg=self.task_bg, fg=self.task_text, anchor="w")
        task_label.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        
        # Delete button
        delete_btn = tk.Button(task_frame, text="🗑️", font=("Arial", 12),
                              bg=self.task_bg, fg="#ff4757", relief="flat",
                              cursor="hand2", bd=0,
                              command=lambda idx=index: self.delete_task(idx))
        delete_btn.pack(side="right", padx=10, pady=10)
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=2)

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()