import json
import os
import sys
from dotenv import load_dotenv
import auth
import lotto645
import win720
import notification

def load_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings

def buy_lotto645(auth_ctrl, settings, username):
    lotto = lotto645.Lotto645()
    user_settings = settings[username]
    lotto_settings = user_settings['lotto']
    
    auto_count = lotto_settings['auto_count']
    manual_count = lotto_settings['manual_count']
    manual_numbers = lotto_settings.get('manual_numbers', [])
    
    responses = []
    
    if auto_count > 0:
        _mode = lotto645.Lotto645Mode.AUTO
        response = lotto.buy_lotto645(auth_ctrl, auto_count, _mode)
        response['balance'] = lotto.get_balance(auth_ctrl=auth_ctrl)
        responses.append(response)
    
    if manual_count > 0 and len(manual_numbers) >= manual_count:
        _mode = lotto645.Lotto645Mode.MANUAL
        response = lotto.buy_lotto645(auth_ctrl, manual_count, _mode, manual_numbers[:manual_count])
        response['balance'] = lotto.get_balance(auth_ctrl=auth_ctrl)
        responses.append(response)
    
    return responses

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

def send_message(notification_type, lottery_type, responses, to_email):
    notify = notification.Notification()

    for response in responses:
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

def check_and_send_results(settings):
    load_dotenv()

    auth_ctrl1 = auth.AuthController()
    auth_ctrl2 = auth.AuthController()

    auth_ctrl1.login(os.getenv('USERNAME1'), os.getenv('PASSWORD1'))
    auth_ctrl2.login(os.getenv('USERNAME2'), os.getenv('PASSWORD2'))

    to_email1 = os.getenv('USERNAME1')
    to_email2 = os.getenv('USERNAME2')

    # 로또 당첨 확인
    result = check_winning_lotto645(auth_ctrl1)
    send_message('win', 'lotto', [result], to_email1)

    result = check_winning_lotto645(auth_ctrl2)
    send_message('win', 'lotto', [result], to_email2)

    # 연금복권 당첨 확인
    result = check_winning_win720(auth_ctrl1)
    send_message('win', 'win720', [result], to_email1)

    result = check_winning_win720(auth_ctrl2)
    send_message('win', 'win720', [result], to_email2)

def buy_and_send_results(settings):
    load_dotenv()

    auth_ctrl1 = auth.AuthController()
    auth_ctrl2 = auth.AuthController()

    auth_ctrl1.login(os.getenv('USERNAME1'), os.getenv('PASSWORD1'))
    auth_ctrl2.login(os.getenv('USERNAME2'), os.getenv('PASSWORD2'))

    to_email1 = os.getenv('USERNAME1')
    to_email2 = os.getenv('USERNAME2')

    if settings['USERNAME1']['buy_lotto']:
        responses = buy_lotto645(auth_ctrl1, settings, 'USERNAME1')
        send_message('buy', 'lotto', responses, to_email1)

    if settings['USERNAME1']['buy_win720']:
        response = buy_win720(auth_ctrl1)
        send_message('buy', 'win720', [response], to_email1)

    if settings['USERNAME2']['buy_lotto']:
        responses = buy_lotto645(auth_ctrl2, settings, 'USERNAME2')
        send_message('buy', 'lotto', responses, to_email2)

    if settings['USERNAME2']['buy_win720']:
        response = buy_win720(auth_ctrl2)
        send_message('buy', 'win720', [response], to_email2)

def run():
    settings = load_settings()

    if len(sys.argv) < 2:
        print("Usage: python controller.py [buy|check]")
        return

    if sys.argv[1] == "buy":
        buy_and_send_results(settings)
    elif sys.argv[1] == "check":
        check_and_send_results(settings)

if __name__ == "__main__":
    run()
