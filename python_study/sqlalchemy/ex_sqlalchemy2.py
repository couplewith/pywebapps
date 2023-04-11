from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from ex_myclasses import Student, base

engine = create_engine('sqlite:///example2.db', echo=True)
base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
sessionobj = Session()
s1 = Student(name='Juhi', age=25, marks=200)
sessionobj.add(s1)

s2 = Student(name='Juhi2', age=24, marks=202)
s3 = Student(name='Juhi3', age=23, marks=203)
s4 = Student(name='Juhi4', age=22, marks=204)
s5 = Student(name='Juhi5', age=21, marks=205)
sessionobj.add_all([s2,s3,s4,s5])
sessionobj.commit()

qry=sessionobj.query(Student)
rows=qry.all()
for row in rows:
   print (row)

# 세션 닫기
sessionobj.close()


# CREATE TABLE "Students" (
#    "StudentID" INTEGER NOT NULL,
#    name VARCHAR,
#    age INTEGER,
#    marks NUMERIC,
#    PRIMARY KEY ("StudentID")
# )
# INFO sqlalchemy.engine.base.Engine ()
# INFO sqlalchemy.engine.base.Engine COMMIT
# INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
# INFO sqlalchemy.engine.base.Engine INSERT INTO "Students" (name, age, marks) VALUES (?, ?, ?)
# INFO sqlalchemy.engine.base.Engine ('Juhi', 25, 200.0)
# INFO sqlalchemy.engine.base.Engine COMMIT
