from flask import Flask, jsonify, Response
from flask_cors import CORS
from Backend.realtime_prediction import generate_frames, most_common_per_interval

app = Flask(__name__)
CORS(app)

@app.route('/get_word')
def get_latest_word():
    if most_common_per_interval:
        return jsonify({'word': most_common_per_interval[-1]})
    return jsonify({'word': None})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
