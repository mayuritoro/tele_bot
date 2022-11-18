import requests
import json
url = "https://api.telegram.org/bot5653233459:AAHWejZRnvy4luWTetBSbQY5jTzS11mA35U/sendMessage"

photo_url = "https://api.telegram.org/bot5653233459:AAHWejZRnvy4luWTetBSbQY5jTzS11mA35U/sendPhoto"

document_url = "https://api.telegram.org/bot5653233459:AAHWejZRnvy4luWTetBSbQY5jTzS11mA35U/sendDocument"

def buttons(chat_id):
  payload = {
      "photo": "https://blog.mint.com/wp-content/uploads/2013/02/1.jpg",
      #"caption": caption,
      "chat_id": chat_id,
      "reply_markup": {
          "inline_keyboard": [
              [
                  {
                      "text": "Show Plans",
                      "callback_data": "Insurance Plan"
                  }
              ]
          ]
      }
  }
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
  }

  response = requests.post(photo_url, json=payload)


def button_1(chat_id):
  payload = {
      "photo": "AgACAgUAAxkBAAIGv2Mhrr21NIyhQKZHdVnObrNS0_SdAAIStTEb3U4IVSXi2GZ7s3TqAQADAgADcwADKQQ",
      "chat_id": chat_id,
    #   "text": "Select one option",
      "reply_markup": {
          "inline_keyboard": [
              [
                  {
                      "text": "Term Life",
                      "callback_data": "Term Life"
                  },
                  {
                      "text": "mediclaim",
                      "callback_data": "Mediclaim"
                  },
                  {
                      "text": "Accidental",
                      "callback_data": "Accidental Insurance"
                  },

              ]
          ]
      }
  }
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
  }

  response = requests.post(photo_url, json=payload)
  print(response)


def term_life(chat_id):
  payload = {
      "chat_id": chat_id,
      'document': 'BQACAgUAAxkBAAIClGMIdmbOEsi8xsAic-Bk0UahnIl5AAJCBgACDBJBVBLbNwoHbsUhKQQ',
      #"text": "Choose Your Plan",
      "reply_markup": {
          "inline_keyboard": [
              [
                  {
                      "text": "25Lac",
                      "callback_data": "25Lac"
                  },
                  {
                      "text": "50Lac",
                      "callback_data": "50Lac"
                  },
                  {
                      "text": "75Lac",
                      "callback_data": "75Lac"
                  },
                  {
                      "text": "1Cr",
                      "callback_data": "1r"
                  },

              ]
          ]
      }
  }
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
  }

  response = requests.post(document_url, json=payload)


def mediclaim(chat_id):
  payload = {
      "chat_id": chat_id,
      #"text": "Choose Your Plan",
      "document":"BQACAgUAAxkBAAICmmMIeJtMVL1v2JTsRhsdMb4uSDvCAAJEBgACDBJBVKwG4QUSEWW7KQQ",
      "reply_markup": {
          "inline_keyboard": [
              [
                  {
                      "text": "2Lac",
                      "callback_data": "mediclaim up to 2Lac"
                  },
                  {
                      "text": "5Lac",
                      "callback_data": "mediclaim up to 5Lac"
                  },
                  {
                      "text": "10Lac",
                      "callback_data": "mediclaim up to 10Lac"
                  },
                  {
                      "text": "25Lac",
                      "callback_data": "mediclaim up to 25Lac"
                  },

              ]
          ]
      }
  }
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
  }

  response = requests.post(document_url, json=payload)

def accidental(chat_id):
  payload = {
      "chat_id": chat_id,
      #"text": "Choose Your Plan",
      "document":"BQACAgUAAxkBAAICmGMIeJMERoZF4atIdkk_L-cYGESUAAJDBgACDBJBVCJlGZUyjyGkKQQ",
      "reply_markup": {
          "inline_keyboard": [
              [
                  {
                      "text": "5Lac",
                      "callback_data": "Plan of 5Lac"
                  },
                  {
                      "text": "10Lac",
                      "callback_data": "Plan of 10Lac"
                  },
                  {
                      "text": "25Lac",
                      "callback_data": "Plan of 25Lac"
                  },
                  {
                      "text": "50Lac",
                      "callback_data": "Plan of 50Lac"
                  },

              ]
          ]
      }
  }
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
  }

  response = requests.post(document_url, json=payload)

def existing_user(chat_id):
  payload = {
      "chat_id": chat_id,
      "text": "Seems you are an existing user! To see your details click here ",
      "reply_markup": {
          "inline_keyboard": [
              [
                  {
                      "text": "Show Details",
                      "callback_data": "show details"
                  }
              ]
          ]
      }
  }
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)

#print(response.text)
# import requests

# url = "https://api.telegram.org/bot5340261920:AAF2GGInKosubny7ox-CWeZyl8IMESgQg5o/sendPhoto"

# payload = {
#     "photo": "AgACAgUAAxkBAAMLYvDs4xqN8GzQGUY555yHLr5joacAAjGxMRtMw4hX56puCadfo3cBAAMCAAN5AAMpBA",
#     # "caption": "Optional",
#     # "disable_notification": False,
#     "reply_to_message_id": 0,
#     "chat_id":1091996976 
# }
# headers = {
#     "Accept": "application/json",
#     "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
#     "Content-Type": "application/json"
# }

# response = requests.post(url, json=payload)

# print(response.text)


