'''
Coder: Zhou Zhou  && Shkaraot
'''

import DataBase
from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)


@app.route('/')
def index():
    print("print table")
    DataBase.print_user_table()

    return render_template("index.html")


@app.route('/findquiz', methods = ['POST','GET'])
def findquiz():
    return "hello"

@app.route('/makequiz', methods = ['POST','GET'])
def quiz():

    if request.method == 'POST':
        result = request.form
        data = ImmutableMultiDict(request.form)
        dict = data.to_dict(flat=False)
        question = dict.get("Question")[0]
        answer = dict.get("Answer")[0]
        DataBase.insert_question((question,answer))
        return render_template("result.html",s= question+"\n"+answer)
    else:

        #return render_template("result.html",s = question+answer)
        return render_template("teacher_or_studentquiz.html",s='Teacher',question='Make Your Questions')

@app.route('/new', methods=['POST', 'GET'])
def new():
    return render_template("Signup.html")

@app.route('/Signup', methods=['POST', 'GET'])
def Signup():
    print("in signup")
    imd = ImmutableMultiDict(request.form)
    print("imd:", imd)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")[0]
    password = dict.get("Password")[0]
    role = dict.get("who")[0]

    if DataBase.username_is_not_exist(name):
        DataBase.insert_user((role,name,password))
        print("template")
        return render_template("signup.html")
    else:
        print("redirect to error")
        return redirect("http://localhost:63342/cse442-spring2022-team-unpaid-workers/templates/Signup.html?_ijt=s7rqo2hienhphcdu4968qssg9l&_ij_reload=RELOAD_ON_SAVE&error=username",code = 301)

@app.route('/user', methods=['POST', 'GET'])
def user():

    print("user")

    imd = ImmutableMultiDict(request.form)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")[0]
    password = dict.get("Password")[0]

    # if username+password is not match

    role = DataBase.user_authentication(name,password)

    if DataBase.username_is_not_exist(name):
        return redirect("http://localhost:9377/?error=username",code = 301)
    elif role is None:
        return redirect("http://localhost:9377/?error=password",code = 301)
    elif role == "Student":
        #jump to student profile
        return render_template('teacher_or_student_homepage.html',s='Student')
    elif role == "Teacher":
        #jump to teacher profile
        return render_template('teacher_or_student_homepage.html',s='Teacher')

if __name__ == '__main__':

    DataBase.creat_user_table()
    app.run(host='0.0.0.0',port=9377,debug=True)






