from flask import Flask, request, jsonify
from services.database import get_db_conn
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Visualized To-Do List Tracker API!"

# -- ADD task --
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (name, description, category, due_date, status) VALUES (%s, %s, %s, %s, %s) RETURNING task_id;",
                (data['name'], data['description'], data['category'], data['due_date'], data['status']))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(' ADD task ', task_id)
    return jsonify({'task_id': task_id}), 201

# -- Retrieve task --
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM tasks;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    print('Retrieve task: ', tasks)
    return jsonify(tasks)