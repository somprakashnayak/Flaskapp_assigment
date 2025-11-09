from flask import Flask, render_template, request, redirect, url_for, abort
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',        # your MySQL username
    'password': 'Som12345',        # your MySQL password
    'database': 'userdb'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Route 1: Hello World
@app.route('/hello')
def hello():
    return "Hello Anshul!"

# Route 2: Show all users
@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('users.html', users=users)

# Route 3: Add new user form
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('users'))
    return render_template('new_user.html')

# Route 4: User detail by ID
@app.route('/users/<int:id>')
def user_detail(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        abort(404, description="User not found")

    return render_template('user_detail.html', user=user)

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return f"<h1>404 - {error.description}</h1>", 404


if __name__ == '__main__':
    app.run(debug=True)
