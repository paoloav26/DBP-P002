from distutils.log import error
from shutil import ExecError
from flask import (
    Flask,
    jsonify,
    abort,
    request,
    render_template,
    redirect,
    url_for,
    session
)
from flask_cors import CORS
import json
import sys
import hashlib
from pytest import Item
from sqlalchemy import desc, func, inspect

from models import *

RATING_PER_PAGE = 5

def pagination_rating(request, selection, isDescendent):
    if isDescendent:
        start = len(selection) - RATING_PER_PAGE
        end = len(selection)
    else:
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * RATING_PER_PAGE
        end = start + RATING_PER_PAGE
    
    ratings = [rating.format() for rating in selection]
    current_ratings = ratings[start:end]
    return current_ratings


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = "totally_secret_key"
    setup_db(app)
    CORS(app, max_age=10)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    def Sha512Hash(Password): 
        HashedPassword=hashlib.sha512(Password.encode('utf-8')).hexdigest()
        return HashedPassword

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.filter_by(username=user_id).first()
    
    # USUARIOS
    @app.route('/usuarios', methods=['GET'])
    def get_usuarios():
        selection = Usuario.query.order_by('username').all()
        usuarios = pagination_rating(request, selection, False)
        
        if len(usuarios) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'usuarios': usuarios,
            'total_usuarios': len(selection)
        })
    
    @app.route('/usuarios', methods=['POST'])
    def create_usuarios():
        error_422 = False
        error_401 = False
        body = request.get_json()
        username = body.get('username', None)
        correo = body.get('correo', None)
        password = body.get('password_', None)
        numeros = ['0','1','2','3','4','5','6','7','8 ','9']
        existe_numero = False
        
        try:
            if username is None or correo is None or password is None:
                error_422 = True
                abort(422)

            temp_correo = Usuario.query.filter_by(correo=correo).first()
            temp_username = Usuario.query.filter_by(username=username).first()

            if temp_correo == None and temp_username == None:
                for i in password:
                    if i in numeros:
                        existe_numero = True
                        
                if len(password) > 8 and existe_numero == True:
                    password = Sha512Hash(password)
                    usuario = Usuario(username=username, correo=correo, password_=password)
                    usuario.insert()
                    new_usuario = username

                    selection = Usuario.query.order_by('username').all()
                    usuarios = pagination_rating(request,selection,True)

                    return jsonify({
                        'success': True,
                        'created': new_usuario,
                        'usuarios': usuarios,
                        'total_usuarios': len(selection)

                    })
                else:
                    error_401 = True
                    abort(401)
            else:
                abort(500)
        except Exception as e:
            print(e)
            if error_422:
                abort(422)
            elif error_401:
                abort(401)
            else:
                abort(500)
            
    @app.route('/usuarios/login', methods=['GET'])
    def login_user():
        pass
        
    @app.route('/usuarios/<username>', methods=['PATCH'])
    def update_usuarios(username):
        error_404 = False
        try:
            usuario = Usuario.query.filter(Usuario.username == username).one_or_none()
            if usuario is None:
                error_404 = True
                abort(404)
            
            body = request.get_json()
            if 'username' in body:
                usuario.username = body.get('username')
            if 'correo' in body:
                usuario.correo = body.get('correo')
            if 'password' in body:
                usuario.password = body.get('password')
            
            usuario.update()
            
            return jsonify({
                'success': True,
                'usuario': username
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)
                
    @app.route('/usuarios/<username>', methods=['DELETE'])
    def delete_usuario(username):
        error_404 = False
        try:
            usuario = Usuario.query.filter(Usuario.username == username).one_or_none()
            if usuario is None:
                error_404 = True
                abort(404)
            
            usuario.delete()
            
            selection = Usuario.query.order_by('username').all()
            usuarios = pagination_rating(request,selection,True)
            
            return jsonify({
                'success': True,
                'deleted': username,
                'usuarios': usuarios,
                'total_usuarios': len(selection)
            })
            
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)
    
    #ITEMS
    @app.route('/items', methods=['GET'])
    def get_items():
        selection = Items.query.order_by('id').all()
        items = pagination_rating(request,selection,False)
        
        if len(items) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'items': items,
            'total_items': len(selection)
        })
    
    @app.route('/items', methods=['POST'])
    def create_items():
        body = request.get_json()
        nombre = body.get('nombre', None)
        descripcion = body.get('descripcion', None)
        calificacion = body.get('calificacion', None)
        imagen = body.get('imagen', None)
        categoria = body.get('categoria',None)
        
        if nombre is None or descripcion is None or calificacion is None or imagen is None or categoria is None:
            abort(422)
            
        try:
            item = Item(nombre=nombre, descripcion=descripcion, calificacion=calificacion, imagen=imagen, categoria=categoria)
            new_item = item.get_id()
            item.insert()
            
            selection = Items.query.order_by('id').all()
            items = pagination_rating(request,selection,True)
            
            return jsonify({
                'success': True,
                'created': new_item,
                'items': items,
                'total_items': len(selection)
                
            })
        except Exception as e:
            print(e)
            abort(500)
    
    @app.route('/items/<id_item>', methods=['PATCH'])
    def update_items(id_item):
        error_404 = False
        try:
            item = Items.query.filter(Items.id == id_item).one_or_none()
            if item is None:
                error_404 = True
                abort(404)
            
            body = request.get_json()
            if 'nombre' in body:
                item.nombre = body.get('nombre')
            if 'descripcion' in body:
                item.descripcion = body.get('descripcion')
            if 'calificacion' in body:
                item.calificacion = body.get('calificacion')
            if 'imagen' in body:
                Items.imagen = body.get('imagen')
            if 'categoria' in body:
                item.categoria = body.get('categoria')
            
            item.update()
            
            return jsonify({
                'success': True,
                'item': id_item
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)
                
    @app.route('/items/<id_items>', methods=['DELETE'])
    def delete_items(id_items):
        error_404 = False
        try:
            item= Items.query.filter(Items.id == id_items).one_or_none()
            if item is None:
                error_404 = True
                abort(404)
            
            item.delete()
            
            selection = Items.query.order_by('id').all()
            items = pagination_rating(request,selection,True)
            
            return jsonify({
                'success': True,
                'deleted': id_items,
                'items': items,
                'total_items': len(selection)
            })
            
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)
                
    #CALIFICA
    @app.route('/calificaciones', methods=['GET'])
    def get_calificaciones():
        selection = Califica.query.order_by('items_id').all()
        calificaciones = pagination_rating(request,selection,False)
        
        if len(calificaciones) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'calificaciones': calificaciones,
            'total_calificaciones': len(selection)
        })
        
    @app.route('/calificaciones', methods=['POST'])
    def create_calificaciones():
        error_404 = False
        error_422 = False
        body = request.get_json()
        usuario_username = body.get('usuario_username', None)
        items_id = body.get('items_id', None)
        puntaje = body.get('puntaje', None)
        comentario = body.get('comentario', None)
        
        if usuario_username is None or items_id is None or puntaje is None or comentario is None or comentario.strip() == '':
            error_422 = True
            abort(422)
            
        #Verificar si existe el usuario e item id en la base de datos
        ver_usuario = Usuario.query.filter(Usuario.username == usuario_username).one_or_none()
        ver_item_id = Items.query.filter(Items.id == items_id).one_or_none()
        
        try:
            if ver_usuario != None and ver_item_id != None:
                califica = Califica(usuario_username=usuario_username, items_id=items_id, puntaje=puntaje, comentario=comentario)
                news = [califica.items_id, califica.usuario_username]
                califica.insert()

                selection = Califica.query.order_by('items_id').all()
                calificaciones = pagination_rating(request,selection,True)

                return jsonify({
                    'success': True,
                    'id_created': news[0],
                    'username_created': news[1],
                    'calificaciones': calificaciones,
                    'total_calificaciones': len(selection)
                })
            else:
                error_404 = True
                abort(404)
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            elif error_422:
                abort(422)
            else:
                abort(500)
    
    @app.route('/calificaciones/<username>/<items_id>', methods=['PATCH'])
    def update_calificaciones(items_id, username):
        error_404 = False
        error_401 = False
        try:
            califica = Califica.query.filter(Califica.items_id == items_id, Califica.usuario_username == username).one_or_none()
            if califica is None:
                error_404 = True
                abort(404)
            
            #Puntaje y comentario tienen que estar OBLIGATORIO, sino no actualiza
            body = request.get_json()
            if 'puntaje' in body and 'comentario' in body:
                comentario = body.get('comentario',None)
                puntaje = body.get('puntaje',None)
                if puntaje is not None and comentario is not None and comentario.strip() != '':
                    califica.puntaje = puntaje
                    califica.comentario = comentario
                else:
                    error_401 = True
                    abort(401)
            else:
                abort(500)
                
            califica.update()
            
            return jsonify({
                'success': True,
                'item_calificado': items_id,
                'username': username
            })
        except:
            if error_404:
                abort(404)
            elif error_401:
                abort(401)
            else:
                abort(500)
                
    @app.route('/calificaciones/<username>/<items_id>', methods=['DELETE'])
    def delete_calificaciones(username, items_id):
        error_404 = False
        try:
            califica = Califica.query.filter(Califica.items_id == items_id, Califica.usuario_username == username).one_or_none()
            if califica is None:
                error_404 = True
                abort(404)
            
            califica.delete()
            
            selection = Califica.query.order_by('items_id').all()
            calificaciones = pagination_rating(request,selection,True)
            
            return jsonify({
                'success': True,
                'deleted_comentario_item': items_id,
                'deleted_comentario_user': username,
                'calificaciones': calificaciones,
                'total_calificaciones': len(selection)
            })
            
        except Exception as e:
            print(e)
            if error_404 == True:
                abort(404)
            else:
                abort(500)
                
    #CATEGORIA
    @app.route('/categorias', methods=['GET'])
    def get_categorias():
        selection = Categorias.query.order_by('categoria').all()
        categorias = pagination_rating(request,selection,False)
        
        if len(categorias) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'categorias': categorias,
            'total_categorias': len(selection)
        })
    
    @app.route('/categorias', methods=['POST'])
    def create_categorias():
        body = request.get_json()
        categoria = body.get('categoria', None)
        
        if categoria is None:
            abort(422)
            
        try:
            categoria = Categorias(categoria=categoria)
            new_categoria = categoria.insert()
            
            selection = Categorias.query.order_by('categoria').all()
            categorias = pagination_rating(request,selection,True)
            
            return jsonify({
                'success': True,
                'created': new_categoria,
                'categorias': categorias,
                'total_categorias': len(selection)
            })
        except Exception as e:
            print(e)
            abort(500)
    
    @app.route('/categorias/<categoria>', methods=['PATCH'])
    def update_categorias(categoria):
        error_404 = False
        try:
            categoria = Categorias.query.filter(Categorias.categoria == categoria).one_or_none()
            if categoria is None:
                error_404 = True
                abort(404)
            
            body = request.get_json()
            if 'categoria' in body:
                categoria.categoria = body.get('categoria')
            
            categoria.update()
            
            return jsonify({
                'success': True,
                'categoria': categoria,
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)
                
    @app.route('/categorias/<categoria>', methods=['DELETE'])
    def delete_categorias(categoria):
        error_404 = False
        try:
            categoria = Categorias.query.filter(Categorias.categoria == categoria).one_or_none()
            if categoria is None:
                error_404 = True
                abort(404)
            
            categoria.delete()
            
            selection = Categorias.query.order_by('categoria').all()
            categorias = pagination_rating(request,selection,True)
            
            return jsonify({
                'success': True,
                'deleted': categoria,
                'categorias': categorias,
                'total_categorias': len(selection)
            })
            
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)
                

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404
        
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'internal server error'
        }), 500
        
        
    @app.errorhandler(405)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 405,
            'message': 'method not allowed'
        }), 405
        
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'unprocessable'
        }), 422
        
    
    @app.errorhandler(401)
    def Unauthorized(error):
        return jsonify({
            'success': False,
            'code': 401,
            'message': 'unauthorized'
        }), 401
    
    return app



'''
from shutil import ExecError
from flask import Flask, jsonify, redirect, render_template, url_for, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import sys
import hashlib
from sqlalchemy import func, inspect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/ratingapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "totally_secret_key"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def Sha512Hash(Password): 
    HashedPassword=hashlib.sha512(Password.encode('utf-8')).hexdigest()
    return HashedPassword

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(username=user_id).first()


#creacion de la bd
class Usuario(db.Model, UserMixin):
    def get_id(self):
           return (self.username)

    __tablename__ = 'usuario'
    username = db.Column(db.String(), primary_key=True)
    correo = db.Column(db.String(), nullable=False, unique=True)
    password_ = db.Column(db.String(), nullable=False)
    username_rel = db.relationship('Califica', backref='usuario', lazy=True)
    
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
    
    def __repr__(self):
        return f'Id: {self.id} Categoria: {self.categoria} Nombre: {self.nombre} Descripcion: {self.descripcion} Calificacion: {self.calificacion}'

class Califica(db.Model):
    __tablename__ = 'califica' 
    usuario_username = db.Column(db.String(), db.ForeignKey('usuario.username'), primary_key=True, nullable=False) 
    items_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(), nullable=True)
    
    def __repr__(self):
        return f'Username: {self.usuario_username} Id Item: {self.items_id} Puntaje: {self.puntaje} Comentario: {self.comentario}'

class Categorias(db.Model):
    categoria = db.Column(db.String(), primary_key=True ,nullable=False)
    cateogia_rel = db.relationship('Items', backref='categorias', lazy=True)
    
    def __repr__(self):
        return f'Categoria: {self.categoria}'


@app.route("/<categoria_actual>")
def home(categoria_actual):
    d = []
    items = Items.query.filter_by(categoria=categoria_actual)
    categorias = Categorias.query.all()
    
    for u in categorias:
        d.append(u.__dict__['categoria'])
        
    if categoria_actual not in d:
        abort(404)
    return render_template("home.html",categoria_actual=categoria_actual,items=items,categorias=categorias)
    
        

@app.route("/<categoria_actual>/<item_id>")
def item_page(categoria_actual,item_id):
    item = Items.query.filter_by(id=int(item_id)).first()
    comentarios = Califica.query.filter_by(items_id=int(item_id))
    conteo = Califica.query.filter_by(items_id=int(item_id)).count()
    total = Califica.query.with_entities(func.sum(Califica.puntaje).label('Putanje_Total')).filter_by(items_id = item_id).first()
    ids = Items.query.all()
    items_ids = []
    lista_evalu = [categoria_actual, int(item_id)]
    
    for u in ids:
        lista = []
        lista.append(u.__dict__['categoria'])
        lista.append(int(u.__dict__['id']))
        items_ids.append(lista)
    
    promedio = 0
    if(conteo == 0 or total == 0):
        promedio = 0
    else:
        promedio=int(total[0]/conteo)
    
    if(current_user.is_authenticated):
        if lista_evalu in items_ids:
            return render_template("item.html",categoria_actual=categoria_actual,item=item,comentarios=comentarios,promedio=promedio ,existe_comentario = existe_comentario(persona=current_user.username,id=item_id))
        else:
            abort(404)
    return render_template("item.html",categoria_actual=categoria_actual,item=item,comentarios=comentarios,promedio=promedio)

@app.route("/agregar_calificacion/<persona>/<id>",methods=['POST'])
def comentar(persona,id):
    response={}
    error=False
    status=200
    try:
        args = request.get_json()
        usuario_username=persona
        items_id=id
        puntaje=args['puntaje_valor']
        comentario=args['comentario']

        if comentario.strip() != '':
            temp_add=Califica(usuario_username=usuario_username,items_id=items_id,puntaje=puntaje,comentario=comentario)
            db.session.add(temp_add)
            db.session.commit()
            response={'status':200,'comentario':args['comentario'],'username':persona}
        else:
            response={'msg':'Completa el campo de Comentarios'}
            status = 400
    except:
        db.session.rollback()
        if(len(Califica.query.filter((Califica.usuario_username==persona) & (Califica.items_id==id)).all())>0):
            response={'msg':'No puedes publicar mas de una vez en un post, modifica o elimina tu comentario actual'}
            status=409
        elif ("comentario" not in args or "puntaje_valor" not in args):
            response={'msg':'Llena todos los campos antes de enviar tu publicacion'}
            status=400
        else:
            response={'msg':''}
            status=500
        print(sys.exc_info())

    finally:
        db.session.close()
        return jsonify(response), status

@app.route("/actualizar_comentario/<item_id>")
def actualizar(item_id):
    item = Items.query.filter_by(id=int(item_id)).first()
    veri_comentario = Califica.query.filter_by(items_id=item_id,usuario_username=current_user.username).all()
    if(current_user.is_authenticated and len(veri_comentario)):
        return render_template('actualizar.html',persona = current_user,item=item)
    return redirect('http://127.0.0.1:5000/404')

@app.route("/actualizar_comentario/<persona>/<item_id>",methods=['POST'])
def actualizar_comentario(persona,item_id):
    response = {}
    error=False
    status=200
    try:
        args = request.get_json()
        puntaje=args['puntaje_valor']
        comentario=args['comentario']
        if comentario.strip() != '':
            db.session.query(Califica).filter(
                Califica.usuario_username == persona,
                Califica.items_id == item_id
            ).update(
                {
                    Califica.comentario : comentario,
                    Califica.puntaje : int(puntaje)
                }
            )
            db.session.commit()
            response={'status':200,'comentario':args['comentario'],'username':persona}
        else:
            response={'msg':'Completa el campo de Comentarios'}
            status = 400
            
            
        
    except:
        db.session.rollback()
        if ("comentario" not in args or "puntaje_valor" not in args):
            response={'msg':'Llena todos los campos antes de actualizar tu publicacion'}
            status=400
        else:
            response={'msg':''}
            status=500
        print(sys.exc_info())

    finally:
        db.session.close()
        return jsonify(response), status

@app.route("/eliminar_comentario/<persona>/<id>", methods=['POST'])
def eliminar(persona,id):
    response = {}
    try:
        usuario_username=persona
        items_id=id
        coment = Califica.query.filter_by(usuario_username=usuario_username,items_id=items_id).first()
        db.session.delete(coment)
        db.session.commit()
        response['msg'] = 'Correcto'
    except Exception as e:
        db.session.rollback()
        print(e)
    finally:
        db.session.close()
    return jsonify(response)
    
@app.route("/search_items",methods=['POST'])
def search_items():
    response={}
    error=False
    try:
        args = request.get_json()
        # aca va la insersion de la data
        search_name=args['search_name']
        categoria=args['categoria']
        items_list = Items.query.filter((Items.nombre.like("%"+search_name+"%")) & (Items.categoria==categoria)).all()
        response = {'html': render_template('template_items.html',items=items_list,categoria_actual=categoria)}
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify(response)

@app.route("/login_validator",methods=['POST'])
def login_validator():
    response={}
    try:
        args = request.get_json()
        #aca va la insersion de la data
        correo=args['email']
        password_=args['password']
        user = Usuario.query.filter_by(correo=correo).first()
        password_=Sha512Hash(password_)
        if user.password_==password_:
            login_user(load_user(user.username))
            response = {"msg":"Logged!"}
        else:
            abort(500)

    except:
        print(sys.exc_info())
        db.session.rollback()
        response = {"msg":"El correo es incorrecto o la contraseña son incorrectos"}
    finally:
        db.session.close()
        return jsonify(response)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout",methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({})

@app.route("/register_validator",methods=['POST'])
def register_validator():
    response={}
    try:
        args = request.get_json()
        correo=args['email']
        password_=args['password']
        username=args['username']

        temp_correo = Usuario.query.filter_by(correo=correo).first()
        temp_username = Usuario.query.filter_by(username=username).first()
        
        if temp_correo==None and temp_username==None:
            numbers=['0','1','2','3','4','5','6','7','8 ','9']
            existe_numbero=0
            for i in range(len(password_)):
                if password_[i] in numbers: existe_numbero=1

            if len(password_)>8 and existe_numbero==1:
                password_=Sha512Hash(password_)
                print(username,password_)
                response['msg']="Register sucessful!"
                temp_add=Usuario(username=username,correo=correo,password_=password_)
                db.session.add(temp_add)
                db.session.commit()
            else:
                response['msg']="La contraseña no cumple con tener 9 caracteres como minimo"
        else:
            abort(500)

    except:
        print(sys.exc_info())
        db.session.rollback()
        if temp_correo != None:
            response['msg']="El correo ya se encuentra en uso"
        elif temp_username != None:
            response['msg']="El username ya se encuentra en uso"
    finally:
        db.session.close()
        return jsonify(response)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/')
def inicio():
    return render_template('index.html',categorias=Categorias.query.all())

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")

def existe_comentario(persona, id):
    if Califica.query.filter_by(usuario_username=persona, items_id=id).first():
        return True
    else:
        return False
    

if __name__ == '__main__': 
    app.run(debug=True, port=5000)
'''