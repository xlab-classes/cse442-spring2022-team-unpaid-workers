import mysql.connector

# this database will be storing sign in and sign up information #
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Shkaraot99@",
    database = "QuizHub"
)
mycursor = db.cursor()

# create database for sign in and sign up username and password if not exist #
mycursor.execute("CREATE DATABASE IF NOT EXISTS QuizHub")

# this function will print the database usernames and password
def print_user_table():
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        print("db usernames: ", row)

    print("print successfully")

# this is creating the table for the username and password storage #
def creat_user_table():
    mycursor.execute("CREATE TABLE IF NOT EXISTS user (role VARCHAR(10),"
                      "username VARCHAR(20),"
                      "password VARCHAR(20),"
                      "_ID int PRIMARY key AUTO_INCREMENT)")

# this function is going to insert the username and password into the table successfully
def insert_user(tuple):
    try:
        creat_user_table()
        mycursor.execute("INSERT INTO user (role,username,password) VALUES (%s,%s,%s)", tuple)
        db.commit()
        print("insert successfully")
        mycursor.execute("SELECT * FROM user")
        for x in mycursor:
            print(x)
    except mysql.connector.Error:
        print("insert failed")

# this function will check if the username exist in the database
def username_is_not_exist(name):
    print(name)
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Shkaraot99@",
        database = "QuizHub"
    )
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        if row[1] == name:
            return False
    return True

# this function is going to check if the user entered the right username and password
# in order to login to the website.
def user_authentication(name, pw):

    try:
        mycursor.execute('SELECT * FROM user')
        print("user_authentication check")
        for row in mycursor:
            print(row)
            if row[1] == name and row[2] == pw:
                print(row[0])
                return row[0]
        print("printing none")
        return None

    except mysql.connector.Error:
        print("check failed")
def create_quiz_table():
    mycursor.execute("CREATE TABLE IF NOT EXISTS user (Question VARCHAR(100),"
                     "Answer VARCHAR(100),"
                     "_ID int PRIMARY key AUTO_INCREMENT)")

def insert_question(input):
    try:
        create_quiz_table()
        mycursor.execute("INSERT INTO user (Question,Answer) VALUES (%s,%s)", tuple)
        db.commit()
        print("insert question successfully")
        mycursor.execute("SELECT * FROM user")
        for x in mycursor:
            print(x)
    except mysql.connector.Error:
        print("insert question failed")

# this function will be deleting the database.
def delete_table():
    mycursor.execute("DROP TABLE user")
