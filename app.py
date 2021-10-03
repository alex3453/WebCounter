import json

from flask import Flask, render_template, request
from flask_cors import cross_origin
from stat_class import Stat

app = Flask(__name__)
stat = Stat()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/makenode', methods=['POST'])
@cross_origin()
def about():
    host = request.headers['host']
    stat.make_note(host)
    return 'Note done'

@app.route('/lst')
def lookstat():
    with open('data.json', 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    app.run(debug=True)
