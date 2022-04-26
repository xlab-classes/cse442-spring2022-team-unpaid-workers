import mysql.connector
def getYourDatabase():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Shkaraot99@",
        database="QuizHub"
    )

    return db

