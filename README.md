# 소개 

동행복권 사이트내에 계정에 예치금만 넣어두시면 이후 매주 로또를 구입하고 당첨을 체크하여 알려드려요!  

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

# 명령어

명령어 구조
```
# python controller.py {FUNCTION} {USER} {PRODUCT} {NUMOFAUTO} {NUMOFMANUAL} {SLOT}
# {FUNCTION} = buy || check   # 구매 || 당첨확인 
# {USER) = USERNAME1 || USERNAME2   # 환경변수에 등록된 유저이름 선택(1개만 선택가능)
# {PRODUCT} = lotto || win720 || both # 로또 || 연금복권 || 둘다
# {NUMOFAUTO} = 0~5   # 자동번호로 구매할 갯수(0~5 선택)
# {NUMOFMANUAL) = 0~5   # 수동번호로 구매할 갯수(lotto만 해당)
# {SLOT} = [1,2,3,4,5,6,]   # 6개 숫자 입력(NUMOFMANUAL에 기입한 숫자만큼 한칸뛰고 이어서 작성)
```


예시_Lotto645

```
# 로또 645를 자동 모드로 1장 구매:
python controller.py buy USERNAME1 AUTO 1

# 로또 645를 수동 모드로 2장 구매 (번호: [1,2,3,4,5,6] 및 [7,8,9,10,11,12]):
python controller.py buy USERNAME1 Manual 2 [1,2,3,4,5,6] [7,8,9,10,11,12]

```

당첨 확인 명령어
```
# 로또 645 당첨 여부 확인:
python controller.py check USERNAME1

```
 

# Reference 

- https://github.com/roeniss/dhlottery-api
- https://github.com/techinpark/lottery-bot
