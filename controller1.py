import os
import sys
from dotenv import load_dotenv

import auth
import lotto645
import win720
import notification

load_dotenv()

def get_credentials_and_email(username_key):
    username = os.environ.get(username_key)
    password = os.environ.get(f'PASSWORD{username_key[-1]}')
    email_to = os.environ.get(f'EMAIL_TO{username_key[-1]}')
    return username, password, email_to

def buy_lotto645(authCtrl: auth.AuthController, auto_cnt: int, manual_cnt: int, manual_numbers: list = None):
    lotto = lotto645.Lotto645()
    response = lotto.buy_lotto645(authCtrl, auto_cnt, manual_cnt, manual_numbers)
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

def buy_and_check(username_key='USERNAME1', lottery_type='both', auto_count=0, manual_count=0, manual_numbers=None, win720_count=0):
    username, password, email_to = get_credentials_and_email(username_key)
    if not username or not password or not email_to:
        print(f"Missing configuration for {username_key}")
        return

    if auto_count + manual_count < 1 or auto_count + manual_count > 5:
        print("Total lotto count must be between 1 and 5")
        return

    if win720_count < 0 or win720_count > 5:
        print("Total win720 count must be between 0 and 5")
        return

    globalAuthCtrl = auth.AuthController()
    try:
        globalAuthCtrl.login(username, password)
    except Exception as e:
        print(e)
        return

    notify = notification.Notification()
    
    # Check winning history
    winning_message = ""
    lotto_winning_response = check_winning_lotto645(globalAuthCtrl)
    if lotto_winning_response.get("data") != "no winning data":
        notify.send_lotto_winning_message(lotto_winning_response, email_to)
        winning_message += f"로또 당첨 이력:\n{lotto_winning_response}\n\n"
    else:
        winning_message += "로또 당첨 이력이 없습니다.\n\n"

    win720_winning_response = check_winning_win720(globalAuthCtrl)
    if win720_winning_response.get("data") != "no winning data":
        notify.send_win720_winning_message(win720_winning_response, email_to)
        winning_message += f"연금복권 당첨 이력:\n{win720_winning_response}\n\n"
    else:
        winning_message += "연금복권 당첨 이력이 없습니다.\n\n"

    # Buy lottery tickets
    buying_message = ""
    if lottery_type in ['lotto', 'both']:
        lotto_response = buy_lotto645(globalAuthCtrl, auto_count, manual_count, manual_numbers)
        notify.send_lotto_buying_message(lotto_response, email_to)
        buying_message += f"로또 구매 이력:\n{lotto_response}\n\n"

    if lottery_type in ['win720', 'both']:
        if win720_count > 0:
            win720_response = buy_win720(globalAuthCtrl, win720_count)
            notify.send_win720_buying_message(win720_response, email_to)
            buying_message += f"연금복권 구매 이력:\n{win720_response}\n\n"
        else:
            buying_message += "연금복권 구매 이력이 없습니다.\n\n"

    if not buying_message:
        buying_message = "구매 이력이 없습니다.\n\n"

    # Combine and send the final message
    final_message = f"당첨 이력:\n{winning_message}\n구매 이력:\n{buying_message}"
    notify._send_email(email_to.split(','), "로또 및 연금복권 구매 및 당첨 이력", final_message)

def buy(username_key='USERNAME1', lottery_type='both', auto_count=0, manual_count=0, manual_numbers=None, win720_count=0):
    username, password, email_to = get_credentials_and_email(username_key)
    if not username or not password or not email_to:
        print(f"Missing configuration for {username_key}")
        return

    if auto_count + manual_count < 1 or auto_count + manual_count > 5:
        print("Total lotto count must be between 1 and 5")
        return

    if win720_count < 0 or win720_count > 5:
        print("Total win720 count must be between 0 and 5")
        return

    globalAuthCtrl = auth.AuthController()
    try:
        globalAuthCtrl.login(username, password)
    except Exception as e:
        print(e)
        return

    notify = notification.Notification()
    
    # Buy lottery tickets
    buying_message = ""
    if lottery_type in ['lotto', 'both']:
        lotto_response = buy_lotto645(globalAuthCtrl, auto_count, manual_count, manual_numbers)
        notify.send_lotto_buying_message(lotto_response, email_to)
        buying_message += f"로또 구매 이력:\n{lotto_response}\n\n"

    if lottery_type in ['win720', 'both']:
        if win720_count > 0:
            win720_response = buy_win720(globalAuthCtrl, win720_count)
            notify.send_win720_buying_message(win720_response, email_to)
            buying_message += f"연금복권 구매 이력:\n{win720_response}\n\n"
        else:
            buying_message += "연금복권 구매 이력이 없습니다.\n\n"

    if not buying_message:
        buying_message = "구매 이력이 없습니다.\n\n"

    # Send the final message
    notify._send_email(email_to.split(','), "로또 및 연금복권 구매 이력", buying_message)

def run():
    if len(sys.argv) < 6:
        print("Usage: python controller.py [buy|buy_and_check] [username1|username2] [lotto|win720|both] [auto_count] [manual_count] [win720_count] [manual_numbers]")
        return

    command = sys.argv[1]
    username_key = sys.argv[2].upper()
    lottery_type = sys.argv[3].lower()
    auto_count = int(sys.argv[4])
    manual_count = int(sys.argv[5])
    win720_count = int(sys.argv[6])
    manual_numbers = sys.argv[7:] if len(sys.argv) > 7 else None

    if command == "buy":
        buy(username_key, lottery_type, auto_count, manual_count, manual_numbers, win720_count)
    elif command == "buy_and_check":
        buy_and_check(username_key, lottery_type, auto_count, manual_count, manual_numbers, win720_count)

if __name__ == "__main__":
    run()
