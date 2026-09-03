from app import app
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Todo, User
from .db import Session
from functools import wraps

todo_bp = Blueprint(
    "todo",
    __name__,
    static_folder="static",
    static_url_path="/static"
)

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if "user_id" not in session:
            app.logger.warning(f"user is not logged in; attempted to access function: {func.__name__}")
            return redirect(url_for('todo.login'))
    
        return func(*args, **kwargs)
    return wrapper

@todo_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        app.logger.info(f"login initiated for user: {username}")
        
        db_session = Session()

        try:
            app.logger.info("querying database for user login")
            user = db_session.query(User).filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, password):
                app.logger.info(f"user {username} authenticated")
                session["user_id"] = user.id
                app.logger.info(f"user logged in as: {username}")
                return redirect(url_for('todo.home'))
            else:
                app.logger.error("Invalid username or password")
                return "Invalid username or password"
        except Exception:
            app.logger.exception(f"Failed login attempt for {username}")
            return "Unable to log in", 401
        finally:
            db_session.close()
    return render_template("login.html")

@todo_bp.route("/")
@require_login
def home():
    user_id = session["user_id"]
    db_session = Session()
    try:
        todos = db_session.query(Todo).order_by(Todo.done, Todo.due_date).filter_by(user_id=user_id).all()
        return render_template("index.html", todos=todos)
    except Exception:
        app.logger.exception("Failed to get task list")
    finally:
        db_session.close()
    return render_template("index.html")
    
    


@todo_bp.route("/add", methods=["POST"])
@require_login
def add():
    new_task = Todo()
    new_task.task = request.form.get("task") or "New task"
    new_task.done = False
    new_task.due_date = request.form.get("due_date") or None
    new_task.user_id = session["user_id"]

    db_session = Session()
    try:
        db_session.add(new_task)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        app.logger.exception("Failed to add task")
        raise
    finally:
        db_session.close()

    return redirect(url_for('todo.home'))

@todo_bp.route("/delete/<int:id>", methods=["POST"])
@require_login
def delete(id):
    db_session = Session()
    try:
        todo = db_session.get(Todo, id)
        if todo:
            db_session.delete(todo)
            db_session.commit()
    except Exception as e:
        db_session.rollback()
        app.logger.exception("Failed to delete task")
        raise
    finally:
        db_session.close()
    return redirect(url_for('todo.home'))

@todo_bp.route("/complete/<int:id>", methods=["POST"])
@require_login
def complete(id):
    db_session = Session()
    try:
        todo = db_session.get(Todo, id)
        if todo:
            todo.done = not todo.done
            db_session.commit()
    except Exception as e:
        db_session.rollback()
        app.logger.exception("Unable to change task status")
        raise
    finally:
        db_session.close()
    return redirect(url_for('todo.home'))

@todo_bp.route("/create_user", methods=["POST"])
def create_user():
    new_user = User()
    new_user.username = request.form.get("username")
    pw = request.form.get("password")
    new_user.password_hash = generate_password_hash(pw)

    db_session = Session()
    try:
        db_session.add(new_user)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        app.logger.exception("Failed to create user")
    finally:
        db_session.close()

    return redirect(url_for('todo.login'))


@todo_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('todo.login'))