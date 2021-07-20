from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__, template_folder='template0')


@app.route('/')
def home():
    # return "Hello World!"
    random_data = random.randint(1, 10)
    current_year = datetime.datetime.now().year
    return render_template("index.html", num=random_data, year=current_year)

@app.route('/guess/<username>')
def guess(username):
    response = requests.get('https://api.genderize.io/?name='+username)
    response_data = response.json()
    response = requests.get('https://api.agify.io?name='+username)
    response_data2 = response.json()
    return render_template("guess.html", person_name=username, gender=response_data['gender'], age=response_data2['age'])

if __name__ == "__main__":
    app.run(debug=True)


