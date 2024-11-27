import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

# Flask server URL
SERVER_URL = "http://127.0.0.1:5000"

# Function to upload health record
def add_health_record():
    patient_data = patient_data_entry.get("1.0", tk.END).strip()
    if not patient_data:
        messagebox.showerror("Error", "Patient data cannot be empty!")
        return

    file_path = file_path_var.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a file!")
        return

    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {'patient_data': patient_data}
            response = requests.post(f"{SERVER_URL}/add_health_record", data=data, files=files)

        if response.status_code == 201:
            result = response.json()
            messagebox.showinfo("Success", f"Record added successfully!\nBlock Hash: {result['block_hash']}")
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error occurred"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to verify blockchain
def verify_blockchain():
    try:
        response = requests.get(f"{SERVER_URL}/verify_chain")
        if response.status_code == 200:
            result = response.json()
            if result["message"] == "Blockchain is valid":
                messagebox.showinfo("Success", "Blockchain is valid!")
            else:
                block_id = result.get("block_id", "Unknown")
                messagebox.showerror("Error", f"Blockchain compromised at block {block_id}!")
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error occurred"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to select file
def select_file():
    file_path = filedialog.askopenfilename(title="Select File")
    if file_path:
        file_path_var.set(file_path)

# GUI setup
root = tk.Tk()
root.title("Blockchain Health Records")

# Patient Data
tk.Label(root, text="Patient Data:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
patient_data_entry = tk.Text(root, height=5, width=40)
patient_data_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

# File selection
tk.Label(root, text="File:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
file_path_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_path_var, width=30, state="readonly")
file_entry.grid(row=1, column=1, padx=10, pady=10)
file_button = tk.Button(root, text="Browse", command=select_file)
file_button.grid(row=1, column=2, padx=10, pady=10)

# Buttons
add_button = tk.Button(root, text="Add Health Record", command=add_health_record, bg="green", fg="white")
add_button.grid(row=2, column=1, padx=10, pady=10)

verify_button = tk.Button(root, text="Verify Blockchain", command=verify_blockchain, bg="blue", fg="white")
verify_button.grid(row=2, column=2, padx=10, pady=10)

# Run the GUI
root.mainloop()
