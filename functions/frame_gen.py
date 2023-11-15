import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT, SIMPLE_MOVEMENT

def frame_gen(env_func, *args, **kwargs):
    get_frame = env_func(*args, **kwargs)
    while True:
        details = next(get_frame, None)
        
        if details is None:
            break
        
        frame = details[0]
        reward = details[1]
        done = details[2]
        info = details[3][0]
        
        model_exists = details[5]
        
        if(model_exists):
            action = details[4]
        else:
            action = details[4][0]
        
        if(info["life"] == 255):
            info["life"] = -1
            reward[0] = 0
            image_to_load = "assets\\images\\NOOP.png"
        
        img = Image.new("RGB", (256, 240), (250, 205, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('C:\\Users\\leomo\\Desktop\\mario-rl-api\\assets\\font\\super-mario-maker-extended.ttf', 20)
        
        draw.text((0, 30),f"Reward : {reward[0]}",(0,0,0),font=font)
        draw.text((0, 70),f"Progress : {info['x_pos']}",(0,0,0),font=font)
        draw.text((0, 110),f"Stage : {info['world']}-{info['stage']}",(0,0,0),font=font)
        draw.text((0, 150),f"Lives Remaining: {info['life'] +1 }",(0,0,0),font=font)
        draw.text((0,190),f"Demo done ? {done[0] }",(0,0,0),font=font)
        details = img
        
        image_to_load = ""
        
        if(action == 1):
            image_to_load = "assets\\images\\Right.png"
        elif(action == 2):
            image_to_load = "assets\\images\\Right A.png"
        elif(action == 3):
            image_to_load = "assets\\images\\Right B.png"
        elif(action == 4):
            image_to_load = "assets\\images\\Right AB.png"
        elif(action == 5):
            image_to_load = "assets\\images\\A.png"
        else:
            image_to_load = "assets\\images\\NOOP.png"
        
        controller_image = np.array(Image.open(image_to_load))
        
        frame = cv2.hconcat([ np.array(img), frame, controller_image])
        
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #ADDED TO CONVERT FROM BGR TO RGB
        _, frame = cv2.imencode('.png', imageRGB)
        frame = frame.tobytes()
        
        
        
        yield (b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')