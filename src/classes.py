
import math
import datetime
from lib import statistics

EXAM_INITIAL_SCORE = 5 
PROJECT_INITIAL_SCORE = 4
PAPER_INITIAL_SCORE = 4
HW_INITIAL_SCORE = 3


class Task(object):

    # t stands for 'task'
    def __init__(self, t_name=None, due_date=None):

        self.start_date = self._set_start_date()

        self.name = t_name
        self.due_date = due_date

        # decided by subclass
        self.base_score = None


    # TODO : expand
    def _set_start_date(self):
        return datetime.datetime.today()

    def _get_days_remaining(self):
        delta = self.due_date.day - self.start_date.day
        return delta

    def add_days_to_due_date(self, num_days):
        self.due_date = self.due_date + datetime.timedelta(days= num_days)
        return


class Exam(Task):

    def __init__(self, t_name=None, due_date=None):
        Task.__init__(self, t_name, due_date)
        self.base_score = EXAM_INITIAL_SCORE

    def get_score(self):

        days_remaining = self._get_days_remaining()
        if days_remaining <= 10:
            return self.base_score + (10 - days_remaining)
        else:
            return self.base_score
    

class Project(Task):

    def __init__(self, t_name=None, due_date=None):
        Task.__init__(self, t_name, due_date)
        self.base_score = PROJECT_INITIAL_SCORE

    def get_score(self):

        days_remaining = self._get_days_remaining()
        if days_remaining <= 10:
            return self.base_score + (10 - days_remaining)
        else:
            return self.base_score


class Paper(Task):

    def __init__(self, t_name=None, due_date=None):
        Task.__init__(self, t_name, due_date)
        self.base_score = PAPER_INITIAL_SCORE

    def get_score(self):

        days_remaining = self._get_days_remaining()
        if days_remaining <= 10:
            return self.base_score + (10 - days_remaining)
        else:
            return self.base_score


class Homework(Task):

    def __init__(self, t_name=None, due_date=None):
        Task.__init__(self, t_name, due_date)
        self.base_score = HW_INITIAL_SCORE

    def get_score(self):

        days_remaining = self._get_days_remaining()
        if days_remaining <= 5:
            return self.base_score + (5 - days_remaining)
        else:
            return self.base_score



## wrapper for DB
# will have actual DB connection code here
class MockDB(object):

    def __init__(self):
        self.contents = []

    def save(self, task):
        self.contents.append(task)




    