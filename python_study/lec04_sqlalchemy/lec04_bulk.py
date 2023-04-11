from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError



# 데이터베이스 연결 설정
engine = create_engine('sqlite:///db/_lec04_bulk.db')  # SQLite 데이터베이스 사용
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
# engine = create_engine('sqlite:///db/lec04.db', strategy=ASYNCIO_STRATEGY )  # SQLite 데이터베이스 사용
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
        return '<User (%r, %r, %r)>' %(self.id, self.name, self.email)

init_db()   ## 테이블이 생성됨

user_list= [
    {'name': 'test',  'email': 'test0@email.com'},
    {'name': 'test1', 'email': 'test1@email.com'},
    {'name': 'test2', 'email': 'test2@amail.com'},
    {'name': 'test3', 'email': 'test3@dmail.com'},
    {'name': 'test4', 'email': 'test4@dmail.com'},
]

# bulk_update_mappings 대신 for 루프를 사용하여 업데이트
for data in user_list:
    try:
        db_session.query(User).filter_by(name=data['name']).update(data)
    except (IntegrityError, FlushError):
        db_session.rollback()
        continue

    # 새로운 데이터인 경우
    if db_session.query(User).filter_by(name=data['name']).count() == 0:
        db_session.add(User(**data))

# 데이터베이스 커밋
db_session.commit()

# Data 조회
#------------------------
testUsers = db_session.query(User).filter(User.name == 'test').first()
print( testUsers )

testUsers = db_session.query(User).filter(User.name == 'test1').all()
print( testUsers )

# 이름에 'test' 문자열이 포함된 사용자 중에서 첫 번째 사용자를 조회
testUser = db_session.query(User).filter(User.name.like('%test%')).first()
print(testUser)

# 이름에 'test' 문자열이 포함된 사용자 중에서 2명만 조회
testUsers = db_session.query(User).filter(User.name.like('%test%')).limit(2).all()
print(testUsers)


