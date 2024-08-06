from flask import Flask, request, render_template, redirect, url_for
import tensorflow as tf
from PIL import Image
import numpy as np
import io
from datetime import datetime

app = Flask(__name__)

# Load your trained model
model = tf.keras.models.load_model('path_to_your_model.h5')

@app.route('/')
def index():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', current_date=current_date)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    # Read image and preprocess
    image = Image.open(io.BytesIO(file.read()))
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    # Run inference
    prediction = model.predict(image)
    result = {
        "prediction": prediction.tolist()
    }

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)