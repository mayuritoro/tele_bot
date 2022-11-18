from files_trial import test_bot 
from files_trial import make_reply
update_id = None
reply = ""
while True:
    tbot = test_bot()
    updates = tbot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for item in updates:
            update_id = item["update_id"]
            print(update_id)
            try:
                try:
                    message = item["message"]["text"]
                    from_= item["message"]["chat"]["id"]
                    name=item['message']['chat']['first_name']
                
                except:
                    message = item["message"]["document"]
                    from_= item["message"]["chat"]["id"]
                    result = item["message"]["document"]["file_id"]
                    name = item["message"]["document"]["file_name"]
                    user_name = item["message"]["from"]["first_name"]
            except:
                message = None
            print("message",message)
            if 'text' in item["message"]:
                reply = make_reply()
            if 'document' in item["message"]:   
                reply = tbot.get_file(result, name, user_name,from_)
            print(reply)
            tbot.send_message(reply,from_)