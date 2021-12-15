from flask import Flask, render_template
from flask_moment import Moment
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_bootstrap import Bootstrap
import os
import uuid
from form import PaletteForm
from color_extractor import color_extractor

app = Flask(__name__)
Bootstrap(app)

# Date in footer
moment = Moment(app)

# Form security
app.config['SECRET_KEY'] = os.urandom(24)

# File upload setting
app.config['UPLOADED_IMAGES_DEST'] = 'static/images/'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

sample_image_directory = 'static/images/sample-image.jpg'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PaletteForm()
    if form.validate_on_submit():
        if form.image.data:
            image_name = images.save(form.image.data, name=str(uuid.uuid4())[:8] + '.')
            image_directory = f"{app.config['UPLOADED_IMAGES_DEST']}{image_name}"
            number = form.number.data
            result = color_extractor(number, image_directory)
            return render_template('index.html', form=form, submit=True,
                                   image_directory=image_directory, result=result)
        else:
            number = form.number.data
            result = color_extractor(number, sample_image_directory)
            return render_template('index.html', form=form, submit=True,
                                   image_directory=sample_image_directory, result=result)
    return render_template('index.html', form=form, submit=False, image_directory=sample_image_directory)


if __name__ == '__main__':
    app.run(debug=True)
------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField


class PaletteForm(FlaskForm):
    image = FileField('Image to upload')
    number = IntegerField('Number of color', default=10, validators=[DataRequired(), NumberRange(min=0, max=30)])
    submit = SubmitField('Run')

------------------------------------------------------------------------
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

    # for logging purposes
    # print(percent)
    # print(clt.cluster_centers_)

    for n in range(len(percent)):
        percent['#%02x%02x%02x' % tuple(clt.cluster_centers_[n, :].astype(int))] = percent.pop(n)
        percent = dict(sorted(percent.items(), key=lambda item: item[1], reverse=True))
    return percent.items()