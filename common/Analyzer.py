# 주식종목 크롤링하여 DB로 저장하기

import pandas as pd
import pymysql
import sqlite3
from datetime import datetime
from datetime import timedelta
import re



class MarketDB:
    dbconfig_file = 'dbconfig.properties'
    DEBUG = True
    def __init__(self, *args):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        if ( args[0].lower() == "mysql" ):
            self.conn = pymysql.connect(option_files=self.dbconfig_file)
            if(self.DEBUG): print("MarketDB::", args[0], self.dbconfig_file)
        elif (args[0].lower() == "sqllite"):
            db_name = ":memory:"
            self.conn = sqlite3.connect('./database.db')
            if(self.DEBUG): print("MarketDB::", args[0], 'sqllite')
        else :
            self.conn = pymysql.connect(host='localhost', user='root',
                                        password='snake.land.', db='INVESTAR', charset='utf8')
        if(self.DEBUG): print("MarketDB::", "db.conn.status", self.conn)
        self.codes = {}
        self.init_db()
        self.get_comp_info()

    def init_db(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        if( not self.conn ) :
            if(self.DEBUG): print("MarketDB::init_db() - db not connected !! ")
            #exit()
            return False
        else:
            if (self.DEBUG): print("MarketDB::init_db() - db connected ok ")

        try:
            with self.conn.cursor() as curs:
                sql = """
                CREATE TABLE IF NOT EXISTS company_info (
                    code VARCHAR(20),
                    company VARCHAR(40),
                    last_update DATE,
                    PRIMARY KEY (code))
                """
                curs.execute(sql)
                if (self.DEBUG): print("MarketDB::init_db() execute ok ", "company_info")
                sql = """
                CREATE TABLE IF NOT EXISTS daily_price (
                    code VARCHAR(20),
                    date DATE,
                    open BIGINT(20),
                    high BIGINT(20),
                    low BIGINT(20),
                    close BIGINT(20),
                    diff BIGINT(20),
                    volume BIGINT(20),
                    PRIMARY KEY (code, date))
                """
                curs.execute(sql)
                if (self.DEBUG): print("MarketDB::init_db() execute ok ", "daily_price")
        #except sqlite3.Error as e:
        except self.conn.Error as e:
            if(self.DEBUG): print(self.__class__, "sql error ~~~", e.args[0])
        finally:
            self.conn.commit()
            if (self.DEBUG): print(self.__class__, " finally OK !! ", self.conn.__str__())
        self.codes = dict()
        return True
        
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes에 저장"""
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql, self.conn)
        for idx in range(len(krx)):
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]

    def get_daily_price(self, code, start_date=None, end_date=None):
        """KRX 종목의 일별 시세를 데이터프레임 형태로 반환
            - code       : KRX 종목코드('005930') 또는 상장기업명('삼성전자')
            - start_date : 조회 시작일('2020-01-01'), 미입력 시 1년 전 오늘
            - end_date   : 조회 종료일('2020-12-31'), 미입력 시 오늘 날짜
        """
        if start_date is None:
            one_year_ago = datetime.today() - timedelta(days=365)
            start_date = one_year_ago.strftime('%Y-%m-%d')
            print("start_date is initialized to '{}'".format(start_date))
        else:
            start_lst = re.split('\D+', start_date)
            if start_lst[0] == '':
                start_lst = start_lst[1:]
            start_year = int(start_lst[0])
            start_month = int(start_lst[1])
            start_day = int(start_lst[2])
            if start_year < 1900 or start_year > 2200:
                print(f"ValueError: start_year({start_year:d}) is wrong.")
                return
            if start_month < 1 or start_month > 12:
                print(f"ValueError: start_month({start_month:d}) is wrong.")
                return
            if start_day < 1 or start_day > 31:
                print(f"ValueError: start_day({start_day:d}) is wrong.")
                return
            start_date=f"{start_year:04d}-{start_month:02d}-{start_day:02d}"

        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            print("end_date is initialized to '{}'".format(end_date))
        else:
            end_lst = re.split('\D+', end_date)
            if end_lst[0] == '':
                end_lst = end_lst[1:] 
            end_year = int(end_lst[0])
            end_month = int(end_lst[1])
            end_day = int(end_lst[2])
            if end_year < 1800 or end_year > 2200:
                print(f"ValueError: end_year({end_year:d}) is wrong.")
                return
            if end_month < 1 or end_month > 12:
                print(f"ValueError: end_month({end_month:d}) is wrong.")
                return
            if end_day < 1 or end_day > 31:
                print(f"ValueError: end_day({end_day:d}) is wrong.")
                return
            end_date = f"{end_year:04d}-{end_month:02d}-{end_day:02d}"
         
        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())

        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print(f"ValueError: Code({code}) doesn't exist.")
        sql = f"SELECT * FROM daily_price WHERE code = '{code}'"\
            f" and date >= '{start_date}' and date <= '{end_date}'"
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df 



        
