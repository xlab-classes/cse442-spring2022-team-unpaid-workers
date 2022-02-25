import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ubcse442",
    database="QuizHub"
)
mycursor = db.cursor(buffered=True)

mycursor.execute("CREATE DATABASE IF NOT EXISTS QuizHub")


def print_user_table():
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        print(row)
    print("print successfully")


def creat_user_table():
    print("usertable")

    mycursor.execute("CREATE TABLE IF NOT EXISTS user (role VARCHAR(10),"
                     "username VARCHAR(20),"
                     "password VARCHAR(20),"
                     "_ID int PRIMARY key AUTO_INCREMENT)")


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


def username_is_not_exist(name):
    print(name)

    mycursor = db.cursor(buffered=True)
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        if row[1] == name:
            print("not exist")
            return False
    print("exist")
    return True


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


def delete_table():
    mycursor.execute("DROP TABLE user")
