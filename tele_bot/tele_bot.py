from flask import Flask, request, render_template, redirect
import requests, json, random, pymysql, os
from trial import buttons, button_1, term_life, mediclaim, accidental, existing_user
from config import mysql
from app import app 
from tables import create_table
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.protobuf.json_format import MessageToDict
from datetime import datetime, date
from dateutil.parser import parse
from flask_sqlalchemy import SQLAlchemy
import fnmatch


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tele_bot.db'
db = SQLAlchemy(app)

class user_info(db.Model):
    mobile_no = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.String(50), nullable = False)


class user_plan(db.Model):
    quote_id = db.Column(db.String, primary_key = True, unique = True)
    full_name = db.Column(db.String, nullable = False)
    mobile_no = db.Column(db.String, nullable = False)
    dob = db.Column(db.Date, nullable = False)
    gender = db.Column(db.String, nullable = False)
    education = db.Column(db.String, nullable = False)
    salary = db.Column(db.String, nullable = False)
    # occupation = db.Column(db.String, nullable = False)
    # insurance_plan = db.Column(db.String, nullable = True)
    coverage = db.Column(db.String, nullable = True)
    file_1 = db.Column(db.String, nullable = False, default="File not inserted")
    file_2 = db.Column(db.String, nullable = False,default="File not inserted")
    file_3 = db.Column(db.String, nullable = False,default="File not inserted")
  

class new_records(db.Model):
    quote_id = db.Column(db.String, primary_key = True, unique = True)
    full_name = db.Column(db.String, nullable = False)
    mobile_no = db.Column(db.String, nullable = False) 
    dob = db.Column(db.Date, nullable = False)
    gender = db.Column(db.String, nullable = False)
    education = db.Column(db.String, nullable = False)
    salary = db.Column(db.String, nullable = False)
    occupation = db.Column(db.String, nullable = False)
    file_1 = db.Column(db.String, nullable = False, default="File not inserted")
    file_2 = db.Column(db.String, nullable = False,default="File not inserted")
    file_3 = db.Column(db.String, nullable = False,default="File not inserted")


db.create_all()


action = ""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/excellarate/Downloads/test-riwj-b789ed055ae2.json"

first_name = ""
@app.route('/webhook', methods = ['POST'])
def webhook():
    req = request.get_json(force = True)
    print(req)
    global first_name
    global user_number
    global insurance_plan
    global coverage
    fulfillmentText = ""
    action=req.get('queryResult').get('action')
    if action == "term_life" or action == "mediclaim" or action == "accidental":
        insurance_plan = action
    elif action == "term_life_upto_25" or action == "term_life_upto_50" or action == "term_life_upto_75" or action == "term_life_upto_1cr":
        coverage = action
    elif action == "mediclaim_upto_2L" or action == "mediclaim_upto_5L" or action == "mediclaim_upto_10L" or action == "mediclaim_upto_25L":
        coverage = action
    elif action == "accidental_5L" or action == "accidental_10L" or action == "accidental_25L" or action == "accidental_50L":
        coverage = action
    if request.method == 'POST':
        if action == 'enter_details':
            dialogflow=req.get('queryResult').get('parameters')
            user_name = (dialogflow.get('person'))
            mobile_no = int(dialogflow.get('phone_number'))
            first_name = user_name
            user_number = mobile_no 
            x = ((user_info.query.filter_by(mobile_no = mobile_no).first()))
            if  x:
                fulfillmentText = {"fulfillmentText":"You are an existing user"}#action = "show_details"
            else:
                user = user_info(mobile_no = mobile_no, name = user_name)
                db.session.add(user)
                db.session.commit()
                fulfillmentText = {"fulfillmentText": action}
                
        elif action == "all_details":
            print(first_name)
            quote_id = str(user_number) + "_" + insurance_plan
            dialogflow=req.get('queryResult').get('parameters')
            salary = (dialogflow.get('salary'))
            occupation = (dialogflow.get('occupation'))
            education = (dialogflow.get('education'))
            dob = (dialogflow.get('dob'))
            user_date = datetime.strptime(parse(dob).strftime('%Y-%m-%d'), '%Y-%m-%d').date()
            gender = (dialogflow.get('gender'))
            details = user_plan(quote_id = quote_id, salary = salary, occupation = occupation, education = education, dob = user_date,
            gender = gender, mobile_no = user_number, full_name = first_name )
            db.session.add(details)
            db.session.commit()
            fulfillmentText = {"fulfillmentText":action}
        else:
            print(first_name)
            fulfillmentText = {"fulfillmentText":action}
           
    return fulfillmentText


user_mobile = 0
class telegram_bot():
    
    def __init__(self):
        self.token = "5653233459:AAHWejZRnvy4luWTetBSbQY5jTzS11mA35U"    #write your token here!
        self.url = f"https://api.telegram.org/bot{self.token}"
        
    def get_updates(self, offset=None):
            url = self.url+"/getUpdates?timeout=100"    # In 100 seconds if user input query then process that, use it as the read timeout from the server
            if offset:
                url = url+f"&offset={offset+1}"
            url_info = requests.get(url)
            return json.loads(url_info.content)
    def get_file(self,file_id, id, user_mobile, file_name ):
        url = self.url + f"/getFile"
        content_url = f"https://api.telegram.org/file/bot{self.token}/" 
        response = requests.post(url = url, params = {'file_id':file_id})
        json_response = json.loads(response.content)
        response = requests.get(url = (content_url + json_response['result']['file_path']))
        if os.path.exists("/home/excellarate/Downloads/tele_bot/"+str(user_mobile)+"_"+str(id)):
            print("directory already exists")
        else:
            os.mkdir(str(user_mobile)+"_"+str(id))
        files_name = str(user_mobile)+"_"+file_name
        path = os.path.join(str(user_mobile)+"_"+str(id), files_name)

        with open(path, 'wb') as f:
            f.write(response.content)
        dir_path = '/home/excellarate/Downloads/tele_bot/'
        count = len(fnmatch.filter(os.listdir(dir_path + str(user_mobile)+"_"+str(id) ), '*.*'))
        all_files = os.listdir(dir_path + str(user_mobile)+"_"+str(id) )
        complete_path = dir_path + (str(user_mobile)+"_"+str(id)) +"/"
        reply = ""
        if count == 1:
            reply = "Please upload your Pan Card"
        elif count == 2:
            reply = "Please upload your salary slip"
        elif count == 3:
            reply = "Documents uploaded successfully!"
        result= user_plan.query.filter_by(mobile_no = user_mobile).all()
        if len(all_files) == 3:
            for i in result:
                i.file_1 = complete_path + all_files[0]
                i.file_2 = complete_path + all_files[1]
                i.file_3 = complete_path + all_files[2]   
                db.session.commit()
        return reply
    def send_document(self, chat_id, file_id):
        url = self.url + f"/sendDocument"
        content_url = f"https://api.telegram.org/file/bot{self.token}/"
        response = requests.post(url = url, params = {'chat_id' :chat_id, 'document':file_id})
    
    def send_message(self,msg,chat_id, user_name, file_id):
        global user_mobile
        files = open("logs.txt", "a")
        text_list = ["Username:", user_name, "\n","Message:", msg, "\n", "Date and Time:", str(datetime.now()), "\n"]
        files.writelines(text_list)
        files.close()
        if len(msg) == 10 and '-' not in msg:
            user_mobile = msg
        final_reply = ""
        if len(msg) > 30:
            file_reply = self.get_file(msg,chat_id, user_mobile, file_id)
            final_reply = file_reply
        else:
            reply = detect_intent_texts('test-riwj', chat_id , msg, 'en')
            if reply == 'enter_details':
                buttons(chat_id)
            elif reply == "insurance_plan":
                button_1(chat_id)
            elif reply == "existing_user":
                existing_user(chat_id)
                
            elif reply == "term_life":
                term_life(chat_id)
            elif reply == "mediclaim":
                mediclaim(chat_id)
            elif reply == "accidental":
                accidental(chat_id)
            elif reply == "term_life_upto_25" or reply == "term_life_upto_50" or reply == "term_life_upto_75" or reply == "term_life_upto_1cr":
                final_reply = "Please enter:\n Education\n Date Of Birth\n Gender\n Occuption Type\n Salary"
            elif reply == "mediclaim_upto_2L" or reply == "mediclaim_upto_5L" or reply == "mediclaim_upto_10L" or reply == "mediclaim_upto_25L":
                final_reply = "Please enter:\n Education\n Date Of Birth\n Gender\n Occuption Type\n Salary"
            elif reply == "accidental_5L" or reply == "accidental_10L" or reply == "accidental_25L" or reply == "accidental_50L":
                final_reply = "Please enter:\n Education\n Date Of Birth\n Gender\n Occuption Type\n Salary" 
            elif reply == "all_details":
                final_reply = "Details Entered Successfully!\n Please upload your Aadhar card"
            else:
                final_reply = reply

        print("final reply:", final_reply)
        url = self.url + f"/sendMessage?chat_id={chat_id}&text={final_reply}"
        if msg is not None:
            requests.get(url)
    
   
    def grab_token(self):
            pass

        
def detect_intent_texts(project_id, session_id, texts, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))


    text_input = dialogflow.TextInput(text=texts, language_code=language_code )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    response_json = MessageToDict(response._pb)
    result = response_json['queryResult']
    
    text_1 = ''

    for i in range(len(result['fulfillmentMessages'])):

        text_1 = (result['fulfillmentMessages'][i]['text']['text'][0])

    return text_1

@app.route('/home', methods=['GET', 'POST'])
def home():
    #print(mobile_no)
    #mobile_no = 8329985531
    result= user_plan.query.all()
    if request.method == "GET":
        return render_template('home.html', data = result)
    elif request.method == "POST":
        for i in result:
            new_data = new_records(quote_id = i.quote_id, mobile_no = i.mobile_no, full_name = i.full_name)
            db.session.add(new_data)
            db.session.commit()
        return redirect('/home')

@app.route('/new/<int:mobile_no>', methods=['GET', 'POST'])
def new_page(mobile_no):
    result= user_plan.query.filter_by(mobile_no = mobile_no).all()
    if request.method == "GET":
        return render_template('trial_page.html', data = result)
    elif request.method == "POST":
        for i in result:
            new_data = new_records(quote_id = i.quote_id, mobile_no = i.mobile_no, full_name = i.full_name,salary = i.salary, occupation = i.occupation,
            education = i.education, dob = i.dob, gender = i.gender)
            db.session.add(new_data)
            db.session.commit()
        return redirect('/new/'+str(mobile_no))

@app.route('/')
def index():
    user_mobile = 0
    checker = new_records.query.all()
    result= user_info.query.all()
    for i in result:
        for i in checker:
            user_mobile = i.mobile_no
        if i.mobile_no == user_mobile:
            del_data = user_plan.query.filter_by(mobile_no = user_mobile).delete()
            db.session.commit()
    new_result = user_plan.query.all()
    return render_template('show_details.html', data = new_result) 
     
if (__name__) == "__main__":
    app.run(port = 5000, debug = True)
                




