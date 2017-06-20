from flask import Flask
from flask import render_template
from flask import jsonify
from valve import Valve

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

@app.route('/openValve', methods=['POST'])
def openValve():
    valve.Open()

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)  # serving on port 5000
IOLoop.instance().start()
