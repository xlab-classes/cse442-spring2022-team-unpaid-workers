'''
Coder: Zhou Zhou  && Shkaraot
'''
import time

import DataBase
from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict
import random
import string
import json
import smtplib

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    print("print table")
    DataBase.print_user_table()
    return render_template("index.html")

@app.route('/updateQuiz', methods=['POST', 'GET'])
def sendEmailNotification(studentName,studentEmail,examName,studentScore):
    gmail_user = 'kylinzh7798@gmail.com'
    gmail_password = "nzl980107"

    sent_from = gmail_user
    to = [studentEmail]
    SUBJECT = examName +' score is out!'
    TEXT = "Hi, "+studentName+"\nYour score is "+str(studentScore)

    email_text = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)

def updateQuiz():
    data = dict(request.form)

    newScore = 0
    i = 0
    name, passcode = DataBase.get_studentName_And_passcode_baseon_submissionID(data['ID'])
    student_answer = json.loads(DataBase.get_studentAnswer_baseon_submissionID(data['ID']))

    print("answer: ", student_answer)

    for k, v in data.items():
        if k != 'ID' and k != 'Update Quiz' and k != 'username':
            newScore += int(v)
            print(i)
            print(type(student_answer))
            print(type(student_answer[i][3]))
            print(type(student_answer[i]))
            student_answer[i][3] = v
            i += 1

    print("ret: ", DataBase.update_student_quiz(json.dumps(student_answer), data['ID']))

    DataBase.update_student_quizscore(name, passcode, newScore)
    username = data.get("username")
    role = DataBase.get_role_baseon_name(username)
    if role == "Teacher":
         sendEmailNotification(name,DataBase.get_userEmail_baseon_name(name),DataBase.get_quiz_name_by_passcode(passcode),newScore)

    return redirect("/homePage/" + username, code=301)

@app.route('/submission/<role>/<id>', methods=['POST', 'GET'])
def studentSubmission(role, id):
    # submission = {"question1":["actual answer","sudent answer","point receive","point worth"]}
    submission_str = DataBase.get_studentAnswer_baseon_submissionID(id)
    print("id", id)
    if role == "student":
        submission = json.loads(submission_str)
        with open("templates/submission.html", "r") as f:
            t = f.read()
        t = t.replace("submissionID", id)
        template = ""
        i = 0
        startPos = t.find("<h3>{{Question_Name}}: </h3>")
        endPos = t.find('<input value="username123" name="username" hidden>')
        print("subm:", submission)
        print("type: ", type(submission))
        for s in submission:
            i += 1
            questionName = s[0]
            actual_answer = s[1]
            student_answer = s[2]
            point_receive = s[3]
            point_worth = s[4]
            template += "<h3>" + str(i) + ". " + questionName + "</h3>" + "\n"
            template += "<p>Correct Answer: " + actual_answer + "</p >" + "\n"
            template += "<p>Student Answer: " + student_answer + "</p >" + "\n"
            template += "<label>Point Worth : <input type = \"text\" name = \"Choice" + str(
                i) + "\" size=\"3\" value=\"" + point_receive + "\" readonly/>/" + point_worth + "</label>" + "\n"
            template += "<br>" + "\n" + "<br>" + "\n"

        name = DataBase.get_studentName_And_passcode_baseon_submissionID(id)[0]
        final_temp = t[:startPos] + template + t[endPos:]
        final_temp = final_temp.replace("username123", name)
        return final_temp

    else:
        submission = json.loads(submission_str)
        with open("templates/submission.html", "r") as f:
            t = f.read()
        t = t.replace("submissionID", id)
        template = ""
        i = 0
        startPos = t.find("<h3>{{Question_Name}}: </h3>")
        endPos = t.find('<input value="username123" name="username" hidden>')
        print("type: ", type(submission))
        for s in submission:
            print("s: ", s)
            i += 1
            questionName = s[0]
            actual_answer = s[1]
            student_answer = s[2]
            point_receive = s[3]
            point_worth = s[4]
            template += "<h3>" + str(i) + ". " + questionName + "</h3>" + "\n"
            template += "<p>Correct Answer: " + actual_answer + "</p >" + "\n"
            template += "<p>Student Answer: " + student_answer + "</p >" + "\n"
            template += "<label>Point Worth : <input type = \"text\" name = \"Choice" + str(
                i) + "\" size=\"3\" value=\"" + point_receive + "\" />/" + point_worth + "</label>" + "\n"
            template += "<br>" + "\n" + "<br>" + "\n"
        passcode = DataBase.get_passcode_baseon_submissionID(id)
        name = DataBase.get_teacherName_baseon_passcode(passcode)
        final_temp = t[:startPos] + template + t[endPos:]
        final_temp = final_temp.replace("username123", name)
        return final_temp

@app.route('/quiz_submit', methods=['POST', 'GET'])
def quiz_submit():
    if request.method == "POST":
        data = dict(request.form)
        studentName = data.get("studentName")
        print('Data:', data)

        passcode = data.get("passcode")

        quizName = DataBase.obtainQuizName(passcode)
        json_quiz = DataBase.find_quiz_data(passcode)[0]
        print("json quiz:", json_quiz[0])
        quiz = json.loads(json_quiz)
        student_score = 0
        print("quiz:", quiz)
        idx = 0
        studentAnswer = []
        for k, v in data.items():
            if k == 'passcode':
                break

            # studentAnswer = [questionName,questionAnswer,studentAnswer, pointGain, pointTotal
            if v == quiz[idx]["answer"][0]:
                student_score += int(quiz[idx]['point'][0])
                studentAnswer.append(
                    [quiz[idx]["question"][0], quiz[idx]["answer"][0], v, quiz[idx]["point"][0], quiz[idx]["point"][0]])
            else:
                studentAnswer.append([quiz[idx]["question"][0], quiz[idx]["answer"][0], v, "0", quiz[idx]["point"][0]])

            idx += 1
        SubmissionID = ''.join(random.choices(string.ascii_lowercase, k=8))
        DataBase.insertScoreRecord(data.get('studentName'), quizName, student_score, passcode, SubmissionID)
        DataBase.insertSubmission(data.get("studentName"), passcode, json.dumps(studentAnswer), SubmissionID)

        return redirect("/homePage/"+studentName,code=301)

@app.route('/accessQuiz', methods=['POST', 'GET'])
def accessQuiz():
    if request.method == "POST":
        data = ImmutableMultiDict(request.form)

        dict = data.to_dict(flat=False)
        passcode = dict.get("Access Code")[0]
        studentName = dict.get("User Name")[0]

        DataBase.print_passcode()

        json_quiz, time_limit = DataBase.find_quiz_data(passcode)

        if json_quiz is None:
            return "passcode " + str(passcode) + "is not exist in the database"
        full_quiz = json.loads(json_quiz)

        quiz_template = ""
        final_template = ""
        f = open("templates/quiz.html", "r")
        for line in f:
            final_template += line

        final_template = final_template.replace("999999", time_limit)
        start_pos = final_template.find("<p>Question1:</p>")
        end_pos = final_template.find('<input type="submit" value="Submit" >')
        print("end_pos ", end_pos)
        quiz_number = 0

        for quiz in full_quiz:
            quiz_number += 1
            question = quiz.get("question")[0]
            question_type = quiz.get("type")
            answer = quiz.get('answer')[0]
            point = quiz.get('point')[0]

            if question_type == "Multiple_Choice":

                choice_A = quiz.get('choice_A')[0]
                choice_B = quiz.get('choice_B')[0]
                choice_C = quiz.get('choice_C')[0]
                choice_D = quiz.get('choice_D')[0]

                template1 = "<p> " + str(quiz_number) + ". " + question + " (" + point + "pts) </p>\n"
                template2 = "<input type=\"radio\" id=\"" + str(quiz_number) + "a\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + choice_A + "\">\n"
                template3 = '<label for="' + str(quiz_number) + 'a">' + choice_A + '</label><br>\n'

                template4 = "<input type=\"radio\" id=\"" + str(quiz_number) + "b\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + choice_B + "\">\n"
                template5 = '<label for="' + str(quiz_number) + 'b">' + choice_B + '</label><br>\n'

                template6 = "<input type=\"radio\" id=\"" + str(quiz_number) + "c\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + choice_C + "\">\n"
                template7 = '<label for="' + str(quiz_number) + 'c">' + choice_C + '</label><br>\n'

                template8 = "<input type=\"radio\" id=\"" + str(quiz_number) + "d\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + choice_D + "\">\n"
                template9 = '<label for="' + str(quiz_number) + 'd">' + choice_D + '</label><br>\n'
                template10 = '<br><br>'
                quiz_template += template1 + template2 + template3 + template4 + template5 + template6 + template7 + template8 + template9 + template10

            elif question_type == "True_or_False":
                template1 = "<p> " + str(quiz_number) + ". " + question + " (" + point + "pts) </p>\n"
                template2 = "<input type=\"radio\" id=\"" + str(quiz_number) + "a\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + 'T' + "\">\n"
                template3 = '<label for="' + str(quiz_number) + 'a">' + "True" + '</label><br>\n'

                template4 = "<input type=\"radio\" id=\"" + str(quiz_number) + "b\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + 'F' + "\">\n"
                template5 = '<label for="' + str(quiz_number) + 'b">' + "False/" + '</label><br>\n'
                quiz_template += template1 + template2 + template3 + template4 + template5 + '<br><br>'

            elif question_type == "Short_Answer":
                template1 = "<p> " + str(quiz_number) + ". " + question + " (" + point + "pts) </p>\n"
                template2 = "<div class=\"form-group\">" + '\n' + "<label for=\"comment\">Short Question_Answer:</label>" + "<textarea class=\"form-control\" name=\"Answer_" + str(
                    quiz_number) + "\" rows=\"5\" id=\"comment\" required></textarea></div>";
                quiz_template += template1 + template2 + '<br><br>'

        quiz_template += '<input value="' + passcode + '" name="passcode" hidden>'
        quiz_template += '<input value="' + studentName + '" name="studentName" hidden>'
        final_template = final_template[:start_pos] + quiz_template + final_template[end_pos:]

        return final_template

@app.route('/buildQuiz', methods=['POST', 'GET'])
def buidQuiz():
    # need change, we now have question type
    if request.method == 'POST':

        data = ImmutableMultiDict(request.form)

        dict = data.to_dict(flat=False)
        print("dictionary：", dict)

        dic_length = len(dict)
        key_list = list(dict)
        full_quiz = []
        quizname = dict.get("Quiz_name")[0]
        hr = dict.get('Time_Limit_hr')[0]

        min = dict.get('Time_Limit_min')[0]

        teacher_name = dict.get("name")[0]
        print(dict)
        print("teachername: ", teacher_name)
        i = 3
        print("keylist: ", key_list)
        while i < (dic_length - 2):

            type = dict.get(key_list[i + 1])[0]
            if type == "Multiple_Choice":
                question = {"question": dict.get(key_list[i])}
                question_type = {"type": type}

                point = {"point": dict.get(key_list[i + 2])}

                answer = {"answer": dict.get(key_list[i + 3])}
                print(question, answer, point)
                a = {"choice_A": dict.get(key_list[i + 4])}
                b = {"choice_B": dict.get(key_list[i + 5])}
                c = {"choice_C": dict.get(key_list[i + 6])}
                d = {"choice_D": dict.get(key_list[i + 7])}
                quiz = {}
                for d in (question, question_type, answer, point, a, b, c, d):
                    quiz.update(d)
                full_quiz.append(quiz)
                i += 8
            elif type == "True_or_False":
                question = {"question": dict.get(key_list[i])}
                question_type = {"type": type}
                point = {"point": dict.get(key_list[i + 2])}
                answer = {"answer": dict.get(key_list[i + 3])[0]}
                quiz = {}
                for d in (question, question_type, point, answer):
                    quiz.update(d)
                full_quiz.append(quiz)
                i += 4
            elif type == "Short_Answer":
                question = {"question": dict.get(key_list[i])}
                question_type = {"type":type}
                point = {"point": dict.get(key_list[i + 2])}
                answer = {"answer": dict.get(key_list[i + 3])}
                quiz = {}
                for d in (question,question_type,answer, point):
                    quiz.update(d)
                full_quiz.append(quiz)
                i += 4
            elif type == "Essay_Question":

                question = {"question": dict.get(key_list[i])}
                question_type = {"type": type}
                point = {"point": dict.get(key_list[i + 2])}
                row = dict.get(key_list[i + 3])[0]
                col = dict.get(key_list[i + 4])[0]
                total = int(row) * int(col)
                rubric = [row, col]
                for j in range(i+5,i+5+total):
                    rubric.append(dict.get(key_list[j])[0])

                i += total + 5
                answer = {"answer": rubric}
                print("ans: ",answer)
                quiz = {}
                for d in (question, question_type, answer, point):
                    quiz.update(d)
                full_quiz.append(quiz)

        name = dict.get('Quiz_name')[0]

        if dict.get('build quiz') is None:
            print("add question: ", full_quiz)
            f = open("templates/teacher_quiz_generate.html", "r")
            t = ""
            for line in f:
                t += line
            t = t.replace("teacher_name", teacher_name)
            start_pos = t.find('<label style="color: white">Question1')

            end_pos = t.find(
                ' <p><input type = "submit" value = "Build Quiz" name="build quiz" style="color: black"/></p >')  # security risk
            quiz_template = ""

            i = 1
            js_template = ""

            quizName_template = '<input type = "text" name = "Quiz_name" size="120" value="' + name + '"'
            time_hour_template = '<input type = "text" id="time_limit_hour" name = "Time_Limit_hr" size="100" value="' + hr + '"'
            time_min_template = '<input type = "text" id="time_limit_min" name = "Time_Limit_min" size="100" value="' + min + '"'
            print("len:",len(full_quiz))
            for q in full_quiz:

                js_template += '<script>' + '\n'
                js_template += 'var x' + str(i) + ' = document.getElementById("option' + str(i) + '");' + '\n'
                js_template += 'x' + str(i) + '.addEventListener("change", myFunction' + str(i) + ');' + '\n'
                js_template += 'function myFunction' + str(i) + '() {' + '\n'
                js_template += 'if (x' + str(i) + '.value == "Multiple_Choice"){' + '\n'
                js_template += 'document.getElementById("question_content' + str(i) + '").innerHTML =' + '\n'
                js_template += '"<label style=\\"color: white\\" >Answer : <input type = \\"text\\" name = \\"Answer_' + str(
                    i) + '\\" size=\\"12\\" required/></label >" +\n'
                js_template += '"<br>"+\n'
                js_template += '"<label style=\\"color: white\\">ChoiceA <input type = \\"text\\" name = \\"Choice_A_' + str(
                    i) + '\\" size=\\"120\\" required/></label >" +\n'
                js_template += '"<label style=\\"color: white\\">ChoiceB <input type = \\"text\\" name = \\"Choice_B_' + str(
                    i) + '\\" size=\\"120\\" required/></label >" +\n'
                js_template += '"<label style=\\"color: white\\">ChoiceC <input type = \\"text\\" name = \\"Choice_C_' + str(
                    i) + '\\" size=\\"120\\" required/></label >" +\n'
                js_template += '"<label style=\\"color: white\\">ChoiceD <input type = \\"text\\" name = \\"Choice_D_' + str(
                    i) + '\\" size=\\"120\\" required/></label >" ;\n'
                js_template += '}' + '\n'
                js_template += 'else if (x' + str(i) + '.value == "Short_Answer"){' + '\n'
                js_template += 'document.getElementById("question_content' + str(i) + '").innerHTML = \n'
                js_template += '"<div class=\\"form-group\\">" +\n'
                js_template += '"<label style=\\"color: white\\" for=\\"comment\\">Short Question_Answer:</label>" +\n'
                js_template += '"<textarea class=\\"form-control\\" name=\\"Answer_' + str(
                    i) + '\\" rows=\\"5\\" id=\\"comment\\" required></textarea></div>";\n'
                js_template += '}' + '\n'
                js_template += 'else if (x' + str(i) + '.value == "Essay_Question"){' + '\n'
                js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML = \n'
                js_template += '"<div class=\\"form-group\\">" +\n'
                js_template += '"<input type = \\"text\\" id=\\"row_text\\" name = \\"row\\" value=\\"0\\" hidden/>" +\n'
                js_template += '"<input type = \\"text\\" id=\\"col_text\\" name = \\"col\\" value=\\"0\\" hidden/>" +\n'
                js_template += '"<label style=\\"color: white\\">Row:</label><input type=\\"number\\" id=\\"row\\" min=\\"1\\" max=\\"5\\" style=\\"color: #1b1b1b\\" required> X "+\n '
                js_template += '"<label style=\\"color: white\\">Column:</label><input type=\\"number\\" id=\\"col\\" min=\\"1\\" max=\\"5\\"  style=\\"color: #1b1b1b\\" required> " +\n'
                js_template += '"<button onclick=\\"displayTable()\\" style=\\"color: #1b1b1b\\" id=\\"update\\" type=\\"button\\">Create Rubric</button>" +\n'
                js_template += '"<table id=\\"rubric\\"></table>" +\n'
                js_template += '"</div>";}'

                js_template += 'else{' + '\n'
                js_template += 'document.getElementById("question_content' + str(i) + '").innerHTML = \n'
                # js_template += '"<label>Answer : <input type = \\"text\\" name = \\"Answer_'+str(i)+'\\" size=\\"12\\"/></label >" +\n'
                js_template += '"<br>" +\n'
                js_template += '"<label style=\\"color: white\\"> T/F answer:</label>" +\n'
                js_template += '"<br>" +\n'
                js_template += '"<input type=\\"radio\\" id=\\"T\\" name=\\"T/F_' + str(
                    i) + '\\" value=\\"True\\" required>" +\n'
                js_template += '"<label style=\\"color: white\\" for=\\"T\\">True</label>" +\n'
                js_template += '"<br>" +\n'
                js_template += '"<input type=\\"radio\\" id=\\"F\\" name=\\"T/F_' + str(
                    i) + '\\" value=\\"False\\">" +\n'
                js_template += '"<label style=\\"color: white\\" for=\\"F\\">False</label><br>"; \n'
                js_template += '}' + '\n'
                js_template += '}' + '\n'
                js_template += '</script>' + '\n'
                js_template += '\n'

                if q.get("type") == "Multiple_Choice":
                    quiz_template += '<label style=\"color: white\"> Question' + str(i) + ' <input type = "text" name = "Question_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + dict.get("Question_" + str(i))[
                                         0] + '" required/></label >' + "<br>" + "\n"
                    quiz_template += '<label style=\"color: white\" for="option' + str(i) + '">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type' + str(i) + '" id="option' + str(
                        i) + '" value="Multiple_Choice" >' + '\n'
                    quiz_template += '<option  value="Multiple_Choice" selected>Multiple Choice</option>' + '\n'

                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label style=\"color: white\">Point Worth : <input type = "text" name = "Point_' + str(
                        i) + '" size="12" style=\"color: black\" value="' + q.get("point")[0] + '"/></label ><br>' + '\n'
                    quiz_template += '<label style=\"color: white\">Answer : <input type = "text" name = "Answer_' + str(
                        i) + '" size="12" style=\"color: black\" value="' + q.get("answer")[0] + '"/></label ><br>' + '\n'
                    # print("point: ",q.get("point"))
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content' + str(i) + '">' + '\n'
                    quiz_template += '</p>' + '\n'

                    # print("choice_A"+ str(i))

                    quiz_template += '<label style=\"color: white\">ChoiceA <input type = "text" name = "Choice_A_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + str(q.get("choice_A")[0]) + '"/></label >' + '\n'
                    quiz_template += '<label style=\"color: white\">ChoiceB <input type = "text" name = "Choice_B_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + str(q.get("choice_B")[0]) + '"/></label >' + '\n'
                    quiz_template += '<label style=\"color: white\">ChoiceC <input type = "text" name = "Choice_C_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + str(q.get("choice_C")[0]) + '"/></label >' + '\n'
                    quiz_template += '<label style=\"color: white\">ChoiceD <input type = "text" name = "Choice_D_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + str(q.get("choice_D")[0]) + '"/></label >' + '\n'
                    quiz_template += '</p>' + '\n'

                elif q.get("type") == "True_or_False":
                    quiz_template += '<label style=\"color: white\"> Question' + str(i) + ' <input type = "text" name = "Question_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + dict.get("Question_" + str(i))[0] + '"/></label >' + "\n"
                    quiz_template += '<label style=\"color: white\" for="option' + str(i) + '">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type' + str(i) + '" id="option' + str(
                        i) + '" value="True_or_False" >' + '\n'
                    # quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
                    # quiz_template += '<option  value="Short_Answer">Short Answer</option>' + '\n'
                    quiz_template += '<option  value="True_or_False" selected>T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label style=\"color: white\">Point Worth : <input type = "text" name = "Point_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + str(dict.get("Point_" + str(i))[0]) + '"/></label >' + '\n'
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content' + str(i) + '">' + '\n'
                    quiz_template += '</p>' + '\n'
                    if q.get("answer") == "True":
                        quiz_template += '<label style=\"color: white\">True <input type = "radio" name = "T/F' + str(
                            i) + '" size="120" value="True" checked/></label >' + '\n' + '<br>'
                        quiz_template += '<label style=\"color: white\">False <input type = "radio" name = "T/F' + str(
                            i) + '" size="120" value="False"></label >' + '\n'
                    else:
                        quiz_template += '<label style=\"color: white\">True <input type = "radio" name = "T/F' + str(
                            i) + '" size="120" value="True" ></label >' + '\n' + '<br>'
                        quiz_template += '<label style=\"color: white\">False <input type = "radio" name = "T/F' + str(
                            i) + '" size="120" value="False" checked/></label >' + '\n'
                    quiz_template += '</p>' + '\n'
                elif q.get("type") == "Essay_Question":
                    row = int(q["answer"][0])
                    col = int(q["answer"][1])
                    quiz_template += '<label style=\"color: white\"> Question' + str(i) + ' <input type = "text" name = "Question_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + q.get("question")[0] + '"/></label >' + "\n"
                    quiz_template += '<label style=\"color: white\" for="option' + str(i) + '">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type' + str(i) + '" id="option' + str(
                        i) + '" value="' + q.get("type") + '" >' + '\n'
                    quiz_template += '<option  value="Essay_Question" selected>Essay_Question</option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label style=\"color: white\">Point Worth : <input type = "text" name = "Point_' + str(
                        i) + '" size="12" style=\"color: black\" value="' + q.get("point")[0] + '"/></label >'
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content' + str(i) + '">' + '\n'
                    quiz_template += '</p>' + '\n'
                    quiz_template += '<input type="text" name="Essay_Question'+str(i)+'_Row" value="'+str(row)+'" hidden><br>\n'
                    quiz_template += '<input type="text" name="Essay_Question'+str(i)+'_Col" value="'+str(col)+'" hidden><br>\n'
                    for j in range(row*col):
                        quiz_template +='<input type="text" name="Essay_Question'+str(i)+'_Cell'+str(j)+'" value="'+str(q["answer"][j+2])+'" hidden><br>\n'
                    quiz_template += '<table id=\'rubric'+str(i)+'\' style="width:100%;color: white">'
                    rubric_template = ""

                    cnt = 2
                    for m in range(row):
                        rubric_template += "<tr>"
                        for n in range(col):
                            rubric_template += "<td>"+q["answer"][cnt]+"</td>"
                            cnt += 1
                        rubric_template += "</tr>"

                    quiz_template += rubric_template +"</table>"

                    print("q: ",q)
                    print(rubric_template)

                elif q.get("type") == "Short_Answer":
                    quiz_template += '<label style=\"color: white\"> Question' + str(i) + ' <input type = "text" name = "Question_' + str(
                        i) + '" size="120" style=\"color: black\" value="' + q.get("question")[0] + '"/></label >' + "\n"
                    quiz_template += '<label style=\"color: white\" for="option' + str(i) + '">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type' + str(i) + '" id="option' + str(
                        i) + '" value="' + q.get("type") + '" >' + '\n'
                    # quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
                    quiz_template += '<option  value="Short_Answer" selected>Short Answer</option>' + '\n'
                    # quiz_template += '<option  value="True_or_False" >T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label style=\"color: white\">Point Worth : <input type = "text" name = "Point_' + str(
                        i) + '" size="12" style=\"color: black\" value="' + q.get("point")[0] + '"/></label >'
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content' + str(i) + '">' + '\n'
                    quiz_template += '</p>' + '\n'
                    quiz_template += '<div class="form-group"><label style=\"color: white\" for="comment">Short Question_Answer:</label><textarea class="form-control" style=\"color: black\" name=\"Answer_' + str(
                        i) + '\" rows=\"5\" id=\"comment\" >' + q.get('answer')[0] + '</textarea></div>'
                    quiz_template += '</p>' + '\n'

                quiz_template += "<br><br>" + "\n\n"
                i += 1
            js_template += '<script>' + '\n'
            js_template += 'var x' + str(i) + ' = document.getElementById("option' + str(i) + '");' + '\n'
            js_template += 'x' + str(i) + '.addEventListener("change", myFunction' + str(i) + ');' + '\n'
            js_template += 'function myFunction' + str(i) + '() {' + '\n'
            js_template += 'if (x' + str(i) + '.value == "Multiple_Choice"){' + '\n'
            js_template += 'document.getElementById("question_content' + str(i) + '").innerHTML =' + '\n'
            js_template += '"<label style=\\"color: white\\" >Answer : <input type = \\"text\\" style=\\"color: black\\" name = \\"Answer_' + str(
                i) + '\\" size=\\"12\\" required/></label >" +\n'
            js_template += '"<br>"+\n'
            js_template += '"<label style=\\"color: white\\">ChoiceA <input type = \\"text\\" style=\\"color: black\\" name = \\"Choice_A_' + str(
                i) + '\\" size=\\"120\\" required/></label >" +\n'
            js_template += '"<label style=\\"color: white\\">ChoiceB <input type = \\"text\\" style=\\"color: black\\" name = \\"Choice_B_' + str(
                i) + '\\" size=\\"120\\" required/></label >" +\n'
            js_template += '"<label style=\\"color: white\\">ChoiceC <input type = \\"text\\" style=\\"color: black\\" name = \\"Choice_C_' + str(
                i) + '\\" size=\\"120\\" required/></label >" +\n'
            js_template += '"<label style=\\"color: white\\">ChoiceD <input type = \\"text\\" style=\\"color: black\\" name = \\"Choice_D_' + str(
                i) + '\\" size=\\"120\\" required/></label >" ;\n'
            js_template += '}' + '\n'
            js_template += 'else if (x' + str(i) + '.value == "Short_Answer"){' + '\n'
            js_template += 'document.getElementById("question_content' + str(i) + '").innerHTML = \n'
            js_template += '"<div class=\\"form-group\\">" +\n'
            js_template += '"<label style=\\"color: white\\" for=\\"comment\\">Short Question_Answer:</label>" +\n'
            js_template += '"<textarea class=\\"form-control\\" name=\\"Answer_' + str(
                i) + '\\" rows=\\"5\\" id=\\"comment\\" required></textarea></div>";\n'
            js_template += '}' + '\n'
            js_template += 'else if (x' + str(i) + '.value == "Essay_Question"){' + '\n'
            js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML = \n'
            js_template += '"<div class=\\"form-group\\">" +\n'
            js_template += '"<input type = \\"text\\" id=\\"row_text\\" name = \\"row\\" value=\\"0\\" hidden/>" +\n'
            js_template += '"<input type = \\"text\\" id=\\"col_text\\" name = \\"col\\" value=\\"0\\" hidden/>" +\n'
            js_template += '"<label style=\\"color: white\\">Row:</label><input type=\\"number\\" id=\\"row\\" min=\\"1\\" max=\\"5\\" style=\\"color: #1b1b1b\\" required> X "+\n '
            js_template += '"<label style=\\"color: white\\">Row:</label> <input type=\\"number\\" id=\\"col\\" min=\\"1\\" max=\\"5\\"  style=\\"color: #1b1b1b\\" required> " +\n'
            js_template += '"<button onclick=\\"displayTable()\\" style=\\"color: #1b1b1b\\" id=\\"update\\" type=\\"button\\">Create Rubric</button>" +\n'
            js_template += '"<table id=\\"rubric\\"></table>" +\n'
            js_template += '"</div>"}' +'\n'

            js_template += 'else{' + '\n'
            js_template += 'document.getElementById("question_content' + str(i) + '").innerHTML = \n'
            # js_template += '"<label>Answer : <input type = \\"text\\" name = \\"Answer_'+str(i)+'\\" size=\\"12\\"/></label >" +\n'
            js_template += '"<br>" +\n'
            js_template += '"<label style=\\"color: white\\"> T/F answer:</label>" +\n'
            js_template += '"<br>" +\n'
            js_template += '"<input type=\\"radio\\" id=\\"T\\" name=\\"T/F_' + str(
                i) + '\\" value=\\"True\\" required>" +\n'
            js_template += '"<label style=\\"color: white\\" for=\\"T\\">True</label>" +\n'
            js_template += '"<br>" +\n'
            js_template += '"<input type=\\"radio\\" id=\\"F\\" name=\\"T/F_' + str(
                i) + '\\" value=\\"False\\">" +\n'
            js_template += '"<label style=\\"color: white\\" for=\\"F\\">False</label><br>"; \n'
            js_template += '}' + '\n'
            js_template += '}' + '\n'
            js_template += '</script>' + '\n'
            js_template += '\n'
            js_template += '</html>'

            new_quiz_template = '<label style=\"color: white\"> Question' + str(i) + ' <input type = "text" style=\"color: black\" name = "Question_' + str(
                i) + '" size="120"/></label >' + "\n"
            new_quiz_template += "<br>" + '\n'
            new_quiz_template += '<label style=\"color: white\" for="option' + str(i) + '">Question Type :</label>' + '\n'
            new_quiz_template += '<select name="question_type' + str(i) + '" id="option' + str(i) + '" >' + '\n'
            new_quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
            new_quiz_template += '<option  value="Short_Answer">Short Answer</option>' + '\n'
            new_quiz_template += '<option  value="True_or_False" >T/F Question </option>' + '\n'
            new_quiz_template += '<option  value="Essay_Question" >Essay Question </option>' + '\n'
            new_quiz_template += '</select><br>' + '\n'
            new_quiz_template += '<label style=\"color: white\" >Point Worth : <input type = "text" style=\"color: black\" name = "Point_' + str(
                i) + '" size="12"/></label >' + '\n'
            new_quiz_template += '<br>' + '\n'
            new_quiz_template += '<p id="question_content' + str(i) + '">' + '\n'
            new_quiz_template += '</p>' + '\n'
            # new_quiz_template += '<p><input type = "submit" value = "Build Quiz" name="build quiz"/></p >' + '\n'
            # new_quiz_template += '<p><input type="submit" value="add Question" name="add question"/></p >' + '\n'
            # new_quiz_template += '<label>ChoiceA <input type = "text" name = "Choice_A_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceB <input type = "text" name = "Choice_B_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceC <input type = "text" name = "Choice_C_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceD <input type = "text" name = "Choice_D_' + str(i) + '" size="120" /></label >' + '\n'
            new_quiz_template += '</p>' + '\n'
            js_start_pos = t.find('<p><input value="starting_pos" name="pos" hidden/></p >') + len(
                '<p><input value="starting_pos" name="pos" hidden/></p >')
            template = t[:start_pos] + quiz_template + new_quiz_template + t[end_pos:js_start_pos] + js_template
            template = template.replace("teacher_name", name)

            template = template.replace('<input type = "text" name = "Quiz_name" size="120" value=""',
                quizName_template)
            template = template.replace(
                '<input type = "text" id="time_limit_hour" name = "Time_Limit_hr" size="100" value=""',
                time_hour_template)
            template = template.replace(
                '<input type = "text" id="time_limit_min" name = "Time_Limit_min" size="100" value=""',
                time_min_template)
            return template

        else:
            # load full quiz into database
            passcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            json_quiz = json.dumps(full_quiz)

            time_limit = (int(hr) * 3600 + int(min) * 60) * 1000

            DataBase.insert_quiz((passcode, teacher_name, quizname, json_quiz, str(time_limit)))
            DataBase.print_Quiz_Data()
            return redirect("/homePage/"+teacher_name, code=301)

    else:
        data = ImmutableMultiDict(request.form)
        dict = data.to_dict(flat=False)
        url = request.url
        start_pos = url.find('=')
        teacher_name = ""
        for i in range(start_pos + 1, len(url)):
            teacher_name += url[i]
        t = ""
        with open("templates/teacher_quiz_generate.html", 'r') as f:
            t = f.read()
        t = t.replace("teacher_name", teacher_name)

        return t

@app.route('/Signup', methods=['POST', 'GET'])
def Signup():
    print("in signup")
    if request.method == 'GET':
        return render_template("index.html")
    else:
        imd = ImmutableMultiDict(request.form)
        print("imd:", imd)
        dict = imd.to_dict(flat=False)
        name = dict.get("Name")[0]
        password = dict.get("Password")[0]
        role = dict.get("who")[0]
        user_email = dict.get("email")[0]
        print(user_email)
        if DataBase.username_is_not_exist(name):
            DataBase.insert_user((role, name, password,user_email))
            print("success, back to index page")
            return render_template("index.html")
        else:
            return redirect("/?error=username", code=301)

@app.route('/homePage/<name>', methods=['GET'])
def homePage(name):
    if request.method == 'GET':

        role = DataBase.get_role_baseon_name(name)
        if DataBase.username_is_not_exist(name):
            return redirect("/?error=username", code=301)
        elif role is None:
            return redirect("/?error=password", code=301)
        elif role == "Student":
            # jump to student profile
            list_of_gradebook = DataBase.find_gradebook_baseon_name(name)
            with open("templates/student_homepage.html", "r") as f:
                t = f.read()
            start_pos = t.find("{{Begin Loop}}")
            end_pos = t.find("{{END LOOP}}")
            front_data = t[:start_pos]
            end_data = t[end_pos + len("{{END LOOP}}"):]
            templates = t[start_pos + len("{{Begin Loop}}"):end_pos]

            newTemp = ''

            for grade_book in list_of_gradebook:
                quiz_name = grade_book[0]
                score = grade_book[1]
                submissionID = grade_book[2]
                s = templates.replace('QuizName', quiz_name).replace('{{Total Point}}', score).replace('role',
                                                                                                       'student').replace(
                    'submissionID', submissionID)
                newTemp += s
            front_data += newTemp
            front_data += end_data
            return front_data

        elif role == "Teacher":
            # jump to teacher profile
            list_of_passcode = DataBase.find_passcode_baseon_teacher_name(name)
            allInformation = DataBase.getInformation()
            newTemplate = ''
            with open("templates/teacher_homepage.html", "r") as f:
                myTemplate = f.read()
            beginTagIndex = myTemplate.find('{{loop}}')
            endTagIndex = myTemplate.find('{{end_loop}}')
            endData = myTemplate[endTagIndex + len('{{end_loop}}'):]
            finalTemplate = myTemplate[:beginTagIndex]
            template = myTemplate[beginTagIndex + len('{{loop}}'):endTagIndex]
            print("all", allInformation)
            print(list_of_passcode)
            for x in allInformation:
                if x[3] in list_of_passcode:
                    quizname = x[1]
                    studentname = x[0]
                    studentGrade = x[2]
                    submissionID = x[4]
                    t = template.replace('{{QuizName}}', quizname).replace('{{StudentName}}', studentname).replace(
                        '{{StudentGrade}}', studentGrade).replace("submissionID", submissionID).replace("role",
                                                                                                        "teacher")
                    newTemplate += t
            finalTemplate += newTemplate
            finalTemplate += endData
            finalTemplate = finalTemplate.replace("teacher_name", name)
            passcode_template = "<p>Passcode List: </p>"
            for code in list_of_passcode:
                passcode_template += DataBase.get_quiz_name_by_passcode(code) + " ----> " + code + '\n<br>\n'
            finalTemplate = finalTemplate.replace('<p>Passcode List: </p>', passcode_template)
            return finalTemplate


@app.route('/user', methods=['POST', 'GET'])
def user():
    print("user")
    if request.method == 'POST':
        imd = ImmutableMultiDict(request.form)
        dict = imd.to_dict(flat=False)
        name = dict.get("Name")[0]
        password = dict.get("Password")[0]

        # if username+password is not match

        role = DataBase.user_authentication(name, password)

        if DataBase.username_is_not_exist(name):
            return redirect("/?error=username", code=301)
        elif role is None:
            return redirect("/?error=password", code=301)
        elif role == "Student":
            # jump to student profile
            list_of_gradebook = DataBase.find_gradebook_baseon_name(name)
            with open("templates/student_homepage.html", "r") as f:
                t = f.read()
            start_pos = t.find("{{Begin Loop}}")
            end_pos = t.find("{{END LOOP}}")
            front_data = t[:start_pos]
            end_data = t[end_pos + len("{{END LOOP}}"):]
            templates = t[start_pos + len("{{Begin Loop}}"):end_pos]

            newTemp = ''

            for grade_book in list_of_gradebook:
                quiz_name = grade_book[0]
                score = grade_book[1]
                submissionID = grade_book[2]
                s = templates.replace('QuizName', quiz_name).replace('{{Total Point}}', score).replace('role',
                                                                                                       'student').replace(
                    'submissionID', submissionID)
                newTemp += s
            front_data += newTemp
            front_data += end_data
            return front_data

        elif role == "Teacher":
            # jump to teacher profile
            list_of_passcode = DataBase.find_passcode_baseon_teacher_name(name)
            allInformation = DataBase.getInformation()
            newTemplate = ''
            with open("templates/teacher_homepage.html", "r") as f:
                myTemplate = f.read()
            beginTagIndex = myTemplate.find('{{loop}}')
            endTagIndex = myTemplate.find('{{end_loop}}')
            endData = myTemplate[endTagIndex + len('{{end_loop}}'):]
            finalTemplate = myTemplate[:beginTagIndex]
            template = myTemplate[beginTagIndex + len('{{loop}}'):endTagIndex]
            print("all", allInformation)
            print(list_of_passcode)
            for x in allInformation:
                if x[3] in list_of_passcode:
                    quizname = x[1]
                    studentname = x[0]
                    studentGrade = x[2]
                    submissionID = x[4]
                    t = template.replace('{{QuizName}}', quizname).replace('{{StudentName}}', studentname).replace(
                        '{{StudentGrade}}', studentGrade).replace("submissionID", submissionID).replace("role",
                                                                                                        "teacher")
                    newTemplate += t
            finalTemplate += newTemplate
            finalTemplate += endData
            finalTemplate = finalTemplate.replace("teacher_name", name)
            passcode_template = "<p>Passcode List: </p>"
            if list_of_passcode is not None:
                for code in list_of_passcode:
                    passcode_template += DataBase.get_quiz_name_by_passcode(code) + "----->" + code + '\n<br>\n'
            finalTemplate = finalTemplate.replace('<p>Passcode List: </p>', passcode_template)
            return finalTemplate


if __name__ == '__main__':

    DataBase.create_Submission_table()
    DataBase.print_submission_table()
    DataBase.creat_user_table()
    DataBase.print_score_record_table()

    app.run(host='0.0.0.0', port=9377, debug=True)
