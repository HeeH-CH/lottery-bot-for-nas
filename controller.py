import os
import sys
from dotenv import load_dotenv

import auth
import lotto645
import notification

load_dotenv()

def check_winning_lotto645(authCtrl: auth.AuthController) -> dict:
    lotto = lotto645.Lotto645()
    item = lotto.check_winning(authCtrl)
    return item

def send_message(mode: int, lottery_type: int, response: dict, email_to: str):
    notify = notification.Notification()

    if mode == 0:
        notify.send_lotto_winning_message(response, email_to)
    elif mode == 1:
        notify.send_lotto_buying_message(response, email_to)
    
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

def buy_lotto645(authCtrl: auth.AuthController, auto_count: int, manual_count: int, manual_numbers: list = None):
    total_count = auto_count + manual_count
    lotto = lotto645.Lotto645()
    response = lotto.buy_lotto645(authCtrl, total_count, auto_count, manual_numbers)
    response['balance'] = lotto.get_balance(auth_ctrl=authCtrl)
    return response

def buy(username_key='USERNAME1', auto_count=0, manual_count=0, manual_numbers=None):
    username, password, email_to = get_credentials_and_email(username_key)
    if not username or not password or not email_to:
        print(f"Missing configuration for {username_key}")
        return

    total_count = auto_count + manual_count
    if total_count < 1 or total_count > 5:
        print("Total count must be between 1 and 5")
        return

    globalAuthCtrl = auth.AuthController()
    try:
        globalAuthCtrl.login(username, password)
    except Exception as e:
        print(e)
        return

    # If manual numbers are provided, repeat the same manual numbers for the manual count
    if manual_numbers:
        repeated_manual_numbers = [manual_numbers] * manual_count
    else:
        repeated_manual_numbers = []

    response = buy_lotto645(globalAuthCtrl, auto_count, manual_count, repeated_manual_numbers)
    send_message(1, 0, response=response, email_to=email_to)

def run():
    if len(sys.argv) < 4:
        print("Usage: python controller.py buy [username1|username2] [auto_count] [manual_count] [manual_numbers...]")
        return

    command = sys.argv[1]
    username_key = sys.argv[2].upper()

    if command == "buy":
        if len(sys.argv) < 5:
            print("Usage: python controller.py buy [username1|username2] [auto_count] [manual_count] [manual_numbers...]")
            return
        auto_count = int(sys.argv[3])
        manual_count = int(sys.argv[4])
        
        manual_numbers = []
        if len(sys.argv) > 5:
            manual_numbers = list(map(int, sys.argv[5].split(',')))

        buy(username_key, auto_count, manual_count, manual_numbers)
    elif command == "check":
        check(username_key)

if __name__ == "__main__":
    run()
