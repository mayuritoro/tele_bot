from flask import Flask, request
import requests
import json
import random
import os

app = Flask(__name__)

class test_bot():
    def __init__(self):
        self.token = "5653233459:AAHWejZRnvy4luWTetBSbQY5jTzS11mA35U"    #write your token here!
        self.url = f"https://api.telegram.org/bot{self.token}"
        

    def get_updates(self, offset=None):
            url = self.url+"/getUpdates?timeout=100"    # In 100 seconds if user input query then process that, use it as the read timeout from the server
            if offset:
                url = url+f"&offset={offset+1}"
            url_info = requests.get(url)
            return json.loads(url_info.content)
    def get_file(self,file_id, name, user_name, id):
        url = self.url + f"/getFile"
        content_url = f"https://api.telegram.org/file/bot{self.token}/" 
        response = requests.post(url = url, params = {'file_id':file_id})
        json_response = json.loads(response.content)
        response = requests.get(url = (content_url + json_response['result']['file_path']))
        if os.path.exists("/home/excellarate/Downloads/tele_bot/"+user_name+str(id)):
            print("directory already exists")
        else:
            os.mkdir(user_name+ str(id))
        file_name = user_name+str(id)+"_"+name
        path = os.path.join(user_name+str(id), file_name)
        
        with open(path, 'wb') as f:
            f.write(response.content)

        return "successful"
    
    def send_message(self,msg,chat_id):
            url = self.url + f"/sendMessage?chat_id={chat_id}&text={msg}"
            if msg is not None:
                requests.get(url)


def make_reply():
    return "text reply"


if (__name__) == "__main__":
    app.run(port = 5000, debug = True)