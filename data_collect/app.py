from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'details_collect'
}

# Create the user_info table if it doesn't exist
def create_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      name TEXT,
                      country_code TEXT,
                      phone_number VARCHAR(15),
                      site_no TEXT,
                      street TEXT,
                      project TEXT,
                      payment TEXT)''')
    connection.commit()
    cursor.close()
    connection.close()

create_table()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123456':
            return render_template('dashboard.html')
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/submit', methods=['POST'])
def submit_info():
    name = request.form['name']
    country_code = request.form['country_code']
    phone_number = request.form['phone_number']
    site_no = request.form['site_no']
    street = request.form['street']
    project = request.form['project']
    payment = request.form['payment']

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user_info (name, country_code, phone_number, site_no, street, project, payment) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (name, country_code, phone_number, site_no, street, project, payment))
        connection.commit()
        flash('Information submitted successfully!')
    except mysql.connector.Error as err:
        flash(f"Database Error: {err}")
    finally:
        cursor.close()
        connection.close()

    # Save to CSV
    with open('user_info.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, country_code, phone_number, site_no, street, project, payment])

    return redirect(url_for('dashboard'))

@app.route('/view_data')
def view_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_info")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('view_data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)