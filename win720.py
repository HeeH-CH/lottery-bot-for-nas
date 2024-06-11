import json
import requests

from bs4 import BeautifulSoup as BS
import auth

class Win720:
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
        "Referer": "https://ol.dhlottery.co.kr/olotto/game/game720.do",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7",
    }

    def buy_Win720(self, auth_ctrl: auth.AuthController, cnt: int) -> dict:
        assert type(auth_ctrl) == auth.AuthController
        assert type(cnt) == int and 1 <= cnt <= 5

        headers = self._generate_req_headers(auth_ctrl)

        data = self._generate_body_for_auto_mode(cnt)

        body = self._try_buying(headers, data)
        self._show_result(body)
        return body

    def _generate_req_headers(self, auth_ctrl: auth.AuthController) -> dict:
        assert type(auth_ctrl) == auth.AuthController
        return auth_ctrl.add_auth_cred_to_headers(self._REQ_HEADERS)

    def _generate_body_for_auto_mode(self, cnt: int) -> dict:
        assert type(cnt) == int and 1 <= cnt <= 5
        SLOTS = ["A", "B", "C", "D", "E"]
        return {
            "direct": "0",
            "nBuyAmount": str(1000 * cnt),
            "param": json.dumps(
                [{"genType": "0", "arrGameChoiceNum": None, "alpabet": slot} for slot in SLOTS[:cnt]]
            ),
            "gameCnt": cnt
        }

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
        weekago = today - timedelta(days=7)
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
