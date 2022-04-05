'''
Coder: Zhou Zhou  && Shkaraot
'''
import time

import DataBase
from flask import Flask, render_template, request, redirect, g
from werkzeug.datastructures import ImmutableMultiDict
import random
import string
import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    print("print table")
    DataBase.print_user_table()
    return render_template("index.html")

@app.route('/changeScore',methods=['POST','GET'])
def changeScore():
    '''data= {"submissionID":["abc12345"],"name":["Jesse"],"question1":['5'],"question2":["2"]...'''
    ''' 1. add values up then update score based on the submissionID
        2. in score_record, change score based on submissionID
        3. redirect to teacher gradebook
    '''
    sumScore = 0
    data = dict(request.form)
    submissionID = data.get("submissionID")[0]
    teacherName = data.get("name")[0]
    # check all keys in the data
    for eachData in data.keys():
        # if id matches the submissionID we looking for
        # and we find question
        if eachData[0] == submissionID and eachData.__contains__("question"):
            # add the question points to the sumScore
            sumScore += int(data[eachData[0]])
            # update score based on submission id
            eachData["score"] = sumScore
    # teacherName = "Jesse" for example
    return redirect("/teacher_grade_book/"+teacherName, code=301)

@app.route('/updateQuiz', methods=['POST', 'GET'])
def updateQuiz():
    pass


@app.route('/submission/<id>', methods=['POST', 'GET'])
def studentSubmission(id):
    # submission = {"question1":["actual answer","sudent answer","point receive","point worth"]}
    submission = DataBase.get_studentAnswer_baseon_submissionID(id)
    with open("templates/submission.html", "r") as f:
        t = f.read()
    template = ""
    i = 0
    startPos = t.find("<h3>{{Question_Name}}: </h3>")
    endPos = t.find('<p><input type = "submit" value = "Update" name="Update Quiz"/></p >')
    for k, v in submission:
        i += 1
        questionName = k
        actual_answer = v[0]
        student_answer = v[1]
        point_receive = v[2]
        point_worth = v[3]
        template += "<h3>" + str(i) + ". " + questionName + "</h3>" + "\n"
        template += "<p>Correct Answer: " + actual_answer + "</p >" + "\n"
        template += "<p>Student Answer: " + student_answer + "</p >" + "\n"
        template += "<label>Point Worth : <input type = \"text\" name = \"Choice" + str(i)+"\" size=\"3\" value=\""+ point_receive + "\" />/" + point_worth + "</label>" + "\n"
        template += "<br>" + "\n" + "<br>" + "\n"

    final_temp = t[:startPos] + template + t[endPos:]
    return final_temp


@app.route('/quiz_submit', methods=['POST', 'GET'])
def quiz_submit():
    if request.method == "POST":
        data = dict(request.form)
        studentName = data.get("studentName")
        print('Data:', data)
        data.pop("studentName")
        passcode = data.get("passcode")

        quizName = DataBase.obtainQuizName(passcode)
        json_quiz = DataBase.find_quiz_data(passcode)
        quiz = json.loads(json_quiz)
        student_score = 0
        for student_question_submission in data:
            question_number = get_question_number(student_question_submission)
            student_choice = data.get(student_question_submission)
            answer = quiz[question_number - 1].get("answer")[0]
            p = 0
            if student_choice == answer:
                p = int(quiz[question_number - 1].get("point")[0]) - int('0')
                student_score += p

        f = open("templates/student_homepage.html", "r")
        t = ""
        for line in f:
            t += line
        t = t.replace('"/student_gradebook/"', '"/student_gradebook/' + studentName + '"')

        start_pos = t.find('<p>Passcode:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Score:</p>') + len(
            '<p>Passcode:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Score:</p>')
        score_template = '<p>' + passcode + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
            student_score) + "<p>"
        final_template = t[:start_pos] + score_template + t[start_pos + 1:]
        DataBase.makeScoreRecord()
        print("quizname", quizName)

        SubmissionID = ''.join(random.choices(string.ascii_lowercase, k=8))
        DataBase.insertScoreRecord(studentName, quizName, str(student_score), passcode, SubmissionID)
        DataBase.getInformation()

        return final_template
    else:
        return "quiz"


def get_question_number(q):
    n = 0
    for i in range(8, len(q)):
        n = n * 10 + int(q[i]) - int('0')
    return n


@app.route('/student_gradebook/<name>', methods=['GET', 'POST'])
def studentGrade(name):
    list_of_gradebook = DataBase.find_gradebook_baseon_name(name)
    with open("templates/student_grade_book.html", "r") as f:
        t = f.read()
    start_pos = t.find("{{Begin Loop}}")
    end_pos = t.find("{{END LOOP}}")
    front_data = t[:start_pos]
    end_data = t[end_pos + len("{{END LOOP}}"):]
    templates = t[start_pos + len("{{Begin Loop}}"):end_pos]
    print('list_of_gradebook:', list_of_gradebook)
    newTemp = ''
    for grade_book in list_of_gradebook:
        print('Hello')
        quiz_name = grade_book[0]
        score = grade_book[1]
        s = templates.replace('{{Quiz Name}}', quiz_name).replace('{{Total Point}}', score)
        newTemp += s
    front_data += newTemp
    front_data += end_data
    return front_data


@app.route('/teacher_grade_book/<name>', methods=['GET'])
def teacherGrade(name):
    # input: teacher name
    list_of_passcode = DataBase.find_passcode_baseon_teacher_name(name)

    allInformation = DataBase.getInformation()

    newTemplate = b''
    with open('templates/teacher_grade_book.html', 'rb') as s:
        myTemplate = s.read()
    beginTagIndex = myTemplate.find(b'{{loop}}')
    endTagIndex = myTemplate.find(b'{{end_loop}}')
    endData = myTemplate[endTagIndex + len(b'{{end_loop}}'):]
    finalTeamplate = myTemplate[:beginTagIndex]
    template = myTemplate[beginTagIndex + len(b'{{loop}}'):endTagIndex]
    print("all", allInformation)
    for x in allInformation:
        if x[3] in list_of_passcode:
            quizname = x[1].encode()
            studentname = x[0].encode()
            studentGrade = x[2].encode()
            t = template.replace(b'{{QuizName}}', quizname).replace(b'{{StudentName}}', studentname).replace(
                b'{{StudentGrade}}', studentGrade)
            newTemplate += t
    finalTeamplate += newTemplate
    finalTeamplate += endData
    return finalTeamplate


@app.route('/accessQuiz', methods=['POST', 'GET'])
def accessQuiz():
    if request.method == "POST":
        data = ImmutableMultiDict(request.form)

        dict = data.to_dict(flat=False)
        passcode = dict.get("Access Code")[0]
        studentName = dict.get("User Name")[0]

        DataBase.print_passcode()
        json_quiz = DataBase.find_quiz_data(passcode)
        print("json:", json_quiz)
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
            question_type = quiz.get("type")[0]
            answer = quiz.get('answer')[0]
            point = quiz.get('point')[0]
            choice_A = quiz.get('choice_A')[0]
            choice_B = quiz.get('choice_B')[0]
            choice_C = quiz.get('choice_C')[0]
            choice_D = quiz.get('choice_D')[0]

            if question_type == "mult":
                template1 = "<p> " + question + " (" + point + "pts) </p>\n"
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

            elif question_type == "t/f":
                template1 = "<p> " + question + " (" + point + "pts) </p>\n"
                template2 = "<input type=\"radio\" id=\"" + str(quiz_number) + "a\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + choice_A + "\">\n"
                template3 = '<label for="' + str(quiz_number) + 'a">' + "TRUE" + '</label><br>\n'

                template4 = "<input type=\"radio\" id=\"" + str(quiz_number) + "b\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + choice_B + "\">\n"
                template5 = '<label for="' + str(quiz_number) + 'b">' + "False" + '</label><br>\n'
                quiz_template += template1 + template2 + template3 + template4 + template5
            elif question_type == "short":
                template1 = "<p> " + question + " (" + point + "pts) </p>\n"
                template2 = "<input type=\"radio\" id=\"" + str(quiz_number) + "a\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + choice_A + "\">\n"
                template3 = '<label for="' + str(quiz_number) + 'a">' + "TRUE" + '</label><br>\n'


        quiz_template += '<input value="' + passcode + '" name="passcode" hidden>'
        quiz_template += '<input value="' + studentName + '" name="studentName" hidden>'
        final_template = final_template[:start_pos] + quiz_template + final_template[end_pos:]

        return final_template

    return "quiz"


@app.route('/buildQuiz', methods=['POST', 'GET'])
def buidQuiz():
    # need change, we now have question type
    print("type", request.method)
    if request.method == 'POST':

        data = ImmutableMultiDict(request.form)

        dict = data.to_dict(flat=False)
        dic_length = len(dict)
        key_list = list(dict)
        full_quiz = []
        quizname = dict.get("Quiz_name")[0]

        print("dict", dict)
        print("key_list",key_list)
        print("len",dic_length)
        i = 3
        while i < (dic_length-2):
            time.sleep(1)
            type = dict.get(key_list[i])[0]

            print("while",i,type)
            if type == "Multiple_Choice":
                print("type: ", type)
                question = {"question": dict.get(key_list[i])}
                question_type = {"type":type}
                answer = {"answer": dict.get(key_list[i+1])}
                point = {"point": dict.get(key_list[i+2])}
                a = {"choice_A": dict.get(key_list[i+3])}
                b = {"choice_B": dict.get(key_list[i+4])}
                c = {"choice_C": dict.get(key_list[i+5])}
                d = {"choice_D": dict.get(key_list[i+6])}
                quiz = {}
                for d in (question, question_type,answer, point, a, b, c, d):
                    quiz.update(d)
                full_quiz.append(quiz)
                i += 8
            elif type == "True_or_False":
                print("type: ", type)
                question = {"question": dict.get(key_list[i])}
                question_type = {"type":type}
                point = {"point": dict.get(key_list[i + 2])}
                answer = {"choice": dict.get(key_list[i + 3])}

                quiz = {}
                for d in (question, question_type, point,answer):
                    quiz.update(d)
                full_quiz.append(quiz)
                i += 4

            elif type == "Short_Answer":
                print("type: ", type)
                question = {"question": dict.get(key_list[i])}
                question_type = {"type":type}
                answer = {"answer": dict.get(key_list[i + 2])}
                point = {"point": dict.get(key_list[i + 3])}
                a = {"choice_A": dict.get(key_list[i + 4])}
                quiz = {}
                for d in (question,question_type,answer, point, a):
                    quiz.update(d)
                full_quiz.append(quiz)
                i += 4


        name = dict.get('Quiz_name')[0]
        hr = dict.get('Time_Limit_hr')
        min = dict.get('Time_Limit_min')

        if dict.get('build quiz') is None:

            f = open("templates/teacher_quiz_generate.html", "r")
            t = ""
            for line in f:
                t += line
            start_pos = t.find('<label>Question1 <input type = "text" name = "Question_1" size="120"/></label >')
            end_pos = t.find(' <p><input type = "submit" value = "Build Quiz" name="build quiz"/></p >')  # security risk
            quiz_template = ""

            i = 1
            js_template = ""

            for q in full_quiz:
                print("here:",q)
                js_template += '<script>' + '\n'
                js_template += 'var x'+str(i)+' = document.getElementById("option' + str(i) + '");'+'\n'
                js_template += 'x'+str(i)+'.addEventListener("change", myFunction'+str(i)+');'+'\n'
                js_template += 'function myFunction'+str(i)+'() {'+'\n'
                js_template += 'if (x'+str(i)+'.value == "Multiple_Choice"){'+'\n'
                js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML ='+'\n'
                js_template += '"<label>Answer : <input type = \\"text\\" name = \\"Answer_'+str(i)+'\\" size=\\"12\\" required/></label >" +\n'
                js_template += '"<br>"+\n'
                js_template += '"<label>ChoiceA <input type = \\"text\\" name = \\"Choice_A_'+str(i)+'\\" size=\\"120\\" required/></label >" +\n'
                js_template += '"<label>ChoiceB <input type = \\"text\\" name = \\"Choice_B_'+str(i)+'\\" size=\\"120\\" required/></label >" +\n'
                js_template += '"<label>ChoiceC <input type = \\"text\\" name = \\"Choice_C_'+str(i)+'\\" size=\\"120\\" required/></label >" +\n'
                js_template += '"<label>ChoiceD <input type = \\"text\\" name = \\"Choice_D_'+str(i)+'\\" size=\\"120\\" required/></label >" ;\n'
                js_template += '}'+'\n'
                js_template += 'else if (x' + str(i) + '.value == "Short_Answer"){'+'\n'
                js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML = \n'
                js_template += '"<div class=\\"form-group\\">" +\n'
                js_template += '"<label for=\\"comment\\">Short Question_Answer:</label>" +\n'
                js_template += '"<textarea class=\\"form-control\\" name=\\"Answer_'+str(i)+'\\" rows=\\"5\\" id=\\"comment\\" required></textarea></div>";\n'
                js_template += '}'+'\n'
                js_template += 'else{'+'\n'
                js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML = \n'
                #js_template += '"<label>Answer : <input type = \\"text\\" name = \\"Answer_'+str(i)+'\\" size=\\"12\\"/></label >" +\n'
                js_template += '"<br>" +\n'
                js_template += '"<label> T/F answer:</label>" +\n'
                js_template += '"<br>" +\n'
                js_template += '"<input type=\\"radio\\" id=\\"T\\" name=\\"T/F_'+str(i)+'\\" value=\\"True\\" required>" +\n'
                js_template += '"<label for=\\"T\\">True</label>" +\n'
                js_template += '"<br>" +\n'
                js_template += '"<input type=\\"radio\\" id=\\"F\\" name=\\"T/F_'+str(i)+'\\" value=\\"False\\">" +\n'
                js_template += '"<label for=\\"F\\">False</label><br>"; \n'
                js_template += '}'+'\n'
                js_template += '}'+'\n'
                js_template += '</script>'+'\n'
                js_template += '\n'


                if q.get("type") == "Multiple_Choice":
                    quiz_template += '<label> Question' +str(i) + ' <input type = "text" name = "Question_' + str(i)+ '" size="120" value="' + q.get("question")[0] + '" required/></label >' + "<br>" +"\n"
                    quiz_template += '<label for="option'+str(i)+'">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type'+str(i)+ '" id="option'+str(i)+'" value="Multiple_Choice" >' +'\n'
                    quiz_template += '<option  value="Multiple_Choice" selected>Multiple Choice</option>' + '\n'
                    # quiz_template += '<option  value="Short_Answer">Short Answer</option>' + '\n'
                    # quiz_template += '<option  value="True_or_False" >T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label>Answer : <input type = "text" name = "Answer_' + str(i) + '" size="12" value="' + q.get("answer")[0]+'"/></label ><br>' + '\n'
                    quiz_template += '<label>Point Worth : <input type = "text" name = "Point_' + str(i) + '" size="12"/></label ><br>' + '\n'
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content'+str(i)+'">' + '\n'
                    quiz_template += '</p>' + '\n'
                    quiz_template += '<label>ChoiceA <input type = "text" name = "Choice_A_' + str(i) + '" size="120" value="'+str(q.get("Choice_A_" + str(i))) +'/></label >' + '\n'
                    quiz_template += '<label>ChoiceB <input type = "text" name = "Choice_B_' + str(i) + '" size="120" value="'+str(q.get("Choice_B_" + str(i))) +'/></label >' + '\n'
                    quiz_template += '<label>ChoiceC <input type = "text" name = "Choice_C_' + str(i) + '" size="120" value="'+str(q.get("Choice_C_" + str(i))) +'/></label >' + '\n'
                    quiz_template += '<label>ChoiceD <input type = "text" name = "Choice_D_' + str(i) + '" size="120" value="'+str(q.get("Choice_D_" + str(i))) +'/></label >' + '\n'
                    quiz_template += '</p>' + '\n'

                elif q.get("type") == "True_or_False":
                    quiz_template += '<label> Question' + str(i) + ' <input type = "text" name = "Question_' + str(i)+ '" size="120" value="' + q.get("question")[0] + '"/></label >' + "\n"
                    quiz_template += '<label for="option'+str(i)+'">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type'+str(i)+'" id="option'+str(i)+'" value="True_or_False" >' +'\n'
                    # quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
                    # quiz_template += '<option  value="Short_Answer">Short Answer</option>' + '\n'
                    quiz_template += '<option  value="True_or_False" selected>T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label>Point Worth : <input type = "text" name = "Point_' + str(i) + '" size="12"/></label ><br>' + '\n'
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content'+str(i)+'">' + '\n'
                    quiz_template += '</p>' + '\n'
                    quiz_template += '<label>True <input type = "radio" name = "T/F' + str(i) + '" size="120" /></label >' + '\n'
                    quiz_template += '<label>False <input type = "radio" name = "T/F' + str(i) + '" size="120" /></label >' + '\n'
                    quiz_template += '</p>' + '\n'

                elif q.get("type") == "Short_Answer":
                    quiz_template += '<label> Question' +str(i) + ' <input type = "text" name = "Question_' + str(i)+ '" size="120" value="' + q.get("question")[0] + '"/></label >' + "\n"
                    quiz_template += '<label for="option'+str(i)+'">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type'+str(i)+ '" id="option'+str(i)+'" value="Short_Answer" >' +'\n'
                    #quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
                    quiz_template += '<option  value="Short_Answer" selected>Short Answer</option>' + '\n'
                    #quiz_template += '<option  value="True_or_False" >T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label>Point Worth : <input type = "text" name = "Point_' + str(i) + '" size="12"/></label >'
                    quiz_template += '<br>' +'\n'
                    quiz_template += '<p id="question_content'+str(i)+'">' + '\n'
                    quiz_template += '</p>'+ '\n'
                    quiz_template += '<div class="form-group"><label for="comment">Short Question_Answer:</label><textarea class="form-control" name="Answer_'+str(i)+'" rows="5" id="comment"></textarea></div>'
                    quiz_template += '</p>'+'\n'

                quiz_template += "<br><br>"+"\n\n"
                i += 1
            js_template += '<script>' + '\n'
            js_template += 'var x'+str(i)+' = document.getElementById("option' + str(i) + '");'+'\n'
            js_template += 'x'+str(i)+'.addEventListener("change", myFunction'+str(i)+');'+'\n'
            js_template += 'function myFunction'+str(i)+'() {'+'\n'
            js_template += 'if (x'+str(i)+'.value == "Multiple_Choice"){'+'\n'
            js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML ='+'\n'
            js_template += '"<label>Answer : <input type = \\"text\\" name = \\"Answer_'+str(i)+'\\" size=\\"12\\" required/></label >" +\n'
            js_template += '"<br>"+\n'
            js_template += '"<label>ChoiceA <input type = \\"text\\" name = \\"Choice_A_'+str(i)+'\\" size=\\"120\\" required/></label >" +\n'
            js_template += '"<label>ChoiceB <input type = \\"text\\" name = \\"Choice_B_'+str(i)+'\\" size=\\"120\\" required/></label >" +\n'
            js_template += '"<label>ChoiceC <input type = \\"text\\" name = \\"Choice_C_'+str(i)+'\\" size=\\"120\\" required/></label >" +\n'
            js_template += '"<label>ChoiceD <input type = \\"text\\" name = \\"Choice_D_'+str(i)+'\\" size=\\"120\\" required/></label >" ;\n'
            js_template += '}'+'\n'
            js_template += 'else if (x' + str(i) + '.value == "Short_Answer"){'+'\n'
            js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML = \n'
            js_template += '"<div class=\\"form-group\\">" +\n'
            js_template += '"<label for=\\"comment\\">Short Question_Answer:</label>" +\n'
            js_template += '"<textarea class=\\"form-control\\" name=\\"Answer_'+str(i)+'\\" rows=\\"5\\" id=\\"comment\\" required></textarea></div>";\n'
            js_template += '}'+'\n'
            js_template += 'else{'+'\n'
            js_template += 'document.getElementById("question_content'+str(i)+'").innerHTML = \n'
            #js_template += '"<label>Answer : <input type = \\"text\\" name = \\"Answer_'+str(i)+'\\" size=\\"12\\"/></label >" +\n'
            js_template += '"<br>" +\n'
            js_template += '"<label> T/F answer:</label>" +\n'
            js_template += '"<br>" +\n'
            js_template += '"<input type=\\"radio\\" id=\\"T\\" name=\\"T/F_'+str(i)+'\\" value=\\"True\\" required>" +\n'
            js_template += '"<label for=\\"T\\">True</label>" +\n'
            js_template += '"<br>" +\n'
            js_template += '"<input type=\\"radio\\" id=\\"F\\" name=\\"T/F_'+str(i)+'\\" value=\\"False\\">" +\n'
            js_template += '"<label for=\\"F\\">False</label><br>"; \n'
            js_template += '}'+'\n'
            js_template += '}'+'\n'
            js_template += '</script>'+'\n'
            js_template += '\n'
            js_template += '</html>'

            new_quiz_template = '<label> Question' +str(i) + ' <input type = "text" name = "Question_' + str(i)+ '" size="120"/></label >' + "\n"
            new_quiz_template += "<br>" + '\n'
            new_quiz_template += '<label for="option'+str(i)+'">Question Type :</label>' + '\n'
            new_quiz_template += '<select name="question_type'+str(i)+ '" id="option'+str(i)+'" >' +'\n'
            new_quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
            new_quiz_template += '<option  value="Short_Answer">Short Answer</option>' + '\n'
            new_quiz_template += '<option  value="True_or_False" >T/F Question </option>' + '\n'
            new_quiz_template += '</select><br>' + '\n'
            new_quiz_template += '<label>Point Worth : <input type = "text" name = "Point_' + str(i) + '" size="12"/></label >' + '\n'
            new_quiz_template += '<br>' + '\n'
            new_quiz_template += '<p id="question_content'+str(i)+'">' + '\n'
            new_quiz_template += '</p>' + '\n'
            new_quiz_template += '<p><input type = "submit" value = "Build Quiz" name="build quiz"/></p >' + '\n'
            new_quiz_template += '<p><input type="submit" value="add Question" name="add question"/></p >' + '\n'
            # new_quiz_template += '<label>ChoiceA <input type = "text" name = "Choice_A_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceB <input type = "text" name = "Choice_B_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceC <input type = "text" name = "Choice_C_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceD <input type = "text" name = "Choice_D_' + str(i) + '" size="120" /></label >' + '\n'
            new_quiz_template += '</p>'+'\n'
            js_start_pos = t.find('<p><input value="starting_pos" name="pos" hidden/></p >')+len('<p><input value="starting_pos" name="pos" hidden/></p >')
            template = t[:start_pos] + quiz_template + new_quiz_template + t[end_pos:js_start_pos]+js_template
            template = template.replace("teacher_name", name)

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

            DataBase.insert_quiz((passcode, name, quizname, json_quiz))

            return template
    else:
        data = ImmutableMultiDict(request.form)
        dict = data.to_dict(flat=False)
        url = request.url
        start_pos = url.find('=')
        name = ""
        for i in range(start_pos + 1, len(url)):
            name += url[i]
        t = ""
        with open("templates/teacher_quiz_generate.html", 'r') as f:
            t = f.read()
        t = t.replace("teacher_name", name)

        return t


@app.route('/Signup', methods=['POST', 'GET'])
def Signup():
    print("in signup")
    if request.method == 'GET':
        return render_template("Signup.html")
    else:
        imd = ImmutableMultiDict(request.form)
        print("imd:", imd)
        dict = imd.to_dict(flat=False)
        name = dict.get("Name")[0]
        password = dict.get("Password")[0]
        role = dict.get("who")[0]

        if DataBase.username_is_not_exist(name):
            DataBase.insert_user((role, name, password))
            print("success, back to index page")
            return render_template("index.html")
        else:
            return redirect("/Signup?error=username", code=301)


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
        return redirect("/?error=username", code=301)
    elif role is None:
        return redirect("/?error=password", code=301)
    elif role == "Student":
        # jump to student profile
        t = ""
        with open("templates/student_homepage.html", "r") as f:
            t = f.read()
        t = t.replace("/student_gradebook/", "/student_gradebook/" + name)
        return t
    elif role == "Teacher":
        # jump to teacher profile
        t = ""
        with open("templates/teacher_homepage.html", "r") as f:
            t = f.read()

        t = t.replace("/teacher_grade_book", "/teacher_grade_book/" + name)

        t = t.replace("teacher_name", name)
        return t


if __name__ == '__main__':
    DataBase.creat_user_table()
    DataBase.print_score_record_table()
    app.run(host='0.0.0.0', port=9377, debug=True)