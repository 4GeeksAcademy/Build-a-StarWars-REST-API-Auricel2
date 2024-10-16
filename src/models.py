from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # Relación con Favoritos, permite acceder a los favoritos de un usuario
    favoritos = db.relationship("Favoritos", backref="user")

    def __repr__(self):
        return self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # agregar todas las columnas
        }
class Personajes(db.Model): 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(30))
     lightsaber_user = db.Column(db.Boolean(), unique=False, nullable=False)

    # Relación con Favoritos, permite acceder a los favoritos que incluyen este personaje
     favoritos = db.relationship("Favoritos", backref="personaje")

     def __repr__(self):
        return self.name

     def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # agregar todas las columnas
        }
    
class Planetas(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(20))

    # Relación con Favoritos, permite acceder a los favoritos que incluyen este planeta
     favoritos = db.relationship("Favoritos", backref="planeta")

     def __repr__(self):
        return self.name

     def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # agregar todas las columnas
        }

class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planetas.id'), nullable=True)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=True)


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id,
        }