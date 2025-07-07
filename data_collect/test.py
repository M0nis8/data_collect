import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import mysql.connector
import csv
import customtkinter as ctk  # Import CustomTkinter

# Set the appearance mode and default color theme
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Change the theme color

def submit_info(event=None):
    name = name_entry.get()
    country_code = country_var.get()
    phone_number = phone_entry.get()
    site_no = site_entry.get()
    street = street_entry.get()
    project = project_entry.get()
    payment = payment_entry.get()

    try:
        data_base = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="details_collect"
        )
        cursor = data_base.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          name TEXT,
                          country_code TEXT,
                          phone_number VARCHAR(15),
                          site_no TEXT,
                          street TEXT,
                          project TEXT,
                          payment TEXT)''')

        cursor.execute("INSERT INTO user_info (name, country_code, phone_number, site_no, street, project, payment) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (name, country_code, phone_number, site_no, street, project, payment))
        data_base.commit()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        data_base.close()

    with open('user_info.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, country_code, phone_number, site_no, street, project, payment])

    clear_entries()

def clear_entries():
    name_entry.delete(0, tk.END)
    country_var.set("")  # Clear the country dropdown
    phone_entry.delete(0, tk.END)
    site_entry.delete(0, tk.END)
    street_entry.delete(0, tk.END)
    project_entry.delete(0, tk.END)
    payment_entry.delete(0, tk.END)

def login():
    user_name = username_entry.get()
    pass_wd = password_entry.get()

    if user_name == "admin" and pass_wd == "123456":
        login_page.destroy()
        main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def main_window():
    global root
    root = ctk.CTk()  # Use CustomTkinter's CTk
    root.title("User Details")
    root.geometry("350x500")  # Set a fixed size for better appearance

    # Create a rounded frame
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    name_label = ctk.CTkLabel(frame, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    global name_entry
    name_entry = ctk.CTkEntry(frame)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    country_label = ctk.CTkLabel(frame, text="Country Code:")
    country_label.grid(row=1, column=0, padx=10, pady=10)

    global country_var
    country_var = tk.StringVar()
    country_options = ["+1", "+44", "+91", "+61", "+355", "+672", "+880", "+43", "+375", "+55"]
    country_dropdown = ctk.CTkOptionMenu(frame, variable=country_var, values=country_options)
    country_dropdown.grid(row=1, column=1, padx=10, pady=10)

    phone_label = ctk.CTkLabel(frame, text="Phone Number:")
    phone_label.grid(row=2, column=0, padx=10, pady=10)

    global phone_entry
    phone_entry = ctk.CTkEntry(frame)
    phone_entry.grid(row=2, column=1, padx=10, pady=10)

    site_label = ctk.CTkLabel(frame, text="Site No.:")
    site_label.grid(row=3, column=0, padx=10, pady=10)

    global site_entry
    site_entry = ctk.CTkEntry(frame)
    site_entry.grid(row=3, column=1, padx=10, pady=10)

    street_label = ctk.CTkLabel(frame, text="Street:")
    street_label.grid(row=4, column=0, padx=10, pady=10)

    global street_entry
    street_entry = ctk.CTkEntry(frame)
    street_entry.grid(row=4, column=1, padx=10, pady=10)

    project_label = ctk.CTkLabel(frame, text="Project:")
    project_label.grid(row=5, column=0, padx=10, pady=10)

    global project_entry
    project_entry = ctk.CTkEntry(frame)
    project_entry.grid(row=5, column=1, padx=10, pady=10)

    payment_label = ctk.CTkLabel(frame, text="Payment:")
    payment_label.grid(row=6, column=0, padx=10, pady=10)

    global payment_entry
    payment_entry = ctk.CTkEntry(frame)
    payment_entry.grid(row=6, column=1, padx=10, pady=10)

    submit_button = ctk.CTkButton(frame, text="Submit", command=submit_info)
    submit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    view_button = ctk.CTkButton(frame, text="View Data", command=view_data)
    view_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    root.bind('<Return>', submit_info)

    root.mainloop()

def view_data():
    global root
    passwd_wind = Toplevel(root)
    passwd_wind.title("user password")
    passwd_wind.geometry("352x150")  

    password_label = ctk.CTkLabel(passwd_wind, text="user password:")
    password_label.grid(row=0, column=0, padx=10, pady=10)

    password_entry = ctk.CTkEntry(passwd_wind, show='*')
    password_entry.grid(row=0, column=1, padx=10, pady=10)

    def check_password():
        if password_entry.get() == "123456":
            passwd_wind.destroy()
            display_data()
        else:
            messagebox.showerror("Error", "Invalid password.")

    submit_password_button = ctk.CTkButton(passwd_wind, text="Submit", command=check_password)
    submit_password_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

def display_data():
    global root
    disp_data = Toplevel(root)
    disp_data.title("User Data")
    disp_data.geometry("600x400")  # Set size for better appearance

    columns = ("ID", "Name", "Country Code", "Phone Number", "Site No.", "Street", "Project", "Payment")
    tree = ttk.Treeview(disp_data, columns=columns, show='headings')
    tree.pack(padx=10, pady=10, fill='both', expand=True)

    tree.column("ID", width=50)
    tree.column("Name", width=100)
    tree.column("Country Code", width=100)
    tree.column("Phone Number", width=100)
    tree.column("Site No.", width=100)
    tree.column("Street", width=100)
    tree.column("Project", width=100)
    tree.column("Payment", width=100)

    for col in columns:
        tree.heading(col, text=col)

    try:
        data_base = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="details_collect"
        )
        cursor = data_base.cursor()

        cursor.execute("SELECT * FROM user_info")
        rows = cursor.fetchall()

        # Insert data into the treeview
        for row in rows:
            tree.insert("", tk.END, values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        data_base.close()

# Login Page
login_page = ctk.CTk()  # Use CustomTkinter's CTk
login_page.title("Login")
login_page.geometry("300x200")  # Set a fixed size for better appearance

username_label = ctk.CTkLabel(login_page, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)

username_entry = ctk.CTkEntry(login_page)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ctk.CTkLabel(login_page, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)

password_entry = ctk.CTkEntry(login_page, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = ctk.CTkButton(login_page, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

login_page.bind('<Return>', lambda event: login())

login_page.mainloop()
