from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]

from .routes import todo_bp
app.register_blueprint(todo_bp, url_prefix="/todo")

from app import routes