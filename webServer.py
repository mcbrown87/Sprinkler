import os
from flask import Flask
from flask import render_template
from flask import jsonify
from mockValve import Valve
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)

valve = Valve()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/isOpen', methods=['GET'])
def getIsOpen():
	return jsonify(isOpen=valve.IsOpen())

@app.route('/closeValve', methods=['POST'])
def closeValve():
    valve.Close()
    return ""

@app.route('/openValve', methods=['POST'])
def openValve():
    valve.Open()
    return ""

@app.route('/openDuration', methods=['GET'])
def getOpenDuration():
    return jsonify(valveOpenDuration=str(valve.ValveOpenDuration()))

@app.route('/config', methods=['GET'])
def getConfig():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/scheduler/config.json', 'r') as config_file:
        return config_file.read()


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)  # serving on port 5000
IOLoop.instance().start()
