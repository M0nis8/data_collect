import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import csv

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def submit_info(event=None):
    name = name_entry.get()
    country_code = country_var.get()
    phone_number = phone_entry.get()
    site_no = site_entry.get()
    street = street_entry.get()
    project = project_entry.get()
    payment = payment_entry.get()

    try:
        data_base = mysql.connector.connect(host="localhost", user="root", password="root", database="details_collect")
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
    name_entry.delete(0, ctk.END)
    country_var.set("")
    phone_entry.delete(0, ctk.END)
    site_entry.delete(0, ctk.END)
    street_entry.delete(0, ctk.END)
    project_entry.delete(0, ctk.END)
    payment_entry.delete(0, ctk.END)

def submit_registration(reg_window, reg_name_entry, reg_email_entry):
    name = reg_name_entry.get()
    email = reg_email_entry.get()

    try:
        data_base = mysql.connector.connect(host="localhost", user="root", password="root", database="details_collect")
        cursor = data_base.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          name TEXT,
                          email VARCHAR(100),
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        cursor.execute("INSERT INTO registrations (name, email) VALUES (%s, %s)", (name, email))
        data_base.commit()
        messagebox.showinfo("Success", "Registration successful!")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        data_base.close()

    reg_window.destroy()  # Close the registration window
    main_window()  # Open the main user details window

def register_user():
    # Create a new window for registration
    reg_window = ctk.CTkToplevel(root)
    reg_window.title("Register")
    reg_window.geometry("300x200")

    name_label = ctk.CTkLabel(reg_window, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)

    reg_name_entry = ctk.CTkEntry(reg_window)
    reg_name_entry.grid(row=0, column=1, padx=5, pady=5)

    email_label = ctk.CTkLabel(reg_window, text="Email:")
    email_label.grid(row=1, column=0, padx=5, pady=5)

    reg_email_entry = ctk.CTkEntry(reg_window)
    reg_email_entry.grid(row=1, column=1, padx=5, pady=5)

    submit_button = ctk.CTkButton(reg_window, text="Register", command=lambda: submit_registration(reg_window, reg_name_entry, reg_email_entry))
    submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

def main_window():
    global root
    root = ctk.CTk()
    root.title("User  Details")
    root.geometry("300x500")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(padx=10, pady=10, fill=ctk.BOTH, expand=True)

    # Name Entry
    name_label = ctk.CTkLabel(frame, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    global name_entry
    name_entry = ctk.CTkEntry(frame, width=200)
    name_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Country Code Dropdown
    country_label = ctk.CTkLabel(frame, text="Country Code:")
    country_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    global country_var
    country_var = ctk.StringVar(value="")
    country_dropdown = ctk.CTkOptionMenu(frame,
        values=["+82 (South Korea)", "+1 (USA)", "+44 (UK)", "+86 (China)"],
        variable=country_var,
        width=200)
    country_dropdown.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Phone Number Entry
    phone_label = ctk.CTkLabel(frame, text="Phone Number:")
    phone_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    global phone_entry
    phone_entry = ctk.CTkEntry(frame, width=200)
    phone_entry.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Site Number Entry
    site_label = ctk.CTkLabel(frame, text="Site Number:")
    site_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
    global site_entry
    site_entry = ctk.CTkEntry(frame, width=200)
    site_entry.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    # Street Entry
    street_label = ctk.CTkLabel(frame, text="Street:")
    street_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
    global street_entry
    street_entry = ctk.CTkEntry(frame, width=200)
    street_entry.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

    # Project Entry
    project_label = ctk.CTkLabel(frame, text="Project:")
    project_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")
    global project_entry
    project_entry = ctk.CTkEntry(frame, width=200)
    project_entry.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

    # Payment Entry
    payment_label = ctk.CTkLabel(frame, text="Payment:")
    payment_label.grid(row=12, column=0, padx=5, pady=5, sticky="w")
    global payment_entry
    payment_entry = ctk.CTkEntry(frame, width=200)
    payment_entry.grid(row=13, column=0, columnspan=2, padx=5, pady=5)

    # Submit Button
    submit_button = ctk.CTkButton(frame, text="Submit", command=submit_info)
    submit_button.grid(row=14, column=0, padx=5, pady=10, sticky="ew")

    # Register Button
    register_button = ctk.CTkButton(frame, text="Register", command=register_user)
    register_button.grid(row=14, column=1, padx=5, pady=10, sticky="ew")

    # Bind Enter key to submit_info
    root.bind('<Return>', submit_info)

# Run the application
if __name__ == "__main__":
    root = ctk.CTk()  # Create the root window
    register_user()  # Open the registration window first
    root.mainloop()  # Start the main loop