from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for
)

from threading import Thread
import logging

import os
import subprocess

import time
import tempfile

app = Flask(__name__)

displays = {}

logging.basicConfig(filename='xvfb.log', level=logging.DEBUG)

def run_command(display_id, command):
    log_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    log_filename = log_file.name

    xvfb_command = f'Xvfb :{display_id} -screen 0 1280x720x24'

    xvfb_process = subprocess.Popen(xvfb_command.split(), stdout=log_file, stderr=log_file)

    time.sleep(1)

    os.environ["DISPLAY"] = f":{display_id}"

    subprocess.Popen(command, shell=True)

    xvfb_process.wait()

    log_file.seek(0)
    log_content = log_file.read()
    log_file.close()

    print(log_content)

    os.remove(log_filename)


@app.route('/')
def index():
    return render_template('index.html', displays=displays)


@app.route('/create_display', methods=['POST'])
def create_display():
    display_id = len(displays) + 10
    command = request.form.get('command')

    if command:
        thread = Thread(target=lambda: run_command(display_id, command))
        thread.start()
        displays[display_id] = {'command': command}

    return redirect(url_for('index'))


@app.route('/stop_display/<int:display_id>', methods=['POST'])
def stop_display(display_id):
    print('TODO')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100)
