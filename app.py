from flask import Flask, render_template, request
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['POST'])
@cross_origin()
def about():
    f = request.get_json()
    print(f)
    return "Add the json request."


if __name__ == "__main__":
    app.run(debug=True)
