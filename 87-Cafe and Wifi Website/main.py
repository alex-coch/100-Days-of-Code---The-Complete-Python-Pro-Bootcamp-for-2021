import flask
from random import randint
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import URL, DataRequired
import sqlite3


class CafeForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    map = StringField(label='Map_URL', validators=[DataRequired(), URL()])
    image = StringField(label='Image_URL', validators=[DataRequired(), URL()])
    location = StringField(label='Location', validators=[DataRequired()])
    sockets =  SelectField(label='Has Sockets',validators=[DataRequired()], choices=['?', '?', '??', '???', '????', '?????'])
    toilet = SelectField(label='Has toilet', validators=[DataRequired()], choices=['YES', 'NO'])
    wifi = SelectField(label='Has WIFI', validators=[DataRequired()], choices=['YES', 'NO'])
    calls = SelectField(label='Can Take Calls', validators=[DataRequired()], choices=['NO', 'YES'])
    seats = StringField(label='Seats No', validators=[DataRequired()])
    price = StringField(label='Coffee Price', validators=[DataRequired()])
    sub = SubmitField(label='Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes', methods=['GET', 'POST'])
def cafes_list():
    db = sqlite3.connect('static/cafes.db')
    cur = db.cursor()
    cur.execute(
        "SELECT name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price FROM cafe")
    cafes = cur.fetchall()

    db.close()
    if flask.request.method == 'POST':
        name = request.form['dodo'].replace('Delete ','')

        db = sqlite3.connect('cafes.db')
        cur = db.cursor()
        cur.execute(f"DELETE FROM cafe WHERE name == '{name}'")
        db.commit()
        db.close()
        return redirect('/')
    return render_template('cafes.html', cafes=cafes)

@app.route('/add', methods=['GET', "POST"])
def add():
    form = CafeForm()
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            info = [randint(40, 400),form.name.data, form.map.data, form.image.data, form.location.data, form.sockets.data, form.toilet.data, form.wifi.data, form.calls.data, form.seats.data, form.price.data]
            db = sqlite3.connect('static/cafes.db')
            cur = db.cursor()
            try:
                cur.execute("INSERT INTO cafe VALUES (?,?,?,?,?,?,?,?,?,?,?)", info)
            except:
                pass
            db.commit()
            db.close()
            return redirect('/')
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)