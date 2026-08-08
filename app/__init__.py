from flask import Flask

app = Flask(__name__)

from .routes import todo_bp
app.register_blueprint(todo_bp, url_prefix="/todo")

from app import routes