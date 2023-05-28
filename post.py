from flask import Flask, g, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'C:/Users/DELL/Desktop/crud-flask/raju.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/create_table')
def create_table():
    db = get_db()
    cursor = db.cursor()

    # Check if the table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.close()
        return 'Table already exists'

    # Execute SQL statement to create a table
    cursor.execute('''CREATE TABLE users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      email TEXT NOT NULL)''')

    db.commit()
    cursor.close()
    return 'Table created successfully'

@app.route('/users', methods=['POST'])
def add_user():
    db = get_db()
    cursor = db.cursor()

    # Get user data from the request
    name = request.json['name']
    email = request.json['email']

    # Execute SQL statement to insert data
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))

    db.commit()
    cursor.close()
    return 'User added successfully'
    
@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    cursor = db.cursor()

    # Execute SQL statement to retrieve all users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    cursor.close()
    return jsonify(users)

@app.route('/update_user', methods=['PUT'])
def update_user():
    data = request.get_json()
    user_id = data['id']
    new_name = data['name']
    new_email = data['email']

    db = get_db()
    cursor = db.cursor()

    # Update the user in the database
    cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (new_name, new_email, user_id))
    db.commit()

    cursor.close()
    return 'User updated successfully'


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user_id = data['id']

    db = get_db()
    cursor = db.cursor()

    # Delete the user from the database
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    db.commit()

    cursor.close()
    return 'User deleted successfully'


if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()
