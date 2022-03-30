from mysql.connector import(connection)
import mysql.connector

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="ubcse442",
#     database="QuizHub"
# )

db = mysql.connector.connect(
    host="oceanus",
    user="tingjiez",
    passwd="50380202",
    database="tingjiez_db"
)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS tingjiez_db")


def print_user_table():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
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
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
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
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
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
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
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
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
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
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Quiz_Data (Passcode VARCHAR(10),"
                     "TeacherName VARCHAR(32),"
                     "QuizName VARCHAR(32),"
                     "Quiz VARCHAR(2048),"
                     "_ID int PRIMARY key AUTO_INCREMENT)")

def print_Quiz_Data():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Quiz_Data')
    for row in mycursor:
        print(row)
    print("print table Quiz_Data successfully")

def insert_quiz(tuple):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

    mycursor = db.cursor()

    try:
        create_quiz_table()
        print("created!")
        print("tuple:",tuple)
        mycursor.execute("INSERT INTO Quiz_Data (Passcode,TeacherName,QuizName,Quiz) VALUES (%s,%s,%s,%s)", tuple)
        print("executed")
        db.commit()
        print("insert question successfully")
        mycursor.execute("SELECT * FROM Quiz_Data")

        for x in mycursor:
            print("Quiz:",x)
    except mysql.connector.Error:
        print("insert question failed")

def find_quiz_name(passcode):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
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
        print("check quiz name failed")

def find_quiz_data(passcode):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

    mycursor = db.cursor()

    try:
        mycursor.execute('SELECT * FROM Quiz_Data')
        print("user_authentication check")
        for row in mycursor:
            print("row:",passcode,row[0])
            if row[0] == passcode:
                print(row[3])
                return row[3]
        return None
    except mysql.connector.Error:
        print("check quiz data failed")

def print_passcode():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Quiz_Data')
    for row in mycursor:
        print(row)
    print("print successfully")



def delete_score_record_table():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    mycursor = db.cursor()
    mycursor.execute("DROP TABLE Score_Record")

def delete_quiz_data_table():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

    mycursor = db.cursor()
    mycursor.execute("DROP TABLE Quiz_Data")

def delete_user_table():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    mycursor = db.cursor()
    mycursor.execute("DROP TABLE user")

def makeScoreRecord():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Score_Record (studentName VARCHAR(2048),"
                 "QuizName VARCHAR(2048),"
                 "score VARCHAR(2048),"
                 "Passcode VARCHAR (10),"    
                 "_ID int PRIMARY key AUTO_INCREMENT)")

def insertScoreRecord(studentName,QuizName,score,passcode,SubmissionID):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    makeScoreRecord()
    mycursor = db.cursor()
    try:

        sql = "INSERT INTO Score_Record (studentName,QuizName,score,Passcode,SubmissionID) VALUES (%s,%s,%s,%s,%s)"
        val = (studentName,QuizName,score,passcode,SubmissionID)
        mycursor.execute(sql,val)
        db.commit()
    except:
        print("Insert Student Record Fail")

def find_passcode_baseon_teacher_name(teacher_name):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    mycursor = db.cursor()
    list_of_passcode = []

    try:
        mycursor.execute('SELECT * FROM Quiz_Data')
        print("user_authentication check")
        for row in mycursor:
            if row[1] == teacher_name:
                list_of_passcode.append(row[0])

        return list_of_passcode
    except mysql.connector.Error:
        print("check find_gradebook_baseon_teacher_name failed")

def find_gradebook_baseon_name(name):
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    makeScoreRecord()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Score_Record')
    all_gradebook = []
    for row in mycursor:
        if row[0] == name:
            # 1.
            # Passcode,TeacherName,QuizName,Quiz -> quiz库

            # 2.
            # student1, cse331, 15, jesse
            # studentName,QuizName,score,passcode -> 分数库
            # 3.
            # user, list_of_passcode
            # 4.
            # user
            all_gradebook.append((row[1],row[2]))
    return all_gradebook

def print_score_record_table():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    makeScoreRecord()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Score_Record')
    for row in mycursor:
        print(row)
    print("print table Score_Record successfully")

def getInformation():
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    mycursor = db.cursor()
    try:
        print("1")
        mycursor.execute("SELECT * FROM Score_Record")
        print("2")
        myresult = mycursor.fetchall()
        print(myresult)
        return myresult
    except:
        print('No Score_Record Table !!!')

def obtainQuizName(passcode):

    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    db = mysql.connector.connect(
        host="oceanus",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )
    mycursor = db.cursor()

    try:
        mycursor.execute('SELECT * FROM Quiz_Data')
        print("user_authentication check")
        for row in mycursor:
            print('row[0]: ',row[0])
            print('row[1]:, ',row[1])
            print('row[2]:', row[2])
            if row[0] == passcode:
                return row[2]
        return None
    except mysql.connector.Error:
        print("check failed")


'''
Table1 users



Table2  Quiz_Data
Quiz -> {passcode,teachername,questions)
Passcode,TeacherName,QuizName,Quiz   -> Get the quiz base on the passcode



Table3  Score_Record    
studentName,QuizName,score,passcode,submissionID   -> record score

Table4 Submission  
when do we insert data to this table? When student submit their quit
[{"question1":["mult","actual question","student answer","point receive"], {"question2":["mult","actual question","student answer","point receive"]]
studentName,passcode, questions, submissionID 
'''
