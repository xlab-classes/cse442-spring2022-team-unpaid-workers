import mysql.connector

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="ubcse442",
#     database="QuizHub"
# )

db = mysql.connector.connect(
    host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
    database="balfxq49nnpzz9niwuoy",
    user="ul05wz30fljlsi0y",
    passwd="49j34qWuliU9gKCXlNt4"
)
mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS balfxq49nnpzz9niwuoy")


def print_user_table():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        print(row)
    print("print successfully")


def creat_user_table():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS user (role VARCHAR(10),"
                     "username VARCHAR(20),"
                     "password VARCHAR(20),"
                     "_ID int PRIMARY key AUTO_INCREMENT)")


def insert_user(tuple):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
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
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        if row[1] == name:
            return False
    return True


def user_authentication(name, pw):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()

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
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Quiz_Data (Passcode VARCHAR(10),"
                     "Quiz VARCHAR(2048),"
                     "_ID int PRIMARY key AUTO_INCREMENT)")


def insert_quiz(tuple):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    print("in insert:",tuple[1])
    # tuple format ->  (passcode,json.format(quiz)
    try:
        create_quiz_table()
        print("created!")
        mycursor.execute("INSERT INTO Quiz_Data (Passcode,Quiz) VALUES (%s,%s)", tuple)
        print("executed")
        db.commit()
        print("insert question successfully")
        mycursor.execute("SELECT * FROM Quiz_Data")

        for x in mycursor:
            print("Quiz:",x)
    except mysql.connector.Error:
        print("insert question failed")


def find_quiz(passcode):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()

    try:
        mycursor.execute('SELECT * FROM Quiz_Data')
        print("user_authentication check")
        for row in mycursor:
            if row[0] == passcode:
                return row[1]
        return None
    except mysql.connector.Error:
        print("check failed")

def print_passcode():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Quiz_Data')
    for row in mycursor:
        print(row)
    print("print successfully")

def makeStudentQuizRecord():
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Quiz_Record (studentName VARCHAR(2048),"
                     "QuizName VARCHAR(2048),"
                     "_ID int PRIMARY key AUTO_INCREMENT)")

def studentTakeQuiz(studentName,quizCode):
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    try:
        makeStudentQuizRecord()
        sql = "INSERT INTO Quiz_Record (studentName,QuizName) VALUES (%s,%s)"
        val = (studentName,quizCode)
        mycursor.execute(sql,val)
        db.commit()
    except:
        print("Insert Student Record Fail")

def delete_quiz_table():
    mycursor.execute("DROP TABLE Quiz_Data")

def delete_user_table():
    mycursor.execute("DROP TABLE user")

def makeScoreRecord():
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Score_Record (studentName VARCHAR(2048),"
                 "QuizName VARCHAR(2048),"
                 "score VARCHAR(2048),"
                 "_ID int PRIMARY key AUTO_INCREMENT)")

def insertScoreRecord(studentName,QuizName,score):
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    try:
        makeStudentQuizRecord()
        sql = "INSERT INTO Score_Record (studentName,QuizName,score) VALUES (%s,%s,%s)"
        val = (studentName,QuizName,score)
        mycursor.execute(sql,val)
        db.commit()
    except:
        print("Insert Student Record Fail")



def getInformation():
    db = mysql.connector.connect(
        host="balfxq49nnpzz9niwuoy-mysql.services.clever-cloud.com",
        database="balfxq49nnpzz9niwuoy",
        user="ul05wz30fljlsi0y",
        passwd="49j34qWuliU9gKCXlNt4"
    )
    mycursor = db.cursor()
    try:
        mycursor.execute("SELECT * FROM Score_Record")
        myresult = mycursor.fetchall()
        print(myresult)
        return myresult
    except:
        print('No Score_Record Table !!!')

