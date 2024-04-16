import sqlite3

def find_path_by_name(name):
    con = sqlite3.connect("Friday.db")
    cursor = con.cursor()

    # Assuming your table already exists, you should not create it again
    # query = "CREATE TABLE IF NOT EXISTS users_custom_commands (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
    # cursor.execute(query)

    # Check if the name exists in the database
    query = "SELECT path FROM users_cuostom_commands WHERE name = ?"
    cursor.execute(query, (name,))
    result = cursor.fetchone()

    if result:
        # If the name is found, print the corresponding path
        print(f"Path for {name}: {result[0]}")
    else:
        print(f"No entry found for {name}")

    con.close()

# Get input from the user
user_input = input("Enter a name to find the corresponding path: ")

# Call the function with the user input
find_path_by_name(user_input)
