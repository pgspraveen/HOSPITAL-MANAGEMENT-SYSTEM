import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database connection
def connect_db():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    disease TEXT)''')
    conn.commit()
    conn.close()

# Add patient
def add_patient():
    name = entry_name.get()
    age_input = entry_age.get()
    gender = combo_gender.get()
    disease = entry_disease.get()

    try:
        age = int(age_input)
        if age < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid non-negative integer for age")
        return

    if name and gender and disease:
        conn = sqlite3.connect("hospital.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)", 
                    (name, age, gender, disease))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient added successfully")
        clear_entries()
        view_patients()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# View patients
def view_patients():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()

    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert("", tk.END, values=row, tags=(tag,))

# Delete patient
def delete_patient():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a patient to delete")
        return

    patient_id = tree.item(selected_item)['values'][0]
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()
    tree.selection_remove(tree.selection())
    messagebox.showinfo("Success", "Patient deleted successfully")
    view_patients()

# Load selected patient into input fields
def load_patient(event):
    selected_item = tree.selection()
    if selected_item:
        patient = tree.item(selected_item)['values']
        entry_name.delete(0, tk.END)
        entry_name.insert(0, patient[1])
        entry_age.delete(0, tk.END)
        entry_age.insert(0, patient[2])
        combo_gender.set(patient[3])
        entry_disease.delete(0, tk.END)
        entry_disease.insert(0, patient[4])

# Update patient
def update_patient():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a patient to update")
        return

    patient_id = tree.item(selected_item)['values'][0]
    name = entry_name.get()
    age_input = entry_age.get()
    gender = combo_gender.get()
    disease = entry_disease.get()

    try:
        age = int(age_input)
        if age < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid non-negative integer for age")
        return

    if name and gender and disease:
        conn = sqlite3.connect("hospital.db")
        cur = conn.cursor()
        cur.execute("UPDATE patients SET name=?, age=?, gender=?, disease=? WHERE id=?",
                    (name, age, gender, disease, patient_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient updated successfully")
        clear_entries()
        view_patients()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# Clear input fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    combo_gender.set("")
    entry_disease.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("750x500")
root.configure(bg="#f0f8ff")

# Style configuration
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#e6f2ff",
                foreground="black",
                rowheight=25,
                fieldbackground="#e6f2ff",
                font=('Arial', 10))

style.configure("Treeview.Heading",
                font=('Arial', 11, 'bold'),
                background="#4da6ff",
                foreground="white")

style.map("Treeview", background=[('selected', '#3399ff')])

style.configure("TButton",
                font=('Arial', 10),
                padding=6)

# Row tags for striping
tree_tag_even = {'background': '#f9fbff'}
tree_tag_odd = {'background': '#d6eaff'}

# Labels and Entry Widgets
tk.Label(root, text="Name", bg="#f0f8ff", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_name = tk.Entry(root, font=('Arial', 10))
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Age", bg="#f0f8ff", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_age = tk.Entry(root, font=('Arial', 10))
entry_age.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Gender", bg="#f0f8ff", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
combo_gender = ttk.Combobox(root, values=["Male", "Female", "Other"], font=('Arial', 10), state="readonly")
combo_gender.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Disease", bg="#f0f8ff", font=('Arial', 10)).grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_disease = tk.Entry(root, font=('Arial', 10))
entry_disease.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Patient", command=add_patient, bg="#99ccff").grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Update Patient", command=update_patient, bg="#66cc66").grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Delete Patient", command=delete_patient, bg="#ff6666").grid(row=4, column=2, padx=10, pady=10)
tk.Button(root, text="View Patients", command=view_patients, bg="#ffcc66").grid(row=4, column=3, padx=10, pady=10)

# Treeview with Scrollbar
tree_frame = tk.Frame(root)
tree_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Age", "Gender", "Disease"),
                    show="headings", yscrollcommand=tree_scroll.set, selectmode="browse")
tree_scroll.config(command=tree.yview)

for col in ("ID", "Name", "Age", "Gender", "Disease"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

tree.tag_configure('evenrow', background='#f9fbff')
tree.tag_configure('oddrow', background='#d6eaff')

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", load_patient)

# Initialize database
connect_db()
view_patients()

root.mainloop()
