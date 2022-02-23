import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ubcse442",
    database="QuizHub"
)
mycursor = db.cursor()



def creat_user_table():

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

    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        if row[1] == name:
            return False
    return True

def user_authentication(name, pw):

    try:
        mycursor.execute('SELECT * FROM user')
        for row in mycursor:
            if row[1] == name and row[2] == pw:
                return row[0]
        return None

    except mysql.connector.Error:
        print("check failed")

def delete_table():
    mycursor.execute("DROP TABLE user")