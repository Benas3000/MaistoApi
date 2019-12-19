from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token , jwt_required ,get_jwt_identity,create_refresh_token,jwt_required , jwt_refresh_token_required
import jwt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=10)
CORS(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    role = db.Column(db.Integer)
    planai = db.relationship('Planas')
    receptai = db.relationship('Receptas')
    maistoProduktai = db.relationship('Maistas')

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
    plano_id = db.Column(db.Integer, db.ForeignKey('planas.id'))

class Planas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(20), unique=True, nullable=False)
    Komentaras = db.Column(db.String(200))
    ivertinimas = db.Column(db.Integer, nullable=False)
    receptai = db.relationship('Receptas')
    vartotojo_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/user', methods=['GET'])
@jwt_required
def get_all_users():
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['role'] = user.role
        output.append(user_data)

    return jsonify({'users' : output}), 201

@app.route('/user', methods=['POST'])
@jwt_required
def create_user():
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    data = request.get_json()

    try:
        users = ''
        users = User.query.filter_by(name=data['name']).first()

        if users == '':
            return jsonify({'message' : 'User with name exsists'}), 400

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, role=True)
        db.session.add(new_user)
        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400   

    return jsonify({'message' : 'New user created!'}), 201

@app.route('/user', methods=['DELETE'])
@jwt_required
def badDeleteUser():
    return jsonify({'message' : "Method not allowed"}), 405

@app.route('/user', methods=['PUT'])
@jwt_required
def badPutUser():
    return jsonify({'message' : "Method not allowed"}), 405





@app.route('/user/<public_id>', methods=['GET'])
@jwt_required
def get_one_user(public_id):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'}),404
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['role'] = user.role

    return jsonify({'user' : user_data}),200


@app.route('/user/<public_id>', methods=['PUT'])
@jwt_required
def promote_user(public_id):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'}), 404

    user.role = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'}), 200

@app.route('/user/<public_id>', methods=['DELETE'])
@jwt_required
def delete_user(public_id):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'}), 204

@app.route('/user/<public_id>', methods=['POST'])
@jwt_required
def badPostUser():
    return jsonify({'message' : "Method not allowed"}), 405

#-----------------------User end----------------------------------------


#----------------------Post--------------------------------------
@app.route('/maistas', methods=['POST'])
@jwt_required
def create_maistas():
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    data = request.get_json()
    try:
        newMaistas = Maistas(pavadinimas=data['pavadinimas'], kcal=data['kcal'], angliavandeniai=data['angliavandeniai'], riebalai=data['riebalai'],
                            sotiejiRiebalai=data['sotiejiRiebalai'], baltymai=data['baltymai'], kokybe=data['kokybe'], vartotojo_id=current_user['id'],
                            recepto_id=data['recepto_id'])

        db.session.add(newMaistas)
        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'New maistas created!'}), 201

@app.route('/maistas', methods=['PUT'])
@jwt_required
def badPutMaistas():
    return jsonify({'message' : "Method not allowed"}), 405

@app.route('/maistas', methods=['DELETE'])
@jwt_required
def badDeleteMaistas():
    return jsonify({'message' : "Method not allowed"}), 405

@app.route('/receptas', methods=['GET'])
@jwt_required
def getAllReceptai():
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    receptas = Receptas.query.all()

    if receptas == None:
        return jsonify({'message' : 'No receptas with this id'}), 404
    output = []

    for receptas in receptas:
        receptas_data = {}
        receptas_data['id'] = receptas.id
        receptas_data['pavadinimas'] = receptas.pavadinimas
        receptas_data['kcal'] = receptas.kcal
        receptas_data['angliavandeniai'] = receptas.angliavandeniai
        receptas_data['riebalai'] = receptas.riebalai
        receptas_data['baltymai'] = receptas.baltymai
        receptas_data['sotiejiRiebalai'] = receptas.sotiejiRiebalai
        receptas_data['kokybe'] = receptas.kokybe
        receptas_data['vartotojo_id'] = receptas.vartotojo_id
        #receptas_data['maistoProduktai'] = receptas.maistoProduktai
        receptas_data['plano_id'] = receptas.plano_id
        
        output.append(receptas_data)

    return jsonify({'receptas' : output}), 200

@app.route('/receptas', methods=['POST'])
@jwt_required
def createReceptas():
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    data = request.get_json()
    try:
        newReceptas = Receptas(pavadinimas=data['pavadinimas'], kcal=data['kcal'], angliavandeniai=data['angliavandeniai'], riebalai=data['riebalai'],
                            sotiejiRiebalai=data['sotiejiRiebalai'], baltymai=data['baltymai'], kokybe=data['kokybe'], vartotojo_id=current_user.get('id'),
                             plano_id=data['plano_id'])

        db.session.add(newReceptas)
        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'New receptas created!'}), 201

@app.route('/receptas', methods=['PUT'])
@jwt_required
def badPutReceptas():
    return jsonify({'message' : "Method not allowed"}), 405

@app.route('/receptas', methods=['DELETE'])
@jwt_required
def badDeleteReceptas():
    return jsonify({'message' : "Method not allowed"}), 405



@app.route('/planas', methods=['POST'])
@jwt_required
def create_planas():
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    data = request.get_json()
    print(data)
    try:
        newPlanas = Planas(pavadinimas=data['pavadinimas'], Komentaras=data['Komentaras'], ivertinimas=data['ivertinimas'], vartotojo_id=current_user['id'])
        db.session.add(newPlanas)
        db.session.commit()
        
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'New planas created!'}), 201

@app.route('/planas', methods=['PUT'])
@jwt_required
def badPutPlanas():
    return jsonify({'message' : "Method not allowed"}), 405

@app.route('/planas', methods=['DELETE'])
@jwt_required
def badDeletePlanas():
    return jsonify({'message' : "Method not allowed"}), 405




@app.route('/planas/<int:id>', methods=['GET'])
@jwt_required
def getPlanas(id):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    planas_data = {}
    planas_data['id'] = planas.id
    planas_data['pavadinimas'] = planas.pavadinimas
    planas_data['Komentaras'] = planas.Komentaras
    planas_data['ivertinimas'] = planas.ivertinimas
    planas_data['vartotojo_id'] = planas.vartotojo_id

    return jsonify({'planas' : planas_data}), 200

@app.route('/planas/<int:id>/receptas/<int:receptasId>', methods=['GET'])
@jwt_required
def getPlanoReceptas(id, receptasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404
        
    receptas_data = {}
    receptas_data['id'] = receptas.id
    receptas_data['pavadinimas'] = receptas.pavadinimas
    receptas_data['kcal'] = receptas.kcal
    receptas_data['angliavandeniai'] = receptas.angliavandeniai
    receptas_data['riebalai'] = receptas.riebalai
    receptas_data['baltymai'] = receptas.baltymai
    receptas_data['sotiejiRiebalai'] = receptas.sotiejiRiebalai
    receptas_data['kokybe'] = receptas.kokybe
    receptas_data['vartotojo_id'] = receptas.vartotojo_id
    receptas_data['plano_id'] = receptas.plano_id

    return jsonify({'planas' : receptas_data}), 200

@app.route('/planas/<int:id>/receptas/<int:receptasId>/maistas/<int:maistasId>', methods=['GET'])
@jwt_required
def getReceptasMaistas(id, receptasId, maistasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404

    maistas = ''
    for maist in receptas.maistoProduktai:
        if(maist.id == maistasId):
            maistas = maist
    if maistas == '':
        return jsonify({'message' : 'No maistas with this id'}), 404

    output = []

    maistas = [maistas]
    
    for maistas in maistas:
        maistas_data = {}
        maistas_data['id'] = maistas.id
        maistas_data['pavadinimas'] = maistas.pavadinimas
        maistas_data['kcal'] = maistas.kcal
        maistas_data['angliavandeniai'] = maistas.angliavandeniai
        maistas_data['riebalai'] = maistas.riebalai
        maistas_data['baltymai'] = maistas.baltymai
        maistas_data['sotiejiRiebalai'] = maistas.sotiejiRiebalai
        maistas_data['kokybe'] = maistas.kokybe
        maistas_data['vartotojo_id'] = maistas.vartotojo_id
        maistas_data['recepto_id'] = maistas.recepto_id
        
        output.append(maistas_data)

    return jsonify({'Maistas' : output}), 200





@app.route('/planas', methods=['GET'])
@jwt_required
def getPlanasAll():
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.all()

    output = []

    for planas in planas:
        planas_data = {}
        planas_data['id'] = planas.id
        planas_data['pavadinimas'] = planas.pavadinimas
        planas_data['Komentaras'] = planas.Komentaras
        planas_data['ivertinimas'] = planas.ivertinimas
        #planas_data['receptai'] = planas.receptai
        planas_data['vartotojo_id'] = planas.vartotojo_id
        
        output.append(planas_data)

    return jsonify({'planas' : output}), 200

@app.route('/planas/<int:id>/receptas', methods=['GET'])
@jwt_required
def getPlanoAllReceptai(id):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = planas.receptai
    output = []

    for receptas in receptas:
        receptas_data = {}
        receptas_data['id'] = receptas.id
        receptas_data['pavadinimas'] = receptas.pavadinimas
        receptas_data['kcal'] = receptas.kcal
        receptas_data['angliavandeniai'] = receptas.angliavandeniai
        receptas_data['riebalai'] = receptas.riebalai
        receptas_data['baltymai'] = receptas.baltymai
        receptas_data['sotiejiRiebalai'] = receptas.sotiejiRiebalai
        receptas_data['kokybe'] = receptas.kokybe
        receptas_data['vartotojo_id'] = receptas.vartotojo_id
        #receptas_data['maistoProduktai'] = receptas.maistoProduktai
        receptas_data['plano_id'] = receptas.plano_id
        
        output.append(receptas_data)

    return jsonify({'planas' : output}), 200

@app.route('/planas/<int:id>/receptas', methods=['POST'])
@jwt_required
def createPlanoRecReceptai(id):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
            return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404
    data = request.get_json()

    try:
        newReceptas = Receptas(pavadinimas=data['pavadinimas'], kcal=data['kcal'], angliavandeniai=data['angliavandeniai'], riebalai=data['riebalai'],
                            sotiejiRiebalai=data['sotiejiRiebalai'], baltymai=data['baltymai'], kokybe=data['kokybe'], vartotojo_id=current_user.get('id'),
                            plano_id=id)

        db.session.add(newReceptas)
        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'New receptas created!'}), 201


@app.route('/planas/<int:id>/receptas/<int:receptasId>/maistas', methods=['GET'])
@jwt_required
def getReceptasAllMaistas(id, receptasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404

    maistas = receptas.maistoProduktai

    output = []

    for maistas in maistas:
        maistas_data = {}
        maistas_data['id'] = maistas.id
        maistas_data['pavadinimas'] = maistas.pavadinimas
        maistas_data['kcal'] = maistas.kcal
        maistas_data['angliavandeniai'] = maistas.angliavandeniai
        maistas_data['riebalai'] = maistas.riebalai
        maistas_data['baltymai'] = maistas.baltymai
        maistas_data['sotiejiRiebalai'] = maistas.sotiejiRiebalai
        maistas_data['kokybe'] = maistas.kokybe
        maistas_data['vartotojo_id'] = maistas.vartotojo_id
        
        output.append(maistas_data)

    return jsonify({'Maistas' : output}), 200

@app.route('/planas/<int:id>/receptas/<int:receptasId>/maistas', methods=['POST'])
@jwt_required
def createReceptasMaistas(id, receptasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404

    data = request.get_json()

    try:
        newMaistas = Maistas(pavadinimas=data['pavadinimas'], kcal=data['kcal'], angliavandeniai=data['angliavandeniai'], riebalai=data['riebalai'],
                            sotiejiRiebalai=data['sotiejiRiebalai'], baltymai=data['baltymai'], kokybe=data['kokybe'], vartotojo_id=current_user.get('id'),
                            recepto_id=receptasId)

        db.session.add(newMaistas)
        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'New receptas created!'}), 201

#------------------------putas----------------

@app.route('/planas/<int:planasId>', methods=['PUT'])
@jwt_required
def updatePlanas(planasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(planasId)
    if not planas:
        return jsonify({'message' : 'No planas found!'}), 404

    data = request.get_json()
    
    try:
        planas.pavadinimas = data['pavadinimas']
        planas.Komentaras = data['Komentaras']
        planas.ivertinimas = data['ivertinimas']

        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'Planas was udated!'}), 200

@app.route('/planas/<int:planasId>/receptas/<int:receptasId>', methods=['PUT'])
@jwt_required
def updateReceptas(planasId, receptasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404

    data = request.get_json()
    try:
        receptas.id = data['id']
        receptas.pavadinimas = data['pavadinimas']
        receptas.kcal = data['kcal']
        receptas.angliavandeniai = data['angliavandeniai']
        receptas.riebalai = data['riebalai']
        receptas.baltymai = data['baltymai']
        receptas.sotiejiRiebalai = data['sotiejiRiebalai']
        receptas.kokybe = data['kokybe']
        receptas.vartotojo_id = data['vartotojo_id']
        receptas.plano_id = data['plano_id']

        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'Receptas was udated!'}), 200


@app.route('/planas/<int:id>/receptas/<int:receptasId>/maistas/<int:maistasId>', methods=['PUT'])
@jwt_required
def updateMaistas(id, receptasId, maistasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404

    maistas = ''
    for maist in receptas.maistoProduktai:
        if(maist.id == maistasId):
            maistas = maist
    if maistas == '':
        return jsonify({'message' : 'No maistas with this id'}), 404


    data = request.get_json()
    try:
        maistas.id = data['id']
        maistas.pavadinimas = data['pavadinimas']
        maistas.kcal = data['kcal']
        maistas.angliavandeniai = data['angliavandeniai']
        maistas.riebalai = data['riebalai']
        maistas.baltymai = data['baltymai']
        maistas.sotiejiRiebalai = data['sotiejiRiebalai']
        maistas.kokybe = data['kokybe']
    except:
        return jsonify({'message' : 'All field must be filled'}), 400 

    return jsonify({'message' : 'Mistas was udated!'}), 200



#-------------------------delete---------------------
@app.route('/planas/<int:id>', methods=['DELETE'])
@jwt_required
def deletePlanas(id):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if not planas:
        return jsonify({'message' : 'No planas found!'}), 404

    db.session.delete(planas)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'}), 204

@app.route('/planas/<int:id>/receptas/<int:receptasId>', methods=['DELETE'])
@jwt_required
def deleteReceptas(id, receptasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}), 404

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404

    db.session.delete(receptas)
    db.session.commit()

    return jsonify({'message' : 'The Receptas has been deleted!'}), 204

@app.route('/planas/<int:id>/receptas/<int:receptasId>/<int:maistasId>', methods=['DELETE'])
@jwt_required
def deleteMaistas(id, receptasId, maistasId):
    current_user = get_jwt_identity()
    if current_user.get('role') == 0:
        return jsonify({'message' : 'Cannot perform that function!'}), 401 

    planas = Planas.query.get(id)

    if planas == None:
        return jsonify({'message' : 'No planas with this id'}),200

    receptas = ''
    for recept in planas.receptai:
        if(recept.id == receptasId):
            receptas = recept
    if receptas == '':
        return jsonify({'message' : 'No receptas with this id'}), 404

    maistas = ''
    for maist in receptas.maistoProduktai:
        if(maist.id == maistasId):
            maistas = maist
    if maistas == '':
        return jsonify({'message' : 'No maistas with this id'}), 404

    db.session.delete(maistas)
    db.session.commit()

    return jsonify({'message' : 'The Maistas has been deleted!'}), 204


#---------------------------------Postai----------------------------------------------
@app.route('/planas/<int:planasId>', methods=['POST'])
@jwt_required
def badupdatePlanas(planasId):
    return jsonify({'message' : "Method not allowed"}), 405

@app.route('/planas/<int:planasId>/receptas/<int:receptasId>', methods=['POST'])
@jwt_required
def badupdateReceptas(planasId, receptasId):
    return jsonify({'message' : "Method not allowed"}), 405

@app.route('/planas/<int:id>/receptas/<int:receptasId>/maistas/<int:maistasId>', methods=['POST'])
@jwt_required
def badupdateMaistas(id, receptasId, maistasId):
    return jsonify({'message' : "Method not allowed"}), 405
   
@app.route('/login',methods=['POST'])
def login():
    content = request.get_json()
    if not content:
         abort(make_response(jsonify(message="worng request format"), 400))
    if  'name' not in content or 'password' not in  content:
        abort(make_response(jsonify(message="all parameters must be set"), 400))
    user = User.query.filter_by(name=content['name']).first()
    if not user :
        abort(make_response(jsonify(message="wrong name/password"), 400))

    if check_password_hash(user.password, content['password']):
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['role'] = user.role

        return jsonify({
                        'access_token': create_access_token(identity=user_data),
                        'refresh_token':create_refresh_token(identity=user_data), 
        }), 200
    abort(make_response(jsonify(message="wrong name/password"), 400))

@app.route('/register',methods = ['POST'])
def register():
    data = request.get_json()

    try:
        users = ''
        users = User.query.filter_by(name=data['name']).first()

        if users == '':
            return jsonify({'message' : 'User with name exsists'}), 400

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, role=1)
        db.session.add(new_user)
        db.session.commit()
    except:
        return jsonify({'message' : 'All field must be filled'}), 400   

    return jsonify({'message' : 'New user created!'}), 201


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


'''
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
'''

if __name__ == '__main__':
    app.run(debug=True)