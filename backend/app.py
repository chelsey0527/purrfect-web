from flask import Flask, request, jsonify
from services.database import get_db_conn
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Visualized To-Do List Tracker API!!"

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

## -- DELETE task --
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE task_id = %s;", (task_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({'message': 'Task not found.'}), 404
        return jsonify({'message': 'Task deleted successfully.'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# -- Update task --
@app.route('/tasks/<int:task_id>', methods=['POST', 'PUT'])
def update_task(task_id):
    data = request.json
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE tasks 
            SET status = %s 
            WHERE task_id = %s
            """, (data['status'], task_id))
        if cur.rowcount == 0:
            return jsonify({'message': 'Task not found.'}), 404
        conn.commit()
        return jsonify({'message': 'Task updated successfully.'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


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