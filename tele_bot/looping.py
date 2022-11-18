from tele_bot import telegram_bot 
update_id = None
message = ""
from_ = ""

while True:
    tbot = telegram_bot()
    updates = tbot.get_updates(offset=update_id)
    updates = updates['result']
    print(updates)
   
    if updates:
        for item in updates:
            update_id = item["update_id"]
            if 'message' in item:
                if 'text' in item["message"]:
                    message = item["message"]["text"]
                    user_name = item["message"]["from"]["username"]
                    name=item['message']['chat']['first_name']
                    from_ = item["message"]["chat"]["id"]
                elif 'document' in item["message"]:
                    message = item["message"]["document"]["file_id"]
                    user_name = item["message"]["from"]["username"]
                    name = item["message"]["document"]["file_name"]
                    from_ = item["message"]["chat"]["id"]
                elif 'photo' in item["message"]:
                    message = item["message"]["photo"][0]["file_id"]
                    name = item["message"]["photo"][0]["file_id"]
                    from_ = item["message"]["chat"]["id"]
            elif 'callback_query' in item:
                message=item['callback_query']['data']
                user_name = item["callback_query"]["from"]["username"]
                from_= item["callback_query"]['from']['id']
                name = ""
            #print("message",message)
            
                
            print("message",message)

            tbot.send_message(message,from_, user_name, name)
