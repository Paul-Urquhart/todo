from flask import Flask, render_template

app = Flask(__name__)

todos = [
    {"id": 1, "task": "Learn Flask", "done": True},
    {"id": 2, "task": "Build a todo app", "done": False},
    {"id": 3, "task": "Deploy with Docker", "done": False},
]

@app.route("/")
def home():
    return render_template("index.html", todos=todos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)