from flask import Flask, render_template, make_response, redirect, url_for, request
from controller import *
from lib.config import *
import sqlite3
import string
import random
import datetime
from lib.mail import email_alert


app = Flask(__name__)
token = ''.join(random.choice(string.ascii_lowercase) for _ in range(STRING_LENGHT))
registration_token = ''.join(random.choice(string.ascii_lowercase) for _ in range(STRING_LENGHT))
waiting_user_list = {}
username = ''




def validate(username, password):
    completion = False
    db = Db_Connection('./lib/database.db')
    rows = db.findRecords('USERS', '*')
    db.close()

    for row in rows:
        dbUser = row[1]
        dbPass = row[2]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion



def check_password(hashed_password, user_password):
    return hashed_password == user_password

def check_registration(username, password, email):
    return len(username) > 0 and len(password) > 0 and len(email) > 0 and '@' in email



@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('signUp') == 'Sign Up':
            return redirect(url_for('registration_page'))
        
        global username
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            logged = True
            db = Db_Connection('./lib/database.db')
            id_user = db.findRecords('USERS', 'id_user', condition=f'username = "{username}"')
            db.add('access_list', 
                    id_user[0][0], 
                    datetime.datetime.now() ,
                    columns='"username", "date"')
            db.close()
            resp = make_response(redirect(url_for('main_page')))
            resp.set_cookie('username',username)
            return resp
    return render_template('login.html', error=error)



@app.route(f'/{token}', methods=['GET','POST'])
def main_page():
    movements = {'right'        :  robot.right,
                 'left'         :  robot.left,
                 'up'           :  robot.forward,
                 'down'         :  robot.backward,
                 'btn_sequence' :  executeSequence(request.form.get('txt_sequence'))}
    

    if request.method == 'POST':
        for key, value in movements.items():
            username = request.cookies.get('username')
            print(username)
            if request.form.get(key) == key.upper():
                db = Db_Connection('./lib/database.db')
                id_user = db.findRecords('USERS','id_user',condition=f'username = "{username}"')
                if status[key]:
                    robot.stop()
                    id_sequenza = STOP
                else:
                    print(value())
                    id_sequenza = db.findRecords('movimenti','id',condition=f'nome = "{key}"')
                
                db.add('movements_history',
                        id_user[0][0],
                        id_sequenza[0][0],
                        columns='"id_user","id_sequenza"')
                status[key] = not status[key]
        
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")


@app.route(f'/registration_page', methods=['GET','POST'])
def registration_page():
    if request.method == 'POST':
        password = request.form['passwrd']
        username = request.form['name']
        email = request.form['mail']
        msg = None
        if check_registration(username, password, email):
            waiting_user_list[registration_token] = (username,password,email)
            email_alert('Alphabot account verification',
                        f'Hello {username}.\nClick the link below to activate your account:\nhttp://127.0.0.1:5000/{registration_token}/',
                        email)
            msg = 'Data correctly submitted! Check your email to confirm the subscrition.'
        else:
            msg = 'Error. You can\'t leave white fields.'

    elif request.method == 'GET':
        return render_template('registration.html')
    
    return render_template("registration.html", msg=msg)



@app.route(f'/{registration_token}/', methods=['GET','POST'])
def confermation():
    if request.method == 'POST':
        return redirect(url_for("login"))
    if request.method == 'GET':
        username,password,email = waiting_user_list[registration_token]
        db = Db_Connection('./lib/database.db')
        db.add('USERS',username, password, email, columns='"USERNAME","PASSWORD","EMAIL"')
        db.close()
        return render_template("confirmation.html")


if __name__ == "__main__":
    app.run(debug=True, host=SERVER_IP)
