import datetime
from models import User, Profile
from flask import Blueprint, jsonify, request
from cloudinary.uploader import upload
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

bpAuth = Blueprint("bpAuth", __name__)

@bpAuth.route('/login', methods=['POST'])
def login():
    return jsonify({ "msg": "Inicio de session"}), 200

@bpAuth.route('/register', methods=['POST'])
def register():
    
    avatar = None
    cv = None
    name = ""
    
    boletas = None
    
    if not 'username' in request.form:
        return jsonify({ "msg": "Username is required"}), 400 
    
    if not 'password' in request.form:
        return jsonify({ "msg": "Password is required"}), 400 
    
    username = request.form['username']
    password = request.form['password']
    
    
    userFound = User.query.filter_by(username=username).first()
    
    if userFound:
        return jsonify({ "msg": "Username already exists"}), 400
    
    
    if 'name' in request.form:
        name = request.form['name']
    
    if 'avatar' in request.files:
        avatar = request.files['avatar']
        
    if 'cv' in request.files:
        cv = request.files['cv']
        
        
    # recibir varios archivos relacionados ejemplo: un grupo de imagenes o archivos    
    if 'boletas' in request.files:
        boletas = request.files.getlist('boletas')
        
        for boleta in boletas:
            print(boleta.filename)
        
    respA = None
    if avatar is not None:
        respA = upload(avatar, folder="empleados/avatars")
        if respA:
            avatar = respA['secure_url']
        else:
            return jsonify({ "msg": "Error al subir el avatar"}), 400
        
    respB = None
    if cv is not None:
        respB = upload(cv, folder="empleados/cv")
        if respB:
            cv = respB['secure_url']
        else:
            return jsonify({ "msg": "Error al subir el cv"}), 400
    
    
    data = {
        "username": username,
        "password": password,
        "name": name,
        "avatar": avatar if avatar is not None else "",
        "cv": cv if cv is not None else ""
    }
    
    user = User()
    user.username = data['username']
    user.password = generate_password_hash(data['password'])
    
    profile = Profile()
    profile.name = data['name']
    profile.avatar = data['avatar']
    profile.cv = data['cv']
    
    user.profile = profile
    user.save()
    
    if user:
        expires = datetime.timedelta(days=3)
        acces_token = create_access_token(identity=user.id, expires_delta=expires)
        
        datos = {
            "access_token": acces_token,
            "user": user.serialize_with_profile()
        }
        
        return jsonify(datos), 200
    
    else:
        return jsonify({"msg": "Error, please try again later!"}), 400