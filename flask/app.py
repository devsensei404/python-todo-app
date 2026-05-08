from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
FILENAME = 'tasks.json'

def load_tasks(username):
    try:
        with open(FILENAME, 'r') as f:
            data = json.load(f)
    except:
        data = {}
    tasks = data.get(username, [])
    task_id = max((t['id'] for t in tasks), default=0) + 1
    return tasks, task_id

def save_tasks(username, tasks):
    try:
        with open(FILENAME, 'r') as f:
            data = json.load(f)
    except:
        data = {}
    data[username] = tasks
    with open(FILENAME, 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/tasks')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    filter_type = request.args.get('filter', 'all')
    tasks, _ = load_tasks(session['username'])
    if filter_type == 'pending':
        tasks = [t for t in tasks if not t['done']]
    elif filter_type == 'completed':
        tasks = [t for t in tasks if t['done']]
    return render_template('index.html', tasks=tasks, filter_type=filter_type, username=session['username'])

@app.route('/add', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form.get('title')
    if title:
        tasks, task_id = load_tasks(session['username'])
        tasks.append({'id': task_id, 'title': title, 'done': False})
        save_tasks(session['username'], tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    tasks, _ = load_tasks(session['username'])
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(session['username'], tasks)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_done(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    tasks, _ = load_tasks(session['username'])
    for t in tasks:
        if t['id'] == task_id:
            t['done'] = not t['done']
    save_tasks(session['username'], tasks)
    return redirect('/tasks')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
