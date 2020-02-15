import subprocess
import json

from flask import Flask, request, render_template

app = Flask(__name__)

DEVICE_STATUS_AWAKE = 0
DEVICE_STATUS_STANDBY = 1

TITLE_IDS = {
    "ALL4": "CUSA00072",
    "AMAZON_PRIME": "CUSA00126",
    "BBC_IPLAYER": "CUSA00122",
    "BBC_NEWS": "CUSA00273",
    "NETFLIX": "CUSA00127",
    "YOUTUBE": "CUSA01116"
}

@app.route('/', methods=['GET'])
def index():
    return render_template('help.html', titles=sorted(TITLE_IDS.keys()))

@app.route('/off', methods=['GET'])
def power_off():
    if get_status_code() == DEVICE_STATUS_AWAKE:
        subprocess.call(["ps4-waker", "standby"])
        return 'powering off ps4'
    return 'ps4 already on standby'

@app.route('/on', methods=['GET'])
def power_on():
    if get_status_code() == DEVICE_STATUS_STANDBY:
        subprocess.call(["ps4-waker"])
    if 'app' in request.args:
        app = request.args.get('app').upper()
        if app in TITLE_IDS:
            subprocess.call(["ps4-waker", "start", TITLE_IDS[app]])
            return 'starting ' + app
    elif 'app_id' in request.args:
        subprocess.call(["ps4-waker", "start", request.args.get('app_id')])
        return 'starting app'
    return 'powering on ps4'

@app.route('/status', methods=['GET'])
def status():
    proc = subprocess.Popen(["ps4-waker", "check"], stdout=subprocess.PIPE)
    stdout = proc.communicate()
    print proc.returncode
    return stdout

def get_status_code():
    proc = subprocess.Popen(["ps4-waker", "check"], stdout=subprocess.PIPE)
    proc.communicate()[0]
    return proc.returncode

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

