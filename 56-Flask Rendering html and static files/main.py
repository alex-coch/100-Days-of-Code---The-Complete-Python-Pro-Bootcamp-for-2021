from flask import render_template
from flask import Flask

# app = Flask(__name__)
# app=Flask(__name__,template_folder='template')
app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
# @app.route('/<name>')
# def hello(name=None):
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    #Run the app in debug mode to auto-reload
    app.run(debug=True)
