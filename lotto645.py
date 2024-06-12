import json
import datetime
import requests
import random

from bs4 import BeautifulSoup as BS
from datetime import timedelta
import auth

class Lotto645:
    _REQ_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://ol.dhlottery.co.kr",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "https://ol.dhlottery.co.kr/olotto/game/game645.do",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7",
    }

    def buy_lotto645(self, auth_ctrl: auth.AuthController, total_count: int, auto_count: int, manual_numbers: list = None) -> dict:
        assert type(auth_ctrl) == auth.AuthController
        assert type(total_count) == int and 1 <= total_count <= 5
        assert type(auto_count) == int and 0 <= auto_count <= total_count

        headers = self._generate_req_headers(auth_ctrl)
        requirements = self._get_requirements(headers)

        if manual_numbers is None:
            manual_numbers = []

        # Generate random numbers for the automatic slots
        for _ in range(auto_count):
            manual_numbers.append(self._generate_random_lotto_numbers())

        data = self._generate_body_for_manual(total_count, requirements, manual_numbers)
        body = self._try_buying(headers, data)
        self._show_result(body)
        return body

    def _generate_random_lotto_numbers(self):
        return sorted(random.sample(range(1, 46), 6))

    def _generate_body_for_manual(self, total_count: int, requirements: list, manual_numbers: list) -> dict:
        assert type(total_count) == int and 1 <= total_count <= 5
        assert type(manual_numbers) == list and all(isinstance(nums, list) and len(nums) == 6 for nums in manual_numbers)

        def format_number(num):
            return f"{num:02}"

        SLOTS = ["A", "B", "C", "D", "E"]
        return {
            "round": self._get_round(),
            "direct": requirements[0],
            "nBuyAmount": str(1000 * total_count),
            "param": json.dumps(
                [{"genType": "1", "arrGameChoiceNum": ",".join(map(format_number, nums)), "alpabet": slot} for nums, slot in zip(manual_numbers, SLOTS[:total_count])]
            ),
            'ROUND_DRAW_DATE': requirements[1],
            'WAMT_PAY_TLMT_END_DT': requirements[2],
            "gameCnt": total_count
        }

    def _generate_req_headers(self, auth_ctrl: auth.AuthController) -> dict:
        assert type(auth_ctrl) == auth.AuthController
        return auth_ctrl.add_auth_cred_to_headers(self._REQ_HEADERS)

    def _get_requirements(self, headers: dict) -> list:
        assert type(headers) == dict

        headers["Referer"] = "https://ol.dhlottery.co.kr/olotto/game/game645.do"
        headers["Content-Type"] = "application/json; charset=UTF-8"
        headers["X-Requested-With"] = "XMLHttpRequest"

        res = requests.post("https://ol.dhlottery.co.kr/olotto/game/egovUserReadySocket.json", headers=headers)
        direct = json.loads(res.text)["ready_ip"]

        res = requests.post("https://ol.dhlottery.co.kr/olotto/game/game645.do", headers=headers)
        soup = BS(res.text, "html5lib")
        draw_date = soup.find("input", id="ROUND_DRAW_DATE").get('value')
        tlmt_date = soup.find("input", id="WAMT_PAY_TLMT_END_DT").get('value')

        return [direct, draw_date, tlmt_date]

    def _get_round(self) -> str:
        res = requests.get("https://www.dhlottery.co.kr/common.do?method=main")
        soup = BS(res.text, "html5lib")
        last_drawn_round = int(soup.find("strong", id="lottoDrwNo").text)
        return str(last_drawn_round + 1)

    def get_balance(self, auth_ctrl: auth.AuthController) -> str:
        headers = self._generate_req_headers(auth_ctrl)
        res = requests.post("https://dhlottery.co.kr/userSsl.do?method=myPage", headers=headers)
        soup = BS(res.text, "html5lib")
        balance = soup.find("p", class_="total_new").find('strong').text
        return balance

    def _try_buying(self, headers: dict, data: dict) -> dict:
        assert type(headers) == dict
        assert type(data) == dict

        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        res = requests.post("https://ol.dhlottery.co.kr/olotto/game/execBuy.do", headers=headers, data=data)

        res.encoding = "utf-8"
        return json.loads(res.text)

    def check_winning(self, auth_ctrl: auth.AuthController) -> dict:
        assert type(auth_ctrl) == auth.AuthController

        headers = self._generate_req_headers(auth_ctrl)
        parameters = self._make_search_date()

        data = {
            "nowPage": 1,
            "searchStartDate": parameters["searchStartDate"],
            "searchEndDate": parameters["searchEndDate"],
            "winGrade": 1,
            "lottoId": "LO40",
            "sortOrder": "DESC"
        }

        res = requests.post("https://dhlottery.co.kr/myPage.do?method=lottoBuyList", headers=headers, data=data)
        soup = BS(res.text, "html5lib")

        winnings = soup.find("table", class_="tbl_data tbl_data_col").find("tbody").find_all("td")
        if len(winnings) == 1:
            return {"data": "no winning data"}

        return {
            "round": winnings[2].text.strip(),
            "money": winnings[6].text.strip(),
            "purchased_date": winnings[0].text.strip(),
            "winning_date": winnings[7].text.strip()
        }

    def _make_search_date(self) -> dict:
        today = datetime.datetime.today()
        today_str = today.strftime("%Y%m%d")
        weekago = today - timedelta(days=21)
        weekago_str = weekago.strftime("%Y%m%d")
        return {
            "searchStartDate": weekago_str,
            "searchEndDate": today_str
        }

    def _show_result(self, body: dict) -> None:
        assert type(body) == dict
        if body.get("loginYn") != "Y":
            print("Login failed.")
            return

        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() == "SUCCESS":
            print("Purchase successful.")
        else:
            print("Purchase failed: " + result.get("resultMsg", "Unknown error"))
