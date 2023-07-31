import re

in_array = ["가나 : 123566",
            "가나힟 : 가123566",
            "가나팖빫나 : 가123566",
            " 힣   :   가123566",
            " 가나Any : 가123566",
            " abc  :  1tab312312223123",
            " 가 나 : 가123566",
            " abc  :  1tab312312223123",
            " 탭탭     :     tabtabafasdf2223123",
            " 6    :  1tab312312223123",
            " F      -       tabtabafasdf2223123"]


reg_pattern1 = r'([가-힣]+|\w+)(\s*):(\s*)(\w+)$'  # 한글 문자열을 인식하는 정규표현식
print(" Result case 1-------------------------------")

for key, arr_value in enumerate(in_array):
    print("[%s] -> [%s]  " %(key , arr_value) )

    match = re.match(reg_pattern1, arr_value)
    if match:
        print(f"  > Result Success ==== : {key} : '{match.group(1)}', '{match.group(4)}' ")
    else:
        print(f"  > Result Failed  ---- : {key} : {match}     <<- {arr_value}")


reg_pattern2 = r'(\w+|\W+)(\s+|\b):(\b|\s+)(\w+)$'
print("\n Result case 2-------------------------------")

for key, arr_value in enumerate(in_array):
    print("[%s] -> [%s]  " %(key , arr_value) )

    match = re.match(reg_pattern2, arr_value)
    if match:
        # print(f"  > Result Success ==== : {key} : {match.group(4)}   |  {arr_value}")
        print(f"  > Result Success ==== : {key} : '{match.group(1)}', '{match.group(4)}' ")
    else:
        print(f"  > Result Failed  ---- : {key} : {match}     <<- {arr_value}")