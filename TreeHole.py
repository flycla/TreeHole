from flask import Flask, request, \
    redirect, url_for, \
    render_template, escape, jsonify
from flask_socketio import SocketIO, emit
from flask_yarn import Yarn

from db import Records
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['CAS_SERVER'] = CAS_SERVER
app.config['CAS_AFTER_LOGIN'] = CAS_AFTER_LOGIN
socketIO = SocketIO(app)
Yarn(app)
if CAS_ENABLE:
    from flask_cas import CAS
    cas = CAS(app)

@socketIO.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketIO.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route('/query')
def query_records():
    since = escape(request.args.get('since'))
    number = escape(request.args.get('number'))
    records = Records(number, since)
    return jsonify(records.get_records_dict())


@app.route('/add', methods=['POST'])
def add_record():
    nickname = escape(request.form.get('nickname'))
    content = escape(request.form.get('content'))
    remark = escape(request.form.get('remark'))
    result = Records.add_record((nickname, content, remark))
    socketIO.emit('recordUpdate', result, broadcast=True)
    return jsonify(result)


@app.route('/')
def index():
    if CAS_ENABLE:
        if cas.username is None:
            return render_template('index.html', action='login')
        else:
            return render_template('index.html', action='logout')
    else:
        return render_template('index.html')

@app.errorhandler(405)
def page_not_found(_):
    return redirect(url_for('index'))


if __name__ == '__main__':
    socketIO.run(app, host=HOST, port=PORT, debug=DEBUG)
