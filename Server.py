'''
Coder: Zhou Zhou  && Shkaraot
'''
import DataBase
from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableMultiDict

from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def index():

    return render_template("HomePage.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    print("signup")
    imd = ImmutableMultiDict(request.form)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")[0]
    password = dict.get("Password")[0]
    role = dict.get("who")[0]

    if DataBase.username_is_not_exist(name):
        DataBase.insert_user((role,name,password))
        return render_template("HomePage.html")
    else:
        return "username is exist, pick another one."




@app.route('/user', methods=['POST', 'GET'])
def user():



    imd = ImmutableMultiDict(request.form)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")[0]
    password = dict.get("Password")[0]




    # if username+password is not match
    role = DataBase.user_authentication(name,password)

    #"student" "teacher" "none"
    if role is None:
        return "Your username or password is incorrect"
    elif role == "Student":
        #jump to student profile
        return "Student: "+name
    elif role == "Teacher":
        #jump to teacher profile
        return "Teacher: "+name

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
    DataBase.creat_user_table()


