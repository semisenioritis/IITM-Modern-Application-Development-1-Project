import sqlite3
import hashlib



# Register a new user
def register(username, password, email, user_type):
    # Connect to database or create it if it doesn't exist

    conn = sqlite3.connect('users.db', check_same_thread=False)

    # Create a table for storing user data
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    user_type INTEGER NOT NULL);''')

    # Hash the password for secure storage
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Insert the new user into the database
    try:
        conn.execute("INSERT INTO users (username, password, email, user_type) VALUES (?, ?, ?, ?)", (username, hashed_password, email, user_type))
        conn.commit()
        # print("User registered successfully!")
        conn.close()
        return True
    except:
        # print("Username or email already exists")
        conn.close()
        return False

# Login an existing user
def login(username, password):
    # Connect to database or create it if it doesn't exist

    conn = sqlite3.connect('users.db', check_same_thread=False)

    # Create a table for storing user data
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    user_type INTEGER NOT NULL);''')

    # Hash the password to compare it to the stored password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Check if the user exists and the password matches
    cursor = conn.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    if cursor.fetchone() is not None:
        # print("Login successful!")
        conn.close()
        return True
    else:
        # print("Invalid username or password")
        conn.close()
        return False


def check_data_exists_in_table(table_name, column_name, data_to_check):
    # Connect to database or create it if it doesn't exist

    conn = sqlite3.connect('users.db', check_same_thread=False)

    # Create a table for storing user data
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    user_type INTEGER NOT NULL);''')
    # Connect to the database
    c = conn.cursor()

    # Build the SQL query
    sql_query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"

    # Execute the query and fetch the results
    c.execute(sql_query, (data_to_check,))
    rows = c.fetchall()

    # Check if any rows were returned
    if len(rows) > 0:
        conn.close()
        return rows
    else:
        conn.close()
        return None

# Example usage
# register("john", "password123", "john@example.com", 1) # admin user
# register("jane", "password456", "jane@example.com", 0) # customer user
# login("john", "password123")

