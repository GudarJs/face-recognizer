import cv2
import locale
from datetime import datetime
from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit

from sdk.face_recognizer import recognize, read_images, decode_image

app = Flask(__name__, static_url_path='', static_folder='statics')
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    name = db.Column(db.String(100))

    def __init__(self, date, name):
        self.date = date
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

model = cv2.face.createEigenFaceRecognizer()
model.load('sdk/training/face_training.yml')
names = read_images()

locale.setlocale(locale.LC_TIME, "es_CO.UTF-8")

@app.route('/')
def home():
    events = Events.query.all()
    return render_template('home.html', events=events)

@app.route('/events', methods=['POST'])
def save_event():
    event = request.get_json(force=True)['event']
    date = datetime.fromtimestamp(
        int(event['date'])
    )
    name = event['name']
    
    if not event:
        abort(400)
    if not date or not name:
        abort(422)

    event = Events(date, name)
    db.session.add(event)
    db.session.commit()

    return jsonify({ 'status': 201, 'id': event.id }), 201

@socketio.on('stream')
def recive_streaming(frame_encoded):
    face = recognize(model, names, decode_image(frame_encoded))
    emit('face', face)

if __name__ == '__main__':
    socketio.run(app, log_output=True, host= '0.0.0.0')
