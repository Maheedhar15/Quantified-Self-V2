from lib2to3.pgen2 import token
from flask import Flask,jsonify, render_template , url_for ,redirect,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


CORS(app, origins='*')



from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager 





# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "54\x85\xfc\x1a*Y\xae"  # Change this!
jwt = JWTManager(app)


class user(db.Model):
    __name__ = "user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    uname = db.Column(db.String(80),nullable=False)
    mail = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(80),nullable=False)

class tracker(db.Model):
    __name__ = "tracker"
    u_id = db.Column(db.String(80),db.ForeignKey('user.uid'),nullable=False)
    tracker_id = db.Column(db.Integer,autoincrement=True,primary_key=True,nullable=False)
    tracker_name = db.Column(db.String(80),nullable=False)
    tracker_description = db.Column(db.String(100))
    tracker_type = db.Column(db.String(40),nullable=False)
    tracker_settings = db.Column(db.String(40))
    date_created = db.Column(db.DateTime,nullable=False, default = datetime.utcnow())

class logtable(db.Model):
    log_id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    user_id = db.Column(db.String(80),db.ForeignKey('user.uid'),nullable=False)
    t_id = db.Column(db.Integer,db.ForeignKey('tracker.tracker_id'),nullable=False)
    Timestamp = db.Column(db.DateTime,nullable=False, default = datetime.utcnow())
    value = db.Column(db.Text,nullable=False)
    Note = db.Column(db.String(80))    

@app.route('/')
@jwt_required()
def home():
    if not get_jwt_identity():
        raise("Identity not verified")
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/login",methods=['GET','POST'])

def login():    
  data = request.json
  print(data['mail'],data['password'])
  encoded_pass = data['password'].encode('utf-8')
  dbdata = user.query.filter_by(mail=data['mail']).first()
  token = create_access_token(identity={"mail":dbdata.mail})
  if(bcrypt.checkpw(encoded_pass,dbdata.password)):
    return jsonify({'access_token': token, 'name':dbdata.uname,'id':dbdata.uid})
  else:
    return "Failure",402
  
@app.route('/register', methods=['GET','POST'])

def register():
    if request.method=='POST':
        data = request.json
        name = data['name']
        mail = data['mail']
        password = data['password']
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cell = user(uname=name,mail=mail,password=pw_hash)
        db.session.add(cell)
        db.session.commit()
        return "Success",200

@app.route('/trackers/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def u_tracker(id):
    table = tracker.query.filter_by(u_id=id).all()
    l = []
    for i in table:
        d = {
            'userid' : i.u_id,
            'trackerid' : i.tracker_id,
            'trackername' : i.tracker_name,
            'trackerdesc' : i.tracker_description,
            'trackertype' : i.tracker_type,
            'tracker_settings' : i.tracker_settings,
            'datecreated' : i.date_created
        }
        l.append(d)
    return jsonify(
        {
            'tracker' : l,
            'message' : 'Success'
        }
    )

@app.route('/trackers/delete/<int:id>', methods=['GET'])
def method_name():
    pass

@app.route('/createtracker/<int:id>', methods=['GET', 'POST'])
def createtracker(id):
    if request.method=='POST':
        data = request.json
        tname = data['tname']
        ttype = data['ttype']
        tdesc = data['tdesc']
        tsettings = data['tsettings']
        cell = tracker(u_id=id,tracker_name=tname,tracker_type=ttype,tracker_description=tdesc,tracker_settings=tsettings)
        db.session.add(cell)
        db.session.commit()
        return "Success",200

if __name__ == "__main__":
    app.run(debug=True)