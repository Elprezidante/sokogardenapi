from flask import Flask, request, jsonify
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection function
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="sokogardenonline"
    )

# SIGNUP ROUTE
@app.route("/api/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]

    hashed_password = generate_password_hash(password)

    connection = connect_db()
    cursor = connection.cursor()

    sql = "INSERT INTO users(username,email,phone,password) VALUES(%s,%s,%s,%s)"
    data = (username, email, phone, hashed_password)

    cursor.execute(sql, data)
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "User registration successful"})


# LOGIN ROUTE
@app.route("/api/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    connection = connect_db()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM users WHERE email=%s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Login failed"})

if __name__ == "__main__":
    app.run(debug=True)
