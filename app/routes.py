from app import app
from flask import render_template, request, redirect

todos = [
    {"id": 1, "task": "Learn Flask", "done": True},
    {"id": 2, "task": "Build a todo app", "done": False},
    {"id": 3, "task": "Deploy with Docker", "done": False},
]

@app.route("/")
def home():
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    todo = request.form["task"]

    new_task = {
        "id": len(todos) + 1,
        "task": todo,
        "done": False
    }

    todos.append(new_task)

    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    for i in range(len(todos)):
        if todos[i]['id'] == id:
            todos.pop(i)
            break
    return redirect("/")

@app.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    for i in range(len(todos)):
        if todos[i]['id'] == id:
            if todos[i]['done'] == False:
                todos[i]['done'] = True
            else:
                todos[i]['done'] = False
    return redirect("/")