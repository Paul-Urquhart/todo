from app import app
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Todo
from .db import Session

todo_bp = Blueprint("todo", __name__)

@todo_bp.route("/")
def home():
    session = Session()
    try:
        todos = session.query(Todo).order_by(Todo.due_date).all()
        return render_template("index.html", todos=todos)
    except Exception as e:
        app.logger.exception("Failed to get task list")
    finally:
        session.close()
    
    


@todo_bp.route("/add", methods=["POST"])
def add():
    new_task = Todo()
    new_task.task = request.form.get("task") or "New task"
    new_task.done = False
    new_task.due_date = request.form.get("due_date") or None

    session = Session()
    try:
        session.add(new_task)
        session.commit()
    except Exception as e:
        session.rollback()
        app.logger.exception("Failed to add task")
        raise
    finally:
        session.close()

    return redirect(url_for('todo.home'))

@todo_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    session = Session()
    try:
        todo = session.get(Todo, id)
        if todo:
            session.delete(todo)
            session.commit()
    except Exception as e:
        session.rollback()
        app.logger.exception("Failed to delete task")
        raise
    finally:
        session.close()
    return redirect(url_for('todo.home'))

@todo_bp.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    session = Session()
    try:
        todo = session.get(Todo, id)
        if todo:
            todo.done = not todo.done
            session.commit()
    except Exception as e:
        session.rollback()
        app.logger.exception("Unable to change task status")
        raise
    finally:
        session.close()
    return redirect(url_for('todo.home'))