from math import sin, cos, sqrt, atan2, radians
import sys
from flask import Flask,render_template,request,abort,session,redirect,url_for,abort
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.exceptions import HTTPException
from flask_session import Session
import datetime
import json
from flask_socketio import SocketIO,emit
from login_required import login_required

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)



app.config['SQLALCHEMY_DATABASE_URI'] ="postgres://rcafsgmbarqugc:73d136d0acca5678583719c4c1b85d9be13a0248de2f60ab0c665d16b1d2e871@ec2-184-72-238-22.compute-1.amazonaws.com:5432/dcoqtcba4o2qem"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)

@app.route('/',methods=['GET','POST'])
@login_required
def index():
    if request.method == 'GET':
        return render_template("index.html",id=session.get("id"),username=session.get("username"))
    else:
        user = User.query.filter_by(username=session.get("username")).first()
        currentloc=json.loads(request.data)
        print(currentloc)
        user.latitude =currentloc["latitude"]
        user.longitude = currentloc['longitude']
        db.session.commit()
        return render_template('index.html',id=session.get("id"),username=session.get("username"))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        passwordagain = request.form.get('passwordagain')
        email = request.form.get('email')
        # if(request.form.get('isadmin') == "on"):
        #     isadmin=True
        # else:
        #     isadmin=False

        if(password != passwordagain):
            abort(400)
            # raise HTTPException(400,"Password doesn't match")
        if(username=="" or not password or not email):
            abort(400)
            # raise HTTPException(400,"Provide username")
        user=User(username = username, password = password, email = email)
        db.session.add(user)
        db.session.commit()
        print(user.id)
        session["id"]=user.id
        session["username"] = username
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if (not username) or (not password):
            abort(400)
        # isadmin = "false"
        # if(request.form.get('isadmin') == "on"):
        #     isadmin="true"
        # else:
        #     isadmin="false"
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(400)
        if(user.password == password ):
            session["username"] = username
            session['id'] = user.id
            return redirect(url_for('index'))
        #if not admin show normal page but if admin show admin interface
        else:
            abort(400)

hardware={
    "latitude":18.5345485,
    "longitude":73.8880104,
}

def shortest_distance_cal(obj1):
    min_id=None
    # approximate radius of earth in km
    R = 6373.0
    min_distance=sys.maxsize
    lat2 = radians(float(hardware["latitude"]))
    lon2 = radians(float(hardware["longitude"]))
    for obj in obj1:
        lat1 = radians(float(obj["latitude"]))
        lon1 = radians(float(obj["longitude"]))
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        if distance < min_distance:
            min_distance=distance
            min_id=obj["id"]
    print(min_id)
    return min_id


def nearestId():
    latlan=[]
    results=User.query.all()
    for result in results:
        latlan.append({"id":result.id,"latitude":result.latitude,"longitude":result.longitude})
    print(latlan)
    min_id=shortest_distance_cal(latlan)
    return min_id

@socketio.on('connect')
def connect():
        id=nearestId()
        emit('nearest',{'id':id,'latitude':hardware["latitude"],'longitude':hardware['longitude']}, broadcast=True)

@app.route('/logout')
def logout():
    user = User.query.filter_by(id=session.get("id")).first()
    user.latitude="999"
    user.longitude="999"
    db.session.commit()
    session.pop('username', None)
    session.pop('id',None)
    return redirect(url_for('index'))

@app.errorhandler(400)
def page_not_found(e):
    return render_template('error.html',code=400)


if __name__ == '__main__':
    socketio.run(app)
