from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
import os
from models import db, User, Task
from auth import auth_bp

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# SQL Server configuration
# For development, we'll use SQLite. In production, configure SQL Server connection string
if os.environ.get('SQL_SERVER_CONNECTION'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQL_SERVER_CONNECTION')
else:
    # Development SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app, origins=['http://localhost:3000'])  # Allow React frontend

# Register blueprints
app.register_blueprint(auth_bp)

# Mock data for backward compatibility
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

# API Routes for React frontend
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """Get all tasks for authenticated user"""
    # TODO: Add authentication middleware
    return jsonify([task for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    """Add a new task for authenticated user"""
    data = request.get_json()
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'message': 'Title and description are required'}), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "description": data['description']
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_remove_task(task_id):
    """Remove a task"""
    global tasks
    original_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    
    if len(tasks) < original_length:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

def init_db():
    """Initialize database tables and create default users"""
    with app.app_context():
        db.create_all()
        
        # Create a default admin user if none exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', email='admin@example.com')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Created default admin user: admin/admin123")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
