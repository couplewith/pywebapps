#ex_myclasses.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
base=declarative_base()
class Student(base):
   __tablename__='Students'
   StudentID=Column(Integer, primary_key=True)
   name=Column(String)
   age=Column(Integer)
   marks=Column(Numeric)