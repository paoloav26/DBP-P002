from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate

database_name='ratingapp'
database_path="postgresql+psycopg2://{}@{}/{}".format('postgres:1234', 'localhost:5432', database_name)
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    username = db.Column(db.String(), primary_key=True)
    correo = db.Column(db.String(), nullable=False, unique=True)
    password_ = db.Column(db.String(), nullable=False)
    username_rel = db.relationship('Califica', backref='usuario', lazy=True)
    
    def get_id(self):
        return (self.username)
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            #return self.username
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'username': self.username,
            'password': self.password_,
            'correo': self.correo
        }
    
    def __repr__(self):
        return f'Username: {self.username} Correo: {self.correo}'
    
class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), nullable=False)
    descripcion = db.Column(db.String(), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(), nullable=False)
    categoria = db.Column(db.String(), db.ForeignKey('categorias.categoria'), nullable=True)
    id_rel = db.relationship('Califica', backref='items', lazy=True)
    
    def get_id(self):
        return self.id
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            #return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'calificacion': self.calificacion,
            'imagen': self.imagen,
            'categoria': self.categoria
        }
    
    def __repr__(self):
        return f'Id: {self.id} Categoria: {self.categoria} Nombre: {self.nombre} Descripcion: {self.descripcion} Calificacion: {self.calificacion}'

class Califica(db.Model):
    __tablename__ = 'califica' 
    usuario_username = db.Column(db.String(), db.ForeignKey('usuario.username'), primary_key=True, nullable=False) 
    items_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(), nullable=True)
    
    def get_usuario(self):
        return self.usuario_username
    
    def get_item_id(self):
        return self.items_id
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            #lista = [self.items_id, self.usuario_username]
            #return lista
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'username': self.usuario_username,
            'item_id': self.items_id,
            'puntaje': self.puntaje,
            'comentario': self.comentario
        }
    
    def __repr__(self):
        return f'Username: {self.usuario_username} Id Item: {self.items_id} Puntaje: {self.puntaje} Comentario: {self.comentario}'

class Categorias(db.Model):
    categoria = db.Column(db.String(), primary_key=True ,nullable=False)
    cateogia_rel = db.relationship('Items', backref='categorias', lazy=True)
    
    def get_categoria(self):
        return self.categoria
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            #return self.categoria
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'categoria': self.categoria
        }
    
    def __repr__(self):
        return f'Categoria: {self.categoria}'
