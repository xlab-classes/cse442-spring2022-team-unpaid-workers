'''
Coder: Zhou Zhou  && Shkaraot
'''
import tkinter

import DataBase
from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict
from tkinter import messagebox

app = Flask(__name__)

@app.route('/makequiz', methods = ['POST','GET'])
def quiz():
    print('makeQuiz')
    if request.method == 'POST':
        result = request.form
        render_template("result.html")
    else:
        return render_template("teacher_or_studentquiz.html",s='Teacher',question='Make Your Questions')

@app.route('/')
def index():
    print('homepage')
    return render_template("HomePage.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    print("in signup")
    imd = ImmutableMultiDict(request.form)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")[0]
    password = dict.get("Password")[0]
    role = dict.get("who")[0]

    if DataBase.username_is_not_exist(name):
        DataBase.insert_user((role,name,password))
        print("signuphere")
        return render_template("HomePage.html")
    else:
        print("redirect to error")
        return redirect("http://localhost:63342/cse442-spring2022-team-unpaid-workers/templates/Signup.html?_ijt=s7rqo2hienhphcdu4968qssg9l&_ij_reload=RELOAD_ON_SAVE&error=username",code = 301)

@app.route('/user', methods=['POST', 'GET'])
def user():
    imd = ImmutableMultiDict(request.form)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")[0]
    password = dict.get("Password")[0]

    # if username+password is not match
    role = DataBase.user_authentication(name,password)
    print(DataBase.username_is_not_exist(name))
    #"student" "teacher" "none"
    if DataBase.username_is_not_exist(name):
        return redirect("http://localhost:8000/?error=username",code = 301)
    elif role is None:
        return redirect("http://localhost:8000/?error=password",code = 301)
    elif role == "Student":
        #jump to student profile
        return render_template('teacher_or_student_homepage.html',s='Student')
    elif role == "Teacher":
        #jump to teacher profile
        return render_template('teacher_or_student_homepage.html',s='Teacher')

if __name__ == '__main__':
    DataBase.creat_user_table()
    app.run(host='0.0.0.0',port=8000,debug=True)


