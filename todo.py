import os
from flask import Flask, render_template, request,redirect,url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("DATABASE_URL")
db = scoped_session(sessionmaker(bind=engine))
app =Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():
    todos = db.execute("SELECT * FROM ToDo").fetchall()
    
    return render_template('index.html', todos = todos)


@app.route("/add_task", methods=["POST"])
def add_task():
    todoitem = request.form.get("task")
    db.execute("insert into todo(task) values(:task)",{"task":todoitem})
    db.commit()
    return redirect(url_for('index'))


@app.route("/update_task",methods=["POST"])
def update_task():
    todoupdate = request.form.getlist("todoupdate")
    print(todoupdate)

    for checked_item in todoupdate:
        db.execute("update todo set status = 'complete' where id = (:id)",{"id":checked_item})
        db.commit()
    
    return redirect(url_for('index'))

