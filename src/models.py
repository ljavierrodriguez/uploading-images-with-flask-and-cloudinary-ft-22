from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    profile = db.relationship('Profile', backref="user", uselist=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "active": self.active
        }
    
    def serialize_with_profile(self):
        return {
            "id": self.id,
            "username": self.username,
            "active": self.active,
            "profile": self.profile.serialize()
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), default="")
    biography = db.Column(db.String(200), default="")
    facebook = db.Column(db.String(200), default="")
    twitter = db.Column(db.String(200), default="")
    instagram = db.Column(db.String(200), default="")
    avatar = db.Column(db.String(200), default="") # campo para guardar la ubicacion de la foto
    cv = db.Column(db.String(200), default="") # campo para guardar la ubicacion del cv 
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "avatar": self.avatar,
            "cv": self.cv
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        