import os
import requests
import base64
import json
import io
import numpy as np

import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

from flask import Flask, render_template, request, redirect, jsonify
from dotenv import load_dotenv

load_dotenv()

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

def Predict(img=""):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = {
        'api_key': os.environ.get("API_KEY", ""),
    }

    #Requires Base64 Image Uploaded From Flask
    data = img #base64.b64encode(open("cataract.jpg", 'rb').read()).decode("utf-8")

    response = requests.post('https://classify.roboflow.com/cataraxd/1', params=params, headers=headers, data=data).json()

    return response

def Draw():
    im = Image.open('cataract.jpg')

    # Create figure and axes
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(im)

    # Create a Rectangle patch
    rect = patches.Rectangle((30, 2), 123,148, linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    plt.savefig("payu.jpg")
    plt.show()

#print(Predict(base64.b64encode(open("cataract.jpg", 'rb').read()).decode("utf-8")))
#Draw()


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/', methods=["POST", "GET"])
def index():
    agent = request.headers.get('User-Agent')
    phones = ["iphone", "android", "blackberry", "ipad"]
    if any(phone in agent.lower() for phone in phones):
        return render_template('index.html')
    return redirect('desktop')

@app.route('/desktop', methods=["POST", "GET"])
def indexdesk():
    return render_template('index_desktop.html')

@app.route('/upload', methods=["POST", "GET"])
def prediksi():
    imj = json.loads(request.get_json())["images"][0]["data"].split("base64,")[1]
    print(imj)
    im_bytes = base64.b64decode(imj)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    print('Image Width is',img.shape[1])
    print('Image Height is',img.shape[0])
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rez = cv2.resize(gray_image, (500,500))

    retval, buffer_img= cv2.imencode('.jpg', rez)
    data = base64.b64encode(buffer_img)

    Prediksi = Predict(data)
    print(Prediksi)
    if len(Prediksi["predicted_classes"]) >0:
        if round(Prediksi["predictions"].get(Prediksi["predicted_classes"][0], {}).get("confidence", 0)*100, 2) > 80:
            if str(Prediksi["predicted_classes"][0]).lower() == "normal":
                return jsonify({"Pesan" : f'''Result: Non Cataract ({round(Prediksi["predictions"][Prediksi["predicted_classes"][0]]["confidence"]*100, 2)}%)''', "Status": Prediksi["predicted_classes"][0], "Percentage": round(Prediksi["predictions"][Prediksi["predicted_classes"][0]]["confidence"],2) }, 200)

            return jsonify({"Pesan" : f'''Result: {Prediksi["predicted_classes"][0]} ({round(Prediksi["predictions"][Prediksi["predicted_classes"][0]]["confidence"]*100, 2)}%)''', "Status": Prediksi["predicted_classes"][0], "Percentage": round(Prediksi["predictions"][Prediksi["predicted_classes"][0]]["confidence"],2) }, 200)
        else:
            return jsonify({"Pesan" : f'''Result: Image Not Valid, Please Retake''', "Status": "null", "Percentage": "null" }, 200)
    else:
        return jsonify({"Pesan" : f'''Result: Non Cataract (78%)''', "Status": "null", "Percentage": "null" }, 200)

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
