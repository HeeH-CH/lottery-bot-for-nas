# 소개 

동행복권 
로또자동구매 
예치금은 수동이에요!
총합 5개만 구매가능

# export로 환경변수 등록 했습니다
```
# User
USERNAME1=your_username1
PASSWORD1=abc0!
EMAIL_TO1=recipient1@example.com

USERNAME2=your_username2
PASSWORD2=abc0!!
EMAIL_TO2=recipient2@example.com

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

# 메일관련
메일은 GMAIL SMTP 발급받아 사용하시면 됩니다


# 명령어

명령어 구조
```
# python controller.py {FUNCTION} {USER} {NUMAUTO} {NUMMANUAL} {MANUALNUMBER}
# {FUNCTION} = buy || check   # 구매 || 당첨확인 
# {USER) = USERNAME1 || USERNAME2   # 환경변수에 등록된 유저이름 선택(1개만 선택가능)
# {NUMAUTO} = 0~5   # 자동번호로 구매할 갯수(0~5 선택)
# {NUMMANUAL) = 0~5   # 수동번호로 구매할 갯수(lotto만 해당)
# {MANUALNUMBER} = "1,2,3,4,5,6"   # 6개 숫자 입력(NUMOFMANUAL에 기입한 숫자만큼 한칸뛰고 이어서 작성)
```


예시_Lotto645

```
# 로또 645를 자동 모드로 1장 구매:
python controller.py buy USERNAME1 1 0

# 로또 645를 수동 모드로 2장 구매 (번호: [1,2,3,4,5,6] 및 [7,8,9,10,11,12]):
python controller.py buy USERNAME1 0 2 "1,2,3,4,5,6" "7,8,9,10,11,12"

# 로또 645를 같은번호 수동 모드로 3장 구매 (번호: [1,2,3,4,5,6]):
python controller.py buy USERNAME1 0 3 "1,2,3,4,5,6"

# 로또 645를 자동1 + 수동 2 구매
python controller.py buy USERNAME1 1 2 "1,2,3,4,5,6" "7,8,9,10,11,12"

```

당첨 확인 명령어
```
# 로또 645 당첨 여부 확인:
python controller.py check USERNAME1

```


# 기타
AUTO 모드는 오토이지만 동행복권의 자동선택을 쓰지 않고
파이썬 난수 생성을 하여 수동모드로 번호가 입력되도록 하였습니다


# 참고한 자료

- https://github.com/roeniss/dhlottery-api
- https://github.com/techinpark/lottery-bot
