import time
from flask import Flask, render_template, request
from lib.config import *
from lib.query import Db_Connection

if not DUMMY:
    from lib.alphabot import Alphabot
else:
    from lib.alphabot_dummy import AlphaBot


robot = AlphaBot()
app = Flask(__name__)


def executeSequence(cmd):

    commands = {'right'        :  robot.right,
                 'left'         :  robot.left,
                 'forward'      :  robot.forward,
                 'backward'     :  robot.backward,
                 'stop'         :  robot.stop}

    #creo db
    db = Db_Connection('./lib/movimenti.db')

    #invio richiesta
    try:
        seq = db.findCommand(cmd)

        for m in seq:
            m = m.split('_')
            print(commands[m[0]]())
            time.sleep(int(m[1]))
            robot.stop()
    except Exception as e:
        print(e)

    db.close()
    return


@app.route("/", methods=['GET', 'POST'])
def index():

    movements = {'right'        :  robot.right,
                 'left'         :  robot.left,
                 'up'           :  robot.forward,
                 'down'         :  robot.backward,
                 'btn_sequence' :  executeSequence(request.form.get('txt_sequence'))}
    

    if request.method == 'POST':
        for key, value in movements.items():
            if request.form.get(key) == key.upper():
                print(value())
        
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True, host='localhost')
