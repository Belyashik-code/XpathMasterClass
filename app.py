from flask import Flask, session, redirect, url_for, request, render_template, render_template_string
from datetime import timedelta
import os
import socket
import random
import string

ip_addresses_list = socket.gethostbyname_ex(socket.gethostname())[2]
ip_address=[ip for ip in ip_addresses_list if ip != "127.0.0.1"][0]


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=5)


def generate_short_hash():
    hash_list = []
    for i in range(20):
        hash_list.append(''.join(random.choices(string.ascii_letters + string.digits, k=32))[:8])
    return hash_list

def get_a(task_id, class_hash):
    if task_id == '1':
        return {"tag": "FLAG"}
    if task_id == '2':
        return {"name": "Fido"}
    if task_id == '3':
        return {"name": "Acana Dog Food"}
    if task_id == '4':
        return {"name": "Kitty"}
    if task_id == '5':
        return {"name": f"item-special-{class_hash[10]}"}
    if task_id == '6':
        return {"elements_names": [f"item-{class_hash[4]}",f"item-{class_hash[6]}",f"item-{class_hash[8]}"]}
    if task_id == '7':
        return {"table_values": ['6','8']}
    if task_id == '8':
        return {"table_values": ['Molly','Fish','6','Nicola','Grey','2']}

@app.route('/')
def home():
    if 'user' in session:
        username = session['user']
        return render_template('index.html', username=username, ip_address=ip_address)
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
    class_hash = generate_short_hash()
    a = get_a(task_id, class_hash)
    with open(f'templates/task_{task_id}.html') as template:
        text = template.read()
    return {'elements': render_template_string(text, class_hash=class_hash), 'a': a}




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
