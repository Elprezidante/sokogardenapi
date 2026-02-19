# Import flask and its components
from itertools import count
from flask import *

# import the pymysql module.It helps us create a connection between python flask and mysql database
import pymysql

# create a flask application and give it a name
app=Flask(__name__)

# Below is the sign  up route
@app.route("/api/signup", methods=["POST"]) 
def signup():
    if request.method=="POST": 
    # extract the different details entered in the form
       username = request.form["username"]
       email = request.form ["email"]
       password = request.form["password"]
       phone = request.form["phone"]


     #  by use of the print lets print all tyhe details with the upcoming request
    # print(username,email,password,phone)
    # Establish a connection between flask and mySQL
    connection=pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")
    # create a cursor to execute the SQL query
    cursor = connection.cursor()
    # structure an SQL to insert the details received from the form
    # %s is a placeholder :It stands in places of actual values ie we shall replace them later on
    sql="INSERT INTO users(username,email,phone,password) VALUES(%s,%s,%s,%s)"
    # create a tuple that will hold all the data gotten from the form
    data = (username,email,password,phone)
    # By use of the cursor execute the SQL as you replace the placeholders with the actual values
    cursor.execute(sql,data)
    # commit the changes to dbase
    connection.commit()
    return jsonify({"message": "User registration was succesful"})

# Below is the login/sign in route
@app.route("/api/login", methods=["POST"])
def login():
    if request.method=="POST":
        # extract the different details entered in the form
        email=request.form["email"]
        password=request.form["password"]
        # print out the details entered
        # print(email,password)
        # Establish a connection to the database
        connection=pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")
        # create a cursor 
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        # Structure the Sql query that will check whether the email and the password entered are correct
        sql = "SELECT * FROM users WHERE email=%s AND password=%s"
        # Put the data received into a tuple
        data=(email,password) 
        # by use of the cursor execute the SQL 
        cursor.execute(sql,data)
        # Check whether there are rows returned and store them in a variable 
        count = cursor.rowcount     
        
          # If there records returned it means both the password and the email otherwise they are wrong
        if count == 0:
            return jsonify({"message": "log in failed"})
        else:
            # There must be a user so we create a variable that will hold the details of the fetched on the database
            user=cursor.fetchone()
            # return the details to the front end as well as a message
            return jsonify({"message":"user log in successful", "user": user})



        
# run application
app.run(debug=True)

