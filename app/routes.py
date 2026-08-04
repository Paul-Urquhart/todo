from app import app
from flask import render_template, request, redirect
from .models import Todo
from .db import Session


@app.route("/")
def home():
    session = Session()
    try:
        todos = session.query(Todo).order_by(Todo.id).all()
        return render_template("index.html", todos=todos)
    finally:
        session.close()
    
    


@app.route("/add", methods=["POST"])
def add():
    new_task = Todo()
    new_task.task = request.form["task"]
    new_task.done = False

    session = Session()
    try:
        session.add(new_task)
        session.commit()
    finally:
        session.close()

    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    session = Session()
    todo = session.get(Todo, id)
    if todo:
        session.delete(todo)
        session.commit()
    session.close()
    return redirect("/")

@app.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    session = Session()
    todo = session.get(Todo, id)
    if todo:
        todo.done = not todo.done
        session.commit()
    session.close()
    return redirect("/")