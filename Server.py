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

@app.route('/aboutUS', methods=['POST', 'GET'])
def aboutUS():
    return render_template('aboutUS.html')

@app.route('/submission/<role>/<submissionId>/rubric',methods=['POST','GET'])
def rubric(role,submissionId):
    if request.method == 'GET':
        return render_template('rubric.html')
    else:
        data = dict(request.form)
        currentData = json.dumps(data)
        DataBase.insert_rubric_table(submissionId,currentData)
        return render_template('rubric.html')

@app.route('/submission/<role>/<submissionId>/displayrubric',methods=['GET'])
def displayRubric(role,submissionId):
    data = DataBase.get_rubric_table_information(submissionId)
    dataDic = json.loads(data)
    with open("templates/rubricTable.html",'r') as f:
        template = f.read()
    templateBegin_index = template.find('{{loop}}')
    end_loop = template.find('{{end_loop}}')
    front_data = template[:templateBegin_index]
    end_data = template[end_loop + len('{{end_loop}}'):]
    templates = template[templateBegin_index + len('{{loop}}'):end_loop]
    newTemp = ''
    dataDic.pop('question_type')

    for x in range(len(dataDic) // 4):

        for y in range(4):
            myinputword = 'input-{}-{}'.format(x,y)
            if y == 0:
                templates = templates.replace('{{QuestionDescription}}',dataDic[myinputword])
            elif y == 1:
                templates = templates.replace('{{0%Description}}',dataDic[myinputword])
            elif y == 2:
                templates = templates.replace('{{50%Description}}',dataDic[myinputword])
            else:
                templates = templates.replace('{{100%Description}}',dataDic[myinputword])
        newTemp += templates
    front_data += newTemp
    front_data += end_data
    return front_data


@app.route('/updateQuiz', methods=['POST', 'GET'])
def updateQuiz():
    data = dict(request.form)

    newScore = 0
    i = 0
    name,passcode = DataBase.get_studentName_And_passcode_baseon_submissionID(data['ID'])
    student_answer = json.loads(DataBase.get_studentAnswer_baseon_submissionID(data['ID']))

    print("answer: ",student_answer)

    for k,v in data.items():
        if k != 'ID' and k != 'Update Quiz' and k!='username':
            newScore += int(v)
            print(i)
            print(type(student_answer))
            print( type(student_answer[i][3]))
            print(type(student_answer[i]))
            student_answer[i][3] = v
            i += 1

    print("ret: ",DataBase.update_student_quiz(json.dumps(student_answer),data['ID']))


    DataBase.update_student_quizscore(name,passcode,newScore)
    username = data.get("username")
    role = DataBase.get_role_baseon_name(username)



    if role == "Student":
        return redirect("/student_gradebook/"+username, code=301)
    else:
        return redirect("/teacher_grade_book/"+username, code=301)

@app.route('/submission/<role>/<id>', methods=['POST', 'GET'])
def studentSubmission(role,id):

    # submission = {"question1":["actual answer","sudent answer","point receive","point worth"]}
    submission_str = DataBase.get_studentAnswer_baseon_submissionID(id)
    print("id",id)
    if role == "student":
        submission = json.loads(submission_str)
        with open("templates/submission.html", "r") as f:
            t = f.read()
        t = t.replace("submissionID",id)
        template = ""
        i = 0
        startPos = t.find("<h3>{{Question_Name}}: </h3>")
        endPos = t.find('<input value="username123" name="username" hidden>')
        print("subm:",submission)
        print("type: ",type(submission))
        for s in submission:
            i+=1
            questionName = s[0]
            actual_answer = s[1]
            student_answer = s[2]
            point_receive = s[3]
            point_worth = s[4]
            template += "<h3>" + str(i) + ". " + questionName + "</h3>" + "\n"
            template += "<p>Correct Answer: " + actual_answer + "</p >" + "\n"
            template += "<p>Student Answer: " + student_answer + "</p >" + "\n"
            template += "<label>Point Worth : <input type = \"text\" name = \"Choice" + str(i)+"\" size=\"3\" value=\""+ point_receive + "\" readonly/>/" + point_worth + "</label>" + "\n"
            template += "<br>" + "\n" + "<br>" + "\n"

        name = DataBase.get_studentName_And_passcode_baseon_submissionID(id)[0]
        final_temp = t[:startPos] + template + t[endPos:]
        final_temp = final_temp.replace("username123",name)
        return final_temp

    else:
        submission = json.loads(submission_str)
        with open("templates/submission.html", "r") as f:
            t = f.read()
        t = t.replace("submissionID",id)
        template = ""
        i = 0
        startPos = t.find("<h3>{{Question_Name}}: </h3>")
        endPos = t.find('<input value="username123" name="username" hidden>')
        print("type: ",type(submission))
        for s in submission:
            print("s: ",s)
            i+=1
            questionName = s[0]
            actual_answer = s[1]
            student_answer = s[2]
            point_receive = s[3]
            point_worth = s[4]
            template += "<h3>" + str(i) + ". " + questionName + "</h3>" + "\n"
            template += "<p>Correct Answer: " + actual_answer + "</p >" + "\n"
            template += "<p>Student Answer: " + student_answer + "</p >" + "\n"
            template += "<label>Point Worth : <input type = \"text\" name = \"Choice" + str(i)+"\" size=\"3\" value=\""+ point_receive + "\" />/" + point_worth + "</label>" + "\n"
            template += "<br>" + "\n" + "<br>" + "\n"
        passcode = DataBase.get_passcode_baseon_submissionID(id)
        name = DataBase.get_teacherName_baseon_passcode(passcode)
        final_temp = t[:startPos] + template + t[endPos:]
        final_temp = final_temp.replace("username123",name)
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
        print("json quiz:",json_quiz[0])
        quiz = json.loads(json_quiz)
        student_score = 0
        print("quiz:",quiz)
        idx = 0
        studentAnswer = []
        for k,v in data.items():
            if k == 'passcode':
                break

            # studentAnswer = [questionName,questionAnswer,studentAnswer, pointGain, pointTotal
            if v == quiz[idx]["answer"][0]:
                student_score += int(quiz[idx]['point'][0])
                studentAnswer.append([quiz[idx]["question"][0],quiz[idx]["answer"][0],v,quiz[idx]["point"][0],quiz[idx]["point"][0]])
            else:
                studentAnswer.append([quiz[idx]["question"][0],quiz[idx]["answer"][0],v,"0",quiz[idx]["point"][0]])

            idx += 1
        SubmissionID = ''.join(random.choices(string.ascii_lowercase, k=8))
        DataBase.insertScoreRecord(data.get('studentName'),quizName,student_score,passcode,SubmissionID)
        DataBase.insertSubmission(data.get("studentName"),passcode,json.dumps(studentAnswer),SubmissionID)

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
        return final_template


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

    newTemp = ''

    for grade_book in list_of_gradebook:

        quiz_name = grade_book[0]
        score = grade_book[1]
        submissionID = grade_book[2]
        s = templates.replace('QuizName', quiz_name).replace('{{Total Point}}', score).replace('role','student').replace('submissionID',submissionID)
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
    print(list_of_passcode)
    for x in allInformation:
        if x[3] in list_of_passcode:
            quizname = x[1].encode()
            studentname = x[0].encode()
            studentGrade = x[2].encode()
            submissionID = x[4].encode()
            t = template.replace(b'{{QuizName}}', quizname).replace(b'{{StudentName}}', studentname).replace(
                b'{{StudentGrade}}', studentGrade).replace(b"submissionID",submissionID).replace(b"role",b"teacher")
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

        json_quiz,time_limit = DataBase.find_quiz_data(passcode)
        print("time:", time_limit)

        if json_quiz is None:
            return "passcode " + str(passcode) + "is not exist in the database"
        full_quiz = json.loads(json_quiz)

        quiz_template = ""
        final_template = ""
        f = open("templates/quiz.html", "r")
        for line in f:
            final_template += line

        final_template = final_template.replace("999999",time_limit)
        start_pos = final_template.find("<p>Question1:</p>")
        end_pos = final_template.find('<input type="submit" value="Submit" >')
        print("end_pos ",end_pos)
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

                template1 = "<p> " + str(quiz_number)+". "+question + " (" + point + "pts) </p>\n"
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
                template1 = "<p> " + str(quiz_number)+". "+question + " (" + point + "pts) </p>\n"
                template2 = "<input type=\"radio\" id=\"" + str(quiz_number) + "a\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + 'T' + "\">\n"
                template3 = '<label for="' + str(quiz_number) + 'a">' + "True" + '</label><br>\n'

                template4 = "<input type=\"radio\" id=\"" + str(quiz_number) + "b\" name=\"question" + str(
                    quiz_number) + "\" value=\"" + 'F' + "\">\n"
                template5 = '<label for="' + str(quiz_number) + 'b">' + "False/" + '</label><br>\n'
                quiz_template += template1 + template2 + template3 + template4 + template5 + '<br><br>'

            elif question_type == "Short_Answer":
                template1 = "<p> " + str(quiz_number)+". "+question + " (" + point + "pts) </p>\n"
                template2 = "<div class=\"form-group\">" + '\n' +"<label for=\"comment\">Short Question_Answer:</label>" + "<textarea class=\"form-control\" name=\"Answer_"+str(quiz_number)+"\" rows=\"5\" id=\"comment\" required></textarea></div>";
                quiz_template += template1+template2 + '<br><br>'

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
        hr = dict.get("hr")
        min = dict.get("min")

        dic_length = len(dict)
        key_list = list(dict)
        full_quiz = []
        quizname = dict.get("Quiz_name")[0]
        hr = dict.get('Time_Limit_hr')[0]

        min = dict.get('Time_Limit_min')[0]

        teacher_name = dict.get("name")[0]
        print(dict)
        print("teachername: ",teacher_name)
        i = 3
        print("keylist: ",key_list)
        while i < (dic_length-2):

            type = dict.get(key_list[i+1])[0]

            if type == "Multiple_Choice":

                question = {"question": dict.get(key_list[i])}
                question_type = {"type":type}

                point = {"point": dict.get(key_list[i + 2])}

                answer = {"answer": dict.get(key_list[i + 3])}
                print(question,answer,point)
                a = {"choice_A": dict.get(key_list[i + 4])}
                b = {"choice_B": dict.get(key_list[i + 5])}
                c = {"choice_C": dict.get(key_list[i + 6])}
                d = {"choice_D": dict.get(key_list[i + 7])}
                quiz = {}
                for d in (question, question_type,answer, point, a, b, c, d):
                    quiz.update(d)
                full_quiz.append(quiz)
                i += 8
            elif type == "True_or_False":
                question = {"question": dict.get(key_list[i])}
                question_type = {"type":type}
                point = {"point": dict.get(key_list[i + 2])}
                answer = {"answer":dict.get(key_list[i + 3])[0]}
                quiz = {}
                for d in (question, question_type, point,answer):
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

        name = dict.get('Quiz_name')[0]


        print("quiz: ",quiz)
        if dict.get('build quiz') is None:
            print("add question: ",full_quiz)
            f = open("templates/teacher_quiz_generate.html", "r")
            t = ""
            for line in f:
                t += line
            t = t.replace("teacher_name",teacher_name)
            start_pos = t.find('<label>Question1 <input type = "text" name = "Question_1" size="120"/></label >')
            end_pos = t.find(' <p><input type = "submit" value = "Build Quiz" name="build quiz"/></p >')  # security risk
            quiz_template = ""

            i = 1
            js_template = ""

            quizName_template = '<input type = "text" name = "Quiz_name" size="120" value="'+name+'"style="display: inline-block;width: 30%; min-width: 100px;" required/>'
            time_hour_template = '<input type = "text" id="time_limit_hour" name = "Time_Limit_hr" size="100" value="'+hr+'"style="display: inline-block;width: 1%; min-width: 50px;" required/>'
            time_min_template = '<input type = "text" id="time_limit_min" name = "Time_Limit_min" size="100" value="'+min+'"style="display: inline-block;width: 1%; min-width: 50px;" required/>'

            for q in full_quiz:

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
                    quiz_template += '<label> Question' +str(i) + ' <input type = "text" name = "Question_' + str(i)+ '" size="120" value="' + dict.get("Question_" + str(i))[0] + '" required/></label >' + "<br>" +"\n"
                    quiz_template += '<label for="option'+str(i)+'">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type'+str(i)+ '" id="option'+str(i)+'" value="Multiple_Choice" >' +'\n'
                    quiz_template += '<option  value="Multiple_Choice" selected>Multiple Choice</option>' + '\n'
                    # quiz_template += '<option  value="Short_Answer">Short Answer</option>' + '\n'
                    # quiz_template += '<option  value="True_or_False" >T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label>Point Worth : <input type = "text" name = "Point_' + str(i) + '" size="12" value="'+ q.get("point")[0]+'"/></label ><br>' + '\n'
                    quiz_template += '<label>Answer : <input type = "text" name = "Answer_' + str(i) + '" size="12" value="' + q.get("answer")[0]+'"/></label ><br>' + '\n'
                    # print("point: ",q.get("point"))
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content'+str(i)+'">' + '\n'
                    quiz_template += '</p>' + '\n'
                    print("choiceA: ",q.get("choice_A"))
                    # print("choice_A"+ str(i))

                    quiz_template += '<label>ChoiceA <input type = "text" name = "Choice_A_' + str(i) + '" size="120" value="'+str(q.get("choice_A")[0])+'"/></label >' + '\n'
                    quiz_template += '<label>ChoiceB <input type = "text" name = "Choice_B_' + str(i) + '" size="120" value="'+str(q.get("choice_B")[0]) +'"/></label >' + '\n'
                    quiz_template += '<label>ChoiceC <input type = "text" name = "Choice_C_' + str(i) + '" size="120" value="'+str(q.get("choice_C")[0]) +'"/></label >' + '\n'
                    quiz_template += '<label>ChoiceD <input type = "text" name = "Choice_D_' + str(i) + '" size="120" value="'+str(q.get("choice_D")[0]) +'"/></label >' + '\n'
                    quiz_template += '</p>' + '\n'

                elif q.get("type") == "True_or_False":
                    quiz_template += '<label> Question' + str(i) + ' <input type = "text" name = "Question_' + str(i)+ '" size="120" value="' + dict.get("Question_" + str(i))[0] + '"/></label >' + "\n"
                    quiz_template += '<label for="option'+str(i)+'">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type'+str(i)+'" id="option'+str(i)+'" value="True_or_False" >' +'\n'
                    # quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
                    # quiz_template += '<option  value="Short_Answer">Short Answer</option>' + '\n'
                    quiz_template += '<option  value="True_or_False" selected>T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label>Point Worth : <input type = "text" name = "Point_' + str(i) + '" size="120" value="'+str(dict.get("Point_"+ str(i))[0]) +'"/></label >' + '\n'
                    quiz_template += '<br>' + '\n'
                    quiz_template += '<p id="question_content'+str(i)+'">' + '\n'
                    quiz_template += '</p>' + '\n'
                    if q.get("answer") == "True":
                        quiz_template += '<label>True <input type = "radio" name = "T/F' + str(i) + '" size="120" value="True" checked/></label >' + '\n' + '<br>'
                        quiz_template += '<label>False <input type = "radio" name = "T/F' + str(i) + '" size="120" value="False"/></label >' + '\n'
                    else:
                        quiz_template += '<label>True <input type = "radio" name = "T/F' + str(i) + '" size="120" value="True" /></label >' + '\n' + '<br>'
                        quiz_template += '<label>False <input type = "radio" name = "T/F' + str(i) + '" size="120" value="False" checked/></label >' + '\n'
                    quiz_template += '</p>' + '\n'

                elif q.get("type") == "Short_Answer":
                    quiz_template += '<label> Question' +str(i) + ' <input type = "text" name = "Question_' + str(i)+ '" size="120" value="' + q.get("question")[0] + '"/></label >' + "\n"
                    quiz_template += '<label for="option'+str(i)+'">Question Type :</label>' + '\n'
                    quiz_template += '<select name="question_type'+str(i)+ '" id="option'+str(i)+'" value="'+q.get("type")+'" >' +'\n'
                    #quiz_template += '<option  value="Multiple_Choice" >Multiple Choice</option>' + '\n'
                    quiz_template += '<option  value="Short_Answer" selected>Short Answer</option>' + '\n'
                    #quiz_template += '<option  value="True_or_False" >T/F Question </option>' + '\n'
                    quiz_template += '</select><br>' + '\n'
                    quiz_template += '<label>Point Worth : <input type = "text" name = "Point_' + str(i) + '" size="12" value="'+q.get("point")[0]+'"/></label >'
                    quiz_template += '<br>' +'\n'
                    quiz_template += '<p id="question_content'+str(i)+'">' + '\n'
                    quiz_template += '</p>'+ '\n'
                    quiz_template += '<div class="form-group"><label for="comment">Short Question_Answer:</label><textarea class="form-control" name="Answer_'+str(i)+'" rows="5" id="comment" >'+q.get('answer')[0]+'</textarea></div>'
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
            # new_quiz_template += '<p><input type = "submit" value = "Build Quiz" name="build quiz"/></p >' + '\n'
            # new_quiz_template += '<p><input type="submit" value="add Question" name="add question"/></p >' + '\n'
            # new_quiz_template += '<label>ChoiceA <input type = "text" name = "Choice_A_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceB <input type = "text" name = "Choice_B_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceC <input type = "text" name = "Choice_C_' + str(i) + '" size="120" /></label >' + '\n'
            # new_quiz_template += '<label>ChoiceD <input type = "text" name = "Choice_D_' + str(i) + '" size="120" /></label >' + '\n'
            new_quiz_template += '</p>'+'\n'
            js_start_pos = t.find('<p><input value="starting_pos" name="pos" hidden/></p >')+len('<p><input value="starting_pos" name="pos" hidden/></p >')
            template = t[:start_pos] + quiz_template + new_quiz_template + t[end_pos:js_start_pos]+js_template
            template = template.replace("teacher_name", name)
            template = template.replace('<input type = "text" name = "Quiz_name" size="120" style="display: inline-block;width: 30%; min-width: 100px;" required/>',quizName_template)
            template = template.replace('<input type = "text" id="time_limit_hour" name = "Time_Limit_hr" size="100" style="display: inline-block;width: 1%; min-width: 50px;" required/>',time_hour_template)
            template = template.replace('<input type = "text" id="time_limit_min" name = "Time_Limit_min" size="100" style="display: inline-block;width: 1%; min-width: 50px;" required/>',time_min_template)
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


            time_limit = (int(hr)*3600+int(min)*60)*1000

            DataBase.insert_quiz((passcode, teacher_name, quizname, json_quiz,str(time_limit)))
            DataBase.print_Quiz_Data()
            print("find ",template.find("teacher_name"))
            print(teacher_name)
            template = template.replace('/teacher_grade_book','/teacher_grade_book/'+teacher_name)
            template = template.replace("teacher_name", teacher_name)
            return template
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
    DataBase.create_Submission_table()
    DataBase.create_quiz_table()
    DataBase.creat_user_table()
    DataBase.makeScoreRecord()
    app.run(host='0.0.0.0', port=9377, debug=True)
