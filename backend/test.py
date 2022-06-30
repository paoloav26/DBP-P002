import unittest
from flask_sqlalchemy import SQLAlchemy
from server import create_app
from models import setup_db, Items, Califica, Categorias, Usuario
import json

"""
- Darle mas logica a las funciones como si fuera una WEB
- Basarse en el anterior modelo de las funciones para la primera entrega
- Preguntar sobre el test case de la barra de busqueda
"""

class TestCaseRatingApp(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'ratingapp_test'
        self.database_path = 'postgresql://{}@{}/{}'.format('postgres:admin', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)
        
        self.new_usuario = {
            'username': 'Chalanoglu',
            'correo': 'chala@gmail.com',
            'password_': 'Chalanoglu12345'
        }
        
        self.new_calificacion = {
            'usuario_username': 'matias', 
            'items_id': 2, 
            'puntaje': 5, 
            'comentario': 'Me gusto, muy chevere TOP'
        }
    
    # TEST USUARIOS
    def test_paginated_usuarios(self):
        res = self.client().get('/usuarios')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['usuarios']))
        self.assertTrue(data['total_usuarios'])
    
    def test_paginated_usuarios_with_404_error(self):
        res = self.client().get('/usuarios?page=5436543')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_create_usuario_success(self):
        res = self.client().post('/usuarios', json=self.new_usuario)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['usuarios']))
        self.assertTrue(data['total_usuarios'])
        
    def test_create_usuario_with_no_password(self):
        res = self.client().post('/usuarios', json={'username': 'Alejandro', 'password_':None, 'correo': 'alejandro123@gmail.com'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_usuario_with_no_email(self):
        res = self.client().post('/usuarios', json={'username': 'Alejandro', 'password_':'Alejandro12345', 'correo': None})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_usuario_with_no_username(self):
        res = self.client().post('/usuarios', json={'username': None, 'password_':'Alejandro12345', 'correo': 'alejandro123@gmail.com'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_usuario_with_incorrect_password_format_no_numbers(self):
        res = self.client().post('/usuarios', json={'username': 'AlejandrosXD', 'password_':'Alejandro', 'correo': 'alejandro123@gmail.com'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_create_usuario_with_incorrect_password_format_size_less_than_8(self):
        res = self.client().post('/usuarios', json={'username': 'AlejandrosXD', 'password_':'A123', 'correo': 'alejandro123@gmail.com'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_delete_usuario_success(self):
        res = self.client().delete('/usuarios/{}'.format(self.new_usuario['username']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['usuarios'])
        self.assertTrue(data['total_usuarios'])
        self.assertEqual(data['deleted'], str(self.new_usuario['username']))
    
    def test_delete_usuario_error_404(self):
        res = self.client().delete('/usuarios/{}'.format('Iker Casillas'))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'])
        
    # TEST ITEMS
    def test_paginated_items(self):
        res = self.client().get('/items')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['items']))
        self.assertTrue(data['total_items'])
        
    def test_paginated_items_error_404(self):
        res = self.client().get('/items?page=3432')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_search_bar_items(self):
        pass
    
    #TEST CATEGORIA
    def test_paginated_categorias(self):
        res = self.client().get('/categorias')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categorias']))
        self.assertTrue(data['total_categorias'])
        
    def test_paginated_categorias_error_404(self):
        res = self.client().get('/categorias?page=50')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    # TEST CALIFICACIONES
    def test_paginated_calificaciones(self):
        res = self.client().get('/calificaciones')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['calificaciones']))
        self.assertTrue(data['total_calificaciones'])
    
    def test_paginated_calificaciones_with_404_error(self):
        res = self.client().get('/calificaciones?page=50')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_calificacion_success(self):
        res = self.client().post('/calificaciones', json=self.new_calificacion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_created'])
        self.assertTrue(data['username_created'])
        self.assertTrue(len(data['calificaciones']))
        self.assertTrue(data['total_calificaciones'])

    def test_create_calificacion_with_no_username(self):
        res = self.client().post('/calificaciones', json={'usuario_username': None, 'items_id': 2, 'puntaje': 5, 'comentario': 'Me gusto, muy chevere TOP'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_calificacion_with_no_id_item(self):
        res = self.client().post('/calificaciones', json={'usuario_username': 'matiazzz', 'items_id': None, 'puntaje': 5, 'comentario': 'Me gusto, muy chevere TOP'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_calificacion_with_no_puntaje(self):
        res = self.client().post('/calificaciones', json={'usuario_username': 'matiazzz', 'items_id': 2, 'puntaje': None, 'comentario': 'Me gusto, muy chevere TOP'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_create_calificacion_with_no_comentario(self):
        res = self.client().post('/calificaciones', json={'usuario_username': 'matiazzz', 'items_id': 2, 'puntaje': 5, 'comentario': None})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_create_calificacion_with_comentario_with_space_blanks(self):
        res = self.client().post('/calificaciones', json={'usuario_username': 'matiazzz', 'items_id': 2, 'puntaje': 5, 'comentario': '        '})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_update_calificacion_success(self):
        res0 = self.client().post('/calificaciones', json=self.new_calificacion)
        data0 = json.loads(res0.data)
        updated_username = data0['username_created']
        updated_id = data0['id_created']

        res = self.client().patch('/calificaciones/{}/{}'.format(updated_username,updated_id), json={'puntaje': 2, 'comentario': 'Aburrido ZZZZ'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['item_calificado'], str(updated_id))
        self.assertEqual(data['username'], str(updated_username))
    
    def test_update_calificacion_with_no_puntaje(self):
        res = self.client().patch('/calificaciones/matias/1', json={'puntaje': None, 'comentario': 'TREMENDO XD'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_update_calificacion_with_no_comentario(self):
        res = self.client().patch('/calificaciones/mosquis/1', json={'puntaje': 1, 'comentario': None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_update_calificacion_with_comentario_with_space_blanks(self):
        res = self.client().patch('/calificaciones/mosquis/1', json={'puntaje': 1, 'comentario': '     '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_update_calificacion_error_url(self):
        res = self.client().patch('/calificaciones/ronaldinho/-24', json={'puntaje': 4, 'Comentario': 'chevere la pelicula'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_calificacion_success(self):
        res0 = self.client().post('/calificaciones', json=self.new_calificacion)
        data0 = json.loads(res0.data)
        deleted_id = data0['id_created']
        deleted_user_coment = data0['username_created']

        res = self.client().delete('/calificaciones/{}/{}'.format(deleted_user_coment, deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['calificaciones'])
        self.assertTrue(data['total_calificaciones'])
        self.assertEqual(data['deleted_comentario_item'], str(deleted_id))
        self.assertEqual(data['deleted_comentario_user'], str(deleted_user_coment))
    
    def test_delete_calificacion_error_404_in_username(self):
        res = self.client().delete('/calificaciones/{}/{}'.format('Jano',1))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_delete_calificacion_error_404_in_itemID(self):
        res = self.client().delete('/calificaciones/{}/{}'.format('matiazzz',-342))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
"""
import pytest
from flask.testing import FlaskClient
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_service_correcto(client: FlaskClient):
    resp = client.post('/register_validator', json={'email': 'AAAAZsome@thing.com', 'password': 'Zholass123','username':'MMMatiasQZ22'})
    assert resp.json.get('msg')== "Register sucessful!"

def test_service_mala_contra(client: FlaskClient):
    resp = client.post('/register_validator', json={'email': 'ERR@thing.com', 'password': '123','username':'ERR`'})
    assert resp.json.get('msg')== "La contraseña no cumple con tener 9 caracteres como minimo"
"""
