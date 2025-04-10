from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Mock data
tasks = [
    {"id": 1, "title": "Task 1", "description": "Description for task 1"},
    {"id": 2, "title": "Task 2", "description": "Description for task 2"},
    {"id": 3, "title": "Task 3", "description": "Description for task 3"}
]

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    if title and description:
        new_task = {
            "id": len(tasks) + 1,
            "title": title,
            "description": description
        }
        tasks.append(new_task)
    return redirect('/')

@app.route('/remove/<int:task_id>')
def remove_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect('/')
