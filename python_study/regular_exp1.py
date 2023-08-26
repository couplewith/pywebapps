import re

in_array = ["가나 : 123566",        # 한글 Or 숫자
            "가나힟 : 가123566",     # 한글 + 숫자
            "가뿱뿕힣   :   가123566",   # 한글 + 숫자
            "가나Any : 가Any123566",     # 한글 + 영어 + 숫자
            "abcㄱㄴㄷ  :  abcㄱㄴㄷ31213", # 한글자음 + 영어 + 숫자
            "가ㄹ나 : 가ㄱㄴ123566",        # 한글자음 + 숫자
            "abc     :   1tab312312223123",   # 공백 + TAB
            "탭탭     :   tabtabafasdf2223123", # 공백 + TAB
            "12349  : 012312223123" ]      # 숫자


reg_pattern1 = r'([ㄱ-ㅣ가-힣]+|\w+)(\s{0,}):(\s{0,})(\w+)$'  # 한글 문자열을 인식하는 정규표현식
print(" Result case 1-------------------------------")

for key, arr_value in enumerate(in_array):
    #print("[%s] -> [%s]  " %(key , arr_value) )

    match = re.match(reg_pattern1, arr_value)
    if match:
        print(f" {key}  > Result Success ==== :  '{match.group(1)}', '{match.group(4)}' ")
    else:
        print(f" {key} > Result Failed  ---- :   '{match}'     <<- {arr_value}")


reg_pattern2 = r'(\w+|\W+)(\s+|\b):(\b|\s+)(\w+)$'
print("\n Result case 2-------------------------------")

for key, arr_value in enumerate(in_array):
    #print("[%s] -> [%s]  " %(key , arr_value) )

    match = re.match(reg_pattern2, arr_value)
    if match:
        print(f" {key}  > Result Success ==== : {key} : '{match.group(1)}', '{match.group(4)}' ")
    else:
        print(f" {key} > Result Failed  ---- :   '{match}'     <<- {arr_value}")