import requests

def send_sms(phone_number, msg_text):
  api_key = '4A2F746D-CA75-BF64-93BC-A58BAE25D160'
  url = "https://sms.ru/sms/send?"
  print(f'{phone_number}: {msg_text}')
  data = {
    'api_id': api_key,
    'to': phone_number,
    'msg': f'SAKURA SHUSHI UZ\nВаш код: {msg_text}',
    'json': 1
  }

  return requests.post(url, data=data)