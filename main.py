# coding: utf-8
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def select_directory():
    directory_path = filedialog.askdirectory(title="Select Directory")
    directory_var.set(directory_path)


def select_txt_file():
    file_path = filedialog.askopenfilename(title="Select TXT File", filetypes=[("Text files", "*.txt")])
    txt_file_var.set(file_path)


def perform_task():
    directory_path = directory_var.get()
    txt_file_path = txt_file_var.get()

    if not directory_path or not txt_file_path:
        result_var.set("Please select both directory and txt file.")
        return

    # Perform your task here, for example, counting lines in the text file
    with open(txt_file_path, 'r') as f:
        result_var.set(f"Task completed.")


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Tkinter File Selection and Task Example")

    # Variables
    directory_var = tk.StringVar()
    txt_file_var = tk.StringVar()
    result_var = tk.StringVar()

    # GUI Elements
    directory_label = tk.Label(root, text="Select Directory:")
    directory_label.grid(row=0, column=0, padx=10, pady=5)

    directory_entry = tk.Entry(root, textvariable=directory_var, width=40)
    directory_entry.grid(row=0, column=1, padx=10, pady=5)

    directory_button = tk.Button(root, text="Browse", command=select_directory)
    directory_button.grid(row=0, column=2, padx=5, pady=5)

    txt_file_label = tk.Label(root, text="Select TXT File:")
    txt_file_label.grid(row=1, column=0, padx=10, pady=5)

    txt_file_entry = tk.Entry(root, textvariable=txt_file_var, width=40)
    txt_file_entry.grid(row=1, column=1, padx=10, pady=5)

    txt_file_button = tk.Button(root, text="Browse", command=select_txt_file)
    txt_file_button.grid(row=1, column=2, padx=5, pady=5)

    task_button = tk.Button(root, text="Perform Task", command=perform_task)
    task_button.grid(row=2, column=0, columnspan=3, pady=10)

    result_label = tk.Label(root, textvariable=result_var)
    result_label.grid(row=3, column=0, columnspan=3, pady=5)

    # Start the Tkinter event loop
    root.mainloop()
