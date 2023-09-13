# On importe tout le nécessaire pour faire tourner notre modèle
from stable_baselines3 import PPO
from functions.env import env
from functions.frame_gen import frame_gen
from flask import Flask, Response, request
from flask_cors import CORS
import os
from routes.api import api_bp
from routes.models import models_bp
from routes.settings import settings_bp


from warnings import filterwarnings
filterwarnings('ignore')

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(models_bp, url_prefix='/api')
app.register_blueprint(settings_bp, url_prefix='/api')

def render_browser(env_func):
    def wrapper(*args, **kwargs):
        @app.route('/render_feed')
        def render_feed():
            
            query = request.args.to_dict()
            
            print(query['model'])
            global selected_model
            selected_model = query['model']
            
            return Response(frame_gen(env_func, *args, **kwargs), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        app.run(host='0.0.0.0', port='5000', debug=False, use_reloader=True)

    return wrapper

selected_model = None

# On commence par charger le dernier modèle 
if selected_model is None:
    selected_model = "best_model_10300000"

@render_browser
def test_policy():
    #Load the model
    model = PPO.load(f"D:/MarioRL/train/{selected_model}")
    
    # Start the game
    print("Starting the game with model : ", selected_model)
    
    state = env.reset()
    
    done = False
    while done == False:
        action, _ = model.predict(state)
        state, reward, done, info = env.step(action)
        yield env.render(mode='rgb_array'), reward, done, info, action
        
test_policy()