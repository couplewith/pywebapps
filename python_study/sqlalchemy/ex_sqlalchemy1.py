from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 연결 설정
engine = create_engine('sqlite:///example.db')  # SQLite 데이터베이스 사용
Base = declarative_base()

# 모델 정의
class User(Base):
    __tablename__ = 'users'  # 테이블 이름 설정
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

# 테이블 생성
Base.metadata.create_all(engine)

# 데이터 추가
new_user = User(name='Alice', age=25)
session = sessionmaker(bind=engine)()
session.add(new_user)
session.commit()

# 데이터 조회
user = session.query(User).filter_by(name='Alice').first()
print(f'ID: {user.id}, Name: {user.name}, Age: {user.age}')

# 세션 닫기
session.close()
