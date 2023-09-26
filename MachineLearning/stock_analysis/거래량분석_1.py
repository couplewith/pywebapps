import csv
from datetime import datetime

# CSV 데이터에서 날짜와 거래량 추출
dates = []
volumes = []

stock_csvdata = '거래량_data_셀트리온_202309.csv'
with open(stock_csvdata, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        date = datetime.strptime(row['일자'], '%Y/%m/%d')
        volume = int(row['거래량'])
        dates.append(date)
        volumes.append(volume)

# 거래량이 증가하는 날짜와 거래량이 줄어든 날짜 식별
increasing_volume_dates = []
decreasing_volume_dates = []

for i in range(1, len(volumes)):
    if volumes[i] > volumes[i - 1]:
        increasing_volume_dates.append(dates[i])
    elif volumes[i] < volumes[i - 1]:
        decreasing_volume_dates.append(dates[i])

# 거래량이 증가하는 날짜 간의 평균 일수 계산
average_days_to_increase = sum((d2 - d1).days for d1, d2 in zip(decreasing_volume_dates, increasing_volume_dates)) / len(increasing_volume_dates)

print(f"거래량이 증가하는데 걸리는 평균 일수: {average_days_to_increase} 일")
