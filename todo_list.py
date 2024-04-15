import customtkinter  # Importing the custom tkinter module
from tkinter import *  # Importing the necessary tkinter modules
from tkinter import messagebox   # Importing the messagebox from tkinter module
import sqlite3     # Importing the sqlite3 module to store data 

class TODO:
    def __init__(self):
        # Connect to the database
        self.connection = sqlite3.connect('todo.db')
        self.cursor = self.connection.cursor()

        # Create tasks table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                status INTEGER NOT NULL
                            )''')
        self.connection.commit()

    # Method to add a task
    def add_task(self):
        # Get the task name from the entry field
        task_name = self.task_entry.get().lower()

        # Check if the task name is the placeholder text
        if task_name == "enter your task:":
            # Show an error message and return if the placeholder text is present
            messagebox.showerror("Error", "Please enter a task before adding")
            return
            
        # Check if the entry field is empty
        if not task_name:
            # Show an error message and return if the entry field is empty
            messagebox.showerror("Error", "Enter your task you want to add")
            return
        
            # Check if the task already exists in the database
        self.cursor.execute("SELECT * FROM tasks WHERE name=?", (task_name,))
        existing_task = self.cursor.fetchone()
        if existing_task:
            # Show an error message if the task already exists
            messagebox.showerror("Error", "Task already exists")
            return
        
        # Clear the listbox before adding a new task
        self.listbox.delete(0, END)

        # Insert the task into the database
        self.cursor.execute("INSERT INTO tasks (name, status) VALUES (?, ?)", (task_name, 0))
        self.connection.commit()

        # Show a success message
        messagebox.showinfo("Info", "Task Added Successfully")


    # Method to display all tasks
    def display_all_tasks(self):
        # Clear the listbox before displaying tasks
        self.listbox.delete(0, END)

        # Fetch all tasks from the database
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        
        # Check if tasks exist
        if tasks:
            self.listbox.insert(END, "All Tasks:")
            # Iterate through tasks and display them in the listbox
            for index, task in enumerate(tasks, start=1):
                self.listbox.insert(END, f"{index}.{task[1]} - {'Complete' if task[2] else 'Incomplete'}")
        else:
            # Show an info message if no tasks are available
            messagebox.showinfo("No Tasks", "No tasks available")

    # Method to search for a task
    def search_task(self):
        # Get the task name to search from the entry field
        search_task_name = self.task_entry.get().lower()

        # Check if the search field is empty
        if not search_task_name:
            messagebox.showerror("Error", "Enter your task you want to search")
            return

        # Clear the listbox before displaying the search result
        self.listbox.delete(0, END)

        # Search for the task in the database
        self.cursor.execute("SELECT * FROM tasks WHERE name=?", (search_task_name,))
        task = self.cursor.fetchone()

        # Check if the task is found
        if task:
            # Display the task details in the listbox
            self.listbox.insert(END,f"Task: {task[1]}, Status: {'Complete' if task[2] else 'Incomplete'}")
        else:
            # Show an error message if the task is not found
            messagebox.showerror("Error", "Task not found")

    # Method to update a task
    def update_task(self):
        # Get the current and new task names from the entry field
        task_names = self.task_entry.get().lower().split(" to ")
        
        # Check if the entry format is correct
        if len(task_names) != 2:
            messagebox.showerror("Error", "Please enter the current task name followed by 'to' and then the new task name.")
            return

        # Extract current and new task names
        current_task_name, new_task_name = task_names

        # Clear the listbox before updating the task
        self.listbox.delete(0, END)

        # Update the task in the database
        self.cursor.execute("UPDATE tasks SET name=? WHERE name=?", (new_task_name, current_task_name))
        self.connection.commit()

        # Check if the task is updated successfully
        if self.cursor.rowcount > 0:
            self.listbox.insert(END,f"Task '{current_task_name}' updated to '{new_task_name}' successfully")
        else:
            # Show an error message if the task is not found
            messagebox.showerror("Error", "Task not found")

    # Method to delete a task
    def delete_task(self):
        # Get the task name to delete from the entry field
        delete_task_name = self.task_entry.get().lower()

        # Check if the delete field is empty
        if not delete_task_name:
            messagebox.showerror("Error", "Enter your task you want to delete")
            return

        # Prompt the user for confirmation
        confirmation = messagebox.askyesno("Confirm Deletion", f"Do you want to delete the task '{delete_task_name}'?")

        # If user confirms deletion
        if confirmation:
            # Clear the listbox before deleting the task
            self.listbox.delete(0, END)

            # Delete the task from the database
            self.cursor.execute("DELETE FROM tasks WHERE name=?", (delete_task_name,))
            self.connection.commit()

            # Check if the task is deleted successfully
            if self.cursor.rowcount > 0:
                self.listbox.insert(END, f"Task '{delete_task_name}' was deleted successfully")
            else:
                # Show an error message if the task is not found
                messagebox.showerror("Error", "Task not found")


    # Method to mark a task as complete
    def complete_task(self):
        # Get the task name to mark as complete from the entry field
        completed_task_name = self.task_entry.get().lower()

        # Check if the complete field is empty
        if not completed_task_name:
            messagebox.showerror("Error", "Enter your task you want to complete")
            return

        # Clear the listbox before marking the task as complete
        self.listbox.delete(0, END)

        # Mark the task as complete in the database
        self.cursor.execute("UPDATE tasks SET status=? WHERE name=?", (1, completed_task_name))
        self.connection.commit()

        # Check if the task is marked as complete successfully
        if self.cursor.rowcount > 0:
            self.listbox.insert(END, f"Task '{completed_task_name}' completed successfully")
        else:
            # Show an error message if the task is not found
            messagebox.showerror("Error", "Task not found")

    # Method to display all completed tasks
    def display_all_complete_tasks(self):
        # Clear the listbox before displaying completed tasks
        self.listbox.delete(0, END)

        # Fetch completed tasks from the database
        self.cursor.execute("SELECT * FROM tasks WHERE status=1")
        tasks = self.cursor.fetchall()

        # Check if completed tasks exist
        if tasks:
            self.listbox.insert(END, "All Completed Tasks:")
            # Iterate through completed tasks and display them in the listbox
            for index, task in enumerate(tasks, start=1):
                self.listbox.insert(END, f"{index}. {task[1]}")
        else:
            # Show an info message if no completed tasks are available
            messagebox.showinfo("Info", "No completed task available")

    # Method to close the database connection
    def close_connection(self):
        self.connection.close()

    # Method to handle entry field click event
    def on_entry_click(self, event):
        if self.task_entry.get() == "Enter Your Task:":
            self.task_entry.delete(0, "end")
            self.task_entry.insert(0, "")
            self.task_entry.configure(fg_color="white", text_color="black")

    # Method to handle focus out event
    def on_focus_out(self, event):
        if self.task_entry.get() == "":
            self.task_entry.insert(0, "Enter Your Task:")
            self.task_entry.configure(fg_color="white", text_color="grey")

    # Method to reset the entry field and listbox
    def reset_all(self):
        self.task_entry.delete(0, END)
        self.listbox.delete(0, END)
        self.task_entry.insert(0, "Enter Your Task:")
        self.task_entry.configure(fg_color="white", text_color="grey")


root = customtkinter.CTk()  # Creating a custom Tkinter window
root.title("TO-DO LIST APPLICATION")  # Setting window title
root.geometry("330x600")  # Setting window size
root.iconbitmap("TO-DO-List-Application/logo.ico")   # setting the window icon
root.config(bg="#09115e")  # Setting window background color
root.resizable(width=False, height=False)  # Making window non-resizable

# Setting fonts for the labels and buttons
font1 = ("Arial", 30, "bold")
font2 = ("Arial", 18, "bold")
font3 = ("Arial", 10, "bold")

frame = Frame(root, bg="#09115e")  # Creating a frame with specified background color
frame.place(relx=0.5, rely=0.5, anchor="center")  # Placing the frame in the center of the window

# Creating a label for the header
header_label = customtkinter.CTkLabel(frame, text="TO-DO LIST\nAPPLICATION", font=font1, bg_color="#09115e", text_color="white")
header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))  # Placing the header label on the grid

todo = TODO()  # Creating an instance of the TODO class

# Creating an entry field for tasks
todo.task_entry = customtkinter.CTkEntry(frame, font=font2, width=280, height=35)
todo.task_entry.insert(0, "Enter Your Task:")  # Setting default text in the entry field
todo.task_entry.configure(fg_color="white", text_color="grey")
todo.task_entry.bind("<FocusIn>", todo.on_entry_click)  # Binding focus in event
todo.task_entry.bind("<FocusOut>", todo.on_focus_out)  # Binding focus out event
todo.task_entry.grid(row=1, column=0, columnspan=2, pady=(10, 20))  # Placing the entry field on the grid

# Creating buttons for various actions

# Add Task Button
add_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Add Task", fg_color="aqua", hover_color="aqua", bg_color="aqua", corner_radius=5, width=120, command=todo.add_task)
add_button.grid(row=2, column=0, pady=(10, 5))  # Placing the Add Task button on the grid

# Update Task Button
update_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Update Task", fg_color="orange", hover_color="orange", bg_color="orange", corner_radius=5, width=120, command=todo.update_task)
update_button.grid(row=2, column=1, pady=(10, 5))  # Placing the Update Task button on the grid

# Search Task Button
search_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Search Task", fg_color="lightgreen", hover_color="lightgreen", bg_color="lightgreen", corner_radius=5, width=120, command=todo.search_task)
search_button.grid(row=3, column=0, pady=(10, 5))  # Placing the Search Task button on the grid

# Delete Task Button
delete_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Delete Task", fg_color="#FF474C", hover_color="#FF474C", bg_color="red", corner_radius=5, width=120, command=todo.delete_task)
delete_button.grid(row=3, column=1, pady=(10, 5))  # Placing the Delete Task button on the grid

# Display All Task Button
display_all_task_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Display All Task", fg_color="#C68642", hover_color="#C68642", bg_color="#C68642", corner_radius=5, width=120, command=todo.display_all_tasks)
display_all_task_button.grid(row=4, column=0, padx=(10, 0), pady=(10, 5))  # Placing the Display All Task button on the grid

# Complete Task Button
complete_task_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Complete Task", fg_color="hotpink", hover_color="hotpink", bg_color="hotpink", corner_radius=5, width=120, command=todo.complete_task)
complete_task_button.grid(row=4, column=1, padx=(10, 0), pady=(10, 5))  # Placing the Complete Task button on the grid

# Display All Complete Task Button
display_complete_task_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Display All Completed Task", fg_color="yellow", hover_color="yellow", bg_color="yellow", corner_radius=5, width=120, command=todo.display_all_complete_tasks)
display_complete_task_button.grid(row=5, column=0, columnspan=2, pady=(10, 5))  # Placing the Display All Complete Task button on the grid

# Creating a listbox to display tasks
todo.listbox = Listbox(frame, width=43, height=10, font=font3)
todo.listbox.grid(row=6, column=0, columnspan=2, pady=(10, 10))  # Placing the listbox on the grid

# Reset Button
reset_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Reset", fg_color="light blue", hover_color="light blue", bg_color="light blue", corner_radius=5, width=120, command=todo.reset_all)
reset_button.grid(row=7, column=0, pady=(10, 5))  # Placing the Reset button on the grid

# Exit Button
exit_button = customtkinter.CTkButton(frame, font=font2, text_color="black", text="Exit", fg_color="red", hover_color="red", bg_color="red", corner_radius=5, width=120, command=root.destroy)
exit_button.grid(row=7, column=1, pady=(10, 5))  # Placing the Exit button on the grid

# Running the main event loop
root.mainloop()  