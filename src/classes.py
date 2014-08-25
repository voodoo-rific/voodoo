

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    password = Column(String(50))
    age = Column(Integer)
    classes = relationship('Class', secondary='students')
    assignments = relationship('Assignment', secondary='student_assignments')


    def jsonify(self):
        return {}


class Class(Base):

    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(50))
    homework_freq = Column(String(50))
    students = relationship('User', secondary='students')


    def jsonify(self):
        return {}


class Assignment(Base):

    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey('classes.id'))
    uni_class = relationship(User, backref=backref('assignments', uselist= True))

    students = relationship('User', secondary= 'student_assignments')


import datetime

BASE_SCORES = {
    "Exam" : 5,
    "Project" : 4,
    "Paper" : 4,
    "Homework" : 3
}

class Task(Base):

    __tablename__ = 'tasks'
    id= Column(Integer, primary_key= True, autoincrement= True)
    description = Column(String(50))
    date_str = Column(String(50))
    total_minutes = Column(Integer)
    task_type = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref=backref('tasks', uselist=True))

    def _get_current_date(self):
        return datetime.datetime.today()

    def _make_datetime(self, datestr):
        return datetime.datetime.strptime(datestr, "%Y/%m/%d")

    def _get_days_remaining(self):
        current_date = self._get_current_date()
        due_date = self._make_datetime(self.date_str)
        delta = (due_date - current_date).days
        return delta

    def get_score(self):
        days_remaining = self._get_days_remaining()
        if days_remaining <= 10:
            return BASE_SCORES[self.task_type] + (10 - days_remaining)
        else:
            return BASE_SCORES[self.task_type]

    def jsonify(self):
        return {
            "id" : self.id,
            "class" : "Task",
            "type" : self.task_type,
            "description" : self.description,
            "due_date" : self.date_str,
            "score" : self.get_score(),
            "total_minutes" : self.total_minutes,
        }


#association tables (many many relationships)

# users <--> classes
class Students(Base):

    __tablename__ = 'students'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)

# users <--> assignments
class StudentAssignments(Base):

    __tablename__ = 'student_assignments'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), primary_key=True)


from sqlalchemy import create_engine
engine = create_engine('sqlite:///db/data/sqlalchemy.db')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)





