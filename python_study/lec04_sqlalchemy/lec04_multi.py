from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.sqlite import insert


# app.teardown_appcontext
# def shutdown_session(exception=None):
#    db_session.remove()

# 데이터베이스 연결 설정
engine = create_engine('sqlite:///db/_lec04_multi.db')  # SQLite 데이터베이스 사용
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
Base = declarative_base()

#데이터베이스 초기화 함수

def init_db():
    Base.metadata.create_all(bind=engine)

class User(Base):
    __tablename__ = "users"

    id   = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    email= Column(String(120), unique=True)

    def __init__(self,name=None, email=None):
        self.name = name
        self.email= email

    def __repr__(self):
        return '<User %r>' %(self.name)

init_db()   ## 테이블이 생성됨


# SQLAlchemy에서는 데이터베이스의 제약 조건을 위반하는 쿼리가 발생하면 IntegrityError 예외가 발생합니다.
# 따라서 중복 키를 삽입하려고 할 때 이 예외를 처리하는 방법은 다음과 같습니다.
#


u0 = User('test', 'test@dmail.com')
u1 = User('test1', 'test1@dmail.com')
u2 = User('test2', 'test2@dmail.com')
u3 = User('test3', 'test3@dmail.com')
user_list= [u0, u1, u2, u3]

# 위의 소스 코드에서는 SQLAlchemy의 일괄 처리 메소드 bulk_update_mappings()를 사용하여 여러 개의 데이터를 일괄적으로 업데이트하려고 시도합니다.
# 그러나 SQLite는 SQLAlchemy의 Bulk Update 동작을 지원하지 않기 때문에 해당 코드는 작동하지 않습니다.

try:
    #db_session.add(u)  # 실제 데이터 베이스 추가된 Pending 상태
    db_session.add_all(user_list)

    # 중복된 데이터를 삽입하는 코드 : # Pending된 내용을 데이터 베이스에 저장한다.
    db_session.commit()

except IntegrityError as e:

    ## 중복된 데이터를 확인하고 처리하는 코드
    db_session.rollback()  # 롤백 처리
    print(f"Error: {e}")

    # 중복된 데이터를 덮어쓰는 코드
    # db_session.query(User).filter_by(unique_field=value).update({"user": new_value})

    # 중복된 데이터를 덮어쓰는 코드
    for obj in user_list:
        stmt = insert(User).values(
            **obj.__dict__
        ).on_conflict_do_update(
            index_elements=['unique_field'],
            set_=obj.__dict__
        )
        db_session.execute(stmt)

    db_session.commit()


# 데이터 베이스 모델 조회 방법
# query 속성에 all, filter, filter_by method를 이용하여 데이터 베이스 질의
#  all : 질의 조건없이 모든 레코드를 가져옴
# filter: 질의 조건에 해당하는 모델을 레코드를 인스턴스로 반환
#          질의 조건이 여러개이면 ","를 이용하여 여러 조건을 적용
#        filter(조건1('<클래스.질의컬럼> <비교연산자> <비교값>', 조건2 ,...)
#        비교 연산자를 사용 " == != <= => 등
# filter_by: 질의 조건에 해당하는 모델을 레코드를 얻을수 있으나 인자를 넘기는 방식이 차이가있음
#         필터의 비교 연산자 사용이 불가,  == 대신 = 를 사용하며
#         !=  <=  >= 등은 사용 불가
#  질의 결과를 가져오는 메소드
#   first(), all, one, limit, offset 등의 메소드를 이용 가능
#   first :  질의 조건에 해당하는 최상위 레코드가 반환  (레코드가 없으면 None를 반환)
#    질의 조건에 레코드가 없으면 예외 상황을 발생 시킴
#   one:  질의 조건에 해당하는 레코드가 없으면 NoResultFound가 발생
#         질의에 해당하는 레코드가 여러개인 경우 MultipleResultFound 발생
#   limit : 레크도가 많을때 몇개를 가져올 것인지 지정하는 메소드
#   offset : 레코드가 많을때 어디서 부터 가져올 것인지 지정하는 메소드
#
# 1. User.query.filter(User.name == 'test').first()
# 2. User.query.filter(User.name == 'test').all()    #
# 3.  User.query.filter(User.name == 'test').first()

testUser = db_session.query(User).filter(User.name == 'test').first()
print( testUser )

testUsers = db_session.query(User).filter(User.name == 'test').all()
print( testUsers )


testUsers = db_session.query(User).filter_by(name = 'test').all()
print( testUsers )