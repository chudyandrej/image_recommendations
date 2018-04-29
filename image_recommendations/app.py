from flask import Flask, render_template, request, send_file
import json
from image_recommender import Recommender


app = Flask(__name__)
recommender_model = Recommender()



@app.route('/')
def hello_world():
    return render_template("index.html", images=[])


@app.route('/text', methods=['POST'])
def text_input():
    text = request.get_data().decode('UTF-8')
    images = recommender_model.recommend_image(text)
    return json.dumps(images), 200, {'ContentType': 'application/json'}


@app.route('/image/<string:name>', methods=['GET'])
def get_image(name=None):
    return send_file("./image_dataset/"+name, mimetype='image/gif')


if __name__ == '__main__':
    app.run()
