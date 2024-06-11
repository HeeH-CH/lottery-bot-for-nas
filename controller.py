import os
import sys
from dotenv import load_dotenv

import auth
import lotto645
import win720
import notification

load_dotenv()

def buy_lotto645(authCtrl: auth.AuthController, cnt: int, mode: str):
    lotto = lotto645.Lotto645()
    _mode = lotto645.Lotto645Mode[mode.upper()]
    response = lotto.buy_lotto645(authCtrl, cnt, _mode)
    response['balance'] = lotto.get_balance(auth_ctrl=authCtrl)
    return response

def check_winning_lotto645(authCtrl: auth.AuthController) -> dict:
    lotto = lotto645.Lotto645()
    item = lotto.check_winning(authCtrl)
    return item

def buy_win720(authCtrl: auth.AuthController, cnt: int):
    pension = win720.Win720()
    response = pension.buy_Win720(authCtrl, cnt)
    response['balance'] = pension.get_balance(auth_ctrl=authCtrl)
    return response

def check_winning_win720(authCtrl: auth.AuthController) -> dict:
    pension = win720.Win720()
    item = pension.check_winning(authCtrl)
    return item

def send_message(mode: int, lottery_type: int, response: dict, email_to: str):
    notify = notification.Notification()

    if mode == 0:
        if lottery_type == 0:
            notify.send_lotto_winning_message(response, email_to)
        else:
            notify.send_win720_winning_message(response, email_to)
    elif mode == 1:
        if lottery_type == 0:
            notify.send_lotto_buying_message(response, email_to)
        else:
            notify.send_win720_buying_message(response, email_to)
    
    # Send email on failure
    if response.get('result', {}).get('resultMsg', 'SUCCESS').upper() != 'SUCCESS':
        subject = "구매 실패 알림"
        message = f"구매 실패: {response.get('result', {}).get('resultMsg', '')}"
        notify._send_email(email_to.split(','), subject, message)

def get_credentials_and_email(username_key):
    username = os.environ.get(username_key)
    password = os.environ.get(f'PASSWORD{username_key[-1]}')
    email_to = os.environ.get(f'EMAIL_TO{username_key[-1]}')
    return username, password, email_to

def check(username_key='USERNAME1'):
    username, password, email_to = get_credentials_and_email(username_key)
    if not username or not password or not email_to:
        print(f"Missing configuration for {username_key}")
        return

    globalAuthCtrl = auth.AuthController()
    try:
        globalAuthCtrl.login(username, password)
    except Exception as e:
        print(e)
        return

    response = check_winning_lotto645(globalAuthCtrl)
    send_message(0, 0, response=response, email_to=email_to)

    response = check_winning_win720(globalAuthCtrl)
    send_message(0, 1, response=response, email_to=email_to)

def buy(username_key='USERNAME1', lottery_type='both', count=1): 
    username, password, email_to = get_credentials_and_email(username_key)
    if not username or not password or not email_to:
        print(f"Missing configuration for {username_key}")
        return

    if count < 1 or count > 5:
        print("Count must be between 1 and 5")
        return

    mode = "AUTO"

    globalAuthCtrl = auth.AuthController()
    try:
        globalAuthCtrl.login(username, password)
    except Exception as e:
        print(e)
        return

    if lottery_type in ['lotto', 'both']:
        response = buy_lotto645(globalAuthCtrl, count, mode)
        send_message(1, 0, response=response, email_to=email_to)

    if lottery_type in ['win720', 'both']:
        response = buy_win720(globalAuthCtrl, count)
        send_message(1, 1, response=response, email_to=email_to)

def run():
    if len(sys.argv) < 4:
        print("Usage: python controller.py [buy|check] [username1|username2] [lotto|win720|both] [count]")
        return

    command = sys.argv[1]
    username_key = sys.argv[2].upper()
    lottery_type = sys.argv[3].lower()
    count = int(sys.argv[4])

    if command == "buy":
        buy(username_key, lottery_type, count)
    elif command == "check":
        check(username_key)

if __name__ == "__main__":
    run()
