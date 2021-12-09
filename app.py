from flask import Flask, render_template, request
from lib.config import *

if not DUMMY:
    from lib.alphabot import Alphabot
else:
    from lib.alphabot_dummy import AlphaBot


robot = AlphaBot()
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():

    movements = {'right'  :  robot.right,
                 'left'   :  robot.left,
                 'up'     :  robot.forward,
                 'down'   :  robot.backward}

    if request.method == 'POST':
        for key, value in movements.items():
            if request.form.get(key) == key.upper():
                print(value())
        
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True, host='localhost')
