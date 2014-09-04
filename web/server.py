
import logging
import json

from lib._flask.flask import (
    Flask, 
    render_template, 
    url_for, 
    jsonify, 
    Response, 
    request,
    make_response,
    send_file,
)


from sqlalchemy import create_engine

from src.scheduler import Scheduler

from src.session_manager import SessionManager

from src.classes import (
    User, Task, Want, Break, Class, Assignment
)


#global db shit
engine = create_engine('sqlite:///db/data/sqlalchemy.db')
session = SessionManager(engine)

app = Flask(__name__)


### templates
@app.route('/')
def index():
    
    #cached : 'prod'
    return send_file('templates/index.html')
    
    
    #uncached : dev
    #return make_response(open('templates/index.html').read())




@app.route('/get_user_classes/<id>')
def get_user_classes(id=1):
    
    user_obj = session.get_one(User, id)
    
    classes = []
    for _class in user_obj.classes:
        classes.append(_class.jsonify())

    return json.dumps(classes)




@app.route('/add_class_to_db', methods= ['GET'])
def add_class_to_db():
 
    user_id = request.args.get('user_id')
    class_name = request.args.get('class_name')
    homework_freq = request.args.get('homework_freq')

    user_obj = session.get_one(User, user_id)
    class_obj = Class(class_name= class_name, homework_freq= homework_freq)

    class_obj.students.append(user_obj)

    session.add(class_obj, commit= True)

    return jsonify([])








################# old shit

@app.route('/get_user_with_id/<id>')
def get_user_with_id(id=1):
    
    id = int(id)
    user = session.get_one(User, id)
    print(user.jsonify())
    return json.dumps(user.jsonify())




@app.route('/get_schedule/<hours>')
def get_schedule(hours=4):
      
    hours = int(hours)


    tasks = session.get_all(Task)
    wants = session.get_all(Want)
    breaks = session.get_all(Break)

    scheduler = Scheduler(hours, tasks, wants, breaks) 

    return json.dumps(scheduler.schedule)


@app.route('/all_users')
def get_all_users():

    results = session.get_all(User)
    users = []
    for obj in results:

        #come back and jsonify
        users.append({"id" : obj.id, "name" : obj.name, "password" : obj.password})


    return json.dumps(users)


# might want to forgo constructing the object here
# if we don't care about displaying the score
@app.route('/all_tasks')
def get_all_tasks():

    results = session.get_all(Task)

    tasks = []

    for obj in results:
        tasks.append(obj.jsonify())


    return json.dumps(tasks)


@app.route('/all_wants')
def get_all_wants():

    results = session.get_all(Want)

    wants = []
    for obj in results:
        wants.append(obj.jsonify())

    return json.dumps(wants)


@app.route('/all_breaks')
def get_all_breaks():

    results = session.get_all(Break)

    breaks = []
    for obj in results:
        breaks.append(obj.jsonify())

    return json.dumps(breaks)


@app.route('/add_minutes', methods = ['GET'])
def add_minutes():
        
    id = request.args.get('id')
    minutes = request.args.get('time_slot')
    item_class = request.args.get('item_class')
     

    obj = session.get_one(Task, id)
    
    # should only be one
    
    total_minutes = obj.total_minutes
    
    total_minutes = int(total_minutes) + int(minutes)


    session.update_one(Task, {'total_minutes':total_minutes}, id, commit=True)


    return json.dumps({"minutes": total_minutes})



@app.route('/reset_minutes', methods = ['GET'])
def reset_minutes():

    id = request.args.get('id')
    item_class = request.args.get('item_class')
    
    session.update_one(Task, {'total_minutes':0}, id, commit=True)
    
    return "ok" 
    
     
         
if __name__ == '__main__':
    app.run()

