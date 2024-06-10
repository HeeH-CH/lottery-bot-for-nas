# 소개 

동행복권 사이트내에 계정에 예치금만 넣어두시면 이후 매주 로또를 구입하고 당첨을 체크하여 알려드려요!  

# export로 환경변수 등록 했습니다

# 명령어

Lotto645 명령어 유형

로또 645를 자동 모드로 1장 구매:
python controller.py buy USERNAME1 lotto 1 0
로또 645를 자동 모드로 5장 구매:
python controller.py buy USERNAME1 lotto 5 0

로또 645를 수동 모드로 1장 구매 (번호: [1,2,3,4,5,6]):
python controller.py buy USERNAME1 lotto 0 1 [1,2,3,4,5,6]
로또 645를 수동 모드로 2장 구매 (번호: [1,2,3,4,5,6] 및 [7,8,9,10,11,12]):
python controller.py buy USERNAME1 lotto 0 2 [1,2,3,4,5,6] [7,8,9,10,11,12]

로또 645를 1장 자동 + 2장 수동 구매 (번호: [1,2,3,4,5,6] 및 [7,8,9,10,11,12]):
python controller.py buy USERNAME1 lotto 1 2 [1,2,3,4,5,6] [7,8,9,10,11,12]
로또 645를 2장 자동 + 3장 수동 구매 (번호: [1,2,3,4,5,6], [7,8,9,10,11,12] 및 [13,14,15,16,17,18]):
python controller.py buy USERNAME1 lotto 2 3 [1,2,3,4,5,6] [7,8,9,10,11,12] [13,14,15,16,17,18]


Win720 명령어 유형

연금복권 720을 1장 구매:
python controller.py buy USERNAME1 win720 1 0
연금복권 720을 5장 구매:
python controller.py buy USERNAME1 win720 5 0


혼합 명령어 유형
로또 645를 2장 자동 + 연금복권 720을 3장 구매:
python controller.py buy USERNAME1 both 2 0 3
로또 645를 1장 자동 + 1장 수동(번호: [1,2,3,4,5,6]) + 연금복권 720을 3장 구매:
python controller.py buy USERNAME1 both 1 1 [1,2,3,4,5,6] 3


당첨 확인 명령어

로또 645와 연금복권 720의 당첨 여부 확인:
python controller.py check USERNAME1
이제 모든 유형의 명령어를 통해 로또 645와 연금복권 720을 자동, 수동 및 혼합 

# Reference 

- https://github.com/roeniss/dhlottery-api
