'''
Coder: Zhou Zhou  && Shkaraot
'''

import DataBase
from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict
import random
import string
import json

app = Flask(__name__)


@app.route('/')
def index():
    print("print table")
    DataBase.print_user_table()
    return render_template("index.html")


@app.route('/quiz_submit',methods=['POST','GET'])
def quiz_submit():
    if request.method == "POST":
        data = ImmutableMultiDict(request.form)
        passcode = data.get("passcode")
        json_quiz = DataBase.find_quiz(passcode)
        quiz = json.loads(json_quiz)
        student_score = 0

        for student_question_submission in data:
            question_number = get_question_number(student_question_submission)
            print(question_number)
            student_choice = data.get(student_question_submission)
            answer = quiz[question_number-1].get("answer")[0]
            if student_choice == answer:
                student_score += int(quiz[question_number-1].get("point")[0])-int('0')
        f = open("templates/student_homepage.html","r")
        t = ""
        for line in f:
            t += line
        start_pos = t.find('<p>Passcode:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Score:</p>')+len('<p>Passcode:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Score:</p>')
        score_template = '<p>'+passcode+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(student_score)+"<p>"
        final_template = t[:start_pos]+score_template+t[start_pos+1:]
        return  final_template
    else:
        return "quiz"

def get_question_number(q):
    n = 0
    for i in range(8,len(q)):
        n = n*10 + int(q[i])- int('0')
    return n


@app.route('/teacher_grade_book', methods=['GET'])
def teacherGrade():

    return render_template("teacher_grade_book.html")


@app.route('/accessQuiz', methods=['POST', 'GET'])
def accessQuiz():
    if request.method == "POST":
        data = ImmutableMultiDict(request.form)
        dict = data.to_dict(flat=False)
        passcode = dict.get("Access Code")[0]
        DataBase.print_passcode()
        json_quiz = DataBase.find_quiz(passcode)
        if json_quiz is None:
            return "passcode " + str(passcode) + "is not exist in the database"
        full_quiz = json.loads(json_quiz)
        quiz_template = ""
        final_template = ""
        f = open("templates/quiz.html", "r")
        for line in f:
            final_template += line

        start_pos = final_template.find("<p>Question1:</p>")
        end_pos = final_template.find("<input type=\"submit\" value=\"Submit\">")

        quiz_number = 0
        for quiz in full_quiz:
            quiz_number += 1
            question = quiz.get("question")[0]
            answer = quiz.get('answer')[0]
            point = quiz.get('point')[0]
            choice_A = quiz.get('choice_A')[0]
            choice_B = quiz.get('choice_B')[0]
            choice_C = quiz.get('choice_C')[0]
            choice_D = quiz.get('choice_D')[0]


            template1 = "<p> " + question + " (" + point + "pts) </p>\n"
            template2 = "<input type=\"radio\" id=\""+str(quiz_number)+"a\" name=\"question"+str(quiz_number)+"\" value=\"" + choice_A+"\">\n"
            template3 = '<label for="' + str(quiz_number)+'a">' + choice_A + '</label><br>\n'

            template4 = "<input type=\"radio\" id=\""+str(quiz_number)+"b\" name=\"question"+str(quiz_number)+"\" value=\"" + choice_B+"\">\n"
            template5 = '<label for="' + str(quiz_number)+'b">' + choice_B + '</label><br>\n'

            template6 = "<input type=\"radio\" id=\""+str(quiz_number)+"c\" name=\"question"+str(quiz_number)+"\" value=\"" + choice_C+"\">\n"
            template7 = '<label for="' + str(quiz_number)+'c">' + choice_C + '</label><br>\n'

            template8 = "<input type=\"radio\" id=\""+str(quiz_number)+"d\" name=\"question"+str(quiz_number)+"\" value=\"" + choice_D+"\">\n"
            template9 = '<label for="' + str(quiz_number)+'d">' + choice_D + '</label><br>\n'
            template10 = '<br><br>'
            quiz_template += template1 + template2 + template3 + template4 + template5 + template6 + template7 + template8 + template9 + template10
        quiz_template += '<input value="' + passcode + '" name="passcode" hidden>'
        final_template = final_template[:start_pos] + quiz_template + final_template[end_pos:]
        return final_template

    return "quiz"


@app.route('/buildQuiz', methods=['POST', 'GET'])
def buidQuiz():
    if request.method == 'POST':

        data = ImmutableMultiDict(request.form)
        dict = data.to_dict(flat=False)
        dic_length = len(dict)
        key_list = list(dict)
        full_quiz = []
        for i in range(0, dic_length - 1, 7):
            question = {"question": dict.get(key_list[i])}
            answer = {"answer": dict.get(key_list[i + 1])}
            point = {"point": dict.get(key_list[i + 2])}
            a = {"choice_A": dict.get(key_list[i + 3])}
            b = {"choice_B": dict.get(key_list[i + 4])}
            c = {"choice_C": dict.get(key_list[i + 5])}
            d = {"choice_D": dict.get(key_list[i + 6])}
            quiz = {}
            for d in (question, answer, point, a, b, c, d):
                quiz.update(d)
            full_quiz.append(quiz)

        if dict.get('build quiz') is None:

            f = open("templates/teacher_or_studentquiz.html", "r")
            t = ""
            for line in f:
                t += line
            start_pos = t.find("<p>Question1 <input type =")
            end_pos = t.find("<p><input type = \"submit\" value")  # security risk
            quiz_template = ""
            i = 1
            for q in full_quiz:
                question_template = "<p>Question" + str(i) + " <input type = \"text\" name = \"Question_" + str(
                    i) + "\"" + " size=\"120\" " + "value=\"" + q.get("question")[0] + "\"/></p>" + "\n\t\t\t\t"
                answer_template = "<p>Answer" + " <input type = \"text\" name = \"Answer_" + str(
                    i) + "\"" + " size=\"12\" " + "value=\"" + q.get("answer")[0] + "\"/></p>" + "\n\t\t\t\t"
                point_template = "<p>Point Worth" + " <input type = \"text\" name = \"Point_" + str(
                    i) + "\"" + " size=\"12\" " + "value=\"" + q.get("point")[0] + "\"/></p>" + "\n\t\t\t\t"
                choice_a_template = "<p>ChoiceA" + " <input type = \"text\" name = \"Choice_A_" + str(
                    i) + "\"" + " size=\"120\" " + "value=\"" + q.get("choice_A")[0] + "\"/></p>" + "\n\t\t\t\t"
                choice_b_template = "<p>ChoiceB" + " <input type = \"text\" name = \"Choice_B_" + str(
                    i) + "\"" + " size=\"120\" " + "value=\"" + q.get("choice_B")[0] + "\"/></p>" + "\n\t\t\t\t"
                choice_c_template = "<p>ChoiceC" + " <input type = \"text\" name = \"Choice_C_" + str(
                    i) + "\"" + " size=\"120\" " + "value=\"" + q.get("choice_C")[0] + "\"/></p>" + "\n\t\t\t\t"
                choice_d_template = "<p>ChoiceD" + " <input type = \"text\" name = \"Choice_D_" + str(
                    i) + "\"" + " size=\"120\" " + "value=\"" + q.get("choice_D")[0] + "\"/></p>" + "\n\t\t\t\t"
                quiz_template = quiz_template + question_template + answer_template + point_template + choice_a_template + choice_b_template + choice_c_template + choice_d_template + "<br><br>"
                i += 1

            new_question_template = "<p>Question" + str(i) + " <input type = \"text\" name = \"Question_" + str(
                i) + "\"" + " size=\"120\" " + "\"/></p>" + "\n"
            new_answer_template = "<p>Answer" + " <input type = \"text\" name = \"Answer_" + str(
                i) + "\"" + " size=\"12\" " + "\"/></p>" + "\n"
            new_point_template = "<p>Point Worth" + " <input type = \"text\" name = \"Point_" + str(
                i) + "\"" + " size=\"12\" " + "\"/></p>" + "\n"
            new_choice_a_template = "<p>ChoiceA" + " <input type = \"text\" name = \"Choice_A_" + str(
                i) + "\"" + " size=\"120\" " + "\"/></p>" + "\n"
            new_choice_b_template = "<p>ChoiceB" + " <input type = \"text\" name = \"Choice_B_" + str(
                i) + "\"" + " size=\"120\" " + "\"/></p>" + "\n"
            new_choice_c_template = "<p>ChoiceC" + " <input type = \"text\" name = \"Choice_C_" + str(
                i) + "\"" + " size=\"120\" " + "\"/></p>" + "\n"
            new_choice_d_template = "<p>ChoiceD" + " <input type = \"text\" name = \"Choice_D_" + str(
                i) + "\"" + " size=\"120\" " + "\"/></p>" + "\n"
            new_quiz_template = new_question_template + new_answer_template + new_point_template + new_choice_a_template + new_choice_b_template + new_choice_c_template + new_choice_d_template

            template = t[:start_pos] + quiz_template + new_quiz_template + t[end_pos:]

            return template

        else:
            # load full quiz into database
            passcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            f = open("templates/teacher_homepage.html", "r")
            t = ""
            for line in f:
                t += line
            start_pos = t.find("<p>Passcode: (Newest on the top)</p>") + len("<p>Passcode: (Newest on the top)</p>")
            template = t[:start_pos] + "\r" + passcode + t[start_pos + 1:]
            json_quiz = json.dumps(full_quiz)
            DataBase.insert_quiz((passcode, json_quiz))

            return template
    else:
        return render_template("teacher_or_studentquiz.html")


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
        DataBase.insert_user((role, name, password))
        print("template")
        return render_template("signup.html")
    else:
        print("redirect to error")
        return redirect(
            "http://localhost:63342/cse442-spring2022-team-unpaid-workers/templates/Signup.html?_ijt=s7rqo2hienhphcdu4968qssg9l&_ij_reload=RELOAD_ON_SAVE&error=username",
            code=301)


@app.route('/user', methods=['POST', 'GET'])
def user():
    print("user")

    imd = ImmutableMultiDict(request.form)
    dict = imd.to_dict(flat=False)
    name = dict.get("Name")[0]
    password = dict.get("Password")[0]

    # if username+password is not match

    role = DataBase.user_authentication(name, password)

    if DataBase.username_is_not_exist(name):
        return redirect("http://localhost:9377/?error=username", code=301)
    elif role is None:
        return redirect("http://localhost:9377/?error=password", code=301)
    elif role == "Student":
        # jump to student profile
        return render_template('student_homepage.html', s='Student')
    elif role == "Teacher":
        # jump to teacher profile
        return render_template('teacher_homepage.html', s='Teacher')


if __name__ == '__main__':
    DataBase.creat_user_table()
    app.run(host='0.0.0.0', port=9377, debug=True)
