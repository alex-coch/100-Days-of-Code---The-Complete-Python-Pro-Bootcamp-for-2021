import binascii
from PIL import Image
import scipy.cluster
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


def color_extractor(number, picture):

    image = cv.imread(picture)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    clt = KMeans(n_clusters=number)
    clt.fit(image.reshape(-1, 3))

    n_pixels = len(clt.labels_)
    counter = Counter(clt.labels_)  # count how many pixels per cluster
    percent = {}
    for i in counter:
        percent[i] = np.round(counter[i] / n_pixels, 2)
    for n in range(len(percent)):
        percent['#%02x%02x%02x' % tuple(clt.cluster_centers_[n, :].astype(int))] = percent.pop(n)
        percent = dict(sorted(percent.items(), key=lambda item: item[1], reverse=True))
    return percent.items()


app = Flask(__name__)
Bootstrap(app)

# Create a directory in a known location to save files to.
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

NUM_CLUSTERS = 10


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # save the single "file" file
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        return redirect(url_for('image', upload=secure_filename(file.filename)))

    return render_template('index.html')


@app.route('/image/<upload>')
def image(upload):

    # numpy code
    print('reading image')
    uploaded_image = Image.open(f'static/uploads/{upload}')
    ar = np.asarray(uploaded_image)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    print('cluster centres:\n', codes)

    color_hexes = []
    for code in codes:
        x = binascii.hexlify(bytearray(int(c) for c in code)).decode('ascii')
        x = f"#{x}"
        color_hexes.append(x)

    print(color_hexes)
    print(color_extractor(8, 'd:\\w.jpg'))

    return render_template("display_colors.html", filename=f"uploads/{upload}",
                           colors=color_hexes)


if __name__ == "__main__":
    app.run(debug=True)


