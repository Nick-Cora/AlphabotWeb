import time
from flask import Flask, render_template, request
from lib.config import *
from lib.query import Db_Connection

if not DUMMY:
    from lib.alphabot import AlphaBot
else:
    from lib.alphabot_dummy import AlphaBot


robot = AlphaBot()
app = Flask(__name__)
status = {  'right'        : 0,
            'left'         : 0,
            'up'           : 0,
            'down'         : 0}


def executeSequence(cmd):
    
    if cmd == None or cmd == "":
        return

    commands = {'right'        :  robot.right,
                 'left'         :  robot.left,
                 'forward'      :  robot.forward,
                 'backward'     :  robot.backward,
                 'stop'         :  robot.stop}

    #apro db
    db = Db_Connection('./lib/database.db')

    #invio richiesta
    try:
        seq = db.findRecords('Movimenti', 'sequenza', condition=f'nome = "{cmd}"')
        seq = seq[0][0].split(';')

        for m in seq:
            m = m.split('_')
            print(commands[m[0]]())
            time.sleep(int(m[1]))
            robot.stop()
    except Exception as e:
        print(e)
    

    db.close()
    return



