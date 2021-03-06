from mysql.connector import(connection)
import mysql.connector

def connector():
    # return mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="ubcse442",
    #     database="QuizHub"
    # )
    return mysql.connector.connect(
        host="oceanus.cse.buffalo.edu",
        user="tingjiez",
        passwd="50380202",
        database="tingjiez_db"
    )

db = connector()
mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS tingjiez_db")


def print_user_table():
    db = connector()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        print(row)
    print("print successfully")


def creat_user_table():
    db = connector()
    mycursor = db.cursor()
    try:
        mycursor.execute("CREATE TABLE IF NOT EXISTS user (role VARCHAR(10),"
                         "username VARCHAR(20),"
                         "password VARCHAR(20),"
                         "email VARCHAR(48),"
                         "_ID int PRIMARY key AUTO_INCREMENT)")
    except mysql.connector.Error:
        print("creating fail")



def get_userEmail_baseon_name(name):
    db = connector()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        if row[1] == name:
            print("got email!")
            return row[3]

    return None

def insert_user(tuple):
    db = connector()
    mycursor = db.cursor()
    try:
        creat_user_table()
        print("tuple: ",tuple)
        mycursor.execute("INSERT INTO user (role,username,password,email) VALUES (%s,%s,%s,%s)", tuple)
        db.commit()
        print("insert successfully")
        mycursor.execute("SELECT * FROM user")

    except mysql.connector.Error:
        print("insert failed")

def get_role_baseon_name(name):
    db = connector()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        if row[1] == name:
            return row[0]
    return None

def username_is_not_exist(name):
    db = connector()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM user')
    for row in mycursor:
        if row[1] == name:
            return False
    return True


def user_authentication(name, pw):
    db = connector()
    mycursor = db.cursor()

    try:
        mycursor.execute('SELECT * FROM user')
        print("user_authentication check")
        for row in mycursor:

            if row[1] == name and row[2] == pw:

                return row[0]
        print("printing none")
        return None

    except mysql.connector.Error:
        print("check failed")


def create_quiz_table():
    db = connector()
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Quiz_Data (Passcode VARCHAR(10),"
                     "TeacherName VARCHAR(32),"
                     "QuizName VARCHAR(32),"
                     "Quiz VARCHAR(2048),"
                     "TimeLimit VARCHAR (20),"
                     "_ID int PRIMARY key AUTO_INCREMENT)")

def print_Quiz_Data():
    db = connector()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Quiz_Data')
    for row in mycursor:
        print(row)
    print("print table Quiz_Data successfully")

def insert_quiz(tuple):
    db = connector()

    mycursor = db.cursor()

    try:
        create_quiz_table()
        mycursor.execute("INSERT INTO Quiz_Data (Passcode,TeacherName,QuizName,Quiz,TimeLimit) VALUES (%s,%s,%s,%s,%s)",tuple)
        db.commit()
        mycursor.execute("SELECT * FROM Quiz_Data")
    except mysql.connector.Error:
        print("insert question failed")

def get_quiz_name_by_passcode(passcode):
    db = connector()
    mycursor = db.cursor()
    try:
        mycursor.execute('SELECT * FROM Quiz_Data')
        print("user_authentication check")
        for row in mycursor:
            if row[0] == passcode:
                return row[2]
        return None
    except mysql.connector.Error:
        print("check quiz name failed")

def find_quiz_data(passcode):
    db = connector()
    mycursor = db.cursor()

    try:
        mycursor.execute('SELECT * FROM Quiz_Data')
        print("user_authentication check")
        for row in mycursor:
            if row[0] == passcode:
                return row[3],row[4]


        return None
    except mysql.connector.Error:
        print("check quiz data failed")

def print_passcode():
    db = connector()

    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Quiz_Data')
    for row in mycursor:
        print(row)
    print("print passcode successfully")



def delete_score_record_table():
    db = connector()
    mycursor = db.cursor()
    mycursor.execute("DROP TABLE Score_Record")

def delete_quiz_data_table():
    db = connector()

    mycursor = db.cursor()
    mycursor.execute("DROP TABLE Quiz_Data")

def delete_user_table():
    db = connector()
    mycursor = db.cursor()
    mycursor.execute("DROP TABLE user")

def print_submission_table():
    db = connector()

    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Submission')
    for row in mycursor:
        print(row)
    print("print submission table successfully")

def delete_submission_table():
    db = connector()
    mycursor = db.cursor()
    mycursor.execute("DROP TABLE Submission")


def makeScoreRecord():
    db = connector()

    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Score_Record (studentName VARCHAR(2048),"
                 "QuizName VARCHAR(2048),"
                 "score VARCHAR(2048),"
                 "Passcode VARCHAR (10),"
                 "SubmissionID VARCHAR (10),"    
                 "_ID int PRIMARY key AUTO_INCREMENT)")

def insertScoreRecord(studentName,QuizName,score,passcode,SubmissionID):
    db = connector()
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
    db = connector()
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
    db = connector()
    makeScoreRecord()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Score_Record')
    all_gradebook = []
    for row in mycursor:
        if row[0] == name:
            all_gradebook.append((row[1],row[2],row[4]))
    return all_gradebook

def print_score_record_table():
    db = connector()
    makeScoreRecord()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Score_Record')
    for row in mycursor:
        print(row)
    print("print table Score_Record successfully")

def getInformation():
    db = connector()
    mycursor = db.cursor()
    try:
        mycursor.execute("SELECT * FROM Score_Record")
        myresult = mycursor.fetchall()

        return myresult
    except:
        print('No Score_Record Table !!!')

def obtainQuizName(passcode):

    db = connector()
    mycursor = db.cursor()

    try:
        mycursor.execute('SELECT * FROM Quiz_Data')
        print("user_authentication check")
        for row in mycursor:

            if row[0] == passcode:
                return row[2]
        return None
    except mysql.connector.Error:
        print("check failed")


def create_Submission_table():
    db = connector()
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Submission (studentName VARCHAR(32),"
                 "passcode VARCHAR(10),"
                 "studentAnswer VARCHAR(2048),"
                 "submissionID VARCHAR (10),"
                 "_ID int PRIMARY key AUTO_INCREMENT)")


def insertSubmission(studentName,passcode,studentAnwer,submissionID):
    db = connector()
    create_Submission_table()
    mycursor = db.cursor()
    try:

        sql = "INSERT INTO Submission (studentName,passcode,studentAnswer,submissionID) VALUES (%s,%s,%s,%s)"
        val = (studentName,passcode,studentAnwer,submissionID)
        mycursor.execute(sql,val)
        db.commit()
    except:
        print("Insert submission Fail")

def get_passcode_baseon_submissionID(id):
    db = connector()
    makeScoreRecord()
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM Score_Record')

    for row in mycursor:
        if row[4] == id:
            return row[3]
    print("get_passcode_baseon_submissionID fail. ID is not found")
    return None

def update_student_quiz(new_quiz,submissionID):
    db = connector()
    try:
        #sql = "INSERT INTO Score_Record (studentName,QuizName,score,Passcode,SubmissionID) VALUES (%s,%s,%s,%s,%s)"

        mycursor = db.cursor()

        sql = "UPDATE Submission SET studentAnswer = %s WHERE submissionID = %s "
        val = (new_quiz,submissionID)
        mycursor.execute(sql,val)
        db.commit()

    except:
        print("update_student_quiz fail")



def update_student_quizscore(name,passcode,newScore):
    db = connector()
    try:
        #sql = "INSERT INTO Score_Record (studentName,QuizName,score,Passcode,SubmissionID) VALUES (%s,%s,%s,%s,%s)"

        mycursor = db.cursor()
        sql = "UPDATE Score_Record SET score = %s WHERE studentName = %s And Passcode = %s"
        val = (newScore,name,passcode)
        mycursor.execute(sql,val)
        db.commit()



        print("score has been updated")
    except:
        print("update score fail")

def get_teacherName_baseon_passcode(passcode):
    db = connector()
    mycursor = db.cursor()
    try:
        mycursor.execute('SELECT * FROM Quiz_Data')

        for row in mycursor:
            if row[0] == passcode:
                return row[1]

        print("In get_teacherName_baseon_passcode, passcode is not found")
        return None
    except mysql.connector.Error:
        print("check get_teacherName_baseon_passcode failed")


def get_studentName_And_passcode_baseon_submissionID(id):
    db = connector()

    mycursor = db.cursor()
    create_Submission_table()
    print("checking studentAnswer")
    try:
        mycursor.execute('SELECT * FROM Submission')
        for row in mycursor:

            if row[3] == id:
                return row[0],row[1]
        return None
    except mysql.connector.Error:
        print("check submission table failed")

def get_studentAnswer_baseon_submissionID(id):
    db = connector()

    mycursor = db.cursor()
    create_Submission_table()
    print("checking studentAnswer: "+str(id))
    try:
        mycursor.execute('SELECT * FROM Submission')
        for row in mycursor:
            print("row",row)
            if row[3] == id:
                return row[2]
        return None
    except mysql.connector.Error:
        print("check submission table failed")





'''
Table1 users



Table2  Quiz_Data
Quiz -> {passcode,teachername,questions)
Passcode,TeacherName,QuizName,Quiz, TimeLimit   -> Get the quiz base on the passcode



Table3  Score_Record    
studentName,QuizName,score,passcode,submissionID   -> record score

Table4 Submission  
when do we insert data to this table? When student submit their quit
[{"question1":["mult","actual question","student answer","point receive"], {"question2":["mult","actual question","student answer","point receive"]]
studentName,passcode, questions, submissionID 
'''
