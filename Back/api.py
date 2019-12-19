from flask import Flask, render_template, url_for, request, redirect, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'benvai'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maistas.db'
os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


class Maistas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(20), unique=True, nullable=False)
    kcal = db.Column(db.Integer)
    angliavandeniai = db.Column(db.Integer)
    riebalai = db.Column(db.Integer)
    sotiejiRiebalai = db.Column(db.Integer)
    baltymai = db.Column(db.Integer)
    kokybe = db.Column(db.Integer, nullable=False)
    vartotojo_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recepto_id = db.Column(db.Integer, db.ForeignKey('receptas.id'), nullable=False)

    def __repr__(self):
        return f"Maistas('{self.pavadinimas}', '{self.kcal}')"

class Receptas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(20), unique=True, nullable=False)
    kcal = db.Column(db.Integer)
    angliavandeniai = db.Column(db.Integer)
    riebalai = db.Column(db.Integer)
    sotiejiRiebalai = db.Column(db.Integer)
    baltymai = db.Column(db.Integer)
    kokybe = db.Column(db.Integer, nullable=False)
    maistoProduktai = db.relationship('Maistas')
    vartotojo_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey('planas.id'), nullable=False)

    def __repr__(self):
        return f"Receptas('{self.pavadinimas}', '{self.kcal}')"

class Planas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(20), unique=True, nullable=False)
    Komentaras = db.Column(db.String(200))
    ivertinimas = db.Column(db.Integer, nullable=False)
    receptai = db.relationship('Receptas')
    vartotojo_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Planas('{self.pavadinimas}', '{self.kcal}')"

class Vartotojas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20))
    planai = db.relationship('Planas')
    receptai = db.relationship('Receptas')
    maistoProduktai = db.relationship('Maistas')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class VartotojoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'password')

vartotojas_schema = VartotojoSchema()
vartotojas_schema = VartotojoSchema(many=True)


maistasJson = ''
receptasJson = ''
planasJson = ''



class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response




#Create
@app.route('/vartotojas', methods=['POST'])
@token_required
def createVartotojas():
    if request.method == 'POST':
        data = request.get_json()
        print("fdfdfdfdf")
        print(data)

        #hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = Vartotojas(name=data['name'], password=data['password'])
        
        
        db.session.add(new_user)
        db.session.commit()
        jsonify({'message' : 'New user created!'})
  

@app.route('/planas', methods=['POST'])
def createPlanas():
    with open('planas1.json', 'r') as f:
        maistasJson = json.load(f)
    
    if request.method == 'POST':
        try:
            return jsonify(maistasJson), 201
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/receptas', methods=['POST'])
def createReceptas():
    with open('receptas1.json', 'r') as f:
        maistasJson = json.load(f)
    
    if request.method == 'POST':
        try:
            return jsonify(maistasJson), 201
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/maistas', methods=['POST'])
def createMaistas():
    with open('maistas.json', 'r') as f:
        maistasJson = json.load(f)
    
    if request.method == 'POST':
        try:
            return jsonify(maistasJson), 201
        except:
            return 408

#GET Metodai
@app.route('/planas', methods=['GET'])
def getPlanasAll():
    with open('planasvisi.json', 'r') as f:
        maistasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            allPlanai = Planas.query.all()
            return jsonify(maistasJson)
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/vartotojas', methods=['GET'])
def getVartotojasAll():
    if request.method == 'GET':
        try:
            allVartotojai = Vartotojas.query.all()
            output = []

            for user in allVartotojai:
                user_data = {}
                user_data['id'] = user.id
                user_data['name'] = user.username
                user_data['password'] = user.password
                output.append(user_data)

            return jsonify({'vartotojai' : output})
        except:
            return InvalidUsage('Item not found', status_code=404)


@app.route('/receptas', methods=['GET'])
def getReceptasAll():
    with open('receptasvisi.json', 'r') as f:
        receptasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            allReceptai = Receptas.query.all()
            return jsonify(receptasJson)
        except:
            return 408

#Gauti recepta pagal id
@app.route('/maistas', methods=['GET'])
def getMaistasAll():
    with open('maistasvisi.json', 'r') as f:
        receptasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            allMaistas = Maistas.query.all()
            return jsonify(receptasJson)
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/planas/<int:id>', methods=['GET'])
def getPlanas(id):
    with open('planas1.json', 'r') as f:
        receptasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            return jsonify(receptasJson)
        except:
            return InvalidUsage('Item not found', status_code=404)



@app.route('/planas/<int:id>/receptas', methods=['GET'])
def getPlanReceptaiAll(id):
    with open('receptasvisi.json', 'r') as f:
        receptasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            rez = Planas.query.get(id)
            return jsonify(receptasJson)
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/planas/<int:id>/receptas/<int:idRec>', methods=['GET'])
def getPlanRecepta(id, idRec):
    with open('receptas1.json', 'r') as f:
        receptasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            rez = Receptas
            return jsonify(receptasJson)
        except:
            return InvalidUsage('Item not found', status_code=404)


@app.route('/planas/<int:id>/receptas/<int:idRec>/maistas', methods=['GET'])
def getPlanoMaistaAll(id, idRec):
    with open('maistasvisi.json', 'r') as f:
        receptasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            return jsonify(receptasJson)
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/planas/<int:id>/receptas/<int:idRec>/maistas/<int:idMaist>', methods=['GET'])
def getPlanoMiasta(id, idRec, idMaist):
    with open('maistas.json', 'r') as f:
        receptasJson = json.load(f)
    
    if request.method == 'GET':
        try:
            return jsonify(receptasJson)
        except:
            return InvalidUsage('Item not found', status_code=404)

#Update
@app.route('/planas/<int:id>', methods=['PUT'])
def updatePlanas(id):
    with open('planas1.json', 'r') as f:
        planasJson = json.load(f)
    
    if request.method == 'PUT':
        try:
            return jsonify(planasJson)
        except:
            return 408

@app.route('/planas/<int:id>/receptas/<int:idRec>', methods=['PUT'])
def updateReceptas(id, idRec):
    with open('receptas1.json', 'r') as f:
        planasJson = json.load(f)
    
    if request.method == 'PUT':
        try:
            return jsonify(planasJson)
        except:
            return 408

@app.route('/planas/<int:id>/receptas/<int:idRec>/maistas/<int:idMaist>', methods=['PUT'])
def updateMaistas(id, idRec, idMaist):
    with open('maistas.json', 'r') as f:
        planasJson = json.load(f)
    
    if request.method == 'PUT':
        try:
            return jsonify(planasJson)
        except:
            return 408

#Delete 
@app.route('/planas/<int:id>', methods=['DELETE'])
def deleteplanas(id):
    with open('planas1.json', 'r') as f:
        planasJson = json.load(f)
    
    if request.method == 'DELETE':
        try:
            return jsonify(planasJson), 204
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/planas/<int:idPlan>/receptas/<int:idRec>', methods=['DELETE'])
def deleteRecepta(idPlan, idRec):
    with open('receptas1.json', 'r') as f:
        planasJson = json.load(f)
    
    if request.method == 'DELETE':
        try:
            return jsonify(planasJson), 204
        except:
            return InvalidUsage('Item not found', status_code=404)

@app.route('/planas/<int:idPlan>/receptas/<int:idRec>/maistas/<int:idMaist>', methods=['DELETE'])
def deleteMaista(idPlan, idRec, idMaist):
    with open('maistas.json', 'r') as f:
        planasJson = json.load(f)
    
    if request.method == 'DELETE':
        try:
            return jsonify(planasJson), 204
        except:
            return InvalidUsage('Item not found', status_code=404)


if __name__ == "__main__":
    app.run(debug=True)