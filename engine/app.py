from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Create the table if not exists
query = "CREATE TABLE IF NOT EXISTS sys_command(id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# Close the database connection
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        name = request.form['Add_Your_New_Commands']
        path = request.form['Add_Your_New_Commands_file_path']

        # Connect to SQLite database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # Insert data into the table
        query = "INSERT INTO sys_command(name, path) VALUES (?, ?)"
        cursor.execute(query, (name, path))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return 'Data added successfully'

if __name__ == '__main__':
    app.run(debug=True)
