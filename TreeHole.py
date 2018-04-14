from flask import Flask, request, \
    redirect, url_for, \
    render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_yarn import Yarn
from flask_cas import CAS

from db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['CAS_SERVER'] = CAS_SERVER
app.config['CAS_AFTER_LOGIN'] = CAS_AFTER_LOGIN
socketIO = SocketIO(app)
Yarn(app)
cas = CAS(app)

@socketIO.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketIO.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route('/query')
def query_records():
    since = request.args.get('since')
    number = request.args.get('number')
    records = Records(number, since)
    return jsonify(records.get_records_dict())


@app.route('/add', methods=['POST'])
def add_record():
    nickname = request.form.get('nickname')
    content = request.form.get('content')
    remark = request.form.get('remark')
    result = Records.add_record((nickname, content, remark))
    socketIO.emit('recordUpdate', result, broadcast=True)
    return jsonify(result)


@app.route('/')
def index():
    if cas.username is None:
        return render_template('index.html', action='login')
    else:
        return render_template('index.html', action='logout')


@app.errorhandler(405)
def page_not_found(_):
    return redirect(url_for('index'))


if __name__ == '__main__':
    socketIO.run(app, host=HOST, port=PORT, debug=DEBUG)
