from flask import Flask, render_template, Response
import os
import cv2

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_PATH)

def frame_gen(env_func, *args, **kwargs):
    get_frame = env_func(*args, **kwargs)
    while True:
        frame = next(get_frame, None)
        if frame is None:
            break
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #ADDED TO CONVERT FROM BGR TO RGB
        _, frame = cv2.imencode('.png', imageRGB)
        frame = frame.tobytes()
        yield (b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

def render_browser(env_func):
    def wrapper(*args, **kwargs):
        @app.route('/render_feed')
        def render_feed():
            return Response(frame_gen(env_func, *args, **kwargs), mimetype='multipart/x-mixed-replace; boundary=frame')

        print("Starting rendering, check `server_ip:5000`.")
        app.run(host='0.0.0.0', port='5000', debug=False)

    return wrapper