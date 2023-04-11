from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from sqlalchemy import desc



# 데이터베이스 연결 설정
engine = create_engine('sqlite:///db/_lec04_bulk.db')  # SQLite 데이터베이스 사용
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

    def __init__(self, name=None, email=None):
        self.name = name
        self.email= email

    def __repr__(self):
        return '<User (%r, %r, %r)>' %(self.id, self.name, self.email)

init_db()   ## 테이블이 생성됨

user_list= [
    {'name': 'test',  'email': 'btest00@email.com'},
    {'name': 'test11', 'email': 'btest11@email.com'},
    {'name': 'test22', 'email': 'btest22@amail.com'},
    {'name': 'test33', 'email': 'btest33@dmail.com'},
    {'name': 'test44', 'email': 'btest44@dmail.com'},
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

# 이름에 'test' 문자열이 포함된 사용자 중에서 10명까지 조회
testUsers = db_session.query(User).filter(User.name.like('%test%')).limit(10).all()
print(testUsers)


# Data 삭제 : like를 이용한 데이터 삭제
#------------------------
# like와 limit를 이용한 데이터 삭제
query = db_session.query(User).filter(User.email.like('%@email.com')).limit(2)
users = query.all()
for user in users:
    db_session.delete(user)
db_session.commit()


# 이름에 'test' 문자열이 포함된 사용자 중에서 첫 번째 사용자를 조회
testUser = db_session.query(User).filter(User.name.like('%test%')).first()
print(testUser)

# 이름에 'test' 문자열이 포함된 사용자 중에서 20명만 조회
testUsers = db_session.query(User).filter(User.name.like('%test%')).limit(20).all()
print(testUsers)

# id 열을 기준으로 내림차순으로 정렬한 결과 반환
testUsers = db_session.query(User).filter(User.name.like('test%')).order_by(desc(User.id)).all()
print('> like :', testUsers)



# id 열을 기준으로 내림차순으로 정렬한 결과 반환
testUsers = db_session.query(User).filter(User.name.in_(['test1','test2','test3'])).order_by(desc(User.id)).all()
print('> IN :', testUsers)



# IS NULL, IS NOT NULL : None

testUsers = db_session.query(User).filter(User.email.is_(None)).all()
print('> IS NULL :', testUsers)

testUsers = db_session.query(User).filter(User.email.isnot(None)).all()
print('> IS NOT NULL :', testUsers)


# and
from sqlalchemy import and_
for user in db_session.query(User).filter(and_(User.name == 'test2',User.email == 'btest20@amail.com')):
    print('> _and :', testUsers)