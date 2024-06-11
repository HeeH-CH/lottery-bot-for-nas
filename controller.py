import os
import sys
from dotenv import load_dotenv
import auth
import lotto645
import win720
import notification

def buy_lotto645(auth_ctrl, cnt, mode, numbers=None):
    lotto = lotto645.Lotto645()
    _mode = lotto645.Lotto645Mode[mode.upper()]
    response = lotto.buy_lotto645(auth_ctrl, cnt, _mode, numbers)
    response['balance'] = lotto.get_balance(auth_ctrl=auth_ctrl)
    return response

def check_winning_lotto645(auth_ctrl):
    lotto = lotto645.Lotto645()
    return lotto.check_winning(auth_ctrl)

def buy_win720(auth_ctrl):
    pension = win720.Win720()
    response = pension.buy_Win720(auth_ctrl)
    response['balance'] = pension.get_balance(auth_ctrl=auth_ctrl)
    return response

def check_winning_win720(auth_ctrl):
    pension = win720.Win720()
    return pension.check_winning(auth_ctrl)

def send_message(notification_type, lottery_type, response, to_email):
    notify = notification.Notification()

    if notification_type == 'buy':
        if lottery_type == 'lotto':
            notify.send_lotto_buying_message(response, to_email)
        elif lottery_type == 'win720':
            notify.send_win720_buying_message(response, to_email)
    elif notification_type == 'win':
        if lottery_type == 'lotto':
            notify.send_lotto_winning_message(response, to_email)
        elif lottery_type == 'win720':
            notify.send_win720_winning_message(response, to_email)

def check_and_send_results():
    load_dotenv()

    auth_ctrl1 = auth.AuthController()
    auth_ctrl2 = auth.AuthController()

    auth_ctrl1.login(os.getenv('USERNAME1'), os.getenv('PASSWORD1'))
    auth_ctrl2.login(os.getenv('USERNAME2'), os.getenv('PASSWORD2'))

    to_email1 = os.getenv('USERNAME1')
    to_email2 = os.getenv('USERNAME2')

    # 로또 당첨 확인
    result = check_winning_lotto645(auth_ctrl1)
    send_message('win', 'lotto', result, to_email1)

    result = check_winning_lotto645(auth_ctrl2)
    send_message('win', 'lotto', result, to_email2)

    # 연금복권 당첨 확인
    result = check_winning_win720(auth_ctrl1)
    send_message('win', 'win720', result, to_email1)

    result = check_winning_win720(auth_ctrl2)
    send_message('win', 'win720', result, to_email2)

def buy_and_send_results():
    load_dotenv()

    auth_ctrl1 = auth.AuthController()
    auth_ctrl2 = auth.AuthController()

    auth_ctrl1.login(os.getenv('USERNAME1'), os.getenv('PASSWORD1'))
    auth_ctrl2.login(os.getenv('USERNAME2'), os.getenv('PASSWORD2'))

    to_email1 = os.getenv('USERNAME1')
    to_email2 = os.getenv('USERNAME2')

    count = int(os.getenv('COUNT'))
    mode = os.getenv('MODE')

    # 로또 구매
    response = buy_lotto645(auth_ctrl1, count, mode)
    send_message('buy', 'lotto', response, to_email1)

    response = buy_lotto645(auth_ctrl2, count, mode)
    send_message('buy', 'lotto', response, to_email2)

    # 연금복권 구매
    response = buy_win720(auth_ctrl1)
    send_message('buy', 'win720', response, to_email1)

    response = buy_win720(auth_ctrl2)
    send_message('buy', 'win720', response, to_email2)

def run():
    if len(sys.argv) < 2:
        print("Usage: python controller.py [buy|check]")
        return

    if sys.argv[1] == "buy":
        buy_and_send_results()
    elif sys.argv[1] == "check":
        check_and_send_results()

if __name__ == "__main__":
    run()
