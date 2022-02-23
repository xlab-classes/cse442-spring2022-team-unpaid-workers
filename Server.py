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
    print("home")
    return render_template("HomePage.html")


@app.route('/user/', methods=['POST', 'GET'])
def result():


    if request.method == "POST":
        print("its post")

    imd = ImmutableMultiDict(request.args)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")
    password = dict.get("Password")


    # if username+password is not match
    role = DataBase.user_authentication(name,password)
    if role is None:
        return "Your username or password is incorrect"
    elif role == "student":
        #jump to student profile
        return "Student: "+name
    elif role == "teacher":
        #jump to teacher profile
        return "Teacher: "+name

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
    DataBase.creat_user_table()

    if DataBase.username_is_not_exist("kylin"):
        DataBase.insert_user(("student", "kylin", "123"))
    else:
        # username is existed, choose another username
        1
