from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError



# 데이터베이스 연결 설정
engine = create_engine('sqlite:///_lec04_err.db')  # SQLite 데이터베이스 사용
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

user_list= [
    {'name': 'test', 'email': 'test@dmail.com'},
    {'name': 'test1', 'email': 'test1@dmail.com'},
    {'name': 'test2', 'email': 'test2@dmail.com'},
    {'name': 'test3', 'email': 'test3@dmail.com'}
]

# bulk_update_mappings 메소드를 사용하여 일괄 업데이트
try:
    db_session.bulk_update_mappings(User, user_list)
    db_session.commit()

except (IntegrityError, FlushError):
    db_session.rollback()

    for data in user_list:
        # 중복된 데이터인 경우
        if db_session.query(User).filter_by(name=data['name']).first():
            db_session.query(User).filter_by(name=data['name']).update(data)

        # 새로운 데이터인 경우
        else:
            db_session.add(User(**data))

    db_session.commit()



# Data 조회
#------------------------
testUser = db_session.query(User).filter(User.name == 'test').first()
print( testUser )

testUsers = db_session.query(User).filter(User.name == 'test').all()
print( testUsers )


testUsers = db_session.query(User).filter_by(name = 'test').all()
print( testUsers )