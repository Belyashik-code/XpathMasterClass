from flask import Flask, session, redirect, url_for, request, render_template
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=5)

def get_a(task_id):
    if task_id == '1':
        return {"tag": "FLAG"}

@app.route('/')
def home():
    if 'user' in session:
        username = session['user']
        return render_template('index.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['username']
        session['user'] = user
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/get_task', methods=['GET'])
def get_task():
    task_id = request.args.get('task_id')
    a = get_a(task_id)
    print(a)
    with open(f'templates/task_{task_id}.html') as template:
        text = template.read()
    return {'elements': text, 'a': a}




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
