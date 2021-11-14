import json
import threading
import time

from flask import Flask, render_template, request
from flask_cors import cross_origin
from stat_class import Stat

app = Flask(__name__)
stat = Stat()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('testcountpage1.html')


@app.route('/makenode', methods=['POST'])
@cross_origin()
def makenode():
    stat.update_stat(request)
    stat.save_json()
    return 'node done'


@app.route('/lst')
def look_stat():
    with open('data.json', 'r') as f:
        try:
            return json.load(f)
        except:
            return 'data is ampty'

#
# def saving():
#     while True:
#         stat.save_json()
#         time.sleep(5)


if __name__ == "__main__":
    # saving_thread = threading.Thread(target=saving)
    # saving_thread.start()
    app.run(debug=True)
