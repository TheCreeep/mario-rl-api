import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def frame_gen(env_func, *args, **kwargs):
    get_frame = env_func(*args, **kwargs)
    while True:
        details = next(get_frame, None)
        frame = details[0]
        reward = details[1]
        done = details[2]
        info = details[3][0]
        
        if frame is None:
            break
        
        img = Image.new("RGB", (256, 240), (250, 205, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('C:\\Users\\leomo\\Desktop\\mario-rl-api\\assets\\font\\super-mario-maker-extended.ttf', 20)
        draw.text((0, 20),"Reward : ",(0,0,0),font=font)
        draw.text((100, 20),f"{reward[0]}",(0,0,0),font=font)
        draw.text((0, 60),"Progress :",(0,0,0),font=font)
        draw.text((120, 60),f"{info['x_pos']}",(0,0,0),font=font)
        draw.text((0, 100),"Stage :",(0,0,0),font=font)
        draw.text((80, 100),f"{info['world']}-{info['stage']}",(0,0,0),font=font)
        draw.text((0, 140),"Lifes : ",(0,0,0),font=font)
        draw.text((80, 140),f"{info['life']}",(0,0,0),font=font)
        draw.text((0,180),"Done ?",(0,0,0),font=font)
        draw.text((80, 180),f"{done[0] }",(0,0,0),font=font)
        details = img
        
        frame = cv2.hconcat([ np.array(img), frame])
        
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #ADDED TO CONVERT FROM BGR TO RGB
        _, frame = cv2.imencode('.png', imageRGB)
        frame = frame.tobytes()
        
        yield (b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
        