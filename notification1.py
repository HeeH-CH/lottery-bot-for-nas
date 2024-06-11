import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Notification:
    def send_lotto_buying_message(self, body: dict, email_to: str) -> None:
        email_list = email_to.split(',')
        result = body.get("result", {})
        subject = f"{result.get('buyRound', 'Unknown')}회 로또 구매 결과"
        if result.get("resultMsg", "FAILURE").upper() == "SUCCESS":
            lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
            message = f"{result['buyRound']}회 로또 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n{lotto_number_str}"
        else:
            message = f"로또 구매 실패: {result.get('resultMsg', '')}"
        self._send_email(email_list, subject, message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list

        lotto_number = [x[:-1] for x in lotto_number]
        lotto_number = [x.replace("|", " ") for x in lotto_number]
        lotto_number = '\n'.join(x for x in lotto_number)
        
        return lotto_number

    def send_win720_buying_message(self, body: dict, email_to: str) -> None:
        email_list = email_to.split(',')
        if body.get("resultCode") == '100':
            win720_round = body.get("resultMsg").split("|")[3]
            win720_number_str = self.make_win720_number_message(body.get("saleTicket"))
            subject = f"{win720_round}회 연금복권 구매 완료"
            message = f"{win720_round}회 연금복권 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n{win720_number_str}"
        else:
            subject = "연금복권 구매 실패"
            message = f"연금복권 구매 실패: {body.get('resultMsg', '')}"
        self._send_email(email_list, subject, message)

    def make_win720_number_message(self, win720_number: str) -> str:
        return "\n".join(win720_number.split(","))

    def send_lotto_winning_message(self, winning: dict, email_to: str) -> None:
        email_list = email_to.split(',')
        try:
            round = winning["round"]
            money = winning["money"]
            subject = f"로또 {winning['round']}회 당첨"
            message = f"로또 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            self._send_email(email_list, subject, message)
        except KeyError:
            return

    def send_win720_winning_message(self, winning: dict, email_to: str) -> None:
        email_list = email_to.split(',')
        try:
            round = winning["round"]
            money = winning["money"]
            subject = f"연금복권 {winning['round']}회 당첨"
            message = f"연금복권 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            self._send_email(email_list, subject, message)
        except KeyError:
            return

    def _send_email(self, email_list: list, subject: str, message: str) -> None:
        host = os.environ.get('EMAIL_HOST')
        port = int(os.environ.get('EMAIL_PORT'))
        host_user = os.environ.get('EMAIL_HOST_USER')
        host_password = os.environ.get('EMAIL_HOST_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = host_user
        msg['To'] = ', '.join(email_list)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(host_user, host_password)
            server.sendmail(host_user, email_list, msg.as_string())
