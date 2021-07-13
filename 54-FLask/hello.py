from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/username/<name>")
def say_bye():
    return "Hello {name}"

if __name__ == "__main__":
    app.run()
