from flask import Flask, render_template, request
from lib.config import *

if not DUMMY:
    from lib.alphabot import AlphaBot
else:
    from lib.alphabot_dummy import AlphaBot


robot = AlphaBot()
app = Flask(__name__)
status = {'right'  :  0,
              'left'   :  0,
              'up'     :  0,
              'down'   :  0}

@app.route("/", methods=['GET', 'POST'])
def index():

    movements = {'right'  :  robot.right,
                 'left'   :  robot.left,
                 'up'     :  robot.forward,
                 'down'   :  robot.backward}
    

    if request.method == 'POST':
        for key, value in movements.items():
            if request.form.get(key) == key.upper():
                if status[key] == 1:
                    robot.stop()
                else:
                    print(value())
                status[key] = not status[key]
        
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.134')
